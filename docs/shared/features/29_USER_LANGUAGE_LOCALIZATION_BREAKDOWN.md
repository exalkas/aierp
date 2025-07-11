# User Language & Localization Settings - Detailed Breakdown

## Document Information

- **Version**: 1.0
- **Date**: January 2025
- **Purpose**: Detailed specification for user language and localization settings
- **Scope**: 4 screens for comprehensive user preference management

---

## 1. DESIGN RATIONALE

### 1.1 Why 4 Separate Settings Screens?

The separation into 4 distinct screens follows the **principle of separation of concerns**:

1. **Language Preferences** - Pure language selection (applies to UI text)
2. **Localization Settings** - Universal formatting preferences (dates, numbers, currency)
3. **Business Locale Settings** - Country-specific business culture and practices
4. **Compliance Preferences** - Regulatory and government integration display preferences

### 1.2 Why Not Just "Greek Locale Settings"?

**The Problem with Language-Specific Settings:**

- Creates inconsistent design (why only Greek?)
- Mixes language preferences with business requirements
- Not scalable to other countries
- Confuses UI translation with business compliance

**The Solution - Country-Based Business Settings:**

- **Business Locale Settings**: Country-specific business practices (Greece, Germany, France, etc.)
- **Compliance Settings**: Regulatory requirements (Greek AADE, German tax, French social security)
- **Extensible Design**: Easy to add new countries without redesigning
- **Clear Separation**: Language ≠ Country ≠ Business Rules ≠ Compliance

---

## 2. SCREEN SPECIFICATIONS

### 2.1 Screen 1: Language Preferences (`/settings/language`)

**Purpose**: Pure language selection for UI text and content

**Features:**

- Primary language selection (main UI language)
- Fallback language selection (when translations missing)
- Content language preferences (for user-generated content)
- Auto-detection settings

**Models Used:**

```typescript
interface UserLanguagePreferences {
  id: string;
  userId: string;
  primaryLanguage: LanguageCode; // "el", "en", "de", "fr"
  fallbackLanguage: LanguageCode; // "en" as default fallback
  contentLanguages: LanguageCode[]; // Multiple content languages
  autoDetectFromBrowser: boolean;
  autoDetectFromLocation: boolean;
  customFields: Record<string, any>;
}
```

**UI Components:**

- Language dropdown with flags and native names
- Fallback language selector
- Auto-detection toggles
- Language completion indicator (% of translations available)

**API Endpoints:**

- `GET /api/i18n/user-preferences` - Get user language preferences
- `PUT /api/i18n/user-preferences` - Update language preferences
- `POST /api/i18n/user-preferences/detect` - Auto-detect language

---

### 2.2 Screen 2: Localization Settings (`/settings/localization`)

**Purpose**: Universal formatting preferences that apply regardless of country

**Features:**

- Date format preferences (DD/MM/YYYY vs MM/DD/YYYY vs YYYY-MM-DD)
- Time format (12h vs 24h)
- Number format (1,234.56 vs 1.234,56 vs 1 234,56)
- Currency display preferences
- Timezone selection

**Models Used:**

```typescript
interface LocalizationSettings {
  id: string;
  userId: string;
  dateFormat: "DD/MM/YYYY" | "MM/DD/YYYY" | "YYYY-MM-DD" | "custom";
  timeFormat: "12h" | "24h";
  numberFormat: "us" | "eu" | "international" | "custom";
  currency: CurrencyCode;
  currencyPosition: "before" | "after";
  timezone: TimezoneCode;
  firstDayOfWeek: "monday" | "sunday";
  customFields: Record<string, any>;
}
```

**UI Components:**

- Date format preview with live examples
- Number format examples
- Currency selector with position preview
- Timezone selector with current time display

**Examples:**

- **Date**: "Today is 15/01/2025" vs "Today is 01/15/2025"
- **Number**: "1,234.56" vs "1.234,56" vs "1 234,56"
- **Currency**: "€1,234.56" vs "1,234.56 €"

---

### 2.3 Screen 3: Business Locale Settings (`/settings/business-locale`)

**Purpose**: Country-specific business culture and operational preferences

**Features:**

- Country selection (determines business rules)
- Business communication style preferences
- Address format preferences
- Phone number format preferences
- Business hours patterns
- Holiday calendar preferences

**Models Used:**

```typescript
interface BusinessLocaleSettings {
  id: string;
  userId: string;
  country: CountryCode; // "GR", "DE", "FR", "US", etc.
  
  // Business Culture
  communicationStyle: "formal" | "informal" | "mixed";
  greetingStyle: "traditional" | "modern" | "international";
  
  // Address Formatting
  addressFormat: AddressFormatSettings;
  showRegion: boolean;
  postalCodeFormat: string;
  
  // Phone Formatting  
  phoneDisplayFormat: "national" | "international";
  phoneInputFormat: "formatted" | "raw";
  
  // Business Operations
  businessHours: BusinessHoursSettings;
  workweekPattern: "monday_friday" | "sunday_thursday" | "custom";
  
  // Calendar
  holidayCalendar: "secular" | "orthodox" | "catholic" | "islamic" | "custom";
  workingDays: DayOfWeek[];
  
  customFields: Record<string, any>;
}
```

**Country-Specific Examples:**

**Greece:**

- Communication: Formal business greetings ("Αγαπητέ κύριε")
- Address: "Πατησίων 123, 10678 Αθήνα, Αττική"
- Phone: "+30 210 123 4567" (Greek format)
- Business Hours: 09:00-17:00 (with 14:00-17:00 siesta consideration)
- Calendar: Orthodox holidays, Orthodox Easter

**Germany:**

- Communication: Very formal ("Sehr geehrte Damen und Herren")
- Address: "Hauptstraße 123, 10115 Berlin"
- Phone: "+49 30 " (German format)
- Business Hours: 09:00-18:00 (strict punctuality)
- Calendar: German public holidays, Protestant/Catholic variations

**France:**

- Communication: Formal with specific titles ("Monsieur/Madame")
- Address: "123 rue de la Paix, 75001 Paris"
- Phone: "+33 1 23 45 67 89" (French format)
- Business Hours: 09:00-18:00 (with lunch break culture)
- Calendar: French public holidays, Catholic calendar

---

### 2.4 Screen 4: Compliance Preferences (`/settings/compliance`)

**Purpose**: Regulatory and government integration display preferences

**Features:**

- Country-specific compliance display rules
- Tax number formatting preferences
- Government form display preferences
- Legal document formatting
- Regulatory notification preferences

**Models Used:**

```typescript
interface ComplianceDisplaySettings {
  id: string;
  userId: string;
  country: CountryCode;
  
  // Tax Number Display
  taxNumberDisplay: {
    format: "grouped" | "continuous" | "masked";
    showValidationStatus: boolean;
    showTaxOfficeInfo: boolean;
  };
  
  // Government Forms
  complianceFormats: {
    formLanguage: "native" | "english" | "both";
    showHelperText: boolean;
    showComplianceStatus: boolean;
    highlightRequiredFields: boolean;
  };
  
  // Government Integration Display
  governmentIntegrationDisplay: {
    showSubmissionStatus: boolean;
    showIntegrationHealth: boolean;
    notificationLevel: "minimal" | "normal" | "detailed";
  };
  
  // Legal Documents
  legalDocumentFormats: {
    templateStyle: "official" | "business" | "simplified";
    includeRegulatoryReferences: boolean;
    showComplianceFooters: boolean;
  };
  
  customFields: Record<string, any>;
}
```

**Greece-Specific Compliance Settings:**

**Tax Number (AFM) Display:**

- Format: "123.456.789" (grouped) vs "9" (continuous)
- Show DOY (Tax Office): "Α' ΑΘΗΝΩΝ"
- Show validation status: ✅ Valid AFM

**AADE Integration Display:**

- Show MyDATA submission status
- Display AADE response codes
- Show invoice QR codes
- Notification level for AADE errors

**Greek Legal Documents:**

- Official government template style
- Include regulatory references (N.4308/2014, etc.)
- Show compliance footers
- Greek legal language vs simplified explanations

**Other Countries Examples:**

**Germany:**

- Tax Number (Steuernummer): Format and validation
- VAT ID (USt-IdNr.): Display preferences
- ELSTER integration status
- German tax form templates

**France:**

- SIRET/SIREN formatting
- TVA number display
- French tax authority integration
- French legal document templates

---

## 3. TECHNICAL IMPLEMENTATION

### 3.1 API Endpoints

```typescript
// Language Preferences
"GET /api/settings/language" - Get user language preferences
"PUT /api/settings/language" - Update language preferences

// Localization Settings  
"GET /api/settings/localization" - Get localization settings
"PUT /api/settings/localization" - Update localization settings

// Business Locale Settings
"GET /api/settings/business-locale" - Get business locale settings  
"PUT /api/settings/business-locale" - Update business locale settings
"GET /api/settings/business-locale/countries" - Get supported countries
"GET /api/settings/business-locale/defaults/:country" - Get country defaults

// Compliance Settings
"GET /api/settings/compliance" - Get compliance settings
"PUT /api/settings/compliance" - Update compliance settings  
"GET /api/settings/compliance/requirements/:country" - Get country requirements
"POST /api/settings/compliance/validate" - Validate compliance settings
```

### 3.2 Custom Hooks

```typescript
// Language Management
useLanguagePreferences() - Manage language selection
useLanguageDetection() - Auto-detect user language
useLanguageFallback() - Handle missing translations

// Localization
useLocalizationSettings() - Manage formatting preferences
useDateTimeFormatting() - Date/time formatting
useNumberFormatting() - Number/currency formatting

// Business Locale
useBusinessLocale() - Manage business locale settings
useCountryDefaults() - Load country-specific defaults
useBusinessCulture() - Business culture preferences

// Compliance
useComplianceSettings() - Manage compliance preferences
useComplianceValidation() - Validate compliance settings
useGovernmentIntegration() - Government integration display
```

### 3.3 Components

```typescript
// Language Components
LanguageSelector - Language dropdown with flags
LanguageProgress - Translation completeness indicator
FallbackLanguageSelector - Fallback language selection

// Localization Components
DateFormatPreview - Live date format examples
NumberFormatPreview - Live number format examples
TimezoneSelector - Timezone selection with current time
CurrencySelector - Currency selection with formatting

// Business Locale Components
CountrySelector - Country selection with business rules
BusinessCultureForm - Communication style preferences
AddressFormatPreview - Address format examples
PhoneFormatPreview - Phone number format examples
BusinessHoursForm - Business hours configuration
HolidayCalendarSelector - Holiday calendar selection

// Compliance Components
ComplianceCountrySelector - Country with compliance info
TaxNumberFormatPreview - Tax number format examples
ComplianceStatusIndicator - Compliance validation status
GovernmentIntegrationStatus - Integration health display
LegalDocumentPreview - Legal document format preview
```

---

## 4. USER EXPERIENCE FLOW

### 4.1 First-Time Setup Wizard

**Step 1: Language Selection**

- Auto-detect browser language
- Show language selector with completion percentages
- Explain fallback language concept

**Step 2: Localization Preferences**

- Pre-fill based on detected country/language
- Show live previews of date/number formats
- Explain impact on reports and documents

**Step 3: Business Locale**

- Select country of business operations
- Load country-specific business culture defaults
- Explain business culture impact

**Step 4: Compliance Setup**

- Show country-specific compliance requirements
- Configure government integration preferences
- Validate compliance settings

### 4.2 Settings Management

**Easy Access:**

- Settings icon in user menu
- Quick language switcher in header
- Context-sensitive settings (e.g., compliance settings in tax forms)

**Change Impact Preview:**

- Show how changes affect existing data
- Preview document format changes
- Warn about compliance implications

---

## 5. EXTENSIBILITY

### 5.1 Adding New Countries

**Business Locale Extension:**

```typescript
// Add new country business rules
const BusinessLocaleCountries = {
  GR: GreekBusinessLocale,
  DE: GermanBusinessLocale,
  FR: FrenchBusinessLocale,
  IT: ItalianBusinessLocale, // New country
  ES: SpanishBusinessLocale, // New country
};
```

**Compliance Extension:**

```typescript
// Add new country compliance rules
const ComplianceCountries = {
  GR: GreekCompliance,
  DE: GermanCompliance,
  FR: FrenchCompliance,
  IT: ItalianCompliance, // New country
  ES: SpanishCompliance, // New country
};
```

### 5.2 Industry-Specific Extensions

**Healthcare Industry:**

- Medical terminology preferences
- Healthcare compliance (HIPAA, GDPR-health)
- Medical document formatting

**Financial Industry:**

- Financial regulatory preferences
- Banking compliance display
- Financial document templates

---

## 6. CONCLUSION

This 4-screen approach provides:

**✅ Logical Separation:**

- Language ≠ Country ≠ Business ≠ Compliance
- Each screen has clear, focused purpose
- No mixing of concerns

**✅ Scalability:**

- Easy to add new countries
- Easy to add new languages
- Easy to add industry-specific rules

**✅ User Experience:**

- Clear understanding of what each setting affects
- Live previews and examples
- Guided setup process

**✅ Greek Market Advantage:**

- Comprehensive Greek business culture support
- Complete AADE/government integration preferences
- Superior Greek compliance display options
- Maintains Greek specialization while being internationally scalable

**✅ International Expansion:**

- Framework ready for Germany, France, Italy, Spain
- Consistent approach across all countries
- Business culture awareness beyond language translation

This design transforms "Greek-specific settings" into a **comprehensive international business localization system** that happens to excel at Greek requirements while being extensible to any country's business culture and compliance needs.
