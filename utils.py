"""
Common utilities for clinical trial matching system
Contains shared functions used across multiple modules
"""

import re
from typing import Optional


def generate_clinicaltrials_url(nct_id: str) -> str:
    """
    Generate standardized ClinicalTrials.gov URL

    Args:
        nct_id: Clinical trial NCT ID

    Returns:
        Full URL to trial details page
    """
    return f"https://clinicaltrials.gov/ct2/show/{nct_id}"


def parse_age(age_str: str) -> int:
    """
    Parse age string to extract numeric value

    Args:
        age_str: Age string like "18 Years", "65 years", etc.

    Returns:
        Numeric age value, 0 if parsing fails
    """
    if not age_str:
        return 0

    numbers = re.findall(r'\d+', age_str)
    return int(numbers[0]) if numbers else 0


def normalize_gender(gender: str) -> str:
    """
    Normalize gender input to standard values

    Args:
        gender: Gender string in various formats

    Returns:
        Normalized gender: "MALE", "FEMALE", or "ALL"
    """
    gender_mapping = {
        "男": "MALE",
        "女": "FEMALE",
        "其他": "ALL",
        "male": "MALE",
        "female": "FEMALE",
        "m": "MALE",
        "f": "FEMALE",
        "other": "ALL"
    }
    return gender_mapping.get(gender.lower(), "ALL")


def clean_text(text: str) -> str:
    """
    Clean and normalize text for matching

    Args:
        text: Raw text string

    Returns:
        Cleaned lowercase text
    """
    if not text:
        return ""

    # Convert to lowercase and strip whitespace
    cleaned = text.lower().strip()

    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned)

    return cleaned


def extract_nct_id(trial_data: dict) -> str:
    """
    Safely extract NCT ID from trial data

    Args:
        trial_data: Trial data dictionary

    Returns:
        NCT ID string or empty string if not found
    """
    try:
        return trial_data.get("protocolSection", {}).get("identificationModule", {}).get("nctId", "")
    except (AttributeError, KeyError):
        return ""


def safe_get_nested(data: dict, keys: list, default=None):
    """
    Safely get nested dictionary values

    Args:
        data: Dictionary to search
        keys: List of keys for nested access
        default: Default value if key path not found

    Returns:
        Value at nested key path or default
    """
    try:
        result = data
        for key in keys:
            result = result[key]
        return result
    except (KeyError, TypeError, AttributeError):
        return default


def format_percentage(value: float, decimal_places: int = 1) -> str:
    """
    Format percentage value with consistent formatting

    Args:
        value: Percentage value (0-100)
        decimal_places: Number of decimal places

    Returns:
        Formatted percentage string
    """
    return f"{value:.{decimal_places}f}%"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to specified length with suffix

    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
        suffix: Suffix to add when truncating

    Returns:
        Truncated text string
    """
    if not text or len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def validate_ecog_score(ecog: str) -> bool:
    """
    Validate ECOG performance status score

    Args:
        ecog: ECOG score string

    Returns:
        True if valid ECOG score
    """
    valid_scores = ["0", "1", "2", "3", "3+", "4"]
    return ecog in valid_scores


def categorize_age_group(age: int) -> str:
    """
    Categorize numeric age into age groups

    Args:
        age: Numeric age

    Returns:
        Age group string
    """
    if age < 18:
        return "Under 18"
    elif age <= 39:
        return "18-39"
    elif age <= 64:
        return "40-64"
    else:
        return "65+"


def is_valid_nct_id(nct_id: str) -> bool:
    """
    Validate NCT ID format

    Args:
        nct_id: NCT ID string

    Returns:
        True if valid NCT ID format
    """
    if not nct_id:
        return False

    # NCT ID should start with NCT followed by 8 digits
    pattern = r'^NCT\d{8}$'
    return bool(re.match(pattern, nct_id))


def calculate_score_level(score: float) -> str:
    """
    Calculate score level description

    Args:
        score: Score percentage (0-100)

    Returns:
        Score level description
    """
    if score >= 80:
        return "🌟 Excellent Match - Highly Recommended!"
    elif score >= 65:
        return "✨ Very Good Match - Definitely Worth Exploring"
    elif score >= 50:
        return "💡 Good Potential - Recommended for Discussion"
    elif score >= 35:
        return "📋 Possible Match - Consider with Your Doctor"
    else:
        return "📞 Worth Asking About - Contact for Eligibility Check"