from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models import QuestionnaireInput
from match_logic import build_initial_trial_pool
from scoring_engine import score_trial, categorize_trials_by_score
from enhanced_data_extraction import get_detailed_trials_batch, enhance_scored_trial_with_details
from compact_visual_report import generate_compact_visual_report
import asyncio
from datetime import datetime
from fastapi.responses import HTMLResponse
app = FastAPI(title="Clinical Trial Match Report API", version="0.2")


@app.get("/")
async def root():
    return {"message": "Welcome to MatchReport API v0.2 - Now with enhanced trial details!"}


@app.post("/match_trials")
async def match_trials(user_input: QuestionnaireInput):
    """
    Enhanced endpoint that returns comprehensive trial matching results
    with detailed facility and contact information
    """

    # Step 1: Get the initial trial pool (your existing logic)
    trials = await build_initial_trial_pool(user_input)
    print(f"🔍 Found {len(trials)} eligible trials after filtering")

    # Step 2: Score each trial (your existing logic)
    scored_trials = [score_trial(trial, user_input) for trial in trials]
    print(f"⚖️ Scored {len(scored_trials)} trials")

    # Step 3: Sort by score (highest first) - NEW!
    scored_trials.sort(key=lambda x: x.get("score_percent", 0), reverse=True)

    # Step 4: Get top trials for detailed information - NEW!
    # Only get detailed info for top 15 trials to avoid overloading API
    top_trials = scored_trials[:15]
    nct_ids = [trial["nct_id"] for trial in top_trials if trial.get("nct_id")]

    if nct_ids:
        print(f"📋 Getting detailed information for top {len(nct_ids)} trials...")

        # Step 5: Get detailed information in parallel - NEW!
        detailed_trials_info = await get_detailed_trials_batch(nct_ids)

        # Step 6: Create lookup dictionary for detailed info
        detailed_info_lookup = {
            info["nct_id"]: info for info in detailed_trials_info if info.get("nct_id")
        }

        # Step 7: Enhance top trials with detailed information - NEW!
        enhanced_top_trials = []
        for trial in top_trials:
            nct_id = trial.get("nct_id", "")
            detailed_info = detailed_info_lookup.get(nct_id, {})
            enhanced_trial = enhance_scored_trial_with_details(trial, detailed_info)
            enhanced_top_trials.append(enhanced_trial)

        print(f"✅ Enhanced {len(enhanced_top_trials)} trials with detailed information")
    else:
        enhanced_top_trials = top_trials
        print("⚠️ No NCT IDs found for detailed information")

    # Step 8: Add remaining trials without detailed info (for completeness)
    remaining_trials = scored_trials[15:] if len(scored_trials) > 15 else []

    # Step 9: Categorize trials by score ranges using unified function
    # Use main API thresholds (conservative)
    categorized_results = categorize_trials_by_score(
        enhanced_top_trials + remaining_trials,
        thresholds={"high": 85, "good": 65, "possible": 40}
    )

    # Step 10: Generate comprehensive response - NEW!
    return {
        "patient_summary": generate_patient_summary(user_input),
        "search_statistics": {
            "total_trials_searched": len(trials),
            "total_qualified_matches": len(scored_trials),
            "high_priority_matches": len(categorized_results["high_priority"]),
            "good_matches": len(categorized_results["good_matches"]),
            "possible_matches": len(categorized_results["possible_matches"]),
            "detailed_info_available": len([t for t in enhanced_top_trials if t.get("locations")])
        },
        "results_by_category": categorized_results,
        "generation_timestamp": datetime.now().isoformat(),
        "report_metadata": {
            "version": "2.0",
            "matching_algorithm": "criteria_based_with_hope_focus",
            "data_source": "clinicaltrials.gov_v2"
        }
    }


@app.post("/match_trials_basic")
async def match_trials_basic(user_input: QuestionnaireInput):
    """
    Basic endpoint without detailed contact info (faster)
    """
    trials = await build_initial_trial_pool(user_input)
    scored = [score_trial(t, user_input) for t in trials]
    scored.sort(key=lambda x: x.get("score_percent", 0), reverse=True)

    return {
        "match_pool_size": len(scored),
        "results": scored,
        "patient_summary": generate_patient_summary(user_input)
    }


def generate_patient_summary(user_input: QuestionnaireInput) -> dict:
    """
    Generate patient summary for the report
    """
    return {
        "gender": user_input.gender,
        "age_group": user_input.age_group,
        "diagnosed": user_input.diagnosed,
        "cancer_types": user_input.cancer_types,
        "gene_mutation": user_input.gene_mutation,
        "metastasis_status": user_input.metastasis_status,
        "recent_surgery": user_input.recent_surgery,
        "ecog_score": user_input.ecog_score,
        "treatment_stage": user_input.treatment_stage,
        "active_infection": user_input.active_infection,
        "recent_drugs": user_input.recent_drugs,
        "health_conditions": user_input.health_conditions,
        "upload_reports": user_input.upload_reports,
        "consent_data_collection": user_input.consent_data_collection,
        # Add computed fields
        "risk_factors": identify_risk_factors(user_input),
        "treatment_readiness": assess_treatment_readiness(user_input)
    }


def identify_risk_factors(user_input: QuestionnaireInput) -> list:
    """
    Identify potential risk factors from patient data
    """
    risk_factors = []

    if user_input.active_infection:
        risk_factors.append("Active infection - may affect trial eligibility")

    if user_input.health_conditions:
        for condition in user_input.health_conditions:
            if any(serious in condition.lower() for serious in ["cardiac", "liver", "kidney", "lung"]):
                risk_factors.append(f"Comorbidity: {condition}")

    if user_input.ecog_score and user_input.ecog_score in ["3", "3+", "4"]:
        risk_factors.append("High ECOG score - may limit trial options")

    if not user_input.gene_mutation:
        risk_factors.append("No genetic testing information - may miss targeted therapy trials")

    return risk_factors


@app.post("/generate_html_report")
async def generate_html_report_endpoint(user_input: QuestionnaireInput):
    """
    Generate compact visual HTML clinical trial matching report with charts
    """
    html_content = await generate_compact_visual_report(user_input)
    return HTMLResponse(content=html_content)


@app.post("/generate_html_report_download")
async def generate_html_report_download(user_input: QuestionnaireInput):
    """
    Generate compact visual HTML report for download
    """
    html_content = await generate_compact_visual_report(user_input)

    # Set headers for file download
    from fastapi.responses import Response
    return Response(
        content=html_content,
        media_type="text/html",
        headers={
            "Content-Disposition": f"attachment; filename=clinical_trial_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        }
    )


def assess_treatment_readiness(user_input: QuestionnaireInput) -> str:
    """
    Assess patient's readiness for clinical trial participation
    """
    if user_input.ecog_score in ["0", "1"] and not user_input.active_infection:
        return "High - Good performance status, no major barriers"
    elif user_input.ecog_score == "2":
        return "Moderate - Some performance limitations"
    elif user_input.active_infection:
        return "Delayed - Active infection needs resolution first"
    else:
        return "Variable - Requires individual assessment"

@app.post("/generate-visual-report-preview", response_class=HTMLResponse)
async def generate_visual_report_preview(user_input: QuestionnaireInput):
    """Preview the visual report directly in browser"""
    html_content = await generate_compact_visual_report(user_input)
    return HTMLResponse(content=html_content)