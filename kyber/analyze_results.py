#!/usr/bin/env python3
"""
Kyber Benchmark Results Analyzer
Parses benchmark output files and generates comparison tables

Author: Thesis Implementation Helper
Usage: ./analyze_results.py <results_directory>
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

# ANSI color codes
class Colors:
    CYAN = '\033[0;36m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

def parse_benchmark_file(filepath: str) -> Dict[str, Dict[str, int]]:
    """
    Parse a single benchmark output file and extract cycle counts
    Returns dict with operation names as keys and {median, average} as values
    """
    results = {}
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
            # Define patterns for different operations
            # Adjust these patterns based on actual output format
            operations = [
                'poly_compress',
                'poly_decompress', 
                'polyvec_compress',
                'polyvec_decompress',
                'indcpa_keypair',
                'indcpa_enc',
                'indcpa_dec',
                'keypair',
                'encaps',
                'decaps'
            ]
            
            for op in operations:
                # Pattern to match: operation_name: median X, average Y
                # or: operation_name   X   Y
                pattern1 = rf'{op}.*?median[:\s]+(\d+).*?average[:\s]+(\d+)'
                pattern2 = rf'{op}\s+(\d+)\s+(\d+)'
                
                match = re.search(pattern1, content, re.IGNORECASE)
                if not match:
                    match = re.search(pattern2, content)
                
                if match:
                    results[op] = {
                        'median': int(match.group(1)),
                        'average': int(match.group(2)) if len(match.groups()) > 1 else int(match.group(1))
                    }
    
    except FileNotFoundError:
        print(f"{Colors.RED}Warning: File not found: {filepath}{Colors.NC}")
    except Exception as e:
        print(f"{Colors.RED}Error parsing {filepath}: {e}{Colors.NC}")
    
    return results

def calculate_improvement(original: int, modified: int) -> Tuple[float, str]:
    """
    Calculate percentage improvement
    Returns (percentage, direction) where direction is 'faster' or 'slower'
    """
    if original == 0:
        return 0.0, 'N/A'
    
    improvement = ((original - modified) / original) * 100
    direction = 'faster' if improvement > 0 else 'slower'
    
    return abs(improvement), direction

def print_table_header(title: str):
    """Print formatted table header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*100}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title:^100}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*100}{Colors.NC}\n")

def print_comparison_table(level: str, all_data: Dict[int, Dict]):
    """Print comparison table for a specific security level"""
    
    print_table_header(f"{level.upper()} - Performance Comparison (Cycle Counts)")
    
    # Header
    header = f"{'Operation':<25} {'Config 1':<18} {'Config 2':<18} {'Config 3':<18} {'Config 4':<18}"
    print(f"{Colors.BOLD}{header}{Colors.NC}")
    print(f"{Colors.CYAN}{'-'*100}{Colors.NC}")
    
    # Get all unique operations
    all_operations = set()
    for config_data in all_data.values():
        all_operations.update(config_data.keys())
    
    all_operations = sorted(all_operations)
    
    # Print data rows
    for op in all_operations:
        row = f"{op:<25}"
        
        for config in [1, 2, 3, 4]:
            if config in all_data and op in all_data[config]:
                median = all_data[config][op].get('median', 0)
                row += f"{median:>15,}   "
            else:
                row += f"{'N/A':>15}   "
        
        print(row)
    
    print(f"{Colors.CYAN}{'-'*100}{Colors.NC}\n")

def print_improvement_analysis(level: str, all_data: Dict[int, Dict]):
    """Print improvement analysis comparing configs to baseline (Config 1)"""
    
    if 1 not in all_data:
        print(f"{Colors.RED}Config 1 (baseline) not found for {level}{Colors.NC}")
        return
    
    print_table_header(f"{level.upper()} - Improvement Analysis (vs Config 1 Baseline)")
    
    baseline = all_data[1]
    
    # Header
    header = f"{'Operation':<25} {'Config 2':<25} {'Config 3':<25} {'Config 4':<25}"
    print(f"{Colors.BOLD}{header}{Colors.NC}")
    print(f"{Colors.CYAN}{'-'*100}{Colors.NC}")
    
    # Get all operations
    all_operations = sorted(baseline.keys())
    
    for op in all_operations:
        if op not in baseline:
            continue
        
        baseline_val = baseline[op].get('median', 0)
        row = f"{op:<25}"
        
        for config in [2, 3, 4]:
            if config in all_data and op in all_data[config]:
                config_val = all_data[config][op].get('median', 0)
                improvement, direction = calculate_improvement(baseline_val, config_val)
                
                # Color code based on improvement
                if direction == 'faster':
                    color = Colors.GREEN
                else:
                    color = Colors.RED
                
                row += f"{color}{improvement:>6.2f}% {direction:<15}{Colors.NC} "
            else:
                row += f"{'N/A':<25}"
        
        print(row)
    
    print(f"{Colors.CYAN}{'-'*100}{Colors.NC}\n")

def generate_summary_statistics(results_dir: str):
    """Generate overall summary statistics"""
    
    print_table_header("Summary Statistics")
    
    configs = [1, 2, 3, 4]
    levels = ['kyber512', 'kyber768', 'kyber1024']
    
    summary_data = {}
    
    for level in levels:
        summary_data[level] = {}
        
        for config in configs:
            config_dir = Path(results_dir) / f"config{config}"
            result_file = config_dir / f"{level}_results.txt"
            
            if result_file.exists():
                data = parse_benchmark_file(str(result_file))
                
                # Calculate average of all operations
                if data:
                    total_cycles = sum(op_data.get('median', 0) for op_data in data.values())
                    avg_cycles = total_cycles // len(data) if len(data) > 0 else 0
                    summary_data[level][config] = {
                        'total': total_cycles,
                        'average': avg_cycles,
                        'count': len(data)
                    }
    
    # Print summary
    for level in levels:
        print(f"{Colors.BOLD}{level.upper()}:{Colors.NC}")
        print(f"{'Config':<15} {'Total Cycles':<20} {'Avg per Op':<20} {'Ops Count':<15}")
        print(f"{Colors.CYAN}{'-'*70}{Colors.NC}")
        
        for config in configs:
            if config in summary_data[level]:
                data = summary_data[level][config]
                print(f"Config {config:<8} {data['total']:>18,}  {data['average']:>18,}  {data['count']:>13}")
        
        print()

def save_results_to_csv(results_dir: str, all_results: Dict):
    """Save parsed results to CSV files for further analysis"""
    
    csv_dir = Path(results_dir) / "csv_exports"
    csv_dir.mkdir(exist_ok=True)
    
    levels = ['kyber512', 'kyber768', 'kyber1024']
    
    for level in levels:
        csv_file = csv_dir / f"{level}_comparison.csv"
        
        with open(csv_file, 'w') as f:
            # Write header
            f.write("Operation,Config1_Median,Config1_Avg,Config2_Median,Config2_Avg,")
            f.write("Config3_Median,Config3_Avg,Config4_Median,Config4_Avg\n")
            
            # Get all operations
            all_ops = set()
            for config_data in all_results.get(level, {}).values():
                all_ops.update(config_data.keys())
            
            # Write data
            for op in sorted(all_ops):
                f.write(f"{op}")
                
                for config in [1, 2, 3, 4]:
                    if config in all_results.get(level, {}) and op in all_results[level][config]:
                        median = all_results[level][config][op].get('median', 0)
                        average = all_results[level][config][op].get('average', 0)
                        f.write(f",{median},{average}")
                    else:
                        f.write(",N/A,N/A")
                
                f.write("\n")
    
    print(f"{Colors.GREEN}✓ CSV files exported to: {csv_dir}{Colors.NC}\n")

def main():
    """Main execution function"""
    
    # Check arguments
    if len(sys.argv) < 2:
        print(f"{Colors.RED}Usage: ./analyze_results.py <results_directory>{Colors.NC}")
        print(f"{Colors.YELLOW}Example: ./analyze_results.py benchmark_results/run_20240101_120000{Colors.NC}")
        sys.exit(1)
    
    results_dir = sys.argv[1]
    
    # Validate directory
    if not os.path.exists(results_dir):
        print(f"{Colors.RED}Error: Directory '{results_dir}' not found!{Colors.NC}")
        sys.exit(1)
    
    print(f"\n{Colors.CYAN}{'='*100}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'Kyber Benchmark Analysis Tool':^100}{Colors.NC}")
    print(f"{Colors.CYAN}{'='*100}{Colors.NC}\n")
    print(f"{Colors.YELLOW}Analyzing results from: {results_dir}{Colors.NC}\n")
    
    # Parse all result files
    configs = [1, 2, 3, 4]
    levels = ['kyber512', 'kyber768', 'kyber1024']
    
    all_results = {}
    
    for level in levels:
        all_results[level] = {}
        
        for config in configs:
            config_dir = Path(results_dir) / f"config{config}"
            result_file = config_dir / f"{level}_results.txt"
            
            if result_file.exists():
                print(f"{Colors.GREEN}✓ Found: {result_file.name}{Colors.NC}")
                all_results[level][config] = parse_benchmark_file(str(result_file))
            else:
                print(f"{Colors.YELLOW}⚠ Missing: {result_file}{Colors.NC}")
    
    print()
    
    # Generate comparison tables
    for level in levels:
        if level in all_results and all_results[level]:
            print_comparison_table(level, all_results[level])
            print_improvement_analysis(level, all_results[level])
    
    # Generate summary
    generate_summary_statistics(results_dir)
    
    # Save to CSV
    save_results_to_csv(results_dir, all_results)
    
    # Final message
    print(f"\n{Colors.CYAN}{'='*100}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.GREEN}Analysis Complete! ✅{Colors.NC}")
    print(f"{Colors.CYAN}{'='*100}{Colors.NC}\n")

if __name__ == "__main__":
    main()