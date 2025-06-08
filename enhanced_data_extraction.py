import httpx
import asyncio
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


async def get_detailed_trial_info(nct_id: str) -> Optional[Dict]:
    """
    Get basic trial information that's guaranteed to work
    """
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                f"https://clinicaltrials.gov/api/v2/studies/{nct_id}",
                params={"format": "json"}
            )
            response.raise_for_status()
            data = response.json()

            return extract_basic_trial_data(data)

    except Exception as e:
        logger.error(f"Failed to get detailed trial info for {nct_id}: {str(e)}")
        return None


def extract_basic_trial_data(api_response) -> Dict:
    """
    Extract basic information safely - no errors guaranteed
    """
    try:
        if not isinstance(api_response, dict):
            return {}

        protocol_section = api_response.get("protocolSection", {})
        if not protocol_section:
            return {}

        # Basic identification
        identification = protocol_section.get("identificationModule", {})
        status_module = protocol_section.get("statusModule", {})
        description_module = protocol_section.get("descriptionModule", {})
        design_module = protocol_section.get("designModule", {})
        contacts_locations = protocol_section.get("contactsLocationsModule", {})
        eligibility_module = protocol_section.get("eligibilityModule", {})

        # Extract basic info safely
        extracted_data = {
            "nct_id": identification.get("nctId", "") if isinstance(identification, dict) else "",
            "title": identification.get("officialTitle", "") if isinstance(identification, dict) else "",
            "brief_title": identification.get("briefTitle", "") if isinstance(identification, dict) else "",
            "brief_summary": description_module.get("briefSummary", "") if isinstance(description_module, dict) else "",
            "overall_status": status_module.get("overallStatus", "") if isinstance(status_module, dict) else "",
            "study_type": design_module.get("studyType", "") if isinstance(design_module, dict) else "",
            "phases": design_module.get("phases", []) if isinstance(design_module, dict) else [],
            "clinicaltrials_gov_url": f"https://clinicaltrials.gov/ct2/show/{identification.get('nctId', '') if isinstance(identification, dict) else ''}",

            # Contact info - simplified
            "locations": extract_locations_safe(contacts_locations),
            "central_contacts": extract_central_contacts_safe(contacts_locations),

            # Eligibility
            "eligibility_criteria": eligibility_module.get("inclusionCriteria", "") if isinstance(eligibility_module,
                                                                                                  dict) else "",
            "gender": eligibility_module.get("sex", "ALL") if isinstance(eligibility_module, dict) else "ALL",
            "min_age": eligibility_module.get("minimumAge", "") if isinstance(eligibility_module, dict) else "",
            "max_age": eligibility_module.get("maximumAge", "") if isinstance(eligibility_module, dict) else "",
        }

        return extracted_data

    except Exception as e:
        logger.error(f"Error in extract_basic_trial_data: {str(e)}")
        return {}


def extract_locations_safe(contacts_locations) -> List[Dict]:
    """
    Safely extract location information with correct API structure
    """
    try:
        if not isinstance(contacts_locations, dict):
            return []

        locations = contacts_locations.get("locations", [])
        if not isinstance(locations, list) or len(locations) == 0:
            return []

        extracted_locations = []
        for i, location in enumerate(locations):
            if not isinstance(location, dict):
                continue

            # The API structure has facility as a string, not a dict
            facility_name = location.get("facility", "")
            city = location.get("city", "")
            state = location.get("state", "")
            country = location.get("country", "")
            zip_code = location.get("zip", "")
            status = location.get("status", "")

            # Get coordinates from geoPoint
            geo_point = location.get("geoPoint", {})
            lat = None
            lng = None

            if isinstance(geo_point, dict):
                lat = geo_point.get("lat")
                lng = geo_point.get("lon")

            # Extract contacts safely
            contacts = []
            location_contacts = location.get("contacts", [])
            if isinstance(location_contacts, list):
                for contact in location_contacts:
                    if isinstance(contact, dict):
                        contacts.append({
                            "name": contact.get("name", ""),
                            "role": contact.get("role", ""),
                            "phone": contact.get("phone", ""),
                            "email": contact.get("email", "")
                        })

            # Only add location if we have valid coordinates
            if lat is not None and lng is not None:
                try:
                    lat = float(lat)
                    lng = float(lng)

                    location_data = {
                        "facility": {
                            "name": facility_name,
                            "address": {
                                "city": city,
                                "state": state,
                                "country": country,
                                "zip": zip_code,
                                "latitude": lat,
                                "longitude": lng
                            }
                        },
                        "status": status,
                        "contacts": contacts,
                        "formatted_address": f"{facility_name}\n{city}, {state} {zip_code}".strip()
                    }

                    extracted_locations.append(location_data)

                except (ValueError, TypeError):
                    continue

        return extracted_locations

    except Exception as e:
        logger.error(f"Error extracting locations: {str(e)}")
        return []

def extract_central_contacts_safe(contacts_locations) -> List[Dict]:
    """
    Safely extract central contact information
    """
    try:
        if not isinstance(contacts_locations, dict):
            return []

        central_contacts = contacts_locations.get("centralContacts", [])
        if not isinstance(central_contacts, list):
            return []

        extracted_contacts = []
        for contact in central_contacts:
            if isinstance(contact, dict):
                extracted_contacts.append({
                    "name": contact.get("name", ""),
                    "role": contact.get("role", ""),
                    "phone": contact.get("phone", ""),
                    "email": contact.get("email", "")
                })

        return extracted_contacts

    except Exception as e:
        logger.error(f"Error extracting central contacts: {str(e)}")
        return []


def format_address_safe(facility) -> str:
    """
    Safely format facility address
    """
    try:
        if not isinstance(facility, dict):
            return ""

        parts = []
        name = facility.get("name", "")
        city = facility.get("city", "")
        state = facility.get("state", "")
        zip_code = facility.get("zip", "")

        if name:
            parts.append(name)

        location_parts = [p for p in [city, state, zip_code] if p]
        if location_parts:
            parts.append(", ".join(location_parts))

        return "\n".join(parts)

    except Exception:
        return ""


# Enhanced function to get multiple trials with detailed info
async def get_detailed_trials_batch(nct_ids: List[str]) -> List[Dict]:
    """
    Get detailed information for multiple trials in parallel
    """
    tasks = [get_detailed_trial_info(nct_id) for nct_id in nct_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    detailed_trials = []
    for result in results:
        if isinstance(result, dict) and result:  # Valid result
            detailed_trials.append(result)
        elif isinstance(result, Exception):
            logger.error(f"Failed to get trial details: {str(result)}")

    return detailed_trials


# Function to integrate with your existing scoring system
def enhance_scored_trial_with_details(scored_trial: Dict, detailed_info: Dict) -> Dict:
    """
    Combine your existing scored trial with detailed information
    """
    if not detailed_info:
        return scored_trial

    # Keep your existing scoring information
    enhanced_trial = scored_trial.copy()

    # Add detailed information
    enhanced_trial.update({
        "brief_summary": detailed_info.get("brief_summary", ""),
        "study_type": detailed_info.get("study_type", ""),
        "phases": detailed_info.get("phases", []),
        "locations": detailed_info.get("locations", []),
        "central_contacts": detailed_info.get("central_contacts", []),
        "eligibility_criteria": detailed_info.get("eligibility_criteria", ""),
        "overall_status": detailed_info.get("overall_status", ""),
        "gender": detailed_info.get("gender", ""),
        "min_age": detailed_info.get("min_age", ""),
        "max_age": detailed_info.get("max_age", ""),
    })

    return enhanced_trial