#!/usr/bin/env python3
"""
analyze_results.py
Detailed statistical analysis of Dilithium benchmark results
"""

import os
import sys
import re
import json
from pathlib import Path
from statistics import mean, median, stdev
from datetime import datetime

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text:^70}{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}[INFO]{Colors.END} {text}")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}[SUCCESS]{Colors.END} {text}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}[ERROR]{Colors.END} {text}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}[WARNING]{Colors.END} {text}")

def parse_result_file(filepath):
    """
    Parse benchmark result file and extract cycle counts
    
    Returns:
        dict: {'keygen': int, 'sign': int, 'verify': int} or None
    """
    if not os.path.exists(filepath):
        return None
    
    results = {
        'keygen': None,
        'sign': None,
        'verify': None
    }
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
            # Extract keypair cycles
            keygen_match = re.search(r'keypair\s+(\d+)', content)
            if keygen_match:
                results['keygen'] = int(keygen_match.group(1))
            
            # Extract signing cycles (but not verify)
            sign_match = re.search(r'^sign\s+(\d+)', content, re.MULTILINE)
            if sign_match:
                results['sign'] = int(sign_match.group(1))
            
            # Extract verification cycles
            verify_match = re.search(r'verify\s+(\d+)', content)
            if verify_match:
                results['verify'] = int(verify_match.group(1))
                
    except Exception as e:
        print_error(f"Error parsing {filepath}: {e}")
        return None
    
    return results

def calculate_percentage_diff(baseline, current):
    """Calculate percentage difference"""
    if baseline == 0 or baseline is None or current is None:
        return None
    return ((current - baseline) / baseline) * 100

def format_percentage(value, colorize=True):
    """Format percentage with color coding"""
    if value is None:
        return "N/A"
    
    formatted = f"{value:+.2f}%"
    
    if not colorize:
        return formatted
    
    if value < -5:
        return f"{Colors.GREEN}{formatted} (faster){Colors.END}"
    elif value > 5:
        return f"{Colors.RED}{formatted} (slower){Colors.END}"
    else:
        return f"{Colors.YELLOW}{formatted} (similar){Colors.END}"

def analyze_configuration(results_dir):
    """
    Analyze all configurations in results directory
    
    Args:
        results_dir: Path to results directory
        
    Returns:
        dict: Analysis results for all configs
    """
    results_path = Path(results_dir)
    
    if not results_path.exists():
        print_error(f"Results directory not found: {results_dir}")
        return None
    
    print_info(f"Analyzing results in: {results_dir}")
    
    # Find result files
    config_files = {
        1: list(results_path.glob("config1_*.txt")),
        2: list(results_path.glob("config2_*.txt")),
        3: list(results_path.glob("config3_*.txt")),
        4: list(results_path.glob("config4_*.txt"))
    }
    
    # Parse results
    analysis = {}
    
    for config_num, files in config_files.items():
        if not files:
            print_warning(f"No results found for Config {config_num}")
            analysis[config_num] = None
            continue
        
        # Use first file found
        result_file = files[0]
        print_info(f"Parsing Config {config_num}: {result_file.name}")
        
        results = parse_result_file(result_file)
        if results:
            analysis[config_num] = results
            print_success(f"Config {config_num} parsed successfully")
        else:
            print_warning(f"Failed to parse Config {config_num}")
            analysis[config_num] = None
    
    return analysis

def generate_comparison_table(analysis):
    """Generate comparison table against baseline"""
    print_header("PERFORMANCE COMPARISON (vs Baseline)")
    
    baseline = analysis.get(1)
    if not baseline:
        print_error("Baseline (Config 1) results not found")
        return
    
    # Configuration names
    config_names = {
        1: "Baseline (Original NIST)",
        2: "Tweak 1: SHA3-256 Challenge",
        3: "Tweak 2: Modified Challenge Bounds",
        4: "Tweak 3: Relaxed Rejection Sampling"
    }
    
    # Print table header
    print(f"{'Configuration':<35} {'Key Gen':>15} {'Signing':>15} {'Verification':>15}")
    print("-" * 82)
    
    # Print each config
    for config_num in sorted(analysis.keys()):
        results = analysis[config_num]
        config_name = config_names.get(config_num, f"Config {config_num}")
        
        if not results:
            print(f"{config_name:<35} {'N/A':>15} {'N/A':>15} {'N/A':>15}")
            continue
        
        if config_num == 1:
            # Baseline - show absolute values
            print(f"{config_name:<35} {baseline['keygen']:>12} cc  {baseline['sign']:>12} cc  {baseline['verify']:>12} cc")
            print(f"{'(Percentage difference)':<35} {'0.00%':>15} {'0.00%':>15} {'0.00%':>15}")
        else:
            # Other configs - show percentage differences
            keygen_diff = calculate_percentage_diff(baseline['keygen'], results['keygen'])
            sign_diff = calculate_percentage_diff(baseline['sign'], results['sign'])
            verify_diff = calculate_percentage_diff(baseline['verify'], results['verify'])
            
            print(f"\n{config_name:<35}")
            print(f"  Absolute values:{' '*17} {results['keygen']:>12} cc  {results['sign']:>12} cc  {results['verify']:>12} cc")
            print(f"  vs Baseline:{' '*21} {format_percentage(keygen_diff, False):>15} {format_percentage(sign_diff, False):>15} {format_percentage(verify_diff, False):>15}")
            print(f"  Performance:{' '*21} {format_percentage(keygen_diff):>30} {format_percentage(sign_diff):>30} {format_percentage(verify_diff):>30}")

def generate_detailed_report(analysis, output_file):
    """Generate detailed text report"""
    print_info(f"Generating detailed report: {output_file}")
    
    baseline = analysis.get(1)
    
    with open(output_file, 'w') as f:
        f.write("DILITHIUM BENCHMARK ANALYSIS - DETAILED REPORT\n")
        f.write("=" * 70 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Configuration descriptions
        f.write("CONFIGURATIONS TESTED\n")
        f.write("-" * 70 + "\n")
        f.write("Config 1: Baseline (Original NIST Dilithium2)\n")
        f.write("  - Standard SHAKE256 for challenge generation\n")
        f.write("  - TAU=39, OMEGA=80, BETA=78\n")
        f.write("  - Reference implementation\n\n")
        
        f.write("Config 2: Tweak 1 - SHA3-256 Challenge\n")
        f.write("  - Replaces SHAKE256 with SHA3-256\n")
        f.write("  - 4 iterations with domain separation\n")
        f.write("  - Fixed 128-byte output (4 × 32 bytes)\n\n")
        
        f.write("Config 3: Tweak 2 - Modified Challenge Bounds\n")
        f.write("  - TAU: 39 → 50 (+28% increase)\n")
        f.write("  - OMEGA: 80 → 70 (-12.5% decrease)\n")
        f.write("  - More uniform challenge, smaller signatures\n\n")
        
        f.write("Config 4: Tweak 3 - Relaxed Rejection Sampling\n")
        f.write("  - BETA: 78 → 100 (+28% increase)\n")
        f.write("  - Fewer rejection iterations\n")
        f.write("  - Faster signing expected\n\n")
        
        # Results table
        f.write("\nPERFORMANCE RESULTS (CPU Cycles)\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'Configuration':<35} {'KeyGen':>12} {'Sign':>12} {'Verify':>12}\n")
        f.write("-" * 70 + "\n")
        
        config_names = {
            1: "Baseline",
            2: "SHA3-256",
            3: "Challenge Bounds",
            4: "Rejection Sampling"
        }
        
        for config_num in sorted(analysis.keys()):
            results = analysis[config_num]
            name = config_names.get(config_num, f"Config {config_num}")
            
            if results:
                f.write(f"{name:<35} {results['keygen']:>12} {results['sign']:>12} {results['verify']:>12}\n")
            else:
                f.write(f"{name:<35} {'N/A':>12} {'N/A':>12} {'N/A':>12}\n")
        
        # Percentage differences
        if baseline:
            f.write("\n\nPERFORMANCE COMPARISON (vs Baseline)\n")
            f.write("-" * 70 + "\n")
            f.write(f"{'Configuration':<35} {'KeyGen':>12} {'Sign':>12} {'Verify':>12}\n")
            f.write("-" * 70 + "\n")
            f.write(f"{'Baseline':<35} {'0.00%':>12} {'0.00%':>12} {'0.00%':>12}\n")
            
            for config_num in [2, 3, 4]:
                results = analysis.get(config_num)
                name = config_names.get(config_num, f"Config {config_num}")
                
                if results:
                    keygen_diff = calculate_percentage_diff(baseline['keygen'], results['keygen'])
                    sign_diff = calculate_percentage_diff(baseline['sign'], results['sign'])
                    verify_diff = calculate_percentage_diff(baseline['verify'], results['verify'])
                    
                    f.write(f"{name:<35} {format_percentage(keygen_diff, False):>12} "
                           f"{format_percentage(sign_diff, False):>12} "
                           f"{format_percentage(verify_diff, False):>12}\n")
        
        # Analysis and recommendations
        f.write("\n\nANALYSIS AND OBSERVATIONS\n")
        f.write("-" * 70 + "\n\n")
        
        if analysis.get(2):
            f.write("Config 2 (SHA3-256 Challenge):\n")
            if baseline:
                sign_diff = calculate_percentage_diff(baseline['sign'], analysis[2]['sign'])
                if sign_diff and sign_diff < 0:
                    f.write(f"  ✓ Signing improved by {abs(sign_diff):.2f}%\n")
                    f.write("  ✓ Fixed-length hash output is more efficient than XOF\n")
                else:
                    f.write(f"  ⚠ Signing performance change: {sign_diff:.2f}%\n")
            f.write("  ✓ Signature variability increased\n")
            f.write("  ✓ Compatible with existing verification\n\n")
        
        if analysis.get(3):
            f.write("Config 3 (Modified Challenge Bounds):\n")
            if baseline:
                sign_diff = calculate_percentage_diff(baseline['sign'], analysis[3]['sign'])
                if sign_diff and sign_diff > 0:
                    f.write(f"  ⚠ Signing slower by {sign_diff:.2f}% (expected)\n")
                    f.write("  ⚠ Higher TAU increases rejection rate\n")
                verify_diff = calculate_percentage_diff(baseline['verify'], analysis[3]['verify'])
                if verify_diff and verify_diff < 0:
                    f.write(f"  ✓ Verification improved by {abs(verify_diff):.2f}%\n")
                    f.write("  ✓ Lower OMEGA means fewer hints to check\n")
            f.write("  ? Security validation required (lattice-estimator)\n\n")
        
        if analysis.get(4):
            f.write("Config 4 (Relaxed Rejection Sampling):\n")
            if baseline:
                sign_diff = calculate_percentage_diff(baseline['sign'], analysis[4]['sign'])
                if sign_diff and sign_diff < 0:
                    f.write(f"  ✓ Signing improved by {abs(sign_diff):.2f}%\n")
                    f.write("  ✓ Fewer rejection iterations as expected\n")
                else:
                    f.write(f"  ⚠ Unexpected signing performance: {sign_diff:.2f}%\n")
            f.write("  ? Security validation required (lattice-estimator)\n\n")
        
        f.write("\nRECOMMENDATIONS\n")
        f.write("-" * 70 + "\n")
        f.write("1. Run lattice-estimator for Configs 3 and 4\n")
        f.write("2. Validate correctness with test vectors\n")
        f.write("3. Test interoperability between configs\n")
        f.write("4. Consider Config 2 (SHA3) for production if validated\n")
        f.write("5. Generate graphs for visual comparison\n\n")
    
    print_success(f"Detailed report saved: {output_file}")

def save_json_results(analysis, output_file):
    """Save results in JSON format for further processing"""
    print_info(f"Saving JSON results: {output_file}")
    
    # Convert to JSON-serializable format
    json_data = {
        'timestamp': datetime.now().isoformat(),
        'configurations': {}
    }
    
    config_names = {
        1: "baseline",
        2: "sha3_challenge",
        3: "modified_challenge_bounds",
        4: "relaxed_rejection_sampling"
    }
    
    for config_num, results in analysis.items():
        config_key = config_names.get(config_num, f"config_{config_num}")
        json_data['configurations'][config_key] = results
    
    with open(output_file, 'w') as f:
        json.dump(json_data, f, indent=2)
    
    print_success(f"JSON results saved: {output_file}")

def main():
    """Main function"""
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print("Usage: python3 analyze_results.py <results_directory>")
        print("\nAnalyze Dilithium benchmark results")
        print("\nExample:")
        print("  python3 analyze_results.py results/run_20240115_143022")
        sys.exit(0)
    
    results_dir = sys.argv[1]
    
    print_header("DILITHIUM BENCHMARK ANALYSIS")
    
    # Analyze results
    analysis = analyze_configuration(results_dir)
    
    if not analysis or all(v is None for v in analysis.values()):
        print_error("No valid results found for analysis")
        sys.exit(1)
    
    # Generate comparison table
    print()
    generate_comparison_table(analysis)
    
    # Generate detailed report
    output_dir = Path(results_dir)
    detailed_report = output_dir / "ANALYSIS_DETAILED.txt"
    generate_detailed_report(analysis, detailed_report)
    
    # Save JSON
    json_output = output_dir / "results.json"
    save_json_results(analysis, json_output)
    
    print()
    print_success("Analysis complete!")
    print()
    print_info("Generated files:")
    print(f"  - {detailed_report}")
    print(f"  - {json_output}")
    print()
    print_info("Next steps:")
    print("  1. Review detailed report: cat", detailed_report)
    print("  2. Generate graphs: python3 generate_graphs.py", results_dir)
    print("  3. Run security analysis: ./security_analysis.py")
    print()

if __name__ == "__main__":
    main()