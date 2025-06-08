from models import QuestionnaireInput
from medical_dictionary import get_cancer_synonyms
import re
from typing import Dict, List, Tuple


def score_trial(trial: dict, user_input: QuestionnaireInput) -> dict:
    """
    Revised scoring system based on survey weight analysis
    Total: 100 points distributed according to medical importance
    """
    explanations = []
    risk_flags = []

    # Extract trial information
    protocol_section = trial.get("protocolSection", {})
    identification = protocol_section.get("identificationModule", {})
    eligibility = protocol_section.get("eligibilityModule", {})

    title = identification.get("officialTitle", "").lower()
    nct_id = identification.get("nctId", "")
    url = f"https://clinicaltrials.gov/ct2/show/{nct_id}"

    inclusion_criteria = eligibility.get("inclusionCriteria", "").lower()
    exclusion_criteria = eligibility.get("exclusionCriteria", "").lower()

    # Initialize score
    match_score = 0

    # ======================
    # 1. CANCER TYPE MATCHING - 30% (30 points) - PRIMARY FILTER
    # ======================
    cancer_score, cancer_explanation = score_cancer_type_match(
        user_input.cancer_types, title, inclusion_criteria
    )
    match_score += cancer_score
    explanations.append(cancer_explanation)

    # ======================
    # 2. GENE MUTATION MATCHING - 20% (20 points) - PRECISION MEDICINE
    # ======================
    gene_score, gene_explanation = score_gene_mutation_match(
        user_input.gene_mutation, title, inclusion_criteria
    )
    match_score += gene_score
    explanations.append(gene_explanation)

    # ======================
    # 3. METASTASIS STATUS - 10% (10 points) - DISEASE STAGE
    # ======================
    metastasis_score, metastasis_explanation = score_metastasis_match(
        user_input.metastasis_status, inclusion_criteria
    )
    match_score += metastasis_score
    explanations.append(metastasis_explanation)

    # ======================
    # 4. ECOG PERFORMANCE STATUS - 10% (10 points) - ELIGIBILITY CRITICAL
    # ======================
    ecog_score, ecog_explanation = score_ecog_match(
        user_input.ecog_score, inclusion_criteria, exclusion_criteria
    )
    match_score += ecog_score
    explanations.append(ecog_explanation)

    # ======================
    # 5. TREATMENT STAGE - 10% (10 points) - TREATMENT CONTEXT
    # ======================
    treatment_score, treatment_explanation = score_treatment_stage_match(
        user_input.treatment_stage, user_input.recent_surgery, inclusion_criteria
    )
    match_score += treatment_score
    explanations.append(treatment_explanation)

    # ======================
    # 6. AGE ELIGIBILITY - 5% (5 points) - HARD REQUIREMENT
    # ======================
    age_score, age_explanation = score_age_eligibility(
        user_input.age_group, eligibility
    )
    match_score += age_score
    if age_score == 0:
        risk_flags.append("Age restriction")
    explanations.append(age_explanation)

    # ======================
    # 7. GENDER ELIGIBILITY - 5% (5 points) - HARD REQUIREMENT
    # ======================
    gender_score, gender_explanation = score_gender_eligibility(
        user_input.gender, eligibility
    )
    match_score += gender_score
    if gender_score == 0:
        risk_flags.append("Gender restriction")
    explanations.append(gender_explanation)

    # ======================
    # 8. HEALTH CONDITIONS - 5% (5 points) - SAFETY EXCLUSIONS
    # ======================
    health_score, health_explanation = score_health_safety(
        user_input.health_conditions, user_input.active_infection, exclusion_criteria
    )
    match_score += health_score
    if health_score < 3:
        risk_flags.append("Health safety concerns")
    explanations.append(health_explanation)

    # ======================
    # 9. PARTICIPATION READINESS - 5% (5 points) - ENGAGEMENT BONUS
    # ======================
    participation_score, participation_explanation = score_participation_readiness(
        user_input.upload_reports, user_input.consent_data_collection
    )
    match_score += participation_score
    explanations.append(participation_explanation)

    # ======================
    # FINAL SCORE CALCULATION
    # ======================
    final_score = max(0, min(100, match_score))

    # Generate recommendation levels
    if final_score >= 85:
        level = "🌟 Excellent Match - Highly Recommended!"
    elif final_score >= 70:
        level = "✨ Very Good Match - Definitely Worth Exploring"
    elif final_score >= 55:
        level = "💡 Good Potential - Recommended for Discussion"
    elif final_score >= 35:
        level = "📋 Possible Match - Consider with Your Doctor"
    else:
        level = "📞 Limited Match - Contact for Eligibility Check"

    return {
        "nct_id": nct_id,
        "title": identification.get("officialTitle", ""),
        "url": url,
        "score_percent": round(final_score, 1),
        "level": level,
        "explanations": explanations,
        "risk_flags": risk_flags
    }


def score_cancer_type_match(cancer_types: List[str], title: str, inclusion: str) -> Tuple[float, str]:
    """
    Score cancer type matching - 30 points maximum
    This is the primary filter - if cancer doesn't match, low score
    """
    if not cancer_types:
        return 5, "⚠️ Cancer type information needed for accurate matching"

    primary_cancer = cancer_types[0].lower()

    # Perfect match in title (25 points)
    if primary_cancer in title:
        return 25, f"🎯 Perfect Cancer Match: {primary_cancer.title()} trial specifically designed for your diagnosis"

    # Good match in inclusion criteria (20 points)
    if primary_cancer in inclusion:
        return 20, f"✅ Strong Cancer Match: {primary_cancer.title()} mentioned in trial eligibility"

    # Synonym match (15 points)
    synonyms = get_cancer_synonyms(primary_cancer)
    for synonym in synonyms:
        if synonym.lower() in title or synonym.lower() in inclusion:
            return 15, f"✅ Cancer Type Match: Trial includes {synonym} which matches your {primary_cancer}"

    # Pan-cancer or solid tumor trials (10 points)
    pan_cancer_keywords = ["solid tumor", "advanced cancer", "metastatic cancer", "any cancer"]
    for keyword in pan_cancer_keywords:
        if keyword in title or keyword in inclusion:
            return 10, f"✅ Broad Eligibility: Pan-cancer trial accepts multiple cancer types"

    # No clear match (5 points - minimum)
    return 5, "⚠️ Cancer type match unclear - requires detailed eligibility review"


def score_gene_mutation_match(gene_mutation: str, title: str, inclusion: str) -> Tuple[float, str]:
    """
    Score gene mutation matching - 20 points maximum
    Critical for precision medicine trials
    """
    if not gene_mutation:
        return 5, "⚠️ No genetic testing information - may miss targeted therapy opportunities"

    gene = gene_mutation.upper()

    # Perfect gene match in title (20 points)
    if gene in title.upper():
        return 20, f"🎯 Perfect Genetic Match: {gene} targeted therapy trial"

    # Gene match in inclusion criteria (18 points)
    if gene in inclusion.upper():
        return 18, f"🎯 Genetic Target Match: Trial specifically targets {gene} mutations"

    # Gene-related patterns (15 points)
    gene_patterns = [
        f"{gene.lower()} mutation",
        f"{gene.lower()} positive",
        f"{gene.lower()}\\+",
        f"{gene.lower()} targeted"
    ]

    for pattern in gene_patterns:
        if re.search(pattern, inclusion, re.IGNORECASE):
            return 15, f"✅ Targeted Therapy Match: Trial focuses on {gene} alterations"

    # Broad molecular profiling (8 points)
    molecular_keywords = ["biomarker", "molecular profiling", "genetic testing", "mutation"]
    if any(keyword in inclusion for keyword in molecular_keywords):
        return 8, f"✅ Molecular Medicine: Trial includes genetic profiling (your {gene} status relevant)"

    # No genetic focus (3 points)
    return 3, f"⚠️ Non-targeted trial - {gene} status may not be primary selection criteria"


def score_metastasis_match(metastasis_status: str, inclusion: str) -> Tuple[float, str]:
    """
    Score metastasis status matching - 10 points maximum
    """
    if not metastasis_status:
        return 5, "⚠️ Disease stage information would help with trial matching"

    status_lower = metastasis_status.lower()

    # Direct status match (10 points)
    if "无转移" in status_lower or "no metastasis" in status_lower:
        if "locally advanced" in inclusion or "non-metastatic" in inclusion:
            return 10, "✅ Disease Stage Match: Trial designed for non-metastatic disease"
        return 7, "✅ Early Stage: Non-metastatic status noted"

    elif "寡转移" in status_lower or "oligometastatic" in status_lower:
        if "oligometastatic" in inclusion or "limited metastases" in inclusion:
            return 10, "✅ Perfect Stage Match: Oligometastatic trial specifically for your disease stage"
        elif "metastatic" in inclusion:
            return 8, "✅ Advanced Disease Match: Metastatic trial appropriate for oligometastatic disease"
        return 6, "✅ Limited Metastatic Disease: May qualify for advanced disease trials"

    elif "广泛转移" in status_lower or "extensive" in status_lower:
        if "metastatic" in inclusion or "advanced" in inclusion:
            return 10, "✅ Advanced Disease Match: Trial designed for metastatic cancer"
        return 6, "✅ Advanced Stage: Extensive metastatic disease noted"

    # Default scoring
    return 5, "✅ Disease stage considered in matching"


def score_ecog_match(ecog_score: str, inclusion: str, exclusion: str) -> Tuple[float, str]:
    """
    Score ECOG performance status - 10 points maximum
    Critical eligibility factor
    """
    if not ecog_score:
        return 5, "⚠️ Performance status assessment needed for accurate trial matching"

    try:
        ecog_num = int(ecog_score.replace("+", "")) if ecog_score.replace("+", "").isdigit() else 4
    except:
        ecog_num = 4

    # Check for ECOG requirements in inclusion criteria
    ecog_patterns = [
        r"ecog.{0,15}[≤<=]\s*([0-3])",
        r"performance.{0,25}status.{0,15}[≤<=]\s*([0-3])",
    ]

    trial_max_ecog = None
    for pattern in ecog_patterns:
        match = re.search(pattern, inclusion, re.IGNORECASE)
        if match:
            try:
                trial_max_ecog = int(match.group(1))
                break
            except:
                continue

    # Scoring based on ECOG compatibility
    if ecog_num <= 1:
        if trial_max_ecog is None or trial_max_ecog >= 1:
            return 10, f"✅ Excellent Performance Status: ECOG {ecog_score} qualifies for most trials"
        elif trial_max_ecog == 0:
            return 8, f"✅ High Performance: ECOG {ecog_score} - may need ECOG 0 confirmation"
        else:
            return 5, f"⚠️ Performance Status: ECOG {ecog_score} may exceed trial requirements"

    elif ecog_num == 2:
        if trial_max_ecog is None or trial_max_ecog >= 2:
            return 8, f"✅ Good Performance Status: ECOG {ecog_score} acceptable for many trials"
        else:
            return 3, f"⚠️ Performance Limitation: ECOG {ecog_score} may limit trial options"

    else:  # ECOG 3+
        if trial_max_ecog and trial_max_ecog >= 3:
            return 6, f"✅ Specialized Trial: ECOG {ecog_score} - trial accepts higher performance scores"
        else:
            return 2, f"⚠️ Performance Concern: ECOG {ecog_score} significantly limits trial eligibility"


def score_treatment_stage_match(treatment_stage: str, recent_surgery: bool, inclusion: str) -> Tuple[float, str]:
    """
    Score treatment stage and surgery timing - 10 points maximum
    """
    score = 0
    explanations = []

    # Treatment stage matching (6 points max)
    if treatment_stage:
        stage_lower = treatment_stage.lower()

        if "未治疗" in stage_lower or "new" in stage_lower or "naive" in stage_lower:
            if "treatment-naive" in inclusion or "first-line" in inclusion or "untreated" in inclusion:
                score += 6
                explanations.append("Treatment-naive status matches trial design")
            else:
                score += 4
                explanations.append("Newly diagnosed - good trial candidate")

        elif "一线" in stage_lower or "first-line" in stage_lower:
            if "first-line" in inclusion or "front-line" in inclusion:
                score += 6
                explanations.append("First-line treatment stage perfect match")
            else:
                score += 4
                explanations.append("First-line treatment status noted")

        elif "二线" in stage_lower or "多线" in stage_lower or "second-line" in stage_lower:
            if "second-line" in inclusion or "previously treated" in inclusion or "refractory" in inclusion:
                score += 6
                explanations.append("Advanced treatment line matches trial focus")
            else:
                score += 3
                explanations.append("Multiple treatment lines - may limit some options")

        elif "复发" in stage_lower or "观察期" in stage_lower or "recurrent" in stage_lower:
            if "recurrent" in inclusion or "relapsed" in inclusion:
                score += 5
                explanations.append("Recurrent disease matches trial population")
            else:
                score += 3
                explanations.append("Disease recurrence noted")
    else:
        score += 2
        explanations.append("Treatment stage to be determined")

    # Recent surgery consideration (4 points max)
    if recent_surgery is True:
        # Recent surgery might be exclusionary for some trials
        if "recent surgery" in inclusion.lower() or "post-operative" in inclusion.lower():
            score += 4
            explanations.append("Recent surgery status matches trial design")
        elif "surgery" in inclusion.lower():
            score += 2
            explanations.append("Recent surgery noted - timing may affect eligibility")
        else:
            score += 1
            explanations.append("Recent surgery - may need safety washout period")
    elif recent_surgery is False:
        score += 3
        explanations.append("No recent surgery - good trial safety profile")
    else:
        score += 2
        explanations.append("Surgery history to be confirmed")

    final_explanation = "✅ Treatment Context: " + ", ".join(explanations)
    return min(score, 10), final_explanation


def score_age_eligibility(age_group: str, eligibility: dict) -> Tuple[float, str]:
    """
    Age eligibility - 5 points (PASS/FAIL with partial credit)
    This is a hard requirement, not a bonus
    """
    min_age = eligibility.get("minimumAge", "")
    max_age = eligibility.get("maximumAge", "")

    if not min_age and not max_age:
        return 5, "✅ Age Eligibility: No age restrictions in trial"

    # Parse user age range
    age_ranges = {
        "18-39": (18, 39),
        "40-64": (40, 64),
        "65+": (65, 100),
        "未满18": (0, 17)
    }

    user_min, user_max = age_ranges.get(age_group, (18, 100))

    # Parse trial age requirements
    trial_min = parse_age(min_age) if min_age else 0
    trial_max = parse_age(max_age) if max_age else 150

    # Check age compatibility
    if user_min >= trial_min and user_max <= trial_max:
        return 5, f"✅ Age Eligible: {age_group} falls within trial age range"
    elif user_max >= trial_min and user_min <= trial_max:  # Partial overlap
        return 3, f"⚠️ Age Borderline: {age_group} partially overlaps with trial requirements"
    else:
        return 0, f"❌ Age Ineligible: {age_group} does not meet trial age requirements ({trial_min}-{trial_max})"


def score_gender_eligibility(gender: str, eligibility: dict) -> Tuple[float, str]:
    """
    Gender eligibility - 5 points (PASS/FAIL)
    This is a hard requirement, not a bonus
    """
    trial_gender = eligibility.get("sex", "ALL").upper()

    if trial_gender == "ALL":
        return 5, "✅ Gender Eligible: Trial open to all genders"

    gender_mapping = {"男": "MALE", "女": "FEMALE", "其他": "ALL"}
    user_gender_mapped = gender_mapping.get(gender.lower(), "ALL")

    if trial_gender == user_gender_mapped:
        return 5, f"✅ Gender Eligible: Trial specifically includes {gender}"
    else:
        return 0, f"❌ Gender Ineligible: Trial restricted to {trial_gender.lower()}, you are {gender}"


def score_health_safety(health_conditions: List[str], active_infection: bool, exclusion: str) -> Tuple[float, str]:
    """
    Health and safety scoring - 5 points maximum
    """
    score = 5  # Start with full points, deduct for risks
    concerns = []

    # Active infection check
    if active_infection:
        infection_exclusions = ["active infection", "ongoing infection", "uncontrolled infection"]
        if any(ex in exclusion.lower() for ex in infection_exclusions):
            score -= 3
            concerns.append("Active infection may require resolution")
        else:
            score -= 1
            concerns.append("Active infection noted")

    # Health conditions check
    if health_conditions:
        serious_conditions_map = {
            "心脏病": ["cardiac", "heart", "cardiovascular"],
            "活动性自身免疫": ["autoimmune", "immune"],
            "严重肝/肾功能异常": ["liver", "hepatic", "renal", "kidney"],
            "怀孕或哺乳": ["pregnancy", "pregnant", "nursing", "lactating"]
        }

        for condition in health_conditions:
            condition_lower = condition.lower()
            for chinese_condition, english_terms in serious_conditions_map.items():
                if chinese_condition in condition_lower or any(term in condition_lower for term in english_terms):
                    # Check if mentioned in exclusion criteria
                    if any(term in exclusion.lower() for term in english_terms):
                        score -= 2
                        concerns.append(f"{condition} may affect eligibility")
                    else:
                        score -= 1
                        concerns.append(f"{condition} requires evaluation")

    score = max(0, score)  # Don't go below 0

    if concerns:
        return score, f"⚠️ Health Safety: {'; '.join(concerns)}"
    else:
        return score, "✅ Health Safety: No major safety concerns identified"


def score_participation_readiness(upload_reports: bool, consent_data_collection: bool) -> Tuple[float, str]:
    """
    Participation readiness - 5 points maximum
    Bonus points for engagement
    """
    score = 0

    if upload_reports:
        score += 3
    if consent_data_collection:
        score += 2

    if score >= 4:
        return 5, "✅ High Engagement: Ready for comprehensive trial participation"
    elif score >= 2:
        return 3, "✅ Good Engagement: Willing to participate in study requirements"
    else:
        return 1, "✅ Basic Participation: Standard trial participation level"


def parse_age(age_str: str) -> int:
    """Parse age string to extract numeric value"""
    if not age_str:
        return 0
    numbers = re.findall(r'\d+', age_str)
    return int(numbers[0]) if numbers else 0


def categorize_trials_by_score(trials: list, thresholds: dict = None) -> dict:
    """
    Categorize trials by revised score ranges
    """
    if thresholds is None:
        # Revised thresholds based on new scoring system
        thresholds = {"high": 75, "good": 60, "possible": 45}

    high_priority = []
    good_matches = []
    possible_matches = []
    low_matches = []

    for trial in trials:
        score = trial.get("score_percent", 0)
        if score >= thresholds["high"]:
            high_priority.append(trial)
        elif score >= thresholds["good"]:
            good_matches.append(trial)
        elif score >= thresholds["possible"]:
            possible_matches.append(trial)
        else:
            low_matches.append(trial)

    return {
        "high_priority": high_priority,
        "good_matches": good_matches,
        "possible_matches": possible_matches,
        "low_matches": low_matches
    }