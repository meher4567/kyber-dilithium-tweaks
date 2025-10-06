#!/usr/bin/env python3
"""
Kyber Interactive Dashboard Generator
Creates an HTML dashboard with all benchmark results

Usage: python create_dashboard.py <benchmark_results_directory>
Example: python create_dashboard.py benchmark_results/run_20240315_120000
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict
from datetime import datetime

def parse_result_file(filepath: str) -> Dict[str, int]:
    """Parse benchmark result file"""
    results = {}
    
    operations = [
        'poly_compress', 'poly_decompress',
        'polyvec_compress', 'polyvec_decompress',
        'indcpa_keypair', 'indcpa_enc', 'indcpa_dec',
        'crypto_kem_keypair', 'crypto_kem_enc', 'crypto_kem_dec'
    ]
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
            for op in operations:
                pattern = rf'{op}.*?Median:\s*(\d+)'
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    results[op] = int(match.group(1))
    except:
        pass
    
    return results

def load_all_results(results_dir: str) -> Dict:
    """Load all benchmark results"""
    all_results = {}
    
    for level in ['kyber512', 'kyber768', 'kyber1024']:
        all_results[level] = {}
        for config in [1, 2, 3, 4]:
            config_dir = Path(results_dir) / f"config{config}"
            result_file = config_dir / f"{level}_results.txt"
            if result_file.exists():
                all_results[level][config] = parse_result_file(str(result_file))
    
    return all_results

def generate_html_dashboard(all_results: Dict, results_dir: str, output_file: Path):
    """Generate complete HTML dashboard"""
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kyber Performance Dashboard</title>
    <style>
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
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .tabs {
            display: flex;
            background: #f5f5f5;
            border-bottom: 2px solid #ddd;
        }
        
        .tab {
            flex: 1;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            background: none;
            font-size: 16px;
        }
        
        .tab:hover {
            background: #e0e0e0;
        }
        
        .tab.active {
            background: white;
            color: #667eea;
            border-bottom: 3px solid #667eea;
        }
        
        .content {
            padding: 40px;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
            animation: fadeIn 0.5s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
        
        .stat-card h3 {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }
        
        .stat-card .value {
            font-size: 2em;
            font-weight: bold;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: bold;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
        }
        
        tr:hover {
            background: #f5f5f5;
        }
        
        .improvement {
            font-weight: bold;
        }
        
        .improvement.positive {
            color: #28a745;
        }
        
        .improvement.negative {
            color: #dc3545;
        }
        
        .section-title {
            font-size: 1.8em;
            margin: 30px 0 20px 0;
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        
        .info-box {
            background: #e3f2fd;
            border-left: 5px solid #2196F3;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        
        .footer {
            background: #f5f5f5;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 2px solid #ddd;
        }
        
        .config-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            margin: 0 5px;
        }
        
        .config-1 { background: #2E86AB; color: white; }
        .config-2 { background: #A23B72; color: white; }
        .config-3 { background: #F18F01; color: white; }
        .config-4 { background: #C73E1D; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 Kyber Performance Dashboard</h1>
            <p>Comprehensive Performance Analysis</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('overview')">Overview</button>
            <button class="tab" onclick="showTab('kyber512')">Kyber512</button>
            <button class="tab" onclick="showTab('kyber768')">Kyber768</button>
            <button class="tab" onclick="showTab('kyber1024')">Kyber1024</button>
            <button class="tab" onclick="showTab('comparison')">Comparison</button>
        </div>
        
        <div class="content">
"""
    
    # Overview Tab
    html += generate_overview_tab(all_results)
    
    # Individual level tabs
    for level in ['kyber512', 'kyber768', 'kyber1024']:
        html += generate_level_tab(level, all_results.get(level, {}))
    
    # Comparison tab
    html += generate_comparison_tab(all_results)
    
    html += """
        </div>
        
        <div class="footer">
            <p><strong>Kyber Benchmark Suite</strong> | Performance Analysis Tool</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                Results Directory: """ + results_dir + """
            </p>
        </div>
    </div>
    
    <script>
        function showTab(tabName) {
            // Hide all tabs
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        // Show overview by default
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('overview').classList.add('active');
        });
    </script>
</body>
</html>
"""
    
    with open(output_file, 'w') as f:
        f.write(html)

def generate_overview_tab(all_results: Dict) -> str:
    """Generate overview tab HTML"""
    
    html = '<div id="overview" class="tab-content active">\n'
    html += '<h2 class="section-title">Performance Overview</h2>\n'
    
    html += '<div class="info-box">'
    html += '<h3>📊 Benchmark Summary</h3>'
    html += '<p>This dashboard presents comprehensive performance analysis of Kyber with different parameter configurations.</p>'
    html += '<p><strong>Configurations:</strong></p>'
    html += '<p><span class="config-badge config-1">Config 1</span> Original NIST Parameters</p>'
    html += '<p><span class="config-badge config-2">Config 2</span> High Compression</p>'
    html += '<p><span class="config-badge config-3">Config 3</span> Balanced</p>'
    html += '<p><span class="config-badge config-4">Config 4</span> Alternative</p>'
    html += '</div>\n'
    
    # Stats cards
    html += '<div class="stats-grid">\n'
    
    # Count total benchmarks
    total_benchmarks = sum(len(configs) for configs in all_results.values())
    html += '<div class="stat-card"><h3>Total Benchmarks</h3><div class="value">' + str(total_benchmarks) + '</div></div>\n'
    
    # Security levels tested
    html += '<div class="stat-card"><h3>Security Levels</h3><div class="value">' + str(len(all_results)) + '</div></div>\n'
    
    # Configurations tested
    html += '<div class="stat-card"><h3>Configurations</h3><div class="value">4</div></div>\n'
    
    html += '</div>\n'
    html += '</div>\n'
    
    return html

def generate_level_tab(level: str, level_results: Dict) -> str:
    """Generate individual security level tab"""
    
    html = f'<div id="{level}" class="tab-content">\n'
    html += f'<h2 class="section-title">{level.upper()} Performance Results</h2>\n'
    
    if not level_results:
        html += '<p>No results available for this security level.</p>\n'
        html += '</div>\n'
        return html
    
    main_ops = ['indcpa_keypair', 'indcpa_enc', 'indcpa_dec']
    
    html += '<table>\n'
    html += '<thead><tr><th>Operation</th><th>Config 1</th><th>Config 2</th><th>Config 3</th><th>Config 4</th></tr></thead>\n'
    html += '<tbody>\n'
    
    for op in main_ops:
        html += '<tr>\n'
        html += f'<td><strong>{op.replace("_", " ").title()}</strong></td>\n'
        
        for config in [1, 2, 3, 4]:
            if config in level_results and op in level_results[config]:
                value = level_results[config][op]
                html += f'<td>{value:,} cycles</td>\n'
            else:
                html += '<td>N/A</td>\n'
        
        html += '</tr>\n'
    
    html += '</tbody>\n'
    html += '</table>\n'
    
    # Improvement analysis
    if 1 in level_results:
        html += '<h3 class="section-title">Improvement Analysis (vs Config 1)</h3>\n'
        html += '<table>\n'
        html += '<thead><tr><th>Operation</th><th>Config 2</th><th>Config 3</th><th>Config 4</th></tr></thead>\n'
        html += '<tbody>\n'
        
        baseline = level_results[1]
        
        for op in main_ops:
            if op not in baseline:
                continue
            
            html += '<tr>\n'
            html += f'<td><strong>{op.replace("_", " ").title()}</strong></td>\n'
            
            base_val = baseline[op]
            
            for config in [2, 3, 4]:
                if config in level_results and op in level_results[config]:
                    curr_val = level_results[config][op]
                    improvement = ((base_val - curr_val) / base_val) * 100
                    
                    css_class = 'positive' if improvement > 0 else 'negative'
                    sign = '+' if improvement > 0 else ''
                    
                    html += f'<td><span class="improvement {css_class}">{sign}{improvement:.2f}%</span></td>\n'
                else:
                    html += '<td>N/A</td>\n'
            
            html += '</tr>\n'
        
        html += '</tbody>\n'
        html += '</table>\n'
    
    html += '</div>\n'
    
    return html

def generate_comparison_tab(all_results: Dict) -> str:
    """Generate comparison across all levels"""
    
    html = '<div id="comparison" class="tab-content">\n'
    html += '<h2 class="section-title">Cross-Level Comparison</h2>\n'
    
    html += '<h3>KeyGen Performance</h3>\n'
    html += '<table>\n'
    html += '<thead><tr><th>Security Level</th><th>Config 1</th><th>Config 2</th><th>Config 3</th><th>Config 4</th></tr></thead>\n'
    html += '<tbody>\n'
    
    op = 'indcpa_keypair'
    
    for level in ['kyber512', 'kyber768', 'kyber1024']:
        if level not in all_results:
            continue
        
        html += '<tr>\n'
        html += f'<td><strong>{level.upper()}</strong></td>\n'
        
        for config in [1, 2, 3, 4]:
            if config in all_results[level] and op in all_results[level][config]:
                value = all_results[level][config][op]
                html += f'<td>{value:,}</td>\n'
            else:
                html += '<td>N/A</td>\n'
        
        html += '</tr>\n'
    
    html += '</tbody>\n'
    html += '</table>\n'
    html += '</div>\n'
    
    return html

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_dashboard.py <benchmark_results_directory>")
        sys.exit(1)
    
    results_dir = sys.argv[1]
    
    if not os.path.exists(results_dir):
        print(f"Error: Directory '{results_dir}' not found!")
        sys.exit(1)
    
    output_file = Path(results_dir) / "dashboard.html"
    
    print("\n" + "="*80)
    print("Kyber Interactive Dashboard Generator")
    print("="*80 + "\n")
    
    print("Loading results...")
    all_results = load_all_results(results_dir)
    
    print("Generating dashboard...")
    generate_html_dashboard(all_results, results_dir, output_file)
    
    print("\n" + "="*80)
    print("✅ Dashboard generated successfully!")
    print("="*80)
    print(f"\nOutput file: {output_file}")
    print(f"\nOpen in browser: file://{output_file.absolute()}")
    print()

if __name__ == "__main__":
    main()