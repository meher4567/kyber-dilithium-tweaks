#!/usr/bin/env python3
"""
generate_tables.py
Generate LaTeX tables from Dilithium benchmark results
"""

import os
import sys
import json
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
        print_info("Run analyze_results.py first to generate JSON")
        return None
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        print_success(f"Loaded results from {json_file}")
        return data
    except Exception as e:
        print_error(f"Failed to load JSON: {e}")
        return None

def format_number(value):
    """Format number with thousand separators"""
    if value is None:
        return "---"
    return f"{int(value):,}"

def calculate_percentage(baseline, current):
    """Calculate percentage difference"""
    if baseline == 0 or baseline is None or current is None:
        return None
    return ((current - baseline) / baseline) * 100

def format_percentage(value):
    """Format percentage with sign"""
    if value is None:
        return "---"
    return f"{value:+.2f}\\%"

def generate_simple_table(data, output_file):
    """
    Generate simple performance table
    """
    print_info("Generating simple LaTeX table...")
    
    configs = data['configurations']
    
    latex = []
    latex.append("% Simple Performance Table")
    latex.append("% Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    latex.append("")
    latex.append("\\begin{table}[htbp]")
    latex.append("\\centering")
    latex.append("\\caption{Dilithium Performance Comparison (CPU Cycles)}")
    latex.append("\\label{tab:dilithium_performance}")
    latex.append("\\begin{tabular}{lccc}")
    latex.append("\\toprule")
    latex.append("\\textbf{Configuration} & \\textbf{Key Generation} & \\textbf{Signing} & \\textbf{Verification} \\\\")
    latex.append("\\midrule")
    
    # Configuration order and names
    config_order = ['baseline', 'sha3_challenge', 'modified_challenge_bounds', 'relaxed_rejection_sampling']
    config_names = {
        'baseline': 'Baseline (NIST)',
        'sha3_challenge': 'SHA3-256 Challenge',
        'modified_challenge_bounds': 'Modified Challenge Bounds',
        'relaxed_rejection_sampling': 'Relaxed Rejection Sampling'
    }
    
    for config_key in config_order:
        config_data = configs.get(config_key)
        if config_data is None:
            continue
        
        name = config_names.get(config_key, config_key)
        keygen = format_number(config_data.get('keygen'))
        sign = format_number(config_data.get('sign'))
        verify = format_number(config_data.get('verify'))
        
        latex.append(f"{name} & {keygen} & {sign} & {verify} \\\\")
    
    latex.append("\\bottomrule")
    latex.append("\\end{tabular}")
    latex.append("\\end{table}")
    latex.append("")
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write('\n'.join(latex))
    
    print_success(f"Saved: {output_file}")

def generate_comparison_table(data, output_file):
    """
    Generate comparison table with percentage differences
    """
    print_info("Generating comparison LaTeX table...")
    
    configs = data['configurations']
    baseline = configs.get('baseline')
    
    if not baseline:
        print_error("Baseline configuration not found")
        return
    
    latex = []
    latex.append("% Comparison Table (vs Baseline)")
    latex.append("% Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    latex.append("")
    latex.append("\\begin{table}[htbp]")
    latex.append("\\centering")
    latex.append("\\caption{Dilithium Performance Comparison vs Baseline}")
    latex.append("\\label{tab:dilithium_comparison}")
    latex.append("\\begin{tabular}{lcccccc}")
    latex.append("\\toprule")
    latex.append("\\multirow{2}{*}{\\textbf{Configuration}} & \\multicolumn{2}{c}{\\textbf{Key Generation}} & \\multicolumn{2}{c}{\\textbf{Signing}} & \\multicolumn{2}{c}{\\textbf{Verification}} \\\\")
    latex.append("\\cmidrule(lr){2-3} \\cmidrule(lr){4-5} \\cmidrule(lr){6-7}")
    latex.append("& Cycles & Diff. & Cycles & Diff. & Cycles & Diff. \\\\")
    latex.append("\\midrule")
    
    # Baseline row
    latex.append(f"Baseline & {format_number(baseline['keygen'])} & --- & {format_number(baseline['sign'])} & --- & {format_number(baseline['verify'])} & --- \\\\")
    
    # Other configurations
    config_order = ['sha3_challenge', 'modified_challenge_bounds', 'relaxed_rejection_sampling']
    config_names = {
        'sha3_challenge': 'SHA3-256',
        'modified_challenge_bounds': 'Challenge Bounds',
        'relaxed_rejection_sampling': 'Rejection Sampling'
    }
    
    for config_key in config_order:
        config_data = configs.get(config_key)
        if config_data is None:
            continue
        
        name = config_names.get(config_key, config_key)
        
        keygen = format_number(config_data.get('keygen'))
        keygen_diff = format_percentage(calculate_percentage(baseline['keygen'], config_data.get('keygen')))
        
        sign = format_number(config_data.get('sign'))
        sign_diff = format_percentage(calculate_percentage(baseline['sign'], config_data.get('sign')))
        
        verify = format_number(config_data.get('verify'))
        verify_diff = format_percentage(calculate_percentage(baseline['verify'], config_data.get('verify')))
        
        latex.append(f"{name} & {keygen} & {keygen_diff} & {sign} & {sign_diff} & {verify} & {verify_diff} \\\\")
    
    latex.append("\\bottomrule")
    latex.append("\\end{tabular}")
    latex.append("\\end{table}")
    latex.append("")
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write('\n'.join(latex))
    
    print_success(f"Saved: {output_file}")

def generate_detailed_table(data, output_file):
    """
    Generate detailed table with configuration descriptions
    """
    print_info("Generating detailed LaTeX table...")
    
    configs = data['configurations']
    
    latex = []
    latex.append("% Detailed Configuration Table")
    latex.append("% Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    latex.append("")
    latex.append("\\begin{table}[htbp]")
    latex.append("\\centering")
    latex.append("\\caption{Dilithium Configurations and Performance Results}")
    latex.append("\\label{tab:dilithium_detailed}")
    latex.append("\\small")
    latex.append("\\begin{tabular}{p{3cm}p{5cm}ccc}")
    latex.append("\\toprule")
    latex.append("\\textbf{Config} & \\textbf{Description} & \\textbf{KeyGen} & \\textbf{Sign} & \\textbf{Verify} \\\\")
    latex.append("\\midrule")
    
    # Configuration details
    config_details = {
        'baseline': {
            'name': 'Config 1\\\\Baseline',
            'desc': 'Original NIST Dilithium2 with SHAKE256 challenge generation. TAU=39, OMEGA=80, BETA=78.'
        },
        'sha3_challenge': {
            'name': 'Config 2\\\\SHA3-256',
            'desc': 'Replaces SHAKE256 with SHA3-256 for challenge. 4 iterations with domain separation. Fixed 128-byte output.'
        },
        'modified_challenge_bounds': {
            'name': 'Config 3\\\\Challenge',
            'desc': 'Modified challenge bounds: TAU=50 (+28\\%), OMEGA=70 (-12.5\\%). More uniform challenge, smaller signatures.'
        },
        'relaxed_rejection_sampling': {
            'name': 'Config 4\\\\Rejection',
            'desc': 'Relaxed rejection sampling: BETA=100 (+28\\%). Fewer rejection iterations, faster signing.'
        }
    }
    
    for config_key in ['baseline', 'sha3_challenge', 'modified_challenge_bounds', 'relaxed_rejection_sampling']:
        config_data = configs.get(config_key)
        if config_data is None:
            continue
        
        details = config_details[config_key]
        name = details['name']
        desc = details['desc']
        
        keygen = format_number(config_data.get('keygen'))
        sign = format_number(config_data.get('sign'))
        verify = format_number(config_data.get('verify'))
        
        latex.append(f"{name} & {desc} & {keygen} & {sign} & {verify} \\\\")
        latex.append("\\midrule")
    
    latex[-1] = latex[-1].replace("\\midrule", "\\bottomrule")  # Replace last midrule with bottomrule
    
    latex.append("\\end{tabular}")
    latex.append("\\end{table}")
    latex.append("")
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write('\n'.join(latex))
    
    print_success(f"Saved: {output_file}")

def generate_parameter_table(output_file):
    """
    Generate table showing parameter changes
    """
    print_info("Generating parameter table...")
    
    latex = []
    latex.append("% Parameter Comparison Table")
    latex.append("% Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    latex.append("")
    latex.append("\\begin{table}[htbp]")
    latex.append("\\centering")
    latex.append("\\caption{Dilithium Parameter Modifications}")
    latex.append("\\label{tab:dilithium_parameters}")
    latex.append("\\begin{tabular}{lcccc}")
    latex.append("\\toprule")
    latex.append("\\textbf{Parameter} & \\textbf{Baseline} & \\textbf{Config 2} & \\textbf{Config 3} & \\textbf{Config 4} \\\\")
    latex.append("\\midrule")
    latex.append("Challenge Hash & SHAKE256 & SHA3-256 & SHAKE256 & SHAKE256 \\\\")
    latex.append("TAU (Challenge weight) & 39 & 39 & 50 & 39 \\\\")
    latex.append("OMEGA (Hint weight) & 80 & 80 & 70 & 80 \\\\")
    latex.append("BETA (Rejection bound) & 78 & 78 & 78 & 100 \\\\")
    latex.append("GAMMA1 & $2^{17}$ & $2^{17}$ & $2^{17}$ & $2^{17}$ \\\\")
    latex.append("GAMMA2 & $(q-1)/88$ & $(q-1)/88$ & $(q-1)/88$ & $(q-1)/88$ \\\\")
    latex.append("\\midrule")
    latex.append("\\textbf{Main Change} & --- & Hash & Challenge & Rejection \\\\")
    latex.append("\\bottomrule")
    latex.append("\\end{tabular}")
    latex.append("\\end{table}")
    latex.append("")
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write('\n'.join(latex))
    
    print_success(f"Saved: {output_file}")

def generate_master_latex(results_dir, output_file):
    """
    Generate master LaTeX file that includes all tables
    """
    print_info("Generating master LaTeX document...")
    
    latex = []
    latex.append("% Master LaTeX Document - Dilithium Benchmark Results")
    latex.append("% Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    latex.append("")
    latex.append("\\documentclass[11pt]{article}")
    latex.append("\\usepackage[utf8]{inputenc}")
    latex.append("\\usepackage[margin=1in]{geometry}")
    latex.append("\\usepackage{booktabs}")
    latex.append("\\usepackage{multirow}")
    latex.append("\\usepackage{graphicx}")
    latex.append("\\usepackage{caption}")
    latex.append("\\usepackage{subcaption}")
    latex.append("")
    latex.append("\\title{Dilithium Performance Analysis\\\\Benchmark Results}")
    latex.append("\\author{Generated Automatically}")
    latex.append("\\date{" + datetime.now().strftime('%B %d, %Y') + "}")
    latex.append("")
    latex.append("\\begin{document}")
    latex.append("")
    latex.append("\\maketitle")
    latex.append("")
    latex.append("\\section{Introduction}")
    latex.append("This document presents the performance analysis of Dilithium digital signature scheme with various optimizations.")
    latex.append("")
    latex.append("\\section{Configuration Parameters}")
    latex.append("\\input{table_parameters.tex}")
    latex.append("")
    latex.append("\\section{Performance Results}")
    latex.append("")
    latex.append("\\subsection{Absolute Performance}")
    latex.append("\\input{table_simple.tex}")
    latex.append("")
    latex.append("\\subsection{Comparative Performance}")
    latex.append("\\input{table_comparison.tex}")
    latex.append("")
    latex.append("\\subsection{Detailed Configuration Analysis}")
    latex.append("\\input{table_detailed.tex}")
    latex.append("")
    latex.append("\\section{Performance Graphs}")
    latex.append("\\begin{figure}[htbp]")
    latex.append("\\centering")
    latex.append("\\includegraphics[width=\\textwidth]{graphs/performance_absolute.png}")
    latex.append("\\caption{Absolute Performance Comparison}")
    latex.append("\\end{figure}")
    latex.append("")
    latex.append("\\begin{figure}[htbp]")
    latex.append("\\centering")
    latex.append("\\includegraphics[width=\\textwidth]{graphs/performance_percentage.png}")
    latex.append("\\caption{Performance Comparison vs Baseline}")
    latex.append("\\end{figure}")
    latex.append("")
    latex.append("\\end{document}")
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write('\n'.join(latex))
    
    print_success(f"Saved: {output_file}")

def main():
    """Main function"""
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print("Usage: python3 generate_tables.py <results_directory>")
        print("\nGenerate LaTeX tables from benchmark results")
        print("\nExample:")
        print("  python3 generate_tables.py results/run_20240115_143022")
        print("\nNote: Run analyze_results.py first to generate results.json")
        sys.exit(0)
    
    results_dir = sys.argv[1]
    
    print("\n" + "="*70)
    print("DILITHIUM LATEX TABLE GENERATION".center(70))
    print("="*70 + "\n")
    
    # Load results
    data = load_results(results_dir)
    if not data:
        sys.exit(1)
    
    # Create tables directory
    tables_dir = Path(results_dir) / "tables"
    tables_dir.mkdir(exist_ok=True)
    print_info(f"Saving tables to: {tables_dir}")
    
    # Generate tables
    generate_simple_table(data, tables_dir / "table_simple.tex")
    generate_comparison_table(data, tables_dir / "table_comparison.tex")
    generate_detailed_table(data, tables_dir / "table_detailed.tex")
    generate_parameter_table(tables_dir / "table_parameters.tex")
    generate_master_latex(results_dir, tables_dir / "master_document.tex")
    
    print("\n" + "="*70)
    print_success("All LaTeX tables generated successfully!")
    print("="*70)
    
    print_info("\nGenerated files:")
    for table_file in tables_dir.glob("*.tex"):
        print(f"  - {table_file}")
    
    print("\n" + print_info("To compile the master document:"))
    print(f"  cd {tables_dir}")
    print("  pdflatex master_document.tex")
    print()
    
    print_info("Or include individual tables in your thesis:")
    print("  \\input{table_simple.tex}")
    print("  \\input{table_comparison.tex}")
    print()

if __name__ == "__main__":
    main()