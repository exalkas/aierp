"use client";

import React, { useState, useEffect } from "react";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  Input,
  Badge,
  EmptyState,
  LoadingButton,
} from "@erp/shared-ui";
import {
  Search,
  Plus,
  User,
  Mail,
  Phone,
  Edit,
  Trash2,
  Star,
  MapPin,
  Building2,
} from "lucide-react";
import { useAuth } from "@erp/shared-ui";

interface Contact {
  id: string;
  business_entity_id: string;
  first_name: string;
  last_name: string;
  display_name: string;
  job_title?: string;
  department?: string;
  email?: string;
  phone?: string;
  mobile?: string;
  is_primary_contact: boolean;
  is_decision_maker: boolean;
  contact_type:
    | "primary"
    | "secondary"
    | "billing"
    | "technical"
    | "sales"
    | "support";
  status: "active" | "inactive" | "bounced" | "unsubscribed";
  preferred_contact_method: "email" | "phone" | "meeting";
  language: "el" | "en";
  last_contact_date?: string;
  total_interactions: number;
  created_at: string;
}

interface ContactListResponse {
  contacts: Contact[];
  total_count: number;
}

export interface ContactListProps {
  businessEntityId: string;
  businessEntityName?: string;
  onCreateClick?: () => void;
  onContactClick?: (contact: Contact) => void;
  onEditClick?: (contact: Contact) => void;
  className?: string;
}

export default function ContactList({
  businessEntityId,
  businessEntityName,
  onCreateClick,
  onContactClick,
  onEditClick,
  className = "",
}: ContactListProps) {
  const { tokens } = useAuth();
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [totalCount, setTotalCount] = useState(0);

  // Fetch contacts for the business entity
  const fetchContacts = async (search: string = "") => {
    if (!tokens?.accessToken || !businessEntityId) {
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const params = new URLSearchParams();
      if (search) params.append("search", search);

      const response = await fetch(
        `/api/v1/contacts/business-entity/${businessEntityId}?${params}`,
        {
          headers: {
            Authorization: `Bearer ${tokens.accessToken}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP ${response.status}`);
      }

      const data: Contact[] = await response.json();
      setContacts(data || []);
      setTotalCount(data?.length || 0);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch contacts");
      console.error("Error fetching contacts:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const delayedSearch = setTimeout(() => {
      fetchContacts(searchTerm);
    }, 300);

    return () => clearTimeout(delayedSearch);
  }, [tokens, businessEntityId, searchTerm]);

  const handleDeleteContact = async (contactId: string) => {
    if (!confirm("Are you sure you want to delete this contact?")) {
      return;
    }

    try {
      const response = await fetch(`/api/v1/contacts/${contactId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${tokens?.accessToken}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to delete contact");
      }

      // Refresh the contact list
      fetchContacts(searchTerm);
    } catch (error) {
      console.error("Error deleting contact:", error);
      // TODO: Show error message to user
    }
  };

  const getContactTypeColor = (type: string) => {
    const colors: Record<string, "info" | "success" | "warning" | "error"> = {
      primary: "success",
      secondary: "info",
      billing: "warning",
      technical: "info",
      sales: "success",
      support: "warning",
    };
    return colors[type] || "info";
  };

  const getStatusBadge = (status: string) => {
    const variants: Record<string, "success" | "warning" | "error" | "info"> = {
      active: "success",
      inactive: "warning",
      bounced: "error",
      unsubscribed: "error",
    };

    return (
      <Badge variant={variants[status] || "info"}>{status.toUpperCase()}</Badge>
    );
  };

  const formatLastContact = (dateString?: string) => {
    if (!dateString) return "Never";

    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.ceil(diffDays / 7)} weeks ago`;
    return `${Math.ceil(diffDays / 30)} months ago`;
  };

  if (error) {
    return (
      <Card className={className}>
        <CardContent>
          <EmptyState
            title="Error Loading Contacts"
            description={error}
            variant="error"
            actions={[
              {
                label: "Retry",
                onClick: () => fetchContacts(searchTerm),
                variant: "primary",
              },
            ]}
          />
        </CardContent>
      </Card>
    );
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Contacts</h3>
          {businessEntityName && (
            <p className="text-gray-600">
              Contact people at {businessEntityName}
            </p>
          )}
        </div>
        {onCreateClick && (
          <Button
            onClick={onCreateClick}
            size="sm"
            className="flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            Add Contact
          </Button>
        )}
      </div>

      {/* Search */}
      <div className="flex gap-4">
        <div className="flex-1">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <Input
              type="text"
              placeholder="Search contacts by name, email, or job title..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>
      </div>

      {/* Contact List */}
      <Card>
        <CardContent>
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <LoadingButton loading={true}>Loading contacts...</LoadingButton>
            </div>
          ) : contacts.length === 0 ? (
            <EmptyState
              title="No Contacts Found"
              description={
                searchTerm
                  ? "Try adjusting your search criteria"
                  : "Add the first contact for this business entity"
              }
              actions={
                onCreateClick
                  ? [
                      {
                        label: "Add Contact",
                        onClick: onCreateClick,
                        variant: "primary",
                        icon: <Plus className="w-4 h-4" />,
                      },
                    ]
                  : undefined
              }
            />
          ) : (
            <div className="space-y-4">
              {contacts.map((contact) => (
                <div
                  key={contact.id}
                  className="p-4 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className="flex-shrink-0">
                        <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
                          <User className="w-5 h-5 text-gray-600" />
                        </div>
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h4
                            className="font-semibold text-gray-900 cursor-pointer hover:text-blue-600"
                            onClick={() => onContactClick?.(contact)}
                          >
                            {contact.display_name}
                          </h4>
                          {contact.is_primary_contact && (
                            <Star className="w-4 h-4 text-yellow-500 fill-current" />
                          )}
                          {contact.is_decision_maker && (
                            <Badge variant="info" size="sm">
                              Decision Maker
                            </Badge>
                          )}
                        </div>
                        {contact.job_title && (
                          <p className="text-sm text-gray-600">
                            {contact.job_title}
                            {contact.department && ` • ${contact.department}`}
                          </p>
                        )}
                        <div className="flex items-center gap-2 mt-1">
                          <Badge
                            variant={getContactTypeColor(contact.contact_type)}
                          >
                            {contact.contact_type.charAt(0).toUpperCase() +
                              contact.contact_type.slice(1)}
                          </Badge>
                          {getStatusBadge(contact.status)}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {onEditClick && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => onEditClick(contact)}
                        >
                          <Edit className="w-4 h-4" />
                        </Button>
                      )}
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDeleteContact(contact.id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
                    <div className="space-y-1">
                      <div className="font-medium text-gray-700">
                        Contact Info
                      </div>
                      {contact.email && (
                        <div className="flex items-center gap-2">
                          <Mail className="w-3 h-3" />
                          <a
                            href={`mailto:${contact.email}`}
                            className="hover:text-blue-600"
                          >
                            {contact.email}
                          </a>
                        </div>
                      )}
                      {contact.phone && (
                        <div className="flex items-center gap-2">
                          <Phone className="w-3 h-3" />
                          <a
                            href={`tel:${contact.phone}`}
                            className="hover:text-blue-600"
                          >
                            {contact.phone}
                          </a>
                        </div>
                      )}
                      {contact.mobile && (
                        <div className="flex items-center gap-2">
                          <Phone className="w-3 h-3" />
                          <a
                            href={`tel:${contact.mobile}`}
                            className="hover:text-blue-600"
                          >
                            {contact.mobile} (Mobile)
                          </a>
                        </div>
                      )}
                    </div>

                    <div className="space-y-1">
                      <div className="font-medium text-gray-700">
                        Preferences
                      </div>
                      <div>
                        Method:{" "}
                        {contact.preferred_contact_method
                          .charAt(0)
                          .toUpperCase() +
                          contact.preferred_contact_method.slice(1)}
                      </div>
                      <div>
                        Language:{" "}
                        {contact.language === "el" ? "Greek" : "English"}
                      </div>
                    </div>

                    <div className="space-y-1">
                      <div className="font-medium text-gray-700">Activity</div>
                      <div>
                        Last contact:{" "}
                        {formatLastContact(contact.last_contact_date)}
                      </div>
                      <div>Interactions: {contact.total_interactions}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Summary */}
      {contacts.length > 0 && (
        <div className="text-sm text-gray-600 text-center">
          Showing {contacts.length} contact{contacts.length !== 1 ? "s" : ""}
        </div>
      )}
    </div>
  );
}
