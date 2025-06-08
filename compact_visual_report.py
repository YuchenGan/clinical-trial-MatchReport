from fastapi.responses import HTMLResponse
from models import QuestionnaireInput
from match_logic import build_initial_trial_pool
from scoring_engine import score_trial, categorize_trials_by_score
from enhanced_data_extraction import get_detailed_trials_batch, enhance_scored_trial_with_details

# Import our new modular components
from visual_report_data import (
    generate_patient_profile_radar_data,
    generate_match_distribution_data,
    generate_trial_locations_data  # ADD THIS IMPORT
)
from visual_report_html import (
    generate_patient_info_with_charts_html,
    generate_compact_trial_section_html
)
from visual_report_css import get_all_styles

from datetime import datetime
from typing import Dict, List
import json


async def generate_compact_visual_report(user_input: QuestionnaireInput) -> str:
    """
    Generate compact visual HTML report with charts and radar diagrams
    """

    # Step 1: Get enhanced trial data
    trials = await build_initial_trial_pool(user_input)
    scored_trials = [score_trial(trial, user_input) for trial in trials]
    scored_trials.sort(key=lambda x: x.get("score_percent", 0), reverse=True)

    # Step 2: Get detailed info for top 20 trials
    top_trials = scored_trials[:20]
    nct_ids = [trial["nct_id"] for trial in top_trials if trial.get("nct_id")]

    if nct_ids:
        detailed_trials_info = await get_detailed_trials_batch(nct_ids)
        detailed_info_lookup = {info["nct_id"]: info for info in detailed_trials_info if info.get("nct_id")}

        enhanced_top_trials = []
        for trial in top_trials:
            nct_id = trial.get("nct_id", "")
            detailed_info = detailed_info_lookup.get(nct_id, {})
            enhanced_trial = enhance_scored_trial_with_details(trial, detailed_info)
            enhanced_top_trials.append(enhanced_trial)
    else:
        enhanced_top_trials = top_trials

    # Step 3: Categorize ALL trials using unified function with hopeful thresholds
    all_trials = enhanced_top_trials + scored_trials[20:]
    categorized_results = categorize_trials_by_score(
        all_trials,
        thresholds={"high": 75, "good": 60, "possible": 45}
    )

    # Step 3.5: Create search stats BEFORE using them
    search_stats = {
        "total_trials_searched": len(trials),
        "total_qualified_matches": len(scored_trials),
        "high_priority_matches": len(categorized_results["high_priority"]),
        "good_matches": len(categorized_results["good_matches"]),
        "possible_matches": len(categorized_results["possible_matches"]),
        "low_matches": len(categorized_results["low_matches"]),
        "detailed_info_available": len([t for t in enhanced_top_trials if t.get("locations")]),
        "best_match_score": max([t.get('score_percent', 0) for t in categorized_results['high_priority']] + [0])
    }

    # Step 4: Generate all data structures
    patient_profile_data = generate_patient_profile_radar_data(user_input)
    match_distribution = generate_match_distribution_data(categorized_results, search_stats)
    trial_locations = generate_trial_locations_data(categorized_results, user_input)

    # Step 5: Generate HTML with charts
    html_content = generate_compact_visual_html_template(
        user_input=user_input,
        categorized_results=categorized_results,
        patient_profile_data=patient_profile_data,
        match_distribution=match_distribution,
        trial_locations=trial_locations,  # ADD THIS
        search_stats=search_stats
    )

    return html_content


def generate_compact_visual_html_template(user_input: QuestionnaireInput, categorized_results: dict,
                                          patient_profile_data: dict, match_distribution: dict,
                                          trial_locations: dict, search_stats: dict) -> str:
    """Generate the complete compact visual HTML report"""

    current_date = datetime.now().strftime("%B %d, %Y")
    current_time = datetime.now().strftime("%I:%M %p EST")
    report_id = f"MR-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Generate sections using imported functions with ALL required parameters
    patient_info_html = generate_patient_info_with_charts_html(
        user_input,
        patient_profile_data,
        match_distribution,
        trial_locations
    )

    # Generate compact trial sections
    high_priority_html = generate_compact_trial_section_html(
        categorized_results["high_priority"],
        "high_priority",
        True
    )
    good_matches_html = generate_compact_trial_section_html(
        categorized_results["good_matches"],
        "good_matches",
        True
    )
    possible_matches_html = generate_compact_trial_section_html(
        categorized_results["possible_matches"],
        "possible_matches",
        True
    )

    # Generate low matches section if there are any
    low_matches_html = ""
    if len(categorized_results["low_matches"]) > 0:
        low_matches_html = generate_compact_trial_section_html(
            categorized_results["low_matches"],
            "low_matches",
            True
        )

    # Convert data to JSON for JavaScript
    match_distribution_json = json.dumps(match_distribution)

    # Trial locations data for JavaScript
    trial_locations_json = json.dumps({
        "user_location": trial_locations.get("user_location", {}),
        "trial_locations": trial_locations.get("trial_locations", []),
        "total_count": trial_locations.get("total_high_priority_locations", 0)
    })

    # Get CSS styles from separate module
    css_styles = get_all_styles()

    # Build the HTML template
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clinical Trial Matching Report - Visual</title>

    <!-- Chart.js for charts -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>

    <!-- Leaflet.js for interactive maps -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>

    {css_styles}
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🎯 Clinical Trial Matching Report</h1>
            <p>Compact Visual Report | Generated on {current_date} at {current_time}</p>
        </div>

        <!-- Visual Summary with Charts -->
        {patient_info_html}

        <!-- Trial Sections -->
        {high_priority_html}
        {good_matches_html}
        {possible_matches_html}
        {low_matches_html}

        <!-- Footer -->
        <div class="footer">
            <h3>🤝 Clinical Trial Support</h3>
            <p><strong>Support:</strong> 1-800-TRIALS | <strong>Email:</strong> support@matchreport.com</p>
            <p style="font-size: 0.9em; opacity: 0.8; margin-top: 10px;">
                Report ID: {report_id} | Generated: {current_date} at {current_time}
            </p>
        </div>
    </div>

    <script>
        // Wait for DOM to be fully loaded before initializing charts
        document.addEventListener('DOMContentLoaded', function() {{
            // Convert data for JavaScript
            const matchData = {match_distribution_json};
            const trialLocationsData = {trial_locations_json};

            console.log('Match data loaded:', matchData);
            console.log('Trial locations data loaded:', trialLocationsData);

            // Update spotlight number with animation
            const spotlightNumber = document.getElementById('spotlightNumber');
            if (spotlightNumber && matchData.spotlight) {{
                let currentNumber = 0;
                const targetNumber = matchData.spotlight.count;
                const increment = Math.ceil(targetNumber / 20) || 1;

                const counter = setInterval(() => {{
                    currentNumber += increment;
                    if (currentNumber >= targetNumber) {{
                        currentNumber = targetNumber;
                        clearInterval(counter);
                    }}
                    spotlightNumber.textContent = currentNumber;
                }}, 50);
            }}

            // Other Matches Horizontal Bar Chart
            const otherCtx = document.getElementById('otherMatchesChart');
            if (otherCtx && matchData.other_matches) {{
                new Chart(otherCtx, {{
                    type: 'bar',
                    data: {{
                        labels: matchData.other_matches.labels,
                        datasets: [{{
                            data: matchData.other_matches.data,
                            backgroundColor: matchData.other_matches.colors,
                            borderWidth: 0,
                            borderRadius: 4
                        }}]
                    }},
                    options: {{
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        aspectRatio: 1.5,
                        plugins: {{
                            legend: {{ display: false }},
                            title: {{
                                display: true,
                                text: matchData.other_matches.total_label || 'Match Quality Distribution',
                                font: {{ 
                                    size: 13,
                                    weight: '600'
                                }},
                                padding: {{ bottom: 4 }} 
                            }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        return context.parsed.x + ' trials';
                                    }}
                                }}
                            }}
                        }},
                        scales: {{
                            x: {{
                                beginAtZero: true,
                                grid: {{ display: false }},
                                ticks: {{
                                    font: {{ 
                                        size: 10,
                                        weight: '500'
                                    }},
                                    padding: 4,
                                    color: '#666',
                                    stepSize: 200
                                }},
                                border: {{ display: false }}
                            }},
                            y: {{
                                grid: {{ display: false }},
                                ticks: {{
                                    font: {{ 
                                        size: 11,
                                        weight: 'bold'
                                    }},
                                    color: '#2c3e50',
                                    padding: 8,
                                    maxRotation: 0,
                                    minRotation: 0
                                }}
                            }}
                        }},
                        layout: {{
                            padding: {{
                                right: 15, 
                                left: 8,    
                                bottom: 20,
                                top: 2
                            }}
                        }},
                        elements: {{
                            bar: {{ borderRadius: 3 }}
                        }}
                    }}
                }});
            }}

            // Update location count
            const locationCountEl = document.getElementById('mapLocationCount');
            if (locationCountEl && trialLocationsData.total_count) {{
                locationCountEl.textContent = `${{trialLocationsData.total_count}} high-priority locations`;
            }} else if (locationCountEl) {{
                locationCountEl.textContent = '11 high-priority locations';
            }}

            // Initialize the interactive map
            initializeTrialMap(trialLocationsData);

            // Add spotlight animation effect
            setTimeout(() => {{
                const spotlightEl = document.querySelector('.spotlight-feature');
                if (spotlightEl && matchData.spotlight && matchData.spotlight.count > 0) {{
                    spotlightEl.style.transform = 'scale(1.05)';
                    setTimeout(() => {{
                        spotlightEl.style.transform = 'scale(1)';
                    }}, 300);
                }}
            }}, 1500);
        }});
        
function initializeTrialMap(trialLocationsData) {{
            console.log('🗺️ Initializing Enhanced Flight Route Map...');
            console.log('Data received:', trialLocationsData);

            // Check if Leaflet is loaded
            if (typeof L === 'undefined') {{
                console.error('❌ Leaflet library not loaded!');
                return;
            }}

            const mapContainer = document.getElementById('leafletMap');
            if (!mapContainer) {{
                console.error('❌ Map container element not found');
                return;
            }}

            // Validate data structure
            if (!trialLocationsData) {{
                console.error('❌ No trial locations data provided');
                return;
            }}

            const userLocation = trialLocationsData.user_location;
            const trialLocations = trialLocationsData.trial_locations || [];

            console.log('👤 User location:', userLocation);
            console.log('🏥 Trial locations count:', trialLocations.length);
            console.log('🏥 First trial location:', trialLocations[0]);

            try {{
                // Initialize the Enhanced Leaflet map
                const map = L.map('leafletMap', {{
                    center: [30.0, 0.0],
                    zoom: 2,
                    maxZoom: 12,
                    minZoom: 1,
                    zoomControl: true
                }});

                // Create a custom pane for flight paths that's always on top
                map.createPane('flightPaths');
                map.getPane('flightPaths').style.zIndex = 650; // Above everything
                map.getPane('flightPaths').style.pointerEvents = 'none';
                map.getPane('flightPaths').style.overflow = 'visible';

                // Add OpenStreetMap tile layer
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '© OpenStreetMap contributors',
                    maxZoom: 18
                }}).addTo(map);

                // Store references for controls
                let flightPaths = [];
                let trialMarkers = [];
                let userMarker = null;
                let animationActive = true; // CHANGED: Start with animation active
                // REMOVED: highlightActive variable

                // Add Enhanced User Location Marker
                
                if (userLocation && userLocation.lat && userLocation.lng) {{
                    console.log('✅ Adding enhanced user marker at:', userLocation.lat, userLocation.lng);
                
                    // custom icon
                    const patientIcon = L.divIcon({{
                        html: `<div class="patient-marker-enhanced" style="
                            background:#e74c3c;width:20px;height:20px;border-radius:50%;
                            border:3px solid white;box-shadow:0 4px 12px rgba(231,76,60,.5);"></div>`,
                        iconSize: [26, 26],
                        iconAnchor: [13, 13],
                        className: 'enhanced-patient-marker'
                    }});
                
                    // ★ 正确创建 userMarker
                    userMarker = L.marker(
                        [userLocation.lat, userLocation.lng],
                        {{ icon: patientIcon, zIndexOffset: 1000 }}
                    ).addTo(map);
                
                    userMarker.bindPopup(`
                        <div style="text-align:center;padding:10px;font-family:'Segoe UI',sans-serif;">
                            <h4 style="margin:0 0 8px 0;color:#e74c3c;">🏠 Your Location</h4>
                            <p style="margin:0;font-weight:bold;color:#2c3e50;">${{userLocation.name}}</p>
                            <p style="margin:5px 0 0 0;font-size:.85em;color:#6c757d;">Starting point for trial searches</p>
                        </div>
                    `);
                }}

                // Add Enhanced Trial Location Markers
                console.log('🏥 Processing trial locations...');
                trialLocations.forEach((trial, index) => {{
                    console.log(`Processing trial ${{index + 1}}:`, trial);
                    
                    // Handle different possible data structures
                    let lat, lng, facilityName, displayName, score, nctId;
                    
                    if (trial.lat && trial.lng) {{
                        lat = parseFloat(trial.lat);
                        lng = parseFloat(trial.lng);
                    }} else if (trial.latitude && trial.longitude) {{
                        lat = parseFloat(trial.latitude);
                        lng = parseFloat(trial.longitude);
                    }} else if (trial.coordinates) {{
                        lat = parseFloat(trial.coordinates.lat || trial.coordinates.latitude);
                        lng = parseFloat(trial.coordinates.lng || trial.coordinates.longitude);
                    }}

                    facilityName = trial.facility_name || trial.name || trial.facility || 'Unknown Facility';
                    displayName = trial.display_name || trial.location || trial.city || facilityName;
                    score = trial.score || trial.match_score || '85';
                    nctId = trial.nct_id || trial.trial_id || `TRIAL-${{index + 1}}`;

                    console.log(`Trial ${{index + 1}} coordinates: lat=${{lat}}, lng=${{lng}}`);

                    if (!lat || !lng || isNaN(lat) || isNaN(lng)) {{
                        console.warn(`⚠️ Trial ${{index + 1}} missing or invalid coordinates`);
                        return;
                    }}

                    // Create enhanced trial icon with trial count
                    const trialIcon = L.divIcon({{
                        html: `<div class="trial-marker-enhanced" style="
                            background: #27ae60; 
                            width: 16px; 
                            height: 16px; 
                            border-radius: 50%; 
                            border: 2px solid white; 
                            box-shadow: 0 3px 8px rgba(39, 174, 96, 0.4); 
                            position: relative;
                            cursor: pointer;
                            z-index: 500;
                        ">
                            <div style="
                                position: absolute; 
                                top: -8px; 
                                right: -8px; 
                                background: white; 
                                color: #27ae60; 
                                border: 1px solid #27ae60; 
                                border-radius: 50%; 
                                width: 14px; 
                                height: 14px; 
                                font-size: 9px; 
                                font-weight: bold; 
                                display: flex; 
                                align-items: center; 
                                justify-content: center; 
                                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                            ">${{trial.trial_count || 1}}</div>
                        </div>`,
                        iconSize: [20, 20],
                        iconAnchor: [10, 10],
                        className: 'enhanced-trial-marker'
                    }});

                    const trialMarker = L.marker([lat, lng], {{
                        icon: trialIcon,
                        zIndexOffset: 500
                    }}).addTo(map);

                    // Calculate distance if user location exists
                    let distanceText = 'Calculating...';
                    if (userLocation && userLocation.lat && userLocation.lng) {{
                        const distance = calculateDistance(userLocation.lat, userLocation.lng, lat, lng);
                        distanceText = `${{Math.round(distance)}} miles`;
                    }}

                    // Enhanced popup for trial details
                    trialMarker.bindPopup(`
                        <div style="padding: 12px; min-width: 240px; font-family: 'Segoe UI', sans-serif;">
                            <h4 style="margin: 0 0 10px 0; color: #27ae60; display: flex; align-items: center; gap: 6px;">
                                🏥 ${{facilityName}}
                            </h4>
                            <div style="background: linear-gradient(135deg, #27ae60, #2ecc71); color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; display: inline-block; margin-bottom: 8px;">
                                Clinical Trial Site
                            </div>
                            <p style="margin: 8px 0; color: #2c3e50;">
                                <strong>📍 Location:</strong> ${{displayName}}
                            </p>
                            <p style="margin: 8px 0; color: #2c3e50;">
                                <strong>🎯 Match Score:</strong> <span style="color: #27ae60; font-weight: bold;">${{score}}%</span>
                            </p>
                            <p style="margin: 8px 0; color: #2c3e50;">
                                <strong>🔬 Trial ID:</strong> ${{nctId}}
                            </p>
                            <div style="background: #e3f2fd; color: #1565c0; padding: 8px; border-radius: 6px; font-size: 0.85em; margin-top: 10px;">
                                <strong>✈️ Distance:</strong> ${{distanceText}}<br>
                                <strong>🕒 Est. Flight:</strong> ${{Math.round(parseFloat(distanceText) / 500)}}h
                            </div>
                        </div>
                    `);

                    trialMarkers.push(trialMarker);
                    console.log(`✅ Added trial marker ${{index + 1}} at [${{lat}}, ${{lng}}]`);

                    // Add Simple Straight Flight Route (FIXED VERSION)
                    if (userLocation && userLocation.lat && userLocation.lng) {{
                        console.log(`Creating flight path from [${{userLocation.lat}}, ${{userLocation.lng}}] to [${{lat}}, ${{lng}}]`);
                        
                        // Create simple straight line with CUSTOM PANE
                        const straightPath = L.polyline(
                          [[userLocation.lat, userLocation.lng], [lat, lng]],
                          {{ 
                            pane: 'flightPaths',
                            fill: false,
                            color: '#FF0000',
                            weight: 6,
                            opacity: 1,
                            dashArray: '20,10',
                            className: 'flight-path-animated'
                          }}
                        ).addTo(map);
                        

                        
                        console.log(`✅ Added flight path ${{index + 1}} to CUSTOM PANE - should be on top of everything`);
                        
                        flightPaths.push(straightPath);
                        console.log(`✅ Added STRAIGHT flight path ${{index + 1}} - should be VISIBLE now`);
                    }}
                }});

                console.log(`✅ Added ${{trialMarkers.length}} trial markers and ${{flightPaths.length}} flight paths`);

                // MODIFIED: Simplified Control Buttons (removed Highlight Trials, made Animate Routes always active)
                const controlContainer = L.DomUtil.create('div', 'map-controls');
                controlContainer.style.cssText = `
                    position: absolute;
                    top: 15px;
                    right: 15px;
                    z-index: 1000;
                    display: flex;
                    flex-direction: column;
                    gap: 8px;
                `;
                mapContainer.appendChild(controlContainer);

                // MODIFIED: Show Animation Status (instead of toggle button)
                const animationStatus = L.DomUtil.create('div', 'animation-status-indicator', controlContainer);
                animationStatus.innerHTML = '✈️ Routes Animating';
                animationStatus.style.cssText = `
                    background: rgba(39, 174, 96, 0.95);
                    color: white;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-size: 0.8em;
                    font-weight: 600;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                `;

                // Add enhanced CSS for flight animations
                const animationStyle = document.createElement('style');
                animationStyle.textContent = `
                    @keyframes flight-dash {{
                        0% {{ stroke-dashoffset: 0; }}
                        100% {{ stroke-dashoffset: -30; }}
                    }}
                    .flight-path-animated {{
                        animation: flight-dash 2s linear infinite !important;
                    }}
                    @keyframes status-pulse {{
                        0%, 100% {{ opacity: 1; }}
                        50% {{ opacity: 0.7; }}
                    }}
                    .animation-status-indicator {{
                        animation: status-pulse 2s infinite;
                    }}
                `;
                document.head.appendChild(animationStyle);

                // REMOVED: Show Distances Button

                // Reset View Button (modified to restart animation)
                const resetBtn = L.DomUtil.create('button', 'map-control-btn', controlContainer);
                resetBtn.innerHTML = '🌍 Reset View';
                resetBtn.style.cssText = `
                    background: rgba(255, 255, 255, 0.95);
                    border: none;
                    padding: 10px 14px;
                    border-radius: 6px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                    cursor: pointer;
                    font-size: 0.85em;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    white-space: nowrap;
                `;
                resetBtn.onclick = function() {{
                    console.log('🔄 Resetting view...');
                    map.setView([30.0, 0.0], 2);
                    
                    // MODIFIED: Always restart animation after reset
                    animationActive = true;
                    startFlightAnimation();
                }};

                // SIMPLIFIED: Function to start flight animation (FIXED)
                function waitForPathElement(path, index, maxRetries = 10) {{
                    let retries = 0;
                    const checkInterval = setInterval(() => {{
                        const element = path.getElement();
                        if (element) {{
                            console.log(`✅ DOM element ready for flight path ${{index + 1}}`);
                
                            path.setStyle({{         
                              color: '#FF0000',
                              weight: 6,
                              opacity: 1,
                              dashArray: '20,10',      // 必须写成 dashArray（Leaflet 属性名）
                            }});
                
                            element.classList.add('flight-path-animated');
                            path.bringToFront(); 
                            clearInterval(checkInterval);
                        }} else {{
                            retries++;
                            if (retries >= maxRetries) {{
                                console.error(`❌ Failed to get DOM element for flight path ${{index + 1}}`);
                                clearInterval(checkInterval);
                            }}
                        }}
                    }}, 300);
                }}
                
                function startFlightAnimation() {{
                    console.log('🎬 Starting flight route animation...');
                    console.log(`Found ${{flightPaths.length}} flight paths to animate`);
                
                    if (flightPaths.length === 0) {{
                        console.error('❌ No flight paths found to animate!');
                        return;
                    }}
                
                    flightPaths.forEach((path, index) => {{
                        setTimeout(() => {{
                            console.log(`🚀 Launching animation setup for flight path ${{index + 1}}`);
                            waitForPathElement(path, index);
                        }}, index * 500);
                    }});
                }}


                // Add Enhanced Legend (unchanged)
                const legend = L.control({{position: 'bottomleft'}});
                legend.onAdd = function(map) {{
                    const div = L.DomUtil.create('div', 'enhanced-map-legend');
                    div.style.cssText = `
                        background: rgba(255, 255, 255, 0.95) !important;
                        padding: 15px !important;
                        border-radius: 10px !important;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.15) !important;
                        backdrop-filter: blur(10px);
                        border: 1px solid rgba(255, 255, 255, 0.2) !important;
                        font-family: 'Segoe UI', sans-serif !important;
                    `;
                    div.innerHTML = `
                        <h4 style="margin: 0 0 12px 0; color: #2c3e50; font-size: 1em; font-weight: 600;">🗺️ Map Legend</h4>
                        <div style="display: flex; align-items: center; margin-bottom: 8px; gap: 10px; font-size: 0.9em;">
                            <div style="width: 14px; height: 14px; border-radius: 50%; background: #e74c3c; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.2); flex-shrink: 0;"></div>
                            <span>Your Location</span>
                        </div>
                        <div style="display: flex; align-items: center; margin-bottom: 8px; gap: 10px; font-size: 0.9em;">
                            <div style="width: 14px; height: 14px; border-radius: 50%; background: #27ae60; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.2); flex-shrink: 0;"></div>
                            <span>Clinical Trial Sites</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px; font-size: 0.9em;">
                            <div style="width: 25px; height: 3px; background: #3498db; border-radius: 2px; opacity: 0.8; flex-shrink: 0;"></div>
                            <span>Animated Flight Routes</span>
                        </div>
                    `;
                    return div;
                }};
                legend.addTo(map);

                // Auto-fit bounds if we have markers
                if (trialMarkers.length > 0 || userMarker) {{
                    const group = new L.featureGroup([...trialMarkers, ...(userMarker ? [userMarker] : [])]);
                    map.fitBounds(group.getBounds().pad(0.1));
                }}

                // ADDED: Start animation automatically after map loads (FIXED TIMING)
                setTimeout(() => {{
                    console.log('🕐 5-second delay complete, starting animation...');
                    startFlightAnimation();
                    
                    // FORCE visibility check after 2 more seconds
                    setTimeout(() => {{
                        console.log('🔍 Checking flight path visibility...');
                        flightPaths.forEach((path, index) => {{
                            const element = path.getElement();
                            if (element) {{
                                const computedStyle = window.getComputedStyle(element);
                                console.log(`Flight path ${{index + 1}} computed style:`, {{
                                    stroke: computedStyle.stroke,
                                    strokeWidth: computedStyle.strokeWidth,
                                    visibility: computedStyle.visibility,
                                    display: computedStyle.display
                                }});
                            }}
                        }});
                    }}, 2000);
                }}, 5000);

                console.log('✅ Enhanced flight route map initialized successfully!');
                console.log(`📊 Summary: ${{trialMarkers.length}} trial sites, ${{flightPaths.length}} flight routes`);
                console.log('🎬 Animation started automatically');

            }} catch (error) {{
                console.error('❌ Error initializing enhanced map:', error);
                mapContainer.innerHTML = `
                    <div style="padding: 20px; color: #dc3545; text-align: center; font-family: 'Segoe UI', sans-serif;">
                        <h4>🗺️ Map Loading Error</h4>
                        <p>Unable to load the interactive map. Please refresh the page.</p>
                        <p style="font-size: 0.85em; color: #6c757d;">Error: ${{error.message}}</p>
                    </div>
                `;
            }}
        }}
 

        // Helper function to create curved flight paths
        function createCurvedFlightPath(start, end) {{
            const points = [];
            const steps = 50;

            for (let i = 0; i <= steps; i++) {{
                const fraction = i / steps;
                const lat = start[0] + (end[0] - start[0]) * fraction;
                const lng = start[1] + (end[1] - start[1]) * fraction;
                
                // Create more pronounced curve for longer distances
                const distance = Math.abs(end[1] - start[1]);
                const curveFactor = Math.min(0.3 * distance, 20); // Max 20 degree curve
                const curveOffset = Math.sin(fraction * Math.PI) * curveFactor;
                const curvedLat = lat + curveOffset;
                
                points.push([curvedLat, lng]);
            }}
            return points;
        }}

        // Distance calculation helper function
        function calculateDistance(lat1, lng1, lat2, lng2) {{
            const R = 3959; // Earth's radius in miles
            const dLat = (lat2 - lat1) * Math.PI / 180;
            const dLng = (lng2 - lng1) * Math.PI / 180;
            const a = Math.sin(dLat/2) * Math.sin(dLat/2) + 
                      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
                      Math.sin(dLng/2) * Math.sin(dLng/2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
            return R * c;
        }}


        // Toggle trial details function
        function toggleDetails(nctId) {{
            const details = document.getElementById('details-' + nctId);
            const btn = document.getElementById('btn-' + nctId);
            if (!details || !btn) return;
            if (details.style.display === 'none' || details.style.display === '') {{
                details.style.display = 'block';
                btn.innerHTML = '▼ Less Details';
                btn.style.backgroundColor = '#dc3545';
                btn.style.color = 'white';
            }} else {{
                details.style.display = 'none';
                btn.innerHTML = '▶ More Details';
                btn.style.backgroundColor = '';
                btn.style.color = '#6c757d';
            }}
        }}
    </script>
</body>
</html>"""

    return html_template