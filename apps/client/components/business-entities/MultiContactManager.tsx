"use client";

import React, { useState, useEffect } from "react";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  Input,
  GreekAddressInput,
  GreekPhoneInput,
  Badge,
  useTranslation,
  ModernTabs,
  TabsContent,
  TabsList,
  TabsTrigger,
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@erp/shared-ui";
import {
  Plus,
  Mail,
  Phone,
  MapPin,
  Star,
  X,
  Globe,
  Building,
  Home,
  Briefcase,
  Truck,
  AlertCircle,
  CheckCircle2,
  Trash2,
  Edit3,
} from "lucide-react";

// Contact method interfaces
interface ContactMethod {
  id: string;
  type: "phone" | "email" | "address";
  subtype_code: string;
  subtype_name: string;
  value: string | AddressValue;
  is_primary: boolean;
  is_verified: boolean;
  quality_score?: number;
  notes?: string;
}

interface AddressValue {
  street: string;
  number: string;
  city: string;
  postalCode: string;
  region: string;
}

interface ContactSubtype {
  id: string;
  code: string;
  name: string;
  name_greek: string;
  method_type: "phone" | "email" | "address";
  icon: string;
  color: string;
  is_default: boolean;
  is_system: boolean;
}

interface MultiContactManagerProps {
  value?: ContactMethod[];
  onChange?: (contacts: ContactMethod[]) => void;
  className?: string;
  disabled?: boolean;
}

const CONTACT_TYPE_ICONS = {
  phone: Phone,
  email: Mail,
  address: MapPin,
};

const SUBTYPE_ICONS = {
  work: Briefcase,
  home: Home,
  main: Building,
  billing: Building,
  shipping: Truck,
  mobile: Phone,
  emergency: AlertCircle,
};

export default function MultiContactManager({
  value = [],
  onChange,
  className = "",
  disabled = false,
}: MultiContactManagerProps) {
  const { t } = useTranslation();
  const [contacts, setContacts] = useState<ContactMethod[]>(value);
  const [subtypes, setSubtypes] = useState<ContactSubtype[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isMobile, setIsMobile] = useState(false);
  const [activeTab, setActiveTab] = useState("phones");

  // Responsive detection
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  // Load contact method subtypes
  useEffect(() => {
    const loadSubtypes = async () => {
      setLoading(true);
      setError(null);

      try {
        const token = localStorage.getItem("token");

        if (!token) {
          throw new Error("AUTHENTICATION_REQUIRED");
        }

        const response = await fetch("/api/v1/contact-method-subtypes/", {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          if (response.status === 401) {
            throw new Error("AUTHENTICATION_FAILED");
          }
          if (response.status === 403) {
            throw new Error("ACCESS_DENIED");
          }
          if (response.status === 500) {
            throw new Error("SERVER_ERROR");
          }
          throw new Error(`API_ERROR_${response.status}`);
        }

        const data = await response.json();
        setSubtypes(data);
      } catch (error) {
        let errorMessage = "An unexpected error occurred";
        let actionMessage = "Please contact support if this persists";

        if (error instanceof Error) {
          switch (error.message) {
            case "AUTHENTICATION_REQUIRED":
              errorMessage = "You need to log in to access this feature";
              actionMessage = "Please log in to continue";
              break;
            case "AUTHENTICATION_FAILED":
              errorMessage = "Your session has expired or is invalid";
              actionMessage = "Please log out and log back in";
              break;
            case "ACCESS_DENIED":
              errorMessage =
                "You don't have permission to access contact method types";
              actionMessage = "Contact your administrator for access";
              break;
            case "SERVER_ERROR":
              errorMessage = "Server is experiencing issues";
              actionMessage =
                "Please try again in a few minutes or contact support";
              break;
            default:
              if (error.message.startsWith("API_ERROR_")) {
                errorMessage = `API returned error ${error.message.replace("API_ERROR_", "")}`;
              } else {
                errorMessage = `Connection failed: ${error.message}`;
                actionMessage = "Check your internet connection and try again";
              }
          }
        }

        console.error("Failed to load contact method subtypes:", {
          error: error instanceof Error ? error.message : error,
          userMessage: errorMessage,
          action: actionMessage,
        });

        setError(`${errorMessage}. ${actionMessage}`);
      } finally {
        setLoading(false);
      }
    };

    loadSubtypes();
  }, []);

  // Update parent when contacts change
  useEffect(() => {
    if (onChange) {
      onChange(contacts);
    }
  }, [contacts, onChange]);

  // Helper functions
  const getContactsByType = (type: "phone" | "email" | "address") => {
    return contacts.filter((contact) => contact.type === type);
  };

  const getSubtypesByType = (type: "phone" | "email" | "address") => {
    return subtypes.filter((subtype) => subtype.method_type === type);
  };

  const generateId = () =>
    `temp_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  const addContact = (type: "phone" | "email" | "address") => {
    const typeSubtypes = getSubtypesByType(type);
    const defaultSubtype =
      typeSubtypes.find((s) => s.is_default) || typeSubtypes[0];

    if (!defaultSubtype) return;

    const newContact: ContactMethod = {
      id: generateId(),
      type,
      subtype_code: defaultSubtype.code,
      subtype_name: defaultSubtype.name,
      value:
        type === "address"
          ? {
              street: "",
              number: "",
              city: "",
              postalCode: "",
              region: "",
            }
          : "",
      is_primary: getContactsByType(type).length === 0, // First one is primary
      is_verified: false,
      quality_score: 0,
    };

    setContacts((prev) => [...prev, newContact]);
  };

  const updateContact = (id: string, updates: Partial<ContactMethod>) => {
    setContacts((prev) =>
      prev.map((contact) =>
        contact.id === id ? { ...contact, ...updates } : contact
      )
    );
  };

  const removeContact = (id: string) => {
    setContacts((prev) => {
      const updated = prev.filter((contact) => contact.id !== id);
      const contact = prev.find((c) => c.id === id);

      // If removing primary contact, make first remaining contact primary
      if (contact?.is_primary && updated.length > 0) {
        const typeContacts = updated.filter((c) => c.type === contact.type);
        if (typeContacts.length > 0) {
          const firstContact = typeContacts[0];
          return updated.map((c) =>
            c.id === firstContact.id ? { ...c, is_primary: true } : c
          );
        }
      }

      return updated;
    });
  };

  const setPrimary = (id: string) => {
    setContacts((prev) => {
      const contact = prev.find((c) => c.id === id);
      if (!contact) return prev;

      return prev.map((c) => ({
        ...c,
        is_primary: c.type === contact.type ? c.id === id : c.is_primary,
      }));
    });
  };

  const getQualityColor = (score: number = 0) => {
    if (score >= 80) return "text-green-600";
    if (score >= 60) return "text-yellow-600";
    return "text-red-600";
  };

  const renderContactItem = (
    contact: ContactMethod,
    type: "phone" | "email" | "address"
  ) => {
    const subtypeOptions = getSubtypesByType(type);
    const TypeIcon = CONTACT_TYPE_ICONS[type];

    return (
      <div
        key={contact.id}
        className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800/50 space-y-3"
      >
        {/* Header with type, primary badge, and actions */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <TypeIcon className="w-4 h-4 text-gray-500" />
            <select
              value={contact.subtype_code}
              onChange={(e) => {
                const subtype = subtypeOptions.find(
                  (s) => s.code === e.target.value
                );
                updateContact(contact.id, {
                  subtype_code: e.target.value,
                  subtype_name: subtype?.name || "",
                });
              }}
              disabled={disabled}
              className="text-sm border-0 bg-transparent font-medium text-gray-900 dark:text-white focus:ring-0"
            >
              {subtypeOptions.map((subtype) => (
                <option key={subtype.code} value={subtype.code}>
                  {subtype.name}
                </option>
              ))}
            </select>

            {contact.is_primary && (
              <Badge variant="secondary" className="text-xs">
                <Star className="w-3 h-3 mr-1" />
                {t("primary", { ns: "business_entities" })}
              </Badge>
            )}

            {contact.is_verified && (
              <CheckCircle2 className="w-4 h-4 text-green-600" />
            )}
          </div>

          <div className="flex items-center gap-1">
            {contact.quality_score !== undefined && (
              <span
                className={`text-xs font-medium ${getQualityColor(contact.quality_score)}`}
              >
                {contact.quality_score}%
              </span>
            )}

            {!contact.is_primary && (
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={() => setPrimary(contact.id)}
                disabled={disabled}
                className="h-8 w-8 p-0"
              >
                <Star className="w-3 h-3" />
              </Button>
            )}

            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={() => removeContact(contact.id)}
              disabled={disabled}
              className="h-8 w-8 p-0 text-red-600 hover:text-red-700"
            >
              <Trash2 className="w-3 h-3" />
            </Button>
          </div>
        </div>

        {/* Contact value input */}
        <div>
          {type === "phone" && (
            <GreekPhoneInput
              value={contact.value as string}
              onChange={(e) =>
                updateContact(contact.id, { value: e.target.value })
              }
              allowLandline={contact.subtype_code !== "mobile"}
              allowMobile={contact.subtype_code !== "landline"}
              disabled={disabled}
              className="w-full"
            />
          )}

          {type === "email" && (
            <Input
              type="email"
              value={contact.value as string}
              onChange={(e) =>
                updateContact(contact.id, { value: e.target.value })
              }
              placeholder="email@example.com"
              disabled={disabled}
              leftIcon={<Mail className="w-4 h-4" />}
              className="w-full"
            />
          )}

          {type === "address" && (
            <GreekAddressInput
              value={contact.value as AddressValue}
              onChange={(value) =>
                updateContact(contact.id, {
                  value: {
                    street: value.street || "",
                    number: value.number || "",
                    city: value.city || "",
                    postalCode: value.postalCode || "",
                    region: value.region || "",
                  },
                })
              }
              disabled={disabled}
              layout="vertical"
            />
          )}
        </div>

        {/* Notes */}
        <div>
          <Input
            value={contact.notes || ""}
            onChange={(e) =>
              updateContact(contact.id, { notes: e.target.value })
            }
            placeholder={t("contact_notes_placeholder", {
              ns: "business_entities",
              defaultValue: "Notes (optional)",
            })}
            disabled={disabled}
            className="text-sm"
          />
        </div>
      </div>
    );
  };

  const renderContactSection = (
    type: "phone" | "email" | "address",
    title: string,
    icon: React.ElementType
  ) => {
    const typeContacts = getContactsByType(type);
    const Icon = icon;

    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h4 className="text-lg font-semibold flex items-center gap-2 text-gray-900 dark:text-white">
            <Icon className="w-5 h-5" />
            {title}
          </h4>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => addContact(type)}
            disabled={disabled}
            className="flex items-center gap-1"
          >
            <Plus className="w-4 h-4" />
            {t("add", { ns: "common" })}
          </Button>
        </div>

        <div className="space-y-3">
          {typeContacts.length === 0 ? (
            <div className="text-center py-8 text-gray-500 dark:text-gray-400">
              <Icon className="w-12 h-12 mx-auto mb-3 opacity-50" />
              <p>
                {t("no_contacts_added", {
                  ns: "business_entities",
                  defaultValue: `No ${title.toLowerCase()} added yet`,
                })}
              </p>
              <p className="text-sm">
                {t("click_add_to_start", {
                  ns: "business_entities",
                  defaultValue: 'Click "Add" to get started',
                })}
              </p>
            </div>
          ) : (
            typeContacts.map((contact) => renderContactItem(contact, type))
          )}
        </div>
      </div>
    );
  };

  // Desktop tabs layout
  const renderDesktopLayout = () => (
    <ModernTabs
      value={activeTab}
      onValueChange={setActiveTab}
      className="w-full"
    >
      <TabsList className="grid w-full grid-cols-3">
        <TabsTrigger value="phones" className="flex items-center gap-2">
          <Phone className="w-4 h-4" />
          {t("phones", { ns: "business_entities", defaultValue: "Phones" })}
          {getContactsByType("phone").length > 0 && (
            <Badge variant="secondary" className="ml-1 text-xs">
              {getContactsByType("phone").length}
            </Badge>
          )}
        </TabsTrigger>
        <TabsTrigger value="emails" className="flex items-center gap-2">
          <Mail className="w-4 h-4" />
          {t("emails", { ns: "business_entities", defaultValue: "Emails" })}
          {getContactsByType("email").length > 0 && (
            <Badge variant="secondary" className="ml-1 text-xs">
              {getContactsByType("email").length}
            </Badge>
          )}
        </TabsTrigger>
        <TabsTrigger value="addresses" className="flex items-center gap-2">
          <MapPin className="w-4 h-4" />
          {t("addresses", {
            ns: "business_entities",
            defaultValue: "Addresses",
          })}
          {getContactsByType("address").length > 0 && (
            <Badge variant="secondary" className="ml-1 text-xs">
              {getContactsByType("address").length}
            </Badge>
          )}
        </TabsTrigger>
      </TabsList>

      <TabsContent value="phones" className="mt-6">
        {renderContactSection(
          "phone",
          t("phone_numbers", {
            ns: "business_entities",
            defaultValue: "Phone Numbers",
          }),
          Phone
        )}
      </TabsContent>

      <TabsContent value="emails" className="mt-6">
        {renderContactSection(
          "email",
          t("email_addresses", {
            ns: "business_entities",
            defaultValue: "Email Addresses",
          }),
          Mail
        )}
      </TabsContent>

      <TabsContent value="addresses" className="mt-6">
        {renderContactSection(
          "address",
          t("addresses", {
            ns: "business_entities",
            defaultValue: "Addresses",
          }),
          MapPin
        )}
      </TabsContent>
    </ModernTabs>
  );

  // Mobile accordion layout
  const renderMobileLayout = () => (
    <Accordion type="single" collapsible className="w-full">
      <AccordionItem value="phones">
        <AccordionTrigger className="flex items-center gap-2">
          <Phone className="w-4 h-4" />
          {t("phone_numbers", {
            ns: "business_entities",
            defaultValue: "Phone Numbers",
          })}
          {getContactsByType("phone").length > 0 && (
            <Badge variant="secondary" className="ml-1 text-xs">
              {getContactsByType("phone").length}
            </Badge>
          )}
        </AccordionTrigger>
        <AccordionContent className="pt-4">
          {renderContactSection(
            "phone",
            t("phone_numbers", {
              ns: "business_entities",
              defaultValue: "Phone Numbers",
            }),
            Phone
          )}
        </AccordionContent>
      </AccordionItem>

      <AccordionItem value="emails">
        <AccordionTrigger className="flex items-center gap-2">
          <Mail className="w-4 h-4" />
          {t("email_addresses", {
            ns: "business_entities",
            defaultValue: "Email Addresses",
          })}
          {getContactsByType("email").length > 0 && (
            <Badge variant="secondary" className="ml-1 text-xs">
              {getContactsByType("email").length}
            </Badge>
          )}
        </AccordionTrigger>
        <AccordionContent className="pt-4">
          {renderContactSection(
            "email",
            t("email_addresses", {
              ns: "business_entities",
              defaultValue: "Email Addresses",
            }),
            Mail
          )}
        </AccordionContent>
      </AccordionItem>

      <AccordionItem value="addresses">
        <AccordionTrigger className="flex items-center gap-2">
          <MapPin className="w-4 h-4" />
          {t("addresses", {
            ns: "business_entities",
            defaultValue: "Addresses",
          })}
          {getContactsByType("address").length > 0 && (
            <Badge variant="secondary" className="ml-1 text-xs">
              {getContactsByType("address").length}
            </Badge>
          )}
        </AccordionTrigger>
        <AccordionContent className="pt-4">
          {renderContactSection(
            "address",
            t("addresses", {
              ns: "business_entities",
              defaultValue: "Addresses",
            }),
            MapPin
          )}
        </AccordionContent>
      </AccordionItem>
    </Accordion>
  );

  if (loading) {
    return (
      <Card className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
        <CardContent className="p-6">
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-gray-600 dark:text-gray-400">
              {t("loading_contact_options", {
                ns: "business_entities",
                defaultValue: "Loading contact options...",
              })}
            </span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700">
        <CardContent className="p-6 text-center">
          <AlertCircle className="w-12 h-12 text-red-600 mb-4" />
          <p className="text-lg font-semibold text-red-800 dark:text-red-200 mb-2">
            {error}
          </p>
          <p className="text-sm text-red-700 dark:text-red-300">
            {t("error_contact_options_action", {
              ns: "business_entities",
              defaultValue: "Please try again or contact support.",
            })}
          </p>
        </CardContent>
      </Card>
    );
  }

  if (!loading && subtypes.length === 0) {
    return (
      <Card className="bg-yellow-50 dark:bg-yellow-900 border border-yellow-200 dark:border-yellow-700">
        <CardContent className="p-6 text-center">
          <AlertCircle className="w-12 h-12 text-yellow-600 mb-4" />
          <p className="text-lg font-semibold text-yellow-800 dark:text-yellow-200 mb-2">
            {t("no_contact_types_configured", {
              ns: "business_entities",
              defaultValue: "No contact method types configured",
            })}
          </p>
          <p className="text-sm text-yellow-700 dark:text-yellow-300">
            {t("contact_admin_for_setup", {
              ns: "business_entities",
              defaultValue:
                "Contact your administrator to set up contact method types before adding contact information.",
            })}
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card
      className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 ${className}`}
    >
      <CardHeader className="bg-gray-50 dark:bg-gray-800/50">
        <h3 className="text-lg font-semibold flex items-center gap-2 text-gray-900 dark:text-white">
          <Mail className="w-5 h-5" />
          {t("contact_information", {
            ns: "business_entities",
            defaultValue: "Contact Information",
          })}
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          {t("contact_info_description", {
            ns: "business_entities",
            defaultValue:
              "Add multiple phone numbers, email addresses, and physical addresses. Mark the most important ones as primary.",
          })}
        </p>
      </CardHeader>
      <CardContent className="p-6">
        {isMobile ? renderMobileLayout() : renderDesktopLayout()}
      </CardContent>
    </Card>
  );
}
