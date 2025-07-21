"""
Greek Reference Data API Endpoints
Provides DOY offices, regions, and other Greek business reference data
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.utils.greek_validation import DOY_CODES, get_doy_list, search_doy
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/greek-reference-data")
async def get_greek_reference_data() -> Dict[str, Any]:
    """
    Get complete Greek reference data including DOY offices, regions, etc.
    
    Returns:
        Dict containing all Greek reference data for frontend components
    """
    try:
        # Convert DOY_CODES to the format expected by frontend
        doy_offices = []
        for doy_code, doy_name in DOY_CODES.items():
            doy_offices.append({
                "doyCode": doy_code,
                "doyNameEl": doy_name,
                "doyNameEn": doy_name,  # For now, use same name for both languages
                "isActive": True
            })
        
        # Basic Greek regions (simplified for now)
        regions = [
            {
                "id": "1",
                "regionCode": "ATT",
                "regionNameEl": "Αττική",
                "regionNameEn": "Attica",
                "isActive": True
            },
            {
                "id": "2", 
                "regionCode": "CMA",
                "regionNameEl": "Κεντρική Μακεδονία",
                "regionNameEn": "Central Macedonia",
                "isActive": True
            },
            {
                "id": "3",
                "regionCode": "CRT", 
                "regionNameEl": "Κρήτη",
                "regionNameEn": "Crete",
                "isActive": True
            },
            {
                "id": "4",
                "regionCode": "THS",
                "regionNameEl": "Θεσσαλία", 
                "regionNameEn": "Thessaly",
                "isActive": True
            },
            {
                "id": "5",
                "regionCode": "WGR",
                "regionNameEl": "Δυτική Ελλάδα",
                "regionNameEn": "Western Greece", 
                "isActive": True
            },
            {
                "id": "6",
                "regionCode": "EMT",
                "regionNameEl": "Ανατολική Μακεδονία και Θράκη",
                "regionNameEn": "Eastern Macedonia and Thrace",
                "isActive": True
            },
            {
                "id": "7",
                "regionCode": "SAG",
                "regionNameEl": "Νότιο Αιγαίο",
                "regionNameEn": "South Aegean",
                "isActive": True
            },
            {
                "id": "8",
                "regionCode": "NAG",
                "regionNameEl": "Βόρειο Αιγαίο", 
                "regionNameEn": "North Aegean",
                "isActive": True
            },
            {
                "id": "9",
                "regionCode": "EPI",
                "regionNameEl": "Ήπειρος",
                "regionNameEn": "Epirus",
                "isActive": True
            },
            {
                "id": "10",
                "regionCode": "ION",
                "regionNameEl": "Ιόνια Νησιά",
                "regionNameEn": "Ionian Islands",
                "isActive": True
            },
            {
                "id": "11",
                "regionCode": "WMA",
                "regionNameEl": "Δυτική Μακεδονία", 
                "regionNameEn": "Western Macedonia",
                "isActive": True
            },
            {
                "id": "12",
                "regionCode": "CGR",
                "regionNameEl": "Στερεά Ελλάδα",
                "regionNameEn": "Central Greece",
                "isActive": True
            },
            {
                "id": "13",
                "regionCode": "PEL",
                "regionNameEl": "Πελοπόννησος",
                "regionNameEn": "Peloponnese", 
                "isActive": True
            }
        ]
        
        # Basic banks (simplified for now)
        banks = [
            {
                "bankCode": "011",
                "bankNameEl": "Εθνική Τράπεζα της Ελλάδος",
                "bankNameEn": "National Bank of Greece",
                "swiftCode": "ETHNGRAA",
                "isActive": True
            },
            {
                "bankCode": "014",
                "bankNameEl": "Alpha Bank",
                "bankNameEn": "Alpha Bank",
                "swiftCode": "CRBAGRAA", 
                "isActive": True
            },
            {
                "bankCode": "026",
                "bankNameEl": "Τράπεζα Πειραιώς",
                "bankNameEn": "Piraeus Bank",
                "swiftCode": "PIRBGRAA",
                "isActive": True
            },
            {
                "bankCode": "017",
                "bankNameEl": "Eurobank",
                "bankNameEn": "Eurobank",
                "swiftCode": "ERBKGRAA",
                "isActive": True
            }
        ]
        
        # Legal forms
        legal_forms = [
            {
                "legalFormCode": "AE",
                "legalFormNameEl": "Ανώνυμη Εταιρεία",
                "legalFormNameEn": "Societe Anonyme", 
                "isActive": True
            },
            {
                "legalFormCode": "EPE",
                "legalFormNameEl": "Εταιρεία Περιορισμένης Ευθύνης",
                "legalFormNameEn": "Limited Liability Company",
                "isActive": True
            },
            {
                "legalFormCode": "OE", 
                "legalFormNameEl": "Ομόρρυθμη Εταιρεία",
                "legalFormNameEn": "General Partnership",
                "isActive": True
            },
            {
                "legalFormCode": "EE",
                "legalFormNameEl": "Ετερόρρυθμη Εταιρεία", 
                "legalFormNameEn": "Limited Partnership",
                "isActive": True
            },
            {
                "legalFormCode": "IKE",
                "legalFormNameEl": "Ιδιωτική Κεφαλαιουχική Εταιρεία",
                "legalFormNameEn": "Private Company",
                "isActive": True
            },
            {
                "legalFormCode": "AT",
                "legalFormNameEl": "Ατομική Επιχείρηση",
                "legalFormNameEn": "Sole Proprietorship",
                "isActive": True
            }
        ]
        
        # Business activities (simplified - normally would be KAD codes)
        business_activities = [
            {
                "kadCode": "6201",
                "kadNameEl": "Δραστηριότητες προγραμματισμού ηλεκτρονικών υπολογιστών",
                "kadNameEn": "Computer programming activities",
                "isActive": True
            },
            {
                "kadCode": "4711",
                "kadNameEl": "Λιανικό εμπόριο σε μη εξειδικευμένα καταστήματα",
                "kadNameEn": "Retail trade in non-specialized stores",
                "isActive": True
            },
            {
                "kadCode": "5610",
                "kadNameEl": "Εστιατόρια και υπηρεσίες κινητών εστιατορίων",
                "kadNameEn": "Restaurants and mobile food service activities",
                "isActive": True
            },
            {
                "kadCode": "6920",
                "kadNameEl": "Λογιστικές και φοροτεχνικές δραστηριότητες",
                "kadNameEn": "Accounting and tax consultancy activities",
                "isActive": True
            }
        ]
        
        return {
            "taxOffices": doy_offices,
            "regions": regions, 
            "banks": banks,
            "legalForms": legal_forms,
            "businessActivities": business_activities,
            "lastUpdated": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error getting Greek reference data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to load Greek reference data")


@router.get("/doy-offices")
async def get_doy_offices() -> List[Dict[str, str]]:
    """
    Get list of all DOY (Tax Office) codes and names
    
    Returns:
        List of DOY offices with codes and names
    """
    try:
        return get_doy_list()
    except Exception as e:
        logger.error(f"Error getting DOY offices: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to load DOY offices")


@router.get("/doy-offices/search")
async def search_doy_offices(
    q: str = Query(..., description="Search query for DOY office name or code")
) -> List[Dict[str, str]]:
    """
    Search DOY offices by name or code
    
    Args:
        q: Search query
        
    Returns:
        List of matching DOY offices
    """
    try:
        return search_doy(q)
    except Exception as e:
        logger.error(f"Error searching DOY offices: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search DOY offices") 