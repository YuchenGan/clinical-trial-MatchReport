"""
Visual Report CSS Styles
CSS styles specifically for compact_visual_report.py.
This file only supports the visual report and doesn't interfere with other modules.
"""


def get_all_styles() -> str:
    """Get all CSS styles for visual report - VISUAL REPORT ONLY"""
    return """
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.5;
            color: #333;
            background-color: #f8f9ff;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.2em;
            margin-bottom: 8px;
        }

        /* FIXED: Better 3-column layout with consistent heights */
        .visual-summary {
            display: grid;
            grid-template-columns: 380px 1fr 2fr;
            gap: 20px;
            margin-bottom: 35px;
            height: 450px; /* Fixed height for alignment */
        }

        .chart-container {
            background: #fff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            min-height: 450px; /* FIXED: Minimum height */
        }

        .chart-container h3 {
            text-align: center;
            margin-bottom: 15px;
            color: #2c3e50;
            font-size: 1.1em;
        }

        /* FIXED: Medical Profile Card - Compact */
        .medical-profile-card {
            background: #fff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            min-height: 450px; /* FIXED: Minimum height to match other columns */
        }

        .profile-header {
            font-weight: bold;
            font-size: 1.1em;
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e9ecef;
            text-align: center;
        }

        .profile-section {
            margin-bottom: 16px;
            flex: 1;
        }

        .profile-section h4 {
            color: #495057;
            font-size: 0.85em;
            margin-bottom: 8px;
            border-bottom: 1px solid #e9ecef;
            padding-bottom: 3px;
        }
        
        .profile-section:last-child {
            margin-bottom: auto;
        }

        .profile-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            font-size: 0.8em;
        }

        .profile-label {
            color: #6c757d;
        }

        .profile-value {
            color: #212529;
            font-weight: 500;
            text-align: right;
        }

        /* FIXED: Compact Spotlight Section */
        .spotlight-section {
            position: relative;
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .spotlight-container {
            display: flex;
            flex-direction: column;
            height: 100%;
            gap: 8px;
            justify-content: space-between; /* ADDED: Distribute content evenly */
            min-height: 420px;
        }


        /* FIXED: Smaller spotlight feature */
         .spotlight-feature {
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
            padding: 18px 25px; /* REDUCED padding */
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 6px 12px rgba(40, 167, 69, 0.3);
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease;
            flex-shrink: 0;
        }
        
        .spotlight-number {
            font-size: 2.8em; /* REDUCED from 3.2em */
            font-weight: bold;
            margin-bottom: 4px;
            animation: countUp 1s ease-out;
        }
        
        .spotlight-label {
            font-size: 1em; /* REDUCED from 1.1em */
            font-weight: 600;
            margin-bottom: 2px;
        }
        
        .spotlight-subtitle {
            font-size: 0.85em; /* REDUCED from 0.9em */
            opacity: 0.9;
        }

        /* FIXED: Better stats boxes layout */
        .stats-boxes-row {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
            margin-bottom: 8px;
            flex-shrink: 0;
        }
        
        .stat-box {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 10px 6px; /* REDUCED padding */
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        
        .stat-number {
            font-size: 1.3em; /* REDUCED from 1.4em */
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 3px;
            line-height: 1;
        }
        
        .stat-label {
            font-size: 0.75em; /* REDUCED from 0.8em */
            font-weight: 600;
            color: #495057;
            margin-bottom: 2px;
            line-height: 1;
        }
        
        .stat-subtitle {
            font-size: 0.7em;
            color: #6c757d;
            line-height: 1;
        }

        .other-matches-chart {
            flex: 1;
            position: relative;
            min-height: 180px;
            padding: 8px 12px 30px 8px; /* ADDED: padding bottom and right for axis labels */
            margin-bottom: 10px; /* ADDED: extra margin at bottom */
            margin-top: 0;
        }

        @keyframes countUp {
            from {
                transform: scale(0.5);
                opacity: 0;
            }
            to {
                transform: scale(1);
                opacity: 1;
            }
        }

        /* Map Section Styles */
        .map-card {
            background: #fff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            min-height: 450px; /* FIXED: Minimum height */
        }

        .map-header {
            font-weight: bold;
            font-size: 1.1em;
            color: #2c3e50;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .map-container {
            flex: 1;
            border-radius: 8px;
            position: relative;
            background: #f0f8ff;
            overflow: hidden;
            min-height: 320px;
            border: 2px solid #e6f3ff;
        }

        /* Rest of your existing CSS... */
        .map-container svg {
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
        }

        .map-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
        }

        .map-point {
            position: absolute;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            cursor: pointer;
            transition: all 0.3s ease;
            border: 3px solid white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }

        .map-point:hover {
            transform: translate(-50%, -50%) scale(1.2);
            z-index: 10;
        }

        .map-point.patient {
            background: #ff4444;
            width: 24px;
            height: 24px;
            z-index: 10;
        }

        .map-point.trial {
            background: #28a745;
        }

        .map-tooltip {
            position: absolute;
            background: white;
            padding: 8px 12px;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            font-size: 0.8em;
            display: none;
            z-index: 20;
            white-space: nowrap;
        }

        .map-legend {
            position: absolute;
            bottom: 15px;
            left: 15px;
            background: white;
            padding: 10px 14px; /* CHANGED: horizontal padding increased */
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            font-size: 0.8em;
            z-index: 15;
            display: flex; /* ADDED: horizontal layout */
            flex-direction: column; /* ADDED: stack rows vertically */
            gap: 6px; /* ADDED: gap between rows */
            width: fit-content; /* ADDED: only as wide as content needs */
            min-width: 110px;
            max-width: 180px; /* ADDED: maximum width limit */
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 0; /* REMOVED: margin since we use gap now */
            white-space: nowrap; /* ADDED: prevent text wrapping */
            font-size: 1em;
        }

        .legend-item:last-child {
            margin-bottom: 0;
        }

        .legend-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: 2px solid white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
            flex-shrink: 0; /* ADDED: prevent dot from shrinking */
        }

        /* Trial sections */
        .section-grid {
            margin-bottom: 30px;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-top: 20px; /* ADDED: Extra top margin */
            clear: both; /* ADDED: Clear any floats */
        }

        .section-header-grid {
            padding: 25px 20px; 
            border-bottom: 2px solid #667eea;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative; 
            z-index: 1; 
        }

        .trial-count-grid {
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }

        .trials-grid-layout {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            padding: 20px;
        }

        .trial-card-grid {
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 20px;
            background: #fff;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .trial-card-grid:hover {
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(102,126,234,0.15);
            transform: translateY(-2px);
        }

        .trial-header-grid {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
        }

        .trial-title-grid {
            font-size: 1em;
            font-weight: bold;
            color: #2c3e50;
            line-height: 1.3;
            flex: 1;
            margin-right: 12px;
        }

        .score-badge-grid {
            padding: 6px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
            white-space: nowrap;
            min-width: 50px;
            text-align: center;
        }

        .score-green-grid {
            background: #28a745;
            color: white;
            box-shadow: 0 2px 4px rgba(40, 167, 69, 0.3);
        }

        .score-yellow-grid {
            background: #ffc107;
            color: #000;
            box-shadow: 0 2px 4px rgba(255, 193, 7, 0.3);
        }

        .score-orange-grid {
            background: #fd7e14;
            color: white;
            box-shadow: 0 2px 4px rgba(253, 126, 20, 0.3);
        }

        .score-red-grid {
            background: #dc3545;
            color: white;
            box-shadow: 0 2px 4px rgba(220, 53, 69, 0.3);
        }

        .trial-meta-grid {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e9ecef;
        }

        .nct-id-grid {
            background: #007bff;
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
        }

        .study-type-grid {
            color: #6c757d;
            font-size: 0.8em;
            font-style: italic;
        }

        .match-indicators-grid {
            display: flex;
            gap: 6px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }

        .match-tag-grid {
            background: #e3f2fd;
            color: #1565c0;
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.7em;
            font-weight: 500;
        }

        .match-tag-grid.gene {
            background: #e8f5e8;
            color: #2e7d32;
        }

        .match-tag-grid.ecog {
            background: #fff3e0;
            color: #f57c00;
        }

        .trial-summary-grid {
            font-size: 0.85em;
            color: #495057;
            line-height: 1.4;
            margin-bottom: 15px;
            min-height: 60px;
        }

        /* Trial location info */
        .trial-location {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 12px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            font-size: 0.85em;
        }

        .location-icon {
            color: #007bff;
            font-size: 1.2em;
        }

        .distance-badge {
            margin-left: auto;
            background: #e3f2fd;
            color: #1565c0;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
        }

        .action-buttons-grid {
            display: flex;
            gap: 8px;
            margin-top: 12px;
        }

        .btn-grid {
            padding: 8px 16px;
            border: none;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }

        .btn-primary-grid {
            background: #007bff;
            color: white;
            flex: 1;
            min-width: 100px;
        }

        .btn-primary-grid:hover {
            background: #0056b3;
            transform: translateY(-1px);
        }

        .expand-btn-grid {
            background: none;
            border: 1px solid #dee2e6;
            color: #6c757d;
            padding: 6px 12px;
            font-size: 0.75em;
            flex: 1.5;
            min-width: 120px;
        }

        .expand-btn-grid:hover {
            background-color: #e9ecef;
            border-color: #adb5bd;
        }

        .trial-details-grid {
            animation: slideDown 0.3s ease-out;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                max-height: 0;
                transform: translateY(-5px);
            }
            to {
                opacity: 1;
                max-height: 400px;
                transform: translateY(0);
            }
        }

        .footer {
            background: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-top: 30px;
        }

        @media (max-width: 1200px) {
            .visual-summary {
                grid-template-columns: 1fr;
                height: auto;
                margin-bottom: 25px; 
            }
            
            .medical-profile-card,
            .chart-container,
            .map-card {
                margin-bottom: 20px;
                min-height: auto; 
            }
        }

        @media (max-width: 768px) {
            .section-header-grid {
                padding: 20px 15px; /* ADDED: Reduced padding on mobile */
            }
            
            .visual-summary {
                margin-bottom: 20px; /* ADDED: Reduced margin on mobile */
            }
            
            .spotlight-container {
                flex-direction: column;
            }
        
            .spotlight-feature {
                padding: 15px 20px; /* CHANGED: from 15px 25px to 15px 20px */
            }
        
            .spotlight-number {
                font-size: 2.5em; /* ADDED: Smaller font on mobile */
            }
        
            .stats-boxes-row {
                grid-template-columns: 1fr;
                gap: 8px;
            }
        
            .other-matches-chart {
                min-height: 180px;
            }
        
            .trials-grid-layout {
                grid-template-columns: 1fr;
            }
        
            .map-container {
                min-height: 300px;
            }
        }

        /* Enhanced Map Controls */
        .map-controls {
            position: absolute;
            top: 15px;
            right: 15px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .map-control-btn {
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
        }

        .map-control-btn:hover {
            background: #f8f9fa;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }

        /* Enhanced Legend Styling */
        .leaflet-bottom.leaflet-left .leaflet-control {
            margin-bottom: 20px;
            margin-left: 20px;
        }

        .enhanced-map-legend {
            background: rgba(255, 255, 255, 0.95) !important;
            padding: 15px !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            font-family: 'Segoe UI', sans-serif !important;
        }

        .enhanced-map-legend h4 {
            margin: 0 0 12px 0;
            color: #2c3e50;
            font-size: 1em;
            font-weight: 600;
        }

        .enhanced-map-legend .legend-item {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            gap: 10px;
            font-size: 0.9em;
        }

        .enhanced-map-legend .legend-dot {
            width: 14px;
            height: 14px;
            border-radius: 50%;
            border: 2px solid white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            flex-shrink: 0;
        }

        .enhanced-map-legend .legend-line {
            width: 25px;
            height: 3px;
            background: #3498db;
            border-radius: 2px;
            opacity: 0.8;
            flex-shrink: 0;
        }

        /* Animated Flight Path Styles */
        .flight-path-animated {
            animation: flight-dash 3s linear infinite;
        }

        @keyframes flight-dash {
            0% { stroke-dashoffset: 0; }
            100% { stroke-dashoffset: -40; }
        }

        /* Enhanced Marker Styles */
        .patient-marker-enhanced {
            animation: pulse-enhanced 2s infinite;
        }

        @keyframes pulse-enhanced {
            0% { 
                box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.7);
                transform: scale(1);
            }
            50% { 
                box-shadow: 0 0 0 10px rgba(231, 76, 60, 0);
                transform: scale(1.05);
            }
            100% { 
                box-shadow: 0 0 0 0 rgba(231, 76, 60, 0);
                transform: scale(1);
            }
        }

        .trial-marker-enhanced {
            transition: all 0.3s ease;
        }

        .trial-marker-enhanced:hover {
            transform: scale(1.2);
            filter: drop-shadow(0 4px 8px rgba(39, 174, 96, 0.5));
        }
        @keyframes flight-dash {
            0% { stroke-dashoffset: 0; }
            100% { stroke-dashoffset: -40; }
        }
        
        @keyframes pulse-enhanced {
            0% { 
                box-shadow: 0 4px 12px rgba(231, 76, 60, 0.5);
                transform: scale(1);
            }
            50% { 
                box-shadow: 0 4px 12px rgba(231, 76, 60, 0.5), 0 0 0 10px rgba(231, 76, 60, 0.2);
                transform: scale(1.05);
            }
            100% { 
                box-shadow: 0 4px 12px rgba(231, 76, 60, 0.5);
                transform: scale(1);
            }
        }
        /* force flight paths visible in Safari / any browser */
        .flight-path-animated {
          stroke: #FF0000 !important;
          stroke-width: 6 !important;
          stroke-dasharray: 20 10 !important;
          stroke-opacity: 1 !important;
        }
    </style>
    """