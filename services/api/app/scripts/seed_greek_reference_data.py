"""
Seed Greek reference data
Script to populate master database with Greek reference data
"""

import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from ..core.database import async_session
from ..models.greek_reference_data import (
    GreekRegion, GreekTaxOffice, GreekVATRate, GreekBusinessActivity,
    GreekLegalForm, GreekBank, PostalCode, VATZone, LocationType
)


async def seed_greek_regions(session: AsyncSession):
    """Seed Greek regions and prefectures"""
    print("Seeding Greek regions...")
    
    regions_data = [
        # Attica
        {"region_code": "ATT", "region_name_el": "Αττική", "region_name_en": "Attica",
         "prefecture_code": "ATT", "prefecture_name_el": "Αττική", "prefecture_name_en": "Attica",
         "location_type": LocationType.MAINLAND, "vat_zone": VATZone.STANDARD,
         "latitude": 37.9838, "longitude": 23.7275},
        
        # Central Macedonia
        {"region_code": "CM", "region_name_el": "Κεντρική Μακεδονία", "region_name_en": "Central Macedonia",
         "prefecture_code": "THE", "prefecture_name_el": "Θεσσαλονίκη", "prefecture_name_en": "Thessaloniki",
         "location_type": LocationType.MAINLAND, "vat_zone": VATZone.STANDARD,
         "latitude": 40.6401, "longitude": 22.9444},
        
        # Crete
        {"region_code": "CR", "region_name_el": "Κρήτη", "region_name_en": "Crete",
         "prefecture_code": "HER", "prefecture_name_el": "Ηράκλειο", "prefecture_name_en": "Heraklion",
         "location_type": LocationType.CRETE, "vat_zone": VATZone.REDUCED_ISLAND,
         "island_group": "crete", "is_tourist_area": True,
         "latitude": 35.3387, "longitude": 25.1442},
        
        # South Aegean
        {"region_code": "SA", "region_name_el": "Νότιο Αιγαίο", "region_name_en": "South Aegean",
         "prefecture_code": "CYC", "prefecture_name_el": "Κυκλάδες", "prefecture_name_en": "Cyclades",
         "location_type": LocationType.AEGEAN_ISLANDS, "vat_zone": VATZone.REDUCED_ISLAND,
         "island_group": "cyclades", "is_tourist_area": True,
         "latitude": 37.0833, "longitude": 25.1667},
        
        # North Aegean
        {"region_code": "NA", "region_name_el": "Βόρειο Αιγαίο", "region_name_en": "North Aegean",
         "prefecture_code": "LES", "prefecture_name_el": "Λέσβος", "prefecture_name_en": "Lesvos",
         "location_type": LocationType.AEGEAN_ISLANDS, "vat_zone": VATZone.REDUCED_ISLAND,
         "island_group": "aegean", "is_tourist_area": True,
         "latitude": 39.1000, "longitude": 26.5500},
        
        # Ionian Islands
        {"region_code": "II", "region_name_el": "Ιόνια Νησιά", "region_name_en": "Ionian Islands",
         "prefecture_code": "COR", "prefecture_name_el": "Κέρκυρα", "prefecture_name_en": "Corfu",
         "location_type": LocationType.IONIAN_ISLANDS, "vat_zone": VATZone.REDUCED_ISLAND,
         "island_group": "ionian", "is_tourist_area": True,
         "latitude": 39.6243, "longitude": 19.9217},
        
        # Western Greece
        {"region_code": "WG", "region_name_el": "Δυτική Ελλάδα", "region_name_en": "Western Greece",
         "prefecture_code": "ACH", "prefecture_name_el": "Αχαΐα", "prefecture_name_en": "Achaea",
         "location_type": LocationType.MAINLAND, "vat_zone": VATZone.STANDARD,
         "latitude": 38.2466, "longitude": 21.7346},
        
        # Central Greece
        {"region_code": "CG", "region_name_el": "Στερεά Ελλάδα", "region_name_en": "Central Greece",
         "prefecture_code": "EUB", "prefecture_name_el": "Εύβοια", "prefecture_name_en": "Euboea",
         "location_type": LocationType.MAINLAND, "vat_zone": VATZone.STANDARD,
         "latitude": 38.4667, "longitude": 23.5833},
        
        # Peloponnese
        {"region_code": "PEL", "region_name_el": "Πελοπόννησος", "region_name_en": "Peloponnese",
         "prefecture_code": "LAC", "prefecture_name_el": "Λακωνία", "prefecture_name_en": "Laconia",
         "location_type": LocationType.MAINLAND, "vat_zone": VATZone.STANDARD,
         "latitude": 37.2653, "longitude": 22.4256},
        
        # Thessaly
        {"region_code": "TH", "region_name_el": "Θεσσαλία", "region_name_en": "Thessaly",
         "prefecture_code": "LAR", "prefecture_name_el": "Λάρισα", "prefecture_name_en": "Larissa",
         "location_type": LocationType.MAINLAND, "vat_zone": VATZone.STANDARD,
         "latitude": 39.6390, "longitude": 22.4194},
        
        # Epirus
        {"region_code": "EP", "region_name_el": "Ήπειρος", "region_name_en": "Epirus",
         "prefecture_code": "IOA", "prefecture_name_el": "Ιωάννινα", "prefecture_name_en": "Ioannina",
         "location_type": LocationType.MAINLAND, "vat_zone": VATZone.STANDARD,
         "latitude": 39.6654, "longitude": 20.8504},
        
        # Western Macedonia
        {"region_code": "WM", "region_name_el": "Δυτική Μακεδονία", "region_name_en": "Western Macedonia",
         "prefecture_code": "KOZ", "prefecture_name_el": "Κοζάνη", "prefecture_name_en": "Kozani",
         "location_type": LocationType.MAINLAND, "vat_zone": VATZone.STANDARD,
         "latitude": 40.3014, "longitude": 21.7888},
        
        # Eastern Macedonia and Thrace
        {"region_code": "EMT", "region_name_el": "Ανατολική Μακεδονία και Θράκη", "region_name_en": "Eastern Macedonia and Thrace",
         "prefecture_code": "EVR", "prefecture_name_el": "Έβρος", "prefecture_name_en": "Evros",
         "location_type": LocationType.MAINLAND, "vat_zone": VATZone.STANDARD,
         "latitude": 41.1533, "longitude": 26.5575},
    ]
    
    for region_data in regions_data:
        region = GreekRegion(**region_data)
        session.add(region)
    
    await session.commit()
    print(f"Seeded {len(regions_data)} Greek regions")


async def seed_greek_tax_offices(session: AsyncSession):
    """Seed Greek tax offices (DOY)"""
    print("Seeding Greek tax offices...")
    
    # Get Athens region for reference
    athens_region = await session.execute(
        text("SELECT id FROM greek_regions WHERE region_code = 'ATT'")
    )
    athens_region_id = athens_region.scalar()
    
    # Get Thessaloniki region for reference
    thessaloniki_region = await session.execute(
        text("SELECT id FROM greek_regions WHERE prefecture_code = 'THE'")
    )
    thessaloniki_region_id = thessaloniki_region.scalar()
    
    tax_offices_data = [
        # Athens Tax Offices
        {"doy_code": "1101", "doy_name_el": "Α' ΑΘΗΝΩΝ", "doy_name_en": "Athens A'",
         "region_id": athens_region_id, "city": "Αθήνα", "address": "Λεωφόρος Κηφισίας 5",
         "postal_code": "11521", "phone": "2107281000", "is_active": True},
        
        {"doy_code": "1102", "doy_name_el": "Β' ΑΘΗΝΩΝ", "doy_name_en": "Athens B'",
         "region_id": athens_region_id, "city": "Αθήνα", "address": "Οδός Πατησίων 10",
         "postal_code": "10432", "phone": "2107282000", "is_active": True},
        
        {"doy_code": "1103", "doy_name_el": "Γ' ΑΘΗΝΩΝ", "doy_name_en": "Athens C'",
         "region_id": athens_region_id, "city": "Αθήνα", "address": "Λεωφόρος Συγγρού 15",
         "postal_code": "11742", "phone": "2107283000", "is_active": True},
        
        # Thessaloniki Tax Offices
        {"doy_code": "1301", "doy_name_el": "Α' ΘΕΣΣΑΛΟΝΙΚΗΣ", "doy_name_en": "Thessaloniki A'",
         "region_id": thessaloniki_region_id, "city": "Θεσσαλονίκη", "address": "Λεωφόρος Στρατού 26",
         "postal_code": "54640", "phone": "2313360000", "is_active": True},
        
        {"doy_code": "1302", "doy_name_el": "Β' ΘΕΣΣΑΛΟΝΙΚΗΣ", "doy_name_en": "Thessaloniki B'",
         "region_id": thessaloniki_region_id, "city": "Θεσσαλονίκη", "address": "Οδός Τσιμισκή 30",
         "postal_code": "54623", "phone": "2313361000", "is_active": True},
        
        {"doy_code": "1303", "doy_name_el": "Γ' ΘΕΣΣΑΛΟΝΙΚΗΣ", "doy_name_en": "Thessaloniki C'",
         "region_id": thessaloniki_region_id, "city": "Θεσσαλονίκη", "address": "Λεωφόρος Νίκης 25",
         "postal_code": "54624", "phone": "2313362000", "is_active": True},
    ]
    
    for tax_office_data in tax_offices_data:
        tax_office = GreekTaxOffice(**tax_office_data)
        session.add(tax_office)
    
    await session.commit()
    print(f"Seeded {len(tax_offices_data)} Greek tax offices")


async def seed_greek_vat_rates(session: AsyncSession):
    """Seed Greek VAT rates"""
    print("Seeding Greek VAT rates...")
    
    vat_rates_data = [
        # Standard VAT rates
        {"rate_code": "STD_24", "rate_name_el": "Κανονικός Συντελεστής ΦΠΑ", "rate_name_en": "Standard VAT Rate",
         "rate_percentage": 24.00, "vat_zone": VATZone.STANDARD, "location_type": LocationType.MAINLAND,
         "description_el": "Κανονικός συντελεστής ΦΠΑ 24% για την ηπειρωτική Ελλάδα",
         "description_en": "Standard VAT rate 24% for mainland Greece",
         "legal_reference": "Κώδικας ΦΠΑ, Άρθρο 21", "effective_from": datetime(2024, 1, 1), "is_active": True},
        
        # Reduced VAT rates for islands
        {"rate_code": "ISLAND_17", "rate_name_el": "Μειωμένος Συντελεστής ΦΠΑ Νησιών", "rate_name_en": "Reduced Island VAT Rate",
         "rate_percentage": 17.00, "vat_zone": VATZone.REDUCED_ISLAND, "location_type": LocationType.AEGEAN_ISLANDS,
         "description_el": "Μειωμένος συντελεστής ΦΠΑ 17% για τα νησιά του Αιγαίου",
         "description_en": "Reduced VAT rate 17% for Aegean islands",
         "legal_reference": "Κώδικας ΦΠΑ, Άρθρο 21α", "effective_from": datetime(2024, 1, 1), "is_active": True},
        
        # Reduced VAT rates for food
        {"rate_code": "FOOD_13", "rate_name_el": "Μειωμένος Συντελεστής ΦΠΑ Τροφίμων", "rate_name_en": "Reduced Food VAT Rate",
         "rate_percentage": 13.00, "vat_zone": VATZone.STANDARD, "business_type": "food_service",
         "product_category": "food", "context_conditions": {"takeaway": True},
         "description_el": "Μειωμένος συντελεστής ΦΠΑ 13% για τρόφιμα προς κατανάλωση εκτός καταστήματος",
         "description_en": "Reduced VAT rate 13% for takeaway food",
         "legal_reference": "Κώδικας ΦΠΑ, Άρθρο 21", "effective_from": datetime(2024, 1, 1), "is_active": True},
        
        # Food service dine-in
        {"rate_code": "FOOD_24", "rate_name_el": "Κανονικός Συντελεστής ΦΠΑ Εστίασης", "rate_name_en": "Standard Food Service VAT Rate",
         "rate_percentage": 24.00, "vat_zone": VATZone.STANDARD, "business_type": "food_service",
         "product_category": "food", "context_conditions": {"dine_in": True},
         "description_el": "Κανονικός συντελεστής ΦΠΑ 24% για εστίαση εντός καταστήματος",
         "description_en": "Standard VAT rate 24% for dine-in food service",
         "legal_reference": "Κώδικας ΦΠΑ, Άρθρο 21", "effective_from": datetime(2024, 1, 1), "is_active": True},
        
        # Healthcare exempt
        {"rate_code": "HEALTH_0", "rate_name_el": "Απαλλαγή ΦΠΑ Υγείας", "rate_name_en": "Healthcare VAT Exemption",
         "rate_percentage": 0.00, "vat_zone": VATZone.VAT_EXEMPT, "business_type": "healthcare",
         "description_el": "Απαλλαγή από ΦΠΑ για υπηρεσίες υγείας",
         "description_en": "VAT exemption for healthcare services",
         "legal_reference": "Κώδικας ΦΠΑ, Άρθρο 22", "effective_from": datetime(2024, 1, 1), "is_active": True},
        
        # Education exempt
        {"rate_code": "EDU_0", "rate_name_el": "Απαλλαγή ΦΠΑ Εκπαίδευσης", "rate_name_en": "Education VAT Exemption",
         "rate_percentage": 0.00, "vat_zone": VATZone.VAT_EXEMPT, "business_type": "education",
         "description_el": "Απαλλαγή από ΦΠΑ για εκπαιδευτικές υπηρεσίες",
         "description_en": "VAT exemption for educational services",
         "legal_reference": "Κώδικας ΦΠΑ, Άρθρο 22", "effective_from": datetime(2024, 1, 1), "is_active": True},
        
        # Books reduced rate
        {"rate_code": "BOOKS_6", "rate_name_el": "Μειωμένος Συντελεστής ΦΠΑ Βιβλίων", "rate_name_en": "Reduced Books VAT Rate",
         "rate_percentage": 6.00, "vat_zone": VATZone.STANDARD, "product_category": "books",
         "description_el": "Μειωμένος συντελεστής ΦΠΑ 6% για βιβλία",
         "description_en": "Reduced VAT rate 6% for books",
         "legal_reference": "Κώδικας ΦΠΑ, Άρθρο 21", "effective_from": datetime(2024, 1, 1), "is_active": True},
    ]
    
    for vat_rate_data in vat_rates_data:
        vat_rate = GreekVATRate(**vat_rate_data)
        session.add(vat_rate)
    
    await session.commit()
    print(f"Seeded {len(vat_rates_data)} Greek VAT rates")


async def seed_greek_legal_forms(session: AsyncSession):
    """Seed Greek legal forms"""
    print("Seeding Greek legal forms...")
    
    legal_forms_data = [
        {"legal_form_code": "AE", "legal_form_name_el": "Ανώνυμη Εταιρεία", "legal_form_name_en": "Societe Anonyme",
         "description_el": "Ανώνυμη εταιρεία με περιορισμένη ευθύνη των μετόχων",
         "description_en": "Limited liability company with shareholders",
         "min_capital": 25000.00, "min_shareholders": 1, "liability_type": "limited",
         "tax_rate": 24.00, "dividend_tax_rate": 5.00, "requires_board": True,
         "requires_auditor": True, "requires_publication": True, "is_active": True},
        
        {"legal_form_code": "EPE", "legal_form_name_el": "Εταιρεία Περιορισμένης Ευθύνης", "legal_form_name_en": "Limited Liability Company",
         "description_el": "Εταιρεία με περιορισμένη ευθύνη των εταίρων",
         "description_en": "Limited liability company with partners",
         "min_capital": 4500.00, "min_shareholders": 1, "max_shareholders": 50,
         "liability_type": "limited", "tax_rate": 24.00, "dividend_tax_rate": 5.00,
         "requires_board": False, "requires_auditor": False, "requires_publication": False, "is_active": True},
        
        {"legal_form_code": "OE", "legal_form_name_el": "Ομόρρυθμη Εταιρεία", "legal_form_name_en": "General Partnership",
         "description_el": "Εταιρεία με απεριόριστη ευθύνη των εταίρων",
         "description_en": "General partnership with unlimited liability",
         "min_capital": 0.00, "min_shareholders": 2, "liability_type": "unlimited",
         "tax_rate": 24.00, "requires_board": False, "requires_auditor": False,
         "requires_publication": False, "is_active": True},
        
        {"legal_form_code": "EE", "legal_form_name_el": "Ετερόρρυθμη Εταιρεία", "legal_form_name_en": "Limited Partnership",
         "description_el": "Εταιρεία με περιορισμένη και απεριόριστη ευθύνη των εταίρων",
         "description_en": "Limited partnership with mixed liability",
         "min_capital": 0.00, "min_shareholders": 2, "liability_type": "mixed",
         "tax_rate": 24.00, "requires_board": False, "requires_auditor": False,
         "requires_publication": False, "is_active": True},
        
        {"legal_form_code": "IKE", "legal_form_name_el": "Ιδιωτική Κεφαλαιουχική Εταιρεία", "legal_form_name_en": "Private Capital Company",
         "description_el": "Ιδιωτική κεφαλαιουχική εταιρεία με ευέλικτη διοίκηση",
         "description_en": "Private capital company with flexible management",
         "min_capital": 1.00, "min_shareholders": 1, "max_shareholders": 50,
         "liability_type": "limited", "tax_rate": 24.00, "dividend_tax_rate": 5.00,
         "requires_board": False, "requires_auditor": False, "requires_publication": False, "is_active": True},
        
        {"legal_form_code": "AT", "legal_form_name_el": "Ατομική Επιχείρηση", "legal_form_name_en": "Sole Proprietorship",
         "description_el": "Ατομική επιχείρηση με απεριόριστη ευθύνη του ιδιοκτήτη",
         "description_en": "Sole proprietorship with unlimited liability",
         "min_capital": 0.00, "min_shareholders": 1, "max_shareholders": 1,
         "liability_type": "unlimited", "tax_rate": 22.00, "requires_board": False,
         "requires_auditor": False, "requires_publication": False, "is_active": True},
    ]
    
    for legal_form_data in legal_forms_data:
        legal_form = GreekLegalForm(**legal_form_data)
        session.add(legal_form)
    
    await session.commit()
    print(f"Seeded {len(legal_forms_data)} Greek legal forms")


async def seed_greek_banks(session: AsyncSession):
    """Seed Greek banks"""
    print("Seeding Greek banks...")
    
    banks_data = [
        {"bank_code": "011", "bank_name_el": "Εθνική Τράπεζα της Ελλάδος", "bank_name_en": "National Bank of Greece",
         "swift_bic": "ETHNGRAA", "country_code": "GR", "bank_type": "commercial",
         "website": "https://www.nbg.gr", "phone": "2103341000", "is_active": True,
         "supports_sepa": True, "supports_instant_payments": True},
        
        {"bank_code": "014", "bank_name_el": "Τράπεζα Πειραιώς", "bank_name_en": "Piraeus Bank",
         "swift_bic": "PIRBGRAA", "country_code": "GR", "bank_type": "commercial",
         "website": "https://www.piraeusbank.gr", "phone": "2103353000", "is_active": True,
         "supports_sepa": True, "supports_instant_payments": True},
        
        {"bank_code": "017", "bank_name_el": "Τράπεζα Αττικής", "bank_name_en": "Attica Bank",
         "swift_bic": "ATTIGRAA", "country_code": "GR", "bank_type": "commercial",
         "website": "https://www.atticabank.gr", "phone": "2103366000", "is_active": True,
         "supports_sepa": True, "supports_instant_payments": False},
        
        {"bank_code": "026", "bank_name_el": "Τράπεζα Eurobank", "bank_name_en": "Eurobank",
         "swift_bic": "EFGBGRAA", "country_code": "GR", "bank_type": "commercial",
         "website": "https://www.eurobank.gr", "phone": "2109555000", "is_active": True,
         "supports_sepa": True, "supports_instant_payments": True},
        
        {"bank_code": "032", "bank_name_el": "Alpha Bank", "bank_name_en": "Alpha Bank",
         "swift_bic": "CRBAGRAA", "country_code": "GR", "bank_type": "commercial",
         "website": "https://www.alpha.gr", "phone": "2103266000", "is_active": True,
         "supports_sepa": True, "supports_instant_payments": True},
        
        {"bank_code": "001", "bank_name_el": "Τράπεζα της Ελλάδος", "bank_name_en": "Bank of Greece",
         "swift_bic": "BNGRGRAA", "country_code": "GR", "bank_type": "central",
         "website": "https://www.bankofgreece.gr", "phone": "2103201111", "is_active": True,
         "supports_sepa": True, "supports_instant_payments": False},
    ]
    
    for bank_data in banks_data:
        bank = GreekBank(**bank_data)
        session.add(bank)
    
    await session.commit()
    print(f"Seeded {len(banks_data)} Greek banks")


async def seed_sample_postal_codes(session: AsyncSession):
    """Seed sample postal codes"""
    print("Seeding sample postal codes...")
    
    # Get Athens region for reference
    athens_region = await session.execute(
        text("SELECT id FROM greek_regions WHERE region_code = 'ATT'")
    )
    athens_region_id = athens_region.scalar()
    
    postal_codes_data = [
        {"postal_code": "10431", "area_name_el": "Κέντρο Αθήνας", "area_name_en": "Athens Center",
         "region_id": athens_region_id, "municipality": "Αθήνα",
         "latitude": 37.9755, "longitude": 23.7348, "is_active": True},
        
        {"postal_code": "11521", "area_name_el": "Αμπελόκηποι", "area_name_en": "Ambelokipi",
         "region_id": athens_region_id, "municipality": "Αθήνα",
         "latitude": 37.9941, "longitude": 23.7590, "is_active": True},
        
        {"postal_code": "15342", "area_name_el": "Αγία Παρασκευή", "area_name_en": "Agia Paraskevi",
         "region_id": athens_region_id, "municipality": "Αγία Παρασκευή",
         "latitude": 37.9912, "longitude": 23.8182, "is_active": True},
        
        {"postal_code": "17778", "area_name_el": "Ταύρος", "area_name_en": "Tavros",
         "region_id": athens_region_id, "municipality": "Αθήνα",
         "latitude": 37.9428, "longitude": 23.7019, "is_active": True},
        
        {"postal_code": "18757", "area_name_el": "Κερατσίνι", "area_name_en": "Keratsini",
         "region_id": athens_region_id, "municipality": "Κερατσίνι-Δραπετσώνα",
         "latitude": 37.9611, "longitude": 23.6131, "is_active": True},
    ]
    
    for postal_code_data in postal_codes_data:
        postal_code = PostalCode(**postal_code_data)
        session.add(postal_code)
    
    await session.commit()
    print(f"Seeded {len(postal_codes_data)} sample postal codes")


async def seed_sample_business_activities(session: AsyncSession):
    """Seed sample business activities (KAD codes)"""
    print("Seeding sample business activities...")
    
    business_activities_data = [
        # Section A - Agriculture
        {"kad_code": "01", "kad_name_el": "Γεωργία, κτηνοτροφία, θήρα, δασοκομία και αλιεία",
         "kad_name_en": "Agriculture, forestry and fishing", "activity_level": 1,
         "section_code": "A", "is_active": True},
        
        {"kad_code": "01.11", "kad_name_el": "Καλλιέργεια δημητριακών (εκτός από το ρύζι), οσπρίων και σπόρων ελαιούχων φυτών",
         "kad_name_en": "Growing of cereals (except rice), leguminous crops and oil seeds",
         "activity_level": 4, "section_code": "A", "division_code": "01", "group_code": "01.1", "class_code": "01.11",
         "vat_implications": {"standard_rate": 24.0, "reduced_rate": 13.0}, "is_active": True},
        
        # Section C - Manufacturing
        {"kad_code": "10", "kad_name_el": "Παραγωγή προϊόντων διατροφής",
         "kad_name_en": "Manufacture of food products", "activity_level": 2,
         "section_code": "C", "division_code": "10", "is_active": True},
        
        {"kad_code": "10.71", "kad_name_el": "Παραγωγή άρτου και νωπών προϊόντων αρτοποιίας",
         "kad_name_en": "Manufacture of bread; manufacture of fresh pastry goods and cakes",
         "activity_level": 4, "section_code": "C", "division_code": "10", "group_code": "10.7", "class_code": "10.71",
         "vat_implications": {"standard_rate": 24.0, "reduced_rate": 13.0}, "is_active": True},
        
        # Section G - Retail
        {"kad_code": "47", "kad_name_el": "Λιανικό εμπόριο, εκτός από το εμπόριο μηχανοκίνητων οχημάτων",
         "kad_name_en": "Retail trade, except of motor vehicles and motorcycles", "activity_level": 2,
         "section_code": "G", "division_code": "47", "is_active": True},
        
        {"kad_code": "47.11", "kad_name_el": "Λιανικό εμπόριο μέσω μη ειδικευμένων καταστημάτων, με κύριο τμήμα τα τρόφιμα",
         "kad_name_en": "Retail sale in non-specialised stores with food, beverages or tobacco predominating",
         "activity_level": 4, "section_code": "G", "division_code": "47", "group_code": "47.1", "class_code": "47.11",
         "vat_implications": {"standard_rate": 24.0, "reduced_rate": 13.0}, "is_active": True},
        
        # Section I - Accommodation and food service
        {"kad_code": "56", "kad_name_el": "Δραστηριότητες υπηρεσιών εστίασης",
         "kad_name_en": "Food and beverage service activities", "activity_level": 2,
         "section_code": "I", "division_code": "56", "is_active": True},
        
        {"kad_code": "56.10", "kad_name_el": "Εστιατόρια και υπηρεσίες κινητής εστίασης",
         "kad_name_en": "Restaurants and mobile food service activities", "activity_level": 3,
         "section_code": "I", "division_code": "56", "group_code": "56.1", "class_code": "56.10",
         "vat_implications": {"dine_in_rate": 24.0, "takeaway_rate": 13.0}, "is_active": True},
        
        # Section M - Professional services
        {"kad_code": "69", "kad_name_el": "Δραστηριότητες νομικών υπηρεσιών και λογιστικής",
         "kad_name_en": "Legal and accounting activities", "activity_level": 2,
         "section_code": "M", "division_code": "69", "is_active": True},
        
        {"kad_code": "69.20", "kad_name_el": "Δραστηριότητες λογιστικής και ελέγχου λογιστικών βιβλίων",
         "kad_name_en": "Accounting, bookkeeping and auditing activities", "activity_level": 3,
         "section_code": "M", "division_code": "69", "group_code": "69.2", "class_code": "69.20",
         "vat_implications": {"standard_rate": 24.0}, "is_active": True},
        
        # Section Q - Health and social work
        {"kad_code": "86", "kad_name_el": "Δραστηριότητες ανθρώπινης υγείας",
         "kad_name_en": "Human health activities", "activity_level": 2,
         "section_code": "Q", "division_code": "86", "is_active": True},
        
        {"kad_code": "86.10", "kad_name_el": "Δραστηριότητες νοσοκομείων",
         "kad_name_en": "Hospital activities", "activity_level": 3,
         "section_code": "Q", "division_code": "86", "group_code": "86.1", "class_code": "86.10",
         "vat_implications": {"exempt": True}, "is_active": True},
    ]
    
    for business_activity_data in business_activities_data:
        business_activity = GreekBusinessActivity(**business_activity_data)
        session.add(business_activity)
    
    await session.commit()
    print(f"Seeded {len(business_activities_data)} sample business activities")


async def main():
    """Main seeding function"""
    print("Starting Greek reference data seeding...")
    
    async with async_session() as session:
        try:
            # Seed data in dependency order
            await seed_greek_regions(session)
            await seed_greek_tax_offices(session)
            await seed_greek_vat_rates(session)
            await seed_greek_legal_forms(session)
            await seed_greek_banks(session)
            await seed_sample_postal_codes(session)
            await seed_sample_business_activities(session)
            
            print("Greek reference data seeding completed successfully!")
            
        except Exception as e:
            print(f"Error during seeding: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main()) 