from pydantic import BaseModel
from typing import List, Optional

class QuestionnaireInput(BaseModel):
    # Question 1: Gender (required)
    gender: str                     # 男、女、其他

    # Question 2: Age (required)
    age_group: str                  # "未满18", "18-39", "40-64", "65+"

    # Question 3: Cancer diagnosis (required)
    diagnosed: bool                 # True/False

    # Question 4: Cancer types (required, can be multiple)
    cancer_types: List[str]         # ["结直肠癌", "肺癌", etc.] - required list

    # Question 5: Gene mutation (required field, can be empty string if unknown)
    gene_mutation: str              # "EGFR", "KRAS", "" for unknown, "不清楚" for unclear

    # Question 6: Metastasis status (required)
    metastasis_status: str          # "无转移", "寡转移", "广泛转移", "不清楚"

    # Question 7: Recent surgery (required)
    recent_surgery: bool            # True/False - now required based on survey

    # Question 8: ECOG score (required)
    ecog_score: str                 # "0", "1", "2", "≥3", "不清楚"

    # Question 9: Treatment stage (required)
    treatment_stage: str            # "尚未治疗", "一线治疗中", "二线或多线", "复发或观察期", "不清楚"

    # Question 10: Active infection (required)
    active_infection: bool          # True/False

    # Question 11: Recent drugs (required list, can be empty)
    recent_drugs: List[str]         # ["化疗药物", "靶向药物", "免疫治疗", etc.]

    # Question 12: Health conditions (required list, can be empty)
    health_conditions: List[str]    # ["心脏病", "活动性自身免疫", etc.]

    # Question 13: Upload reports willingness (required)
    upload_reports: bool            # True/False

    # Question 14: Data collection consent (required)
    consent_data_collection: bool   # True/False

    # Add these paitent info
    patient_name: str
    date_of_birth: str  # Format: "MM/DD/YYYY"
    current_location: str  # e.g., "New York, NY"
    preferred_country: str  # e.g., "United States", "Canada", etc.