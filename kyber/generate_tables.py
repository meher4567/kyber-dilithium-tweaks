#!/usr/bin/env python3
"""
Kyber LaTeX Table Generator
Generates publication-quality LaTeX tables from benchmark results

Usage: python generate_tables.py <benchmark_results_directory>
Example: python generate_tables.py benchmark_results/run_20240315_120000
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List

OPERATIONS = [
    'poly_compress',
    'poly_decompress',
    'polyvec_compress',
    'polyvec_decompress',
    'indcpa_keypair',
    'indcpa_enc',
    'indcpa_dec',
    'crypto_kem_keypair',
    'crypto_kem_enc',
    'crypto_kem_dec'
]

def parse_result_file(filepath: str) -> Dict[str, Dict[str, int]]:
    """Parse benchmark result file and extract cycle counts"""
    results = {}
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
            for op in OPERATIONS:
                # Extract median and average
                median_pattern = rf'{op}.*?Median:\s*(\d+)'
                average_pattern = rf'{op}.*?Average:\s*(\d+)'
                
                median_match = re.search(median_pattern, content, re.IGNORECASE)
                average_match = re.search(average_pattern, content, re.IGNORECASE)
                
                if median_match:
                    results[op] = {
                        'median': int(median_match.group(1)),
                        'average': int(average_match.group(1)) if average_match else int(median_match.group(1))
                    }
    
    except Exception as e:
        print(f"Warning: Error parsing {filepath}: {e}")
    
    return results

def load_all_results(results_dir: str) -> Dict:
    """Load results from all configurations"""
    all_results = {}
    
    configs = [1, 2, 3, 4]
    levels = ['kyber512', 'kyber768', 'kyber1024']
    
    for level in levels:
        all_results[level] = {}
        
        for config in configs:
            config_dir = Path(results_dir) / f"config{config}"
            result_file = config_dir / f"{level}_results.txt"
            
            if result_file.exists():
                all_results[level][config] = parse_result_file(str(result_file))
    
    return all_results

def generate_main_operations_table(all_results: Dict, output_dir: Path):
    """Generate LaTeX table for main KEM operations"""
    
    levels = ['kyber512', 'kyber768', 'kyber1024']
    main_ops = ['indcpa_keypair', 'indcpa_enc', 'indcpa_dec']
    
    for level in levels:
        if level not in all_results:
            continue
        
        output_file = output_dir / f'{level}_main_operations.tex'
        
        with open(output_file, 'w') as f:
            f.write("% " + "="*70 + "\n")
            f.write(f"% {level.upper()} Main Operations Performance Table\n")
            f.write("% Generated automatically by generate_tables.py\n")
            f.write("% " + "="*70 + "\n\n")
            
            f.write("\\begin{table}[htbp]\n")
            f.write("\\centering\n")
            f.write("\\caption{Performance Analysis of " + level.upper() + 
                   " for Different Configurations (Cycle Counts)}\n")
            f.write("\\label{tab:" + level + "_performance}\n")
            f.write("\\begin{tabular}{|l|c|c|c|c|}\n")
            f.write("\\hline\n")
            f.write("\\textbf{Operation} & \\textbf{Config 1} & \\textbf{Config 2} & " +
                   "\\textbf{Config 3} & \\textbf{Config 4} \\\\\n")
            f.write("\\hline\n")
            
            for op in main_ops:
                op_name = op.replace('_', '\\_')
                line = f"{op_name}"
                
                for config in [1, 2, 3, 4]:
                    if config in all_results[level] and op in all_results[level][config]:
                        median = all_results[level][config][op]['median']
                        line += f" & {median:,}"
                    else:
                        line += " & N/A"
                
                line += " \\\\\n"
                f.write(line)
            
            f.write("\\hline\n")
            f.write("\\end{tabular}\n")
            f.write("\\end{table}\n\n")
        
        print(f"✓ Generated: {output_file}")

def generate_detailed_operations_table(all_results: Dict, output_dir: Path):
    """Generate LaTeX table for detailed operations"""
    
    levels = ['kyber512', 'kyber768', 'kyber1024']
    detail_ops = ['poly_compress', 'poly_decompress', 'polyvec_compress', 'polyvec_decompress']
    
    for level in levels:
        if level not in all_results:
            continue
        
        output_file = output_dir / f'{level}_detailed_operations.tex'
        
        with open(output_file, 'w') as f:
            f.write("% " + "="*70 + "\n")
            f.write(f"% {level.upper()} Detailed Operations Performance Table\n")
            f.write("% " + "="*70 + "\n\n")
            
            f.write("\\begin{table}[htbp]\n")
            f.write("\\centering\n")
            f.write("\\caption{Detailed Performance Analysis of " + level.upper() + "}\n")
            f.write("\\label{tab:" + level + "_detailed}\n")
            f.write("\\begin{tabular}{|l|c|c|c|c|}\n")
            f.write("\\hline\n")
            f.write("\\textbf{Operation} & \\textbf{Config 1} & \\textbf{Config 2} & " +
                   "\\textbf{Config 3} & \\textbf{Config 4} \\\\\n")
            f.write("\\hline\n")
            
            for op in detail_ops:
                op_name = op.replace('_', '\\_')
                line = f"{op_name}"
                
                for config in [1, 2, 3, 4]:
                    if config in all_results[level] and op in all_results[level][config]:
                        median = all_results[level][config][op]['median']
                        line += f" & {median:,}"
                    else:
                        line += " & N/A"
                
                line += " \\\\\n"
                f.write(line)
            
            f.write("\\hline\n")
            f.write("\\end{tabular}\n")
            f.write("\\end{table}\n\n")
        
        print(f"✓ Generated: {output_file}")

def generate_improvement_table(all_results: Dict, output_dir: Path):
    """Generate LaTeX table showing improvement percentages"""
    
    levels = ['kyber512', 'kyber768', 'kyber1024']
    main_ops = ['indcpa_keypair', 'indcpa_enc', 'indcpa_dec']
    
    output_file = output_dir / 'performance_improvement.tex'
    
    with open(output_file, 'w') as f:
        f.write("% " + "="*70 + "\n")
        f.write("% Performance Improvement Table (vs Config 1 Baseline)\n")
        f.write("% " + "="*70 + "\n\n")
        
        f.write("\\begin{table}[htbp]\n")
        f.write("\\centering\n")
        f.write("\\caption{Performance Improvement vs Baseline Configuration (\\%)}\n")
        f.write("\\label{tab:improvement}\n")
        f.write("\\begin{tabular}{|l|l|c|c|c|}\n")
        f.write("\\hline\n")
        f.write("\\textbf{Level} & \\textbf{Operation} & \\textbf{Config 2} & " +
               "\\textbf{Config 3} & \\textbf{Config 4} \\\\\n")
        f.write("\\hline\n")
        
        for level in levels:
            if level not in all_results or 1 not in all_results[level]:
                continue
            
            baseline = all_results[level][1]
            
            for i, op in enumerate(main_ops):
                if op not in baseline:
                    continue
                
                base_val = baseline[op]['median']
                
                # First row for this level includes level name
                if i == 0:
                    line = f"\\multirow{{{len(main_ops)}}}{{*}}{{{level.upper()}}}"
                else:
                    line = ""
                
                op_name = op.replace('_', '\\_')
                line += f" & {op_name}"
                
                for config in [2, 3, 4]:
                    if config in all_results[level] and op in all_results[level][config]:
                        curr_val = all_results[level][config][op]['median']
                        improvement = ((base_val - curr_val) / base_val) * 100
                        
                        if improvement > 0:
                            line += f" & \\textcolor{{ForestGreen}}{{+{improvement:.2f}\\%}}"
                        elif improvement < 0:
                            line += f" & \\textcolor{{red}}{{{improvement:.2f}\\%}}"
                        else:
                            line += " & 0.00\\%"
                    else:
                        line += " & N/A"
                
                line += " \\\\\n"
                f.write(line)
            
            f.write("\\hline\n")
        
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n\n")
        
        f.write("% Note: Requires \\usepackage{xcolor} and \\usepackage{multirow}\n")
    
    print(f"✓ Generated: {output_file}")

def generate_median_average_table(all_results: Dict, output_dir: Path):
    """Generate table with both median and average values"""
    
    levels = ['kyber512', 'kyber768', 'kyber1024']
    
    for level in levels:
        if level not in all_results:
            continue
        
        output_file = output_dir / f'{level}_median_average.tex'
        
        with open(output_file, 'w') as f:
            f.write("% " + "="*70 + "\n")
            f.write(f"% {level.upper()} Median and Average Performance\n")
            f.write("% " + "="*70 + "\n\n")
            
            f.write("\\begin{table}[htbp]\n")
            f.write("\\centering\n")
            f.write("\\caption{" + level.upper() + " Performance - Median and Average}\n")
            f.write("\\label{tab:" + level + "_med_avg}\n")
            f.write("\\begin{tabular}{|l|c|c|c|c|}\n")
            f.write("\\hline\n")
            f.write("\\multirow{2}{*}{\\textbf{Operation}} & " +
                   "\\multicolumn{2}{c|}{\\textbf{Config 1}} & " +
                   "\\multicolumn{2}{c|}{\\textbf{Config 2}} \\\\\n")
            f.write("\\cline{2-5}\n")
            f.write(" & Median & Average & Median & Average \\\\\n")
            f.write("\\hline\n")
            
            main_ops = ['indcpa_keypair', 'indcpa_enc', 'indcpa_dec']
            
            for op in main_ops:
                op_name = op.replace('_', '\\_')
                line = f"{op_name}"
                
                for config in [1, 2]:
                    if config in all_results[level] and op in all_results[level][config]:
                        median = all_results[level][config][op]['median']
                        average = all_results[level][config][op]['average']
                        line += f" & {median:,} & {average:,}"
                    else:
                        line += " & N/A & N/A"
                
                line += " \\\\\n"
                f.write(line)
            
            f.write("\\hline\n")
            f.write("\\end{tabular}\n")
            f.write("\\end{table}\n\n")
        
        print(f"✓ Generated: {output_file}")

def generate_summary_table(all_results: Dict, output_dir: Path):
    """Generate summary table across all security levels"""
    
    output_file = output_dir / 'summary_all_levels.tex'
    
    with open(output_file, 'w') as f:
        f.write("% " + "="*70 + "\n")
        f.write("% Summary Table - All Security Levels\n")
        f.write("% " + "="*70 + "\n\n")
        
        f.write("\\begin{table}[htbp]\n")
        f.write("\\centering\n")
        f.write("\\caption{KeyGen Performance Across All Levels and Configurations}\n")
        f.write("\\label{tab:summary_keygen}\n")
        f.write("\\begin{tabular}{|l|c|c|c|c|}\n")
        f.write("\\hline\n")
        f.write("\\textbf{Security Level} & \\textbf{Config 1} & \\textbf{Config 2} & " +
               "\\textbf{Config 3} & \\textbf{Config 4} \\\\\n")
        f.write("\\hline\n")
        
        levels = ['kyber512', 'kyber768', 'kyber1024']
        op = 'indcpa_keypair'
        
        for level in levels:
            if level not in all_results:
                continue
            
            line = f"{level.upper()}"
            
            for config in [1, 2, 3, 4]:
                if config in all_results[level] and op in all_results[level][config]:
                    median = all_results[level][config][op]['median']
                    line += f" & {median:,}"
                else:
                    line += " & N/A"
            
            line += " \\\\\n"
            f.write(line)
        
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n\n")
    
    print(f"✓ Generated: {output_file}")

def generate_latex_document(output_dir: Path):
    """Generate complete LaTeX document with all tables"""
    
    output_file = output_dir / 'complete_tables.tex'
    
    with open(output_file, 'w') as f:
        f.write("% " + "="*70 + "\n")
        f.write("% Complete LaTeX Document with All Performance Tables\n")
        f.write("% Compile with: pdflatex complete_tables.tex\n")
        f.write("% " + "="*70 + "\n\n")
        
        f.write("\\documentclass[11pt,a4paper]{article}\n")
        f.write("\\usepackage[margin=1in]{geometry}\n")
        f.write("\\usepackage{booktabs}\n")
        f.write("\\usepackage{multirow}\n")
        f.write("\\usepackage{xcolor}\n")
        f.write("\\usepackage{graphicx}\n")
        f.write("\\usepackage{float}\n\n")
        
        f.write("\\title{Kyber Performance Analysis Results}\n")
        f.write("\\author{Performance Benchmarking Suite}\n")
        f.write("\\date{\\today}\n\n")
        
        f.write("\\begin{document}\n\n")
        f.write("\\maketitle\n")
        f.write("\\tableofcontents\n")
        f.write("\\newpage\n\n")
        
        f.write("\\section{Main Operations Performance}\n\n")
        
        levels = ['kyber512', 'kyber768', 'kyber1024']
        for level in levels:
            table_file = f'{level}_main_operations.tex'
            if (output_dir / table_file).exists():
                f.write(f"\\subsection{{{level.upper()}}}\n")
                f.write(f"\\input{{{table_file}}}\n\n")
        
        f.write("\\section{Detailed Operations}\n\n")
        
        for level in levels:
            table_file = f'{level}_detailed_operations.tex'
            if (output_dir / table_file).exists():
                f.write(f"\\subsection{{{level.upper()}}}\n")
                f.write(f"\\input{{{table_file}}}\n\n")
        
        f.write("\\section{Performance Improvement Analysis}\n\n")
        f.write("\\input{performance_improvement.tex}\n\n")
        
        f.write("\\section{Summary}\n\n")
        f.write("\\input{summary_all_levels.tex}\n\n")
        
        f.write("\\end{document}\n")
    
    print(f"✓ Generated: {output_file}")
    print(f"  Compile with: cd {output_dir} && pdflatex complete_tables.tex")

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_tables.py <benchmark_results_directory>")
        print("Example: python generate_tables.py benchmark_results/run_20240315_120000")
        sys.exit(1)
    
    results_dir = sys.argv[1]
    
    if not os.path.exists(results_dir):
        print(f"Error: Directory '{results_dir}' not found!")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path(results_dir) / "latex_tables"
    output_dir.mkdir(exist_ok=True)
    
    print("\n" + "="*80)
    print("Kyber LaTeX Table Generator")
    print("="*80 + "\n")
    
    print("Loading benchmark results...")
    all_results = load_all_results(results_dir)
    
    print("\nGenerating LaTeX tables...")
    print("-"*80)
    
    generate_main_operations_table(all_results, output_dir)
    generate_detailed_operations_table(all_results, output_dir)
    generate_improvement_table(all_results, output_dir)
    generate_median_average_table(all_results, output_dir)
    generate_summary_table(all_results, output_dir)
    generate_latex_document(output_dir)
    
    print("\n" + "="*80)
    print("✅ All LaTeX tables generated successfully!")
    print("="*80)
    print(f"\nOutput directory: {output_dir}")
    print("\nGenerated files:")
    for file in sorted(output_dir.glob("*.tex")):
        print(f"  - {file.name}")
    print()

if __name__ == "__main__":
    main()