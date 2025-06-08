"""
Visual Report HTML Generation - FIXED VERSION
HTML generation functions specifically for compact_visual_report.py.
This file only supports the visual report and doesn't interfere with other modules.
"""

from typing import Dict, List
from models import QuestionnaireInput


def generate_patient_info_with_charts_html(user_input: QuestionnaireInput, patient_profile_data: Dict = None,
                                           match_distribution_data: Dict = None,
                                           trial_locations_data: Dict = None) -> str:
    """Generate patient info section with charts - VISUAL REPORT ONLY"""

    # Use data from the data processing functions if provided
    if patient_profile_data:
        patient_name = patient_profile_data.get('patient_name', 'Not specified')
        date_of_birth = patient_profile_data.get('date_of_birth', 'Not specified')
        calculated_age = patient_profile_data.get('calculated_age', 'Not specified')
        gender = patient_profile_data.get('gender', 'Not specified')
        cancer_types_str = patient_profile_data.get('cancer_types_str', 'Not specified')
        gene_mutation = patient_profile_data.get('gene_mutation', 'Not specified')
        metastasis_status = patient_profile_data.get('metastasis_status', 'Not specified')
        current_location = patient_profile_data.get('current_location', 'Not specified')
        preferred_country = patient_profile_data.get('preferred_country', 'Not specified')
    else:
        # Fallback to direct user_input access
        cancer_types_str = ', '.join(user_input.cancer_types) if hasattr(user_input,
                                                                         'cancer_types') and user_input.cancer_types else 'Not specified'
        patient_name = user_input.patient_name if hasattr(user_input,
                                                          'patient_name') and user_input.patient_name else 'Not specified'
        date_of_birth = user_input.date_of_birth if hasattr(user_input,
                                                            'date_of_birth') and user_input.date_of_birth else 'Not specified'
        gender = user_input.gender.title() if hasattr(user_input, 'gender') and user_input.gender else 'Not specified'
        calculated_age = 'Not specified'
        gene_mutation = user_input.gene_mutation if hasattr(user_input,
                                                            'gene_mutation') and user_input.gene_mutation else 'Not specified'
        metastasis_status = user_input.metastasis_status if hasattr(user_input,
                                                                    'metastasis_status') and user_input.metastasis_status else 'Not specified'
        current_location = user_input.current_location if hasattr(user_input,
                                                                  'current_location') and user_input.current_location else 'Not specified'
        preferred_country = user_input.preferred_country if hasattr(user_input,
                                                                    'preferred_country') and user_input.preferred_country else 'Not specified'

    # Get stats boxes data
    stats_boxes = match_distribution_data.get('stats_boxes', {}) if match_distribution_data else {}

    # Get location count
    location_count_text = trial_locations_data.get('location_count_text',
                                                   'Loading locations...') if trial_locations_data else 'Loading locations...'

    return f"""
        <div class="visual-summary">
            <!-- Medical Profile Card -->
            <div class="medical-profile-card">
                <div class="profile-header">MY MEDICAL PROFILE</div>

                <div class="profile-section">
                    <h4>Patient Information</h4>
                    <div class="profile-item">
                        <span class="profile-label">Name:</span>
                        <span class="profile-value">{patient_name}</span>
                    </div>
                    <div class="profile-item">
                        <span class="profile-label">Date of Birth:</span>
                        <span class="profile-value">{date_of_birth}</span>
                    </div>
                    <div class="profile-item">
                        <span class="profile-label">Age:</span>
                        <span class="profile-value">{calculated_age}</span>
                    </div>
                    <div class="profile-item">
                        <span class="profile-label">Gender:</span>
                        <span class="profile-value">{gender}</span>
                    </div>
                </div>

                <div class="profile-section">
                    <h4>Diagnosis</h4>
                    <div class="profile-item">
                        <span class="profile-label">Cancer Type:</span>
                        <span class="profile-value">{cancer_types_str}</span>
                    </div>
                    <div class="profile-item">
                        <span class="profile-label">Gene Mutation:</span>
                        <span class="profile-value">{gene_mutation}</span>
                    </div>
                    <div class="profile-item">
                        <span class="profile-label">Disease Status:</span>
                        <span class="profile-value">{metastasis_status}</span>
                    </div>
                </div>

                <div class="profile-section">
                    <h4>Location</h4>
                    <div class="profile-item">
                        <span class="profile-label">Current:</span>
                        <span class="profile-value">{current_location}</span>
                    </div>
                    <div class="profile-item">
                        <span class="profile-label">Preferred Country:</span>
                        <span class="profile-value">{preferred_country}</span>
                    </div>
                </div>
            </div>

            <!-- Match Results Section with Stats -->
            <div class="chart-container spotlight-section">
                <h3>🎯 Match Results</h3>
                <div class="spotlight-container">
                    <div class="spotlight-feature">
                        <div class="spotlight-number" id="spotlightNumber">0</div>
                        <div class="spotlight-label">High-Priority</div>
                        <div class="spotlight-subtitle">Matches Found!</div>
                    </div>

                    <!-- Stats Boxes Row -->
                    <div class="stats-boxes-row">
                        <div class="stat-box">
                            <div class="stat-number">{stats_boxes.get('total_searched', {}).get('count', '1832')}</div>
                            <div class="stat-label">{stats_boxes.get('total_searched', {}).get('label', 'Trials')}</div>
                            <div class="stat-subtitle">{stats_boxes.get('total_searched', {}).get('subtitle', 'Searched')}</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-number">{stats_boxes.get('qualified_matches', {}).get('count', '1832')}</div>
                            <div class="stat-label">{stats_boxes.get('qualified_matches', {}).get('label', 'Qualified')}</div>
                            <div class="stat-subtitle">{stats_boxes.get('qualified_matches', {}).get('subtitle', 'Matches')}</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-number">{stats_boxes.get('best_match', {}).get('count', '86%')}</div>
                            <div class="stat-label">{stats_boxes.get('best_match', {}).get('label', 'Best')}</div>
                            <div class="stat-subtitle">{stats_boxes.get('best_match', {}).get('subtitle', 'Match')}</div>
                        </div>
                    </div>

                    <div class="other-matches-chart">
                        <canvas id="otherMatchesChart" width="300" height="200"></canvas>
                    </div>
                </div>
            </div>

            <!-- Enhanced Interactive Trial Locations Map -->
            <div class="map-card">
                <div class="map-header">
                    <span>✈️ Trial Locations & Flight Routes</span>
                    <span style="font-size: 0.9em; color: #6c757d;" id="mapLocationCount">{location_count_text}</span>
                </div>
                
                <!-- Enhanced map container with better styling -->
                <div class="map-container" id="trialMapContainer" style="position: relative;">
                    <div id="leafletMap" style="
                        width: 100%; 
                        height: 100%; 
                        min-height: 350px; 
                        border-radius: 8px;
                        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
                    "></div>
                </div>
            </div>
        </div>
    """


def generate_compact_trial_section_html(trials: List[Dict], section_type: str, show_detailed: bool = False) -> str:
    """Generate trial section HTML - VISUAL REPORT ONLY"""

    if not trials:
        return ""

    section_config = {
        "high_priority": {
            "title": "🌟 High-Priority Matches (75%+)",
            "color": "#28a745"
        },
        "good_matches": {
            "title": "✨ Very Good Matches (60-74%)",
            "color": "#ffc107"
        },
        "possible_matches": {
            "title": "💡 Good Potential Matches (45-59%)",
            "color": "#fd7e14"
        },
        "low_matches": {
            "title": "🔍 Needs Review Matches (<45%)",
            "color": "#dc3545"
        }
    }

    config = section_config.get(section_type, {
        "title": "Clinical Trials",
        "color": "#667eea"
    })

    # Show more trials for high priority, fewer for others
    display_count = 20 if section_type == "high_priority" else 10
    trials_to_show = trials[:display_count]

    trial_cards_html = ""
    for trial in trials_to_show:
        trial_cards_html += generate_compact_trial_card_html(trial, show_detailed)

    return f"""
        <div class="section-grid">
            <div class="section-header-grid">
                <div class="section-title-area">
                    <h2 style="color: #2c3e50; font-size: 1.4em; margin-bottom: 5px;">{config['title']}</h2>
                </div>
                <div class="trial-count-grid" style="background: {config['color']};">
                    {len(trials)} trials
                </div>
            </div>
            <div class="trials-grid-layout">
                {trial_cards_html}
            </div>
        </div>
    """

def generate_compact_trial_card_html(trial: Dict, show_detailed: bool = False) -> str:
    """Generate individual trial card HTML - VISUAL REPORT ONLY"""

    score = trial.get("score_percent", 0)
    if score >= 75:
        score_class = "score-green-grid"
        score_text = f"{score:.0f}%"
    elif score >= 60:
        score_class = "score-yellow-grid"
        score_text = f"{score:.0f}%"
    elif score >= 45:
        score_class = "score-orange-grid"
        score_text = f"{score:.0f}%"
    else:
        score_class = "score-red-grid"
        score_text = f"{score:.0f}%"

    # Generate match indicators
    match_tags = []
    explanations = trial.get("explanations", [])
    for explanation in explanations:
        if "gene" in explanation.lower() or "EGFR" in explanation or "基因" in explanation:
            match_tags.append('<span class="match-tag-grid gene">Gene Match</span>')
        elif "ECOG" in explanation:
            match_tags.append('<span class="match-tag-grid ecog">ECOG OK</span>')
        if len(match_tags) >= 2:
            break

    match_tags_html = "".join(match_tags[:2])

    # Brief summary
    brief_summary = trial.get("brief_summary") or trial.get("description", "") or "No summary available."
    if len(brief_summary) > 120:
        brief_summary = brief_summary[:120] + "..."

    # Extract location information
    location_html = ""
    locations = trial.get("locations", [])
    if locations and len(locations) > 0:
        # Get the first location
        location = locations[0]
        facility = location.get("facility", {})
        facility_name = facility.get("name", "Unknown Facility")
        city = facility.get("address", {}).get("city", "")
        state = facility.get("address", {}).get("state", "")
        country = facility.get("address", {}).get("country", "USA")

        location_str = f"{city}, {state}" if city and state else "Location TBD"

        # For now, mock distance - in production, calculate from user's location
        distance = "Calculating..."

        location_html = f'''
            <div class="trial-location">
                <span class="location-icon">📍</span>
                <span><strong>{facility_name}</strong> - {location_str}</span>
                <span class="distance-badge">{distance}</span>
            </div>
        '''

    # Detailed explanations for expandable section
    detailed_explanations = ""
    if show_detailed and len(explanations) > 0:
        for explanation in explanations[:5]:
            if explanation.startswith("✅"):
                detailed_explanations += f'<div style="margin-bottom: 6px; padding: 4px; background: #d4edda; color: #155724; border-radius: 4px; font-size: 0.8em;">✅ {explanation[2:].strip()}</div>'
            elif explanation.startswith("⚠️"):
                detailed_explanations += f'<div style="margin-bottom: 6px; padding: 4px; background: #fff3cd; color: #856404; border-radius: 4px; font-size: 0.8em;">⚠️ {explanation[2:].strip()}</div>'
            elif explanation.startswith("🎯"):
                detailed_explanations += f'<div style="margin-bottom: 6px; padding: 4px; background: #cce5ff; color: #004085; border-radius: 4px; font-size: 0.8em;">🎯 {explanation[2:].strip()}</div>'
            else:
                detailed_explanations += f'<div style="margin-bottom: 6px; padding: 4px; background: #d4edda; color: #155724; border-radius: 4px; font-size: 0.8em;">✅ {explanation}</div>'

    nct_id = trial.get("nct_id", "").replace("NCT", "")
    trial_url = trial.get('url', trial.get('clinicaltrials_gov_url', '#'))
    trial_title = trial.get('title', trial.get('brief_title', 'Clinical Trial'))
    if len(trial_title) > 80:
        trial_title = trial_title[:80] + "..."

    # Generate expand button and details section
    expand_button = ""
    details_section = ""
    if show_detailed and detailed_explanations:
        expand_button = f'<button class="btn-grid expand-btn-grid" id="btn-{nct_id}" onclick="toggleDetails(\'{nct_id}\')">▶ More Details</button>'
        details_section = f'''
            <div class="trial-details-grid" id="details-{nct_id}" style="display: none; margin-top: 10px; padding-top: 10px; border-top: 1px solid #dee2e6;">
                {detailed_explanations}
            </div>
        '''

    return f"""
        <div class="trial-card-grid">
            <div class="trial-header-grid">
                <div class="trial-title-grid">{trial_title}</div>
                <div class="score-badge-grid {score_class}">{score_text}</div>
            </div>

            <div class="trial-meta-grid">
                <div class="nct-id-grid">{trial.get('nct_id', 'NCT')}</div>
                <div class="study-type-grid">INTERVENTIONAL</div>
            </div>

            <div class="match-indicators-grid">
                {match_tags_html}
            </div>

            <div class="trial-summary-grid">
                {brief_summary}
            </div>

            {location_html}

            <div class="action-buttons-grid">
                <a href="{trial_url}" class="btn-grid btn-primary-grid" target="_blank">
                    View Details
                </a>
                {expand_button}
            </div>

            {details_section}
        </div>
    """