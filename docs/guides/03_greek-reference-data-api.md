# Greek Reference Data API Reference

## 🏛️ Overview

This guide provides API endpoints for accessing Greek reference data that's shared across all companies in the multi-tenant system.

## 📋 Prerequisites

- API service running on port 8000
- Database migrated to version 0005+
- Greek reference data seeded

## 🔗 Base Endpoints

All Greek reference data endpoints are under `/api/v1/reference/`:

### Greek Regions

**Get all regions:**

```http
GET /api/v1/reference/regions
```

**Response:**

```json
[
  {
    "id": "uuid",
    "region_code": "ATT",
    "region_name_el": "Αττική",
    "region_name_en": "Attica",
    "prefecture_code": "ATT",
    "prefecture_name_el": "Αττική",
    "prefecture_name_en": "Attica",
    "location_type": "mainland",
    "vat_zone": "standard",
    "island_group": null,
    "is_tourist_area": false
  }
]
```

**Get region by code:**

```http
GET /api/v1/reference/regions/ATT
```

### Greek Tax Offices (DOY)

**Get all tax offices:**

```http
GET /api/v1/reference/tax-offices
```

**Filter by region:**

```http
GET /api/v1/reference/tax-offices?region_code=ATT
```

**Response:**

```json
[
  {
    "id": "uuid",
    "doy_code": "1101",
    "doy_name_el": "Α' ΑΘΗΝΩΝ",
    "doy_name_en": "Athens A'",
    "city": "Αθήνα",
    "address": "Λεωφόρος Κηφισίας 5",
    "postal_code": "11521",
    "phone": "2107281000",
    "region": {
      "region_name_el": "Αττική",
      "region_name_en": "Attica"
    }
  }
]
```

### Greek VAT Rates

**Get VAT rate suggestion:**

```http
POST /api/v1/reference/vat-rates/suggest
Content-Type: application/json

{
  "business_type": "food_service",
  "product_category": "beverages",
  "location_type": "mainland",
  "context": {
    "takeaway": true
  }
}
```

**Response:**

```json
{
  "suggested_rate": 13.00,
  "rate_code": "FOOD_13",
  "rate_name_el": "Μειωμένος Συντελεστής ΦΠΑ Τροφίμων",
  "rate_name_en": "Reduced Food VAT Rate",
  "confidence": "high",
  "legal_reference": "Κώδικας ΦΠΑ, Άρθρο 21",
  "description_el": "Μειωμένος συντελεστής ΦΠΑ 13% για τρόφιμα προς κατανάλωση εκτός καταστήματος"
}
```

**Get all VAT rates:**

```http
GET /api/v1/reference/vat-rates
```

**Filter VAT rates:**

```http
GET /api/v1/reference/vat-rates?business_type=food_service&location_type=mainland
```

### Greek Business Activities (KAD)

**Get all business activities:**

```http
GET /api/v1/reference/business-activities
```

**Get by section:**

```http
GET /api/v1/reference/business-activities?section=C
```

**Search by name:**

```http
GET /api/v1/reference/business-activities?search=εστίαση
```

**Response:**

```json
[
  {
    "id": "uuid",
    "kad_code": "56.10",
    "kad_name_el": "Εστιατόρια και υπηρεσίες κινητής εστίασης",
    "kad_name_en": "Restaurants and mobile food service activities",
    "activity_level": 3,
    "section_code": "I",
    "division_code": "56",
    "group_code": "56.1",
    "class_code": "56.10",
    "vat_implications": {
      "dine_in_rate": 24.0,
      "takeaway_rate": 13.0
    }
  }
]
```

### Greek Legal Forms

**Get all legal forms:**

```http
GET /api/v1/reference/legal-forms
```

**Get legal form by code:**

```http
GET /api/v1/reference/legal-forms/EPE
```

**Response:**

```json
{
  "id": "uuid",
  "legal_form_code": "EPE",
  "legal_form_name_el": "Εταιρεία Περιορισμένης Ευθύνης",
  "legal_form_name_en": "Limited Liability Company",
  "description_el": "Εταιρεία με περιορισμένη ευθύνη των εταίρων",
  "min_capital": 4500.00,
  "min_shareholders": 1,
  "max_shareholders": 50,
  "liability_type": "limited",
  "tax_rate": 24.00,
  "dividend_tax_rate": 5.00,
  "requires_board": false,
  "requires_auditor": false
}
```

### Greek Banks

**Get all banks:**

```http
GET /api/v1/reference/banks
```

**Get bank by code:**

```http
GET /api/v1/reference/banks/011
```

**Filter active banks:**

```http
GET /api/v1/reference/banks?is_active=true&supports_sepa=true
```

**Response:**

```json
[
  {
    "id": "uuid",
    "bank_code": "011",
    "bank_name_el": "Εθνική Τράπεζα της Ελλάδος",
    "bank_name_en": "National Bank of Greece",
    "swift_bic": "ETHNGRAA",
    "country_code": "GR",
    "bank_type": "commercial",
    "supports_sepa": true,
    "supports_instant_payments": true
  }
]
```

### Postal Codes

**Get postal codes:**

```http
GET /api/v1/reference/postal-codes
```

**Search by postal code:**

```http
GET /api/v1/reference/postal-codes/10431
```

**Filter by region:**

```http
GET /api/v1/reference/postal-codes?region_code=ATT
```

**Response:**

```json
[
  {
    "id": "uuid",
    "postal_code": "10431",
    "area_name_el": "Κέντρο Αθήνας",
    "area_name_en": "Athens Center",
    "municipality": "Αθήνα",
    "region": {
      "region_name_el": "Αττική",
      "region_name_en": "Attica"
    }
  }
]
```

## 🎯 Frontend Integration Examples

### React Query Hooks

```typescript
// useGreekRegions.ts
export const useGreekRegions = () => {
  return useQuery({
    queryKey: ['greek-regions'],
    queryFn: () => api.get('/reference/regions'),
    staleTime: 1000 * 60 * 60, // 1 hour
  });
};

// useVATRateSuggestion.ts
export const useVATRateSuggestion = () => {
  return useMutation({
    mutationFn: (params: VATSuggestionParams) => 
      api.post('/reference/vat-rates/suggest', params),
  });
};

// useDOYOffices.ts
export const useDOYOffices = (regionCode?: string) => {
  return useQuery({
    queryKey: ['doy-offices', regionCode],
    queryFn: () => api.get('/reference/tax-offices', { 
      params: { region_code: regionCode } 
    }),
    enabled: !!regionCode,
  });
};
```

### Component Examples

```tsx
// GreekRegionSelector.tsx
export const GreekRegionSelector = ({ value, onChange }: Props) => {
  const { data: regions } = useGreekRegions();
  
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger>
        <SelectValue placeholder={t('select_region')} />
      </SelectTrigger>
      <SelectContent>
        {regions?.map(region => (
          <SelectItem key={region.id} value={region.region_code}>
            {region.region_name_el} ({region.region_name_en})
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
};

// VATRateCalculator.tsx
export const VATRateCalculator = ({ businessType, productCategory, context }: Props) => {
  const suggestVAT = useVATRateSuggestion();
  
  const calculateVAT = async () => {
    const result = await suggestVAT.mutateAsync({
      business_type: businessType,
      product_category: productCategory,
      location_type: "mainland",
      context
    });
  
    return result.suggested_rate;
  };
  
  // ... component implementation
};
```

## 🔧 Caching Strategy

All Greek reference data should be cached aggressively since it changes infrequently:

```typescript
// API client configuration
const greekReferenceQueryOptions = {
  staleTime: 1000 * 60 * 60 * 24, // 24 hours
  gcTime: 1000 * 60 * 60 * 24 * 7, // 7 days
  retry: 3,
};

// Apply to all reference data queries
export const useGreekRegions = () => useQuery({
  queryKey: ['greek-regions'],
  queryFn: () => api.get('/reference/regions'),
  ...greekReferenceQueryOptions,
});
```

## 🚀 Performance Tips

1. **Prefetch reference data** on app startup
2. **Use Select components** with search/filter for large datasets
3. **Cache API responses** for 24 hours minimum
4. **Lazy load** large datasets like business activities
5. **Use debounced search** for autocomplete components

## 🔐 Security Notes

- Greek reference data is **read-only** for companies
- No authentication required for reference endpoints
- Rate limiting applies (1000 requests/hour per IP)
- Data is validated and sanitized at API level

## 📝 Common Use Cases

### Company Registration Form

```typescript
// Use DOY selector, legal form selector, region selector
const [doyCode, setDoyCode] = useState('');
const [legalForm, setLegalForm] = useState('');
const [region, setRegion] = useState('');
```

### Product VAT Configuration

```typescript
// Context-aware VAT calculation
const [businessType] = useState('food_service');
const [isDineIn, setIsDineIn] = useState(false);

const vatRate = useMemo(() => {
  return suggestVATRate({
    business_type: businessType,
    context: { dine_in: isDineIn }
  });
}, [businessType, isDineIn]);
```

### Address Forms

```typescript
// Postal code validation with region detection
const [postalCode, setPostalCode] = useState('');
const { data: postalData } = usePostalCode(postalCode);

useEffect(() => {
  if (postalData?.region) {
    setRegion(postalData.region.region_code);
  }
}, [postalData]);
```

This reference data system ensures consistent, up-to-date Greek business information across your entire application! 🇬🇷
