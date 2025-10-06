#!/usr/bin/env python3
"""
create_dashboard.py
Generate interactive HTML dashboard from Dilithium benchmark results
"""

import os
import sys
import json
import base64
from pathlib import Path
from datetime import datetime

def print_info(text):
    """Print info message"""
    print(f"[INFO] {text}")

def print_success(text):
    """Print success message"""
    print(f"[SUCCESS] {text}")

def print_error(text):
    """Print error message"""
    print(f"[ERROR] {text}")

def load_results(results_dir):
    """Load results from JSON file"""
    json_file = Path(results_dir) / "results.json"
    
    if not json_file.exists():
        print_error(f"results.json not found in {results_dir}")
        return None
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        print_success(f"Loaded results from {json_file}")
        return data
    except Exception as e:
        print_error(f"Failed to load JSON: {e}")
        return None

def encode_image_to_base64(image_path):
    """Encode image to base64 for embedding in HTML"""
    try:
        with open(image_path, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        return f"data:image/png;base64,{encoded}"
    except Exception as e:
        print_error(f"Failed to encode image {image_path}: {e}")
        return ""

def format_number(value):
    """Format number with thousand separators"""
    if value is None:
        return "N/A"
    return f"{int(value):,}"

def calculate_percentage(baseline, current):
    """Calculate percentage difference"""
    if baseline == 0 or baseline is None or current is None:
        return None
    return ((current - baseline) / baseline) * 100

def format_percentage(value):
    """Format percentage with color"""
    if value is None:
        return '<span class="neutral">N/A</span>'
    
    if value < -5:
        color_class = "improvement"
        icon = "↓"
    elif value > 5:
        color_class = "degradation"
        icon = "↑"
    else:
        color_class = "neutral"
        icon = "≈"
    
    return f'<span class="{color_class}">{icon} {value:+.2f}%</span>'

def generate_html(data, results_dir, output_file):
    """Generate complete HTML dashboard"""
    print_info("Generating HTML dashboard...")
    
    configs = data['configurations']
    baseline = configs.get('baseline')
    
    # Check for graph images
    graphs_dir = Path(results_dir) / "graphs"
    graph_absolute = graphs_dir / "performance_absolute.png"
    graph_percentage = graphs_dir / "performance_percentage.png"
    graph_operations = graphs_dir / "performance_by_operation.png"
    
    # Encode images if they exist
    img_absolute = encode_image_to_base64(graph_absolute) if graph_absolute.exists() else ""
    img_percentage = encode_image_to_base64(graph_percentage) if graph_percentage.exists() else ""
    img_operations = encode_image_to_base64(graph_operations) if graph_operations.exists() else ""
    
    # Start HTML
    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html lang='en'>")
    html.append("<head>")
    html.append("    <meta charset='UTF-8'>")
    html.append("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
    html.append("    <title>Dilithium Performance Dashboard</title>")
    html.append("    <style>")
    html.append("""
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 50px;
        }
        
        .section h2 {
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 25px;
            font-size: 1.8em;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        }
        
        .card h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .card .metric {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding: 8px 0;
            border-bottom: 1px solid #dee2e6;
        }
        
        .card .metric:last-child {
            border-bottom: none;
        }
        
        .card .metric .label {
            font-weight: 600;
            color: #495057;
        }
        
        .card .metric .value {
            font-family: 'Courier New', monospace;
            color: #212529;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }
        
        thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #dee2e6;
        }
        
        tbody tr:hover {
            background-color: #f1f3f5;
        }
        
        tbody tr:last-child td {
            border-bottom: none;
        }
        
        .improvement {
            color: #28a745;
            font-weight: 600;
        }
        
        .degradation {
            color: #dc3545;
            font-weight: 600;
        }
        
        .neutral {
            color: #ffc107;
            font-weight: 600;
        }
        
        .graph-container {
            margin: 30px 0;
            text-align: center;
        }
        
        .graph-container img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .graph-container h3 {
            margin-bottom: 15px;
            color: #495057;
        }
        
        .info-box {
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        
        .info-box p {
            margin: 5px 0;
            color: #0d47a1;
        }
        
        footer {
            background: #343a40;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }
        
        .config-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-right: 10px;
        }
        
        .badge-baseline { background: #3498db; color: white; }
        .badge-sha3 { background: #2ecc71; color: white; }
        .badge-challenge { background: #f39c12; color: white; }
        .badge-rejection { background: #e74c3c; color: white; }
        
        @media print {
            body {
                background: white;
            }
            .container {
                box-shadow: none;
            }
        }
    """)
    html.append("    </style>")
    html.append("</head>")
    html.append("<body>")
    html.append("    <div class='container'>")
    
    # Header
    html.append("        <header>")
    html.append("            <h1>🔐 Dilithium Performance Dashboard</h1>")
    html.append(f"            <p>Benchmark Results - Generated {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>")
    html.append("        </header>")
    
    html.append("        <div class='content'>")
    
    # Overview Section
    html.append("            <div class='section'>")
    html.append("                <h2>📊 Configuration Overview</h2>")
    html.append("                <div class='info-box'>")
    html.append("                    <p><strong>Test Environment:</strong> Dilithium2 (NIST Level 2 Security)</p>")
    html.append(f"                    <p><strong>Results Directory:</strong> {Path(results_dir).name}</p>")
    html.append("                    <p><strong>Configurations Tested:</strong> 4 variants with different optimizations</p>")
    html.append("                </div>")
    html.append("            </div>")
    
    # Configuration Cards
    html.append("            <div class='section'>")
    html.append("                <h2>⚙️ Performance Metrics</h2>")
    html.append("                <div class='grid'>")
    
    config_info = {
        'baseline': {
            'name': 'Config 1: Baseline',
            'badge': 'badge-baseline',
            'desc': 'Original NIST Implementation'
        },
        'sha3_challenge': {
            'name': 'Config 2: SHA3-256',
            'badge': 'badge-sha3',
            'desc': 'SHA3-256 Challenge Generation'
        },
        'modified_challenge_bounds': {
            'name': 'Config 3: Challenge Bounds',
            'badge': 'badge-challenge',
            'desc': 'Modified TAU and OMEGA'
        },
        'relaxed_rejection_sampling': {
            'name': 'Config 4: Rejection Sampling',
            'badge': 'badge-rejection',
            'desc': 'Relaxed BETA Parameter'
        }
    }
    
    for config_key, info in config_info.items():
        config_data = configs.get(config_key)
        if config_data is None:
            continue
        
        html.append("                    <div class='card'>")
        html.append(f"                        <h3><span class='config-badge {info['badge']}'>{info['name']}</span></h3>")
        html.append(f"                        <p style='color: #6c757d; margin-bottom: 15px; font-size: 0.9em;'>{info['desc']}</p>")
        
        html.append("                        <div class='metric'>")
        html.append("                            <span class='label'>Key Generation:</span>")
        html.append(f"                            <span class='value'>{format_number(config_data.get('keygen'))} cycles</span>")
        html.append("                        </div>")
        
        html.append("                        <div class='metric'>")
        html.append("                            <span class='label'>Signing:</span>")
        html.append(f"                            <span class='value'>{format_number(config_data.get('sign'))} cycles</span>")
        html.append("                        </div>")
        
        html.append("                        <div class='metric'>")
        html.append("                            <span class='label'>Verification:</span>")
        html.append(f"                            <span class='value'>{format_number(config_data.get('verify'))} cycles</span>")
        html.append("                        </div>")
        
        html.append("                    </div>")
    
    html.append("                </div>")
    html.append("            </div>")
    
    # Comparison Table
    if baseline:
        html.append("            <div class='section'>")
        html.append("                <h2>📈 Performance Comparison (vs Baseline)</h2>")
        html.append("                <table>")
        html.append("                    <thead>")
        html.append("                        <tr>")
        html.append("                            <th>Configuration</th>")
        html.append("                            <th>Key Generation</th>")
        html.append("                            <th>Signing</th>")
        html.append("                            <th>Verification</th>")
        html.append("                        </tr>")
        html.append("                    </thead>")
        html.append("                    <tbody>")
        
        # Baseline row
        html.append("                        <tr>")
        html.append("                            <td><strong>Baseline</strong></td>")
        html.append(f"                            <td>{format_number(baseline['keygen'])} cycles</td>")
        html.append(f"                            <td>{format_number(baseline['sign'])} cycles</td>")
        html.append(f"                            <td>{format_number(baseline['verify'])} cycles</td>")
        html.append("                        </tr>")
        
        # Other configs
        for config_key in ['sha3_challenge', 'modified_challenge_bounds', 'relaxed_rejection_sampling']:
            config_data = configs.get(config_key)
            if config_data is None:
                continue
            
            name = config_info[config_key]['name']
            
            keygen_diff = calculate_percentage(baseline['keygen'], config_data.get('keygen'))
            sign_diff = calculate_percentage(baseline['sign'], config_data.get('sign'))
            verify_diff = calculate_percentage(baseline['verify'], config_data.get('verify'))
            
            html.append("                        <tr>")
            html.append(f"                            <td><strong>{name}</strong></td>")
            html.append(f"                            <td>{format_number(config_data.get('keygen'))} cycles<br>{format_percentage(keygen_diff)}</td>")
            html.append(f"                            <td>{format_number(config_data.get('sign'))} cycles<br>{format_percentage(sign_diff)}</td>")
            html.append(f"                            <td>{format_number(config_data.get('verify'))} cycles<br>{format_percentage(verify_diff)}</td>")
            html.append("                        </tr>")
        
        html.append("                    </tbody>")
        html.append("                </table>")
        html.append("                <div class='info-box' style='margin-top: 20px;'>")
        html.append("                    <p><strong>Legend:</strong> <span class='improvement'>↓ Green</span> = Faster (Improvement), ")
        html.append("                    <span class='neutral'>≈ Yellow</span> = Similar, ")
        html.append("                    <span class='degradation'>↑ Red</span> = Slower (Degradation)</p>")
        html.append("                </div>")
        html.append("            </div>")
    
    # Graphs
    if img_absolute:
        html.append("            <div class='section'>")
        html.append("                <h2>📊 Visual Analysis</h2>")
        html.append("                <div class='graph-container'>")
        html.append("                    <h3>Absolute Performance Comparison</h3>")
        html.append(f"                    <img src='{img_absolute}' alt='Absolute Performance'>")
        html.append("                </div>")
        
        if img_percentage:
            html.append("                <div class='graph-container'>")
            html.append("                    <h3>Percentage Difference vs Baseline</h3>")
            html.append(f"                    <img src='{img_percentage}' alt='Percentage Comparison'>")
            html.append("                </div>")
        
        if img_operations:
            html.append("                <div class='graph-container'>")
            html.append("                    <h3>Performance by Operation Type</h3>")
            html.append(f"                    <img src='{img_operations}' alt='Operations Comparison'>")
            html.append("                </div>")
        
        html.append("            </div>")
    
    html.append("        </div>")
    
    # Footer
    html.append("        <footer>")
    html.append("            <p>Dilithium Performance Dashboard | Generated by automated benchmarking suite</p>")
    html.append(f"            <p>Results from: {results_dir}</p>")
    html.append("        </footer>")
    
    html.append("    </div>")
    html.append("</body>")
    html.append("</html>")
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write('\n'.join(html))
    
    print_success(f"Dashboard saved: {output_file}")

def main():
    """Main function"""
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print("Usage: python3 create_dashboard.py <results_directory>")
        print("\nGenerate interactive HTML dashboard from benchmark results")
        print("\nExample:")
        print("  python3 create_dashboard.py results/run_20240115_143022")
        print("\nNote: Run analyze_results.py and generate_graphs.py first")
        sys.exit(0)
    
    results_dir = sys.argv[1]
    
    print("\n" + "="*70)
    print("DILITHIUM DASHBOARD GENERATION".center(70))
    print("="*70 + "\n")
    
    # Load results
    data = load_results(results_dir)
    if not data:
        sys.exit(1)
    
    # Generate dashboard
    output_file = Path(results_dir) / "dashboard.html"
    generate_html(data, results_dir, output_file)
    
    print("\n" + "="*70)
    print_success("Dashboard generated successfully!")
    print("="*70)
    
    print_info(f"\nOpen in browser: {output_file}")
    print_info("Or run: firefox " + str(output_file))
    print()

if __name__ == "__main__":
    main()