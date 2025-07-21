"""
Greek Business Validation Utilities
AFM, DOY, and address validation functions for Greek ERP/CRM system
"""

import re
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

# Greek DOY (Tax Office) codes and names mapping
DOY_CODES = {
    "1101": "Α' ΑΘΗΝΩΝ",
    "1102": "Β' ΑΘΗΝΩΝ", 
    "1103": "Γ' ΑΘΗΝΩΝ",
    "1104": "Δ' ΑΘΗΝΩΝ",
    "1105": "Ε' ΑΘΗΝΩΝ",
    "1106": "ΣΤ' ΑΘΗΝΩΝ",
    "1107": "Ζ' ΑΘΗΝΩΝ",
    "1108": "Η' ΑΘΗΝΩΝ",
    "1109": "ΚΗΦΙΣΙΑΣ",
    "1110": "ΑΜΑΡΟΥΣΙΟΥ",
    "1111": "ΝΕΑΣ ΙΩΝΙΑΣ",
    "1112": "ΗΡΑΚΛΕΙΟΥ ΑΤΤΙΚΗΣ",
    "1113": "ΑΧΑΡΝΩΝ",
    "1114": "ΠΕΙΡΑΙΑ",
    "1115": "Β' ΠΕΙΡΑΙΑ",
    "1116": "ΚΑΛΛΙΘΕΑΣ",
    "1117": "ΝΙΚΑΙΑΣ",
    "1118": "ΚΕΡΑΤΣΙΝΙΟΥ",
    "1119": "ΕΛΕΥΣΙΝΑΣ",
    "1120": "ΑΙΓΑΛΕΩ",
    "1121": "ΑΓ. ΔΗΜΗΤΡΙΟΥ",
    "1122": "ΓΛΥΦΑΔΑΣ",
    "1123": "ΠΑΛΑΙΟΥ ΦΑΛΗΡΟΥ",
    "1124": "ΠΕΙΡΑΜΑΤΟΣ",
    "1201": "Α' ΘΕΣΣΑΛΟΝΙΚΗΣ",
    "1202": "Β' ΘΕΣΣΑΛΟΝΙΚΗΣ",
    "1203": "Γ' ΘΕΣΣΑΛΟΝΙΚΗΣ",
    "1204": "Δ' ΘΕΣΣΑΛΟΝΙΚΗΣ",
    "1205": "ΚΑΛΑΜΑΡΙΑΣ",
    "1206": "ΣΤΑΥΡΟΥΠΟΛΗΣ",
    "1207": "ΛΑΓΚΑΔΑ",
    "1208": "ΚΑΤΕΡΙΝΗΣ",
    "1209": "ΓΙΑΝΝΙΤΣΩΝ",
    "1210": "ΕΔΕΣΣΗΣ",
    "1211": "ΚΙΛΚΙΣ",
    "1212": "ΣΕΡΡΩΝ",
    "1213": "ΔΡΑΜΑΣ",
    "1214": "ΚΑΒΑΛΑΣ",
    "1215": "ΞΑΝΘΗΣ",
    "1216": "ΚΟΜΟΤΗΝΗΣ",
    "1217": "ΑΛΕΞΑΝΔΡΟΥΠΟΛΗΣ",
    "1301": "ΛΑΡΙΣΑΣ",
    "1302": "ΒΟΛΟΥ",
    "1303": "ΤΡΙΚΑΛΩΝ",
    "1304": "ΚΑΡΔΙΤΣΑΣ",
    "1305": "ΦΑΡΣΑΛΩΝ",
    "1401": "ΠΑΤΡΩΝ",
    "1402": "ΑΙΓΙΟΥ",
    "1403": "ΠΥΡΓΟΥ",
    "1404": "ΑΜΑΛΙΑΔΑΣ",
    "1405": "ΖΑΚΥΝΘΟΥ",
    "1406": "ΚΕΦΑΛΛΗΝΙΑΣ",
    "1407": "ΚΕΡΚΥΡΑΣ",
    "1408": "ΛΕΥΚΑΔΑΣ",
    "1501": "ΗΡΑΚΛΕΙΟΥ",
    "1502": "ΧΑΝΙΩΝ",
    "1503": "ΡΕΘΥΜΝΗΣ",
    "1504": "ΛΑΣΙΘΙΟΥ",
    "1505": "ΑΓ. ΝΙΚΟΛΑΟΥ",
    "1601": "ΜΥΤΙΛΗΝΗΣ",
    "1602": "ΧΙΟΥ",
    "1603": "ΣΑΜΟΥ",
    "1604": "ΣΥΡΟΥ",
    "1605": "ΝΑΞΟΥ",
    "1606": "ΠΑΡΟΥ",
    "1607": "ΘΗΡΑΣ",
    "1608": "ΜΥΚΟΝΟΥ",
    "1609": "ΡΟΔΟΥ",
    "1610": "ΚΩ",
    "1611": "ΚΑΛΥΜΝΟΥ",
    "1612": "ΚΑΡΠΑΘΟΥ"
}

def validate_afm(afm: str) -> Dict[str, Any]:
    """
    Validate Greek AFM (Tax Identification Number)
    
    Args:
        afm: AFM string to validate
        
    Returns:
        Dict with validation result, is_valid boolean, and error message if any
    """
    result = {
        "is_valid": False,
        "afm": afm,
        "error": None,
        "normalized_afm": None
    }
    
    if not afm:
        result["error"] = "AFM is required"
        return result
    
    # Remove spaces and convert to string
    afm = str(afm).replace(" ", "").strip()
    
    # Check length
    if len(afm) != 9:
        result["error"] = "AFM must be exactly 9 digits"
        return result
    
    # Check if all characters are digits
    if not afm.isdigit():
        result["error"] = "AFM must contain only digits"
        return result
    
    # AFM validation algorithm
    try:
        # Convert to list of integers
        digits = [int(d) for d in afm]
        
        # Calculate check digit using official algorithm
        sum_total = 0
        for i in range(8):
            sum_total += digits[i] * (2 ** (8 - i))
        
        check_digit = sum_total % 11
        
        # Handle special cases
        if check_digit == 10:
            check_digit = 0
        
        # Validate check digit
        if check_digit != digits[8]:
            result["error"] = "Invalid AFM - check digit mismatch"
            return result
        
        # AFM is valid
        result["is_valid"] = True
        result["normalized_afm"] = afm
        
        return result
        
    except Exception as e:
        result["error"] = f"AFM validation error: {str(e)}"
        return result

def validate_amka(amka: str) -> Dict[str, Any]:
    """
    Validate Greek AMKA (Social Security Number)
    
    Args:
        amka: AMKA string to validate
        
    Returns:
        Dict with validation result, is_valid boolean, and error message if any
    """
    result = {
        "is_valid": False,
        "amka": amka,
        "error": None,
        "normalized_amka": None
    }
    
    if not amka:
        result["error"] = "AMKA is required"
        return result
    
    # Remove spaces and convert to string
    amka = str(amka).replace(" ", "").strip()
    
    # Check length
    if len(amka) != 11:
        result["error"] = "AMKA must be exactly 11 digits"
        return result
    
    # Check if all characters are digits
    if not amka.isdigit():
        result["error"] = "AMKA must contain only digits"
        return result
    
    # AMKA validation algorithm
    try:
        # Convert to list of integers
        digits = [int(d) for d in amka]
        
        # Basic validation - check date components
        # First 6 digits represent birth date (DDMMYY)
        day = digits[0] * 10 + digits[1]
        month = digits[2] * 10 + digits[3]
        year = digits[4] * 10 + digits[5]
        
        # Validate day (01-31)
        if day < 1 or day > 31:
            result["error"] = "Invalid AMKA - invalid day"
            return result
        
        # Validate month (01-12)
        if month < 1 or month > 12:
            result["error"] = "Invalid AMKA - invalid month"
            return result
        
        # Calculate check digit using Luhn algorithm
        sum_total = 0
        for i in range(10):
            digit = digits[i]
            if i % 2 == 0:  # Even positions (0-indexed)
                digit *= 2
                if digit > 9:
                    digit = digit // 10 + digit % 10
            sum_total += digit
        
        check_digit = (10 - (sum_total % 10)) % 10
        
        # Validate check digit
        if check_digit != digits[10]:
            result["error"] = "Invalid AMKA - check digit mismatch"
            return result
        
        # AMKA is valid
        result["is_valid"] = True
        result["normalized_amka"] = amka
        
        return result
        
    except Exception as e:
        result["error"] = f"AMKA validation error: {str(e)}"
        return result

def validate_doy(doy: str) -> Dict[str, Any]:
    """
    Validate Greek DOY (Tax Office) code
    
    Args:
        doy: DOY code to validate
        
    Returns:
        Dict with validation result, is_valid boolean, office name, and error message if any
    """
    result = {
        "is_valid": False,
        "doy": doy,
        "doy_name": None,
        "error": None
    }
    
    if not doy:
        result["error"] = "DOY is required"
        return result
    
    # Remove spaces and convert to string
    doy = str(doy).replace(" ", "").strip()
    
    # Check if DOY exists in our mapping
    if doy in DOY_CODES:
        result["is_valid"] = True
        result["doy_name"] = DOY_CODES[doy]
        return result
    
    # Check if it's a 4-digit number (for future DOY codes)
    if len(doy) == 4 and doy.isdigit():
        result["is_valid"] = True
        result["doy_name"] = f"Unknown DOY Office ({doy})"
        return result
    
    result["error"] = "Invalid DOY code format or unknown DOY office"
    return result

def validate_greek_postal_code(postal_code: str, city: str = None) -> Dict[str, Any]:
    """
    Validate Greek postal code
    
    Args:
        postal_code: Postal code to validate
        city: Optional city name for additional validation
        
    Returns:
        Dict with validation result
    """
    result = {
        "is_valid": False,
        "postal_code": postal_code,
        "region": None,
        "error": None
    }
    
    if not postal_code:
        result["error"] = "Postal code is required"
        return result
    
    # Remove spaces and convert to string
    postal_code = str(postal_code).replace(" ", "").strip()
    
    # Check length (Greek postal codes are 5 digits)
    if len(postal_code) != 5:
        result["error"] = "Greek postal code must be exactly 5 digits"
        return result
    
    # Check if all characters are digits
    if not postal_code.isdigit():
        result["error"] = "Postal code must contain only digits"
        return result
    
    # Basic region validation based on first digits
    first_two = postal_code[:2]
    region_mapping = {
        "10": "Αττική (Κέντρο Αθηνών)",
        "11": "Αττική (Βόρεια Αθήνα)",
        "12": "Αττική (Νότια Αθήνα)",
        "13": "Αττική (Ανατολική Αθήνα)",
        "14": "Αττική (Δυτική Αθήνα)",
        "15": "Αττική (Πειραιάς)",
        "16": "Αττική (Νότια Προάστια)",
        "17": "Αττική (Βόρεια Προάστια)",
        "18": "Αττική (Ανατολική Αττική)",
        "19": "Αττική (Δυτική Αττική)",
        "20": "Αττική (Νησιά Αργοσαρωνικού)",
        "50": "Κεντρική Μακεδονία (Θεσσαλονίκη)",
        "51": "Κεντρική Μακεδονία",
        "52": "Κεντρική Μακεδονία",
        "53": "Κεντρική Μακεδονία",
        "54": "Κεντρική Μακεδονία",
        "55": "Κεντρική Μακεδονία",
        "56": "Ανατολική Μακεδονία και Θράκη",
        "57": "Ανατολική Μακεδονία και Θράκη",
        "58": "Ανατολική Μακεδονία και Θράκη",
        "59": "Ανατολική Μακεδονία και Θράκη",
        "60": "Ανατολική Μακεδονία και Θράκη",
        "61": "Ανατολική Μακεδονία και Θράκη",
        "62": "Ανατολική Μακεδονία και Θράκη",
        "63": "Ανατολική Μακεδονία και Θράκη",
        "64": "Ανατολική Μακεδονία και Θράκη",
        "65": "Ανατολική Μακεδονία και Θράκη",
        "66": "Ανατολική Μακεδονία και Θράκη",
        "67": "Ανατολική Μακεδονία και Θράκη",
        "68": "Ανατολική Μακεδονία και Θράκη",
        "69": "Ανατολική Μακεδονία και Θράκη",
        "70": "Κρήτη",
        "71": "Κρήτη",
        "72": "Κρήτη",
        "73": "Κρήτη",
        "74": "Κρήτη",
        "80": "Νότιο Αιγαίο",
        "81": "Νότιο Αιγαίο",
        "82": "Νότιο Αιγαίο",
        "83": "Νότιο Αιγαίο",
        "84": "Νότιο Αιγαίο",
        "85": "Νότιο Αιγαίο",
        "86": "Δωδεκάνησα",
        "87": "Δωδεκάνησα"
    }
    
    region = region_mapping.get(first_two, "Unknown Region")
    
    result["is_valid"] = True
    result["region"] = region
    
    return result

def validate_greek_phone(phone: str) -> Dict[str, Any]:
    """
    Validate Greek phone number
    
    Args:
        phone: Phone number to validate
        
    Returns:
        Dict with validation result
    """
    result = {
        "is_valid": False,
        "phone": phone,
        "normalized_phone": None,
        "phone_type": None,
        "error": None
    }
    
    if not phone:
        result["error"] = "Phone number is required"
        return result
    
    # Remove spaces, dashes, parentheses
    phone_clean = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Handle international format
    if phone_clean.startswith('+30'):
        phone_clean = phone_clean[3:]
    elif phone_clean.startswith('0030'):
        phone_clean = phone_clean[4:]
    
    # Remove leading zero if present
    if phone_clean.startswith('0'):
        phone_clean = phone_clean[1:]
    
    # Validate length and format
    if len(phone_clean) == 10 and phone_clean.isdigit():
        # Determine phone type
        if phone_clean.startswith('2'):
            phone_type = "Landline"
        elif phone_clean.startswith('69'):
            phone_type = "Mobile"
        elif phone_clean.startswith('68'):
            phone_type = "Mobile"
        elif phone_clean.startswith('67'):
            phone_type = "Mobile"
        else:
            phone_type = "Unknown"
        
        result["is_valid"] = True
        result["normalized_phone"] = f"+30{phone_clean}"
        result["phone_type"] = phone_type
    else:
        result["error"] = "Invalid Greek phone number format"
    
    return result

def validate_greek_address(address_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate complete Greek address
    
    Args:
        address_data: Dict containing address fields
        
    Returns:
        Dict with validation result for entire address
    """
    result = {
        "is_valid": True,
        "errors": [],
        "warnings": [],
        "validated_fields": {}
    }
    
    # Validate postal code
    if "postal_code" in address_data:
        postal_validation = validate_greek_postal_code(
            address_data["postal_code"], 
            address_data.get("city")
        )
        result["validated_fields"]["postal_code"] = postal_validation
        if not postal_validation["is_valid"]:
            result["is_valid"] = False
            result["errors"].append(f"Postal code: {postal_validation['error']}")
    
    # Validate required fields
    required_fields = ["address_street", "address_city"]
    for field in required_fields:
        if field not in address_data or not address_data[field]:
            result["is_valid"] = False
            result["errors"].append(f"{field.replace('address_', '').title()} is required")
    
    # Validate city name (basic check for Greek characters)
    if "address_city" in address_data and address_data["address_city"]:
        city = address_data["address_city"]
        if not re.match(r'^[Α-Ωα-ωA-Za-z\s\-\.]+$', city):
            result["warnings"].append("City name contains unusual characters")
    
    return result

def get_doy_list() -> List[Dict[str, str]]:
    """
    Get list of all DOY offices
    
    Returns:
        List of dicts with doy_code and doy_name
    """
    return [
        {"doy_code": code, "doy_name": name}
        for code, name in DOY_CODES.items()
    ]

def search_doy(query: str) -> List[Dict[str, str]]:
    """
    Search DOY offices by name or code
    
    Args:
        query: Search query
        
    Returns:
        List of matching DOY offices
    """
    if not query:
        return []
    
    query = query.upper().strip()
    results = []
    
    for code, name in DOY_CODES.items():
        if query in code or query in name:
            results.append({"doy_code": code, "doy_name": name})
    
    return results[:10]  # Limit results 