#!/usr/bin/env python3
"""
Kyber Performance Visualization Generator
Generates publication-quality graphs from benchmark results

Usage: python generate_graphs.py <benchmark_results_directory>
Example: python generate_graphs.py benchmark_results/run_20240315_120000
"""

import os
import sys
import re
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from typing import Dict, List, Tuple

# Set publication-quality defaults
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 16

# Color scheme (professional)
COLORS = {
    'config1': '#2E86AB',  # Blue
    'config2': '#A23B72',  # Purple
    'config3': '#F18F01',  # Orange
    'config4': '#C73E1D',  # Red
}

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

def parse_result_file(filepath: str) -> Dict[str, int]:
    """Parse benchmark result file and extract cycle counts"""
    results = {}
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
            for op in OPERATIONS:
                # Try multiple patterns
                patterns = [
                    rf'{op}.*?Median:\s*(\d+)',
                    rf'{op}.*?median[:\s]+(\d+)',
                    rf'{op}\s+(\d+)',
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        results[op] = int(match.group(1))
                        break
    
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
                print(f"✓ Loaded {level} Config {config}")
            else:
                print(f"⚠ Missing: {result_file}")
    
    return all_results

def plot_operation_comparison(all_results: Dict, output_dir: Path):
    """Create bar charts comparing operations across configurations"""
    
    levels = ['kyber512', 'kyber768', 'kyber1024']
    
    # Main operations to highlight
    main_ops = ['indcpa_keypair', 'indcpa_enc', 'indcpa_dec']
    
    for level in levels:
        if level not in all_results:
            continue
        
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        fig.suptitle(f'{level.upper()} - Performance Comparison', 
                     fontsize=16, fontweight='bold')
        
        for idx, op in enumerate(main_ops):
            ax = axes[idx]
            
            configs = [1, 2, 3, 4]
            values = []
            labels = []
            colors = []
            
            for config in configs:
                if config in all_results[level] and op in all_results[level][config]:
                    values.append(all_results[level][config][op])
                    labels.append(f'Config {config}')
                    colors.append(COLORS[f'config{config}'])
            
            if values:
                bars = ax.bar(labels, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
                
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(height):,}',
                           ha='center', va='bottom', fontsize=9)
                
                ax.set_ylabel('Cycles', fontweight='bold')
                ax.set_title(op.replace('_', ' ').title(), fontweight='bold')
                ax.grid(axis='y', alpha=0.3, linestyle='--')
                
                # Format y-axis with commas
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        
        plt.tight_layout()
        output_file = output_dir / f'{level}_operation_comparison.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Generated: {output_file}")

def plot_improvement_chart(all_results: Dict, output_dir: Path):
    """Create improvement percentage charts vs Config 1 baseline"""
    
    levels = ['kyber512', 'kyber768', 'kyber1024']
    main_ops = ['indcpa_keypair', 'indcpa_enc', 'indcpa_dec']
    
    for level in levels:
        if level not in all_results or 1 not in all_results[level]:
            continue
        
        baseline = all_results[level][1]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(main_ops))
        width = 0.25
        
        for i, config in enumerate([2, 3, 4]):
            if config not in all_results[level]:
                continue
            
            improvements = []
            for op in main_ops:
                if op in baseline and op in all_results[level][config]:
                    base_val = baseline[op]
                    curr_val = all_results[level][config][op]
                    improvement = ((base_val - curr_val) / base_val) * 100
                    improvements.append(improvement)
                else:
                    improvements.append(0)
            
            offset = width * (i - 1)
            bars = ax.bar(x + offset, improvements, width, 
                         label=f'Config {config}',
                         color=COLORS[f'config{config}'],
                         alpha=0.8, edgecolor='black', linewidth=1.2)
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                label_y = height + 0.5 if height > 0 else height - 0.5
                ax.text(bar.get_x() + bar.get_width()/2., label_y,
                       f'{height:.1f}%',
                       ha='center', va='bottom' if height > 0 else 'top',
                       fontsize=9)
        
        ax.set_xlabel('Operation', fontweight='bold')
        ax.set_ylabel('Improvement vs Config 1 (%)', fontweight='bold')
        ax.set_title(f'{level.upper()} - Performance Improvement',
                    fontsize=16, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([op.replace('_', ' ').title() for op in main_ops])
        ax.legend()
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        
        plt.tight_layout()
        output_file = output_dir / f'{level}_improvement.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Generated: {output_file}")

def plot_all_levels_comparison(all_results: Dict, output_dir: Path):
    """Compare same operation across all security levels"""
    
    levels = ['kyber512', 'kyber768', 'kyber1024']
    main_ops = ['indcpa_keypair', 'indcpa_enc', 'indcpa_dec']
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Cross-Level Performance Comparison (Config 1 Baseline)',
                 fontsize=16, fontweight='bold')
    
    for idx, op in enumerate(main_ops):
        ax = axes[idx]
        
        x = np.arange(len(levels))
        width = 0.2
        
        for i, config in enumerate([1, 2, 3, 4]):
            values = []
            for level in levels:
                if level in all_results and config in all_results[level]:
                    if op in all_results[level][config]:
                        values.append(all_results[level][config][op])
                    else:
                        values.append(0)
                else:
                    values.append(0)
            
            offset = width * (i - 1.5)
            ax.bar(x + offset, values, width,
                  label=f'Config {config}',
                  color=COLORS[f'config{config}'],
                  alpha=0.8, edgecolor='black', linewidth=1.2)
        
        ax.set_ylabel('Cycles', fontweight='bold')
        ax.set_title(op.replace('_', ' ').title(), fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([l.upper() for l in levels])
        ax.legend()
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    plt.tight_layout()
    output_file = output_dir / 'all_levels_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Generated: {output_file}")

def plot_heatmap(all_results: Dict, output_dir: Path):
    """Create heatmap showing performance across operations and configs"""
    
    levels = ['kyber512', 'kyber768', 'kyber1024']
    
    for level in levels:
        if level not in all_results:
            continue
        
        # Prepare data matrix
        configs = [1, 2, 3, 4]
        ops_to_show = ['poly_compress', 'polyvec_compress', 
                       'indcpa_keypair', 'indcpa_enc', 'indcpa_dec']
        
        data = []
        for op in ops_to_show:
            row = []
            for config in configs:
                if config in all_results[level] and op in all_results[level][config]:
                    row.append(all_results[level][config][op])
                else:
                    row.append(0)
            data.append(row)
        
        data = np.array(data)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        im = ax.imshow(data, cmap='YlOrRd', aspect='auto')
        
        # Set ticks
        ax.set_xticks(np.arange(len(configs)))
        ax.set_yticks(np.arange(len(ops_to_show)))
        ax.set_xticklabels([f'Config {c}' for c in configs])
        ax.set_yticklabels([op.replace('_', ' ').title() for op in ops_to_show])
        
        # Rotate x labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Add text annotations
        for i in range(len(ops_to_show)):
            for j in range(len(configs)):
                text = ax.text(j, i, f'{int(data[i, j]):,}',
                             ha="center", va="center", color="black", fontsize=9)
        
        ax.set_title(f'{level.upper()} - Performance Heatmap (Cycles)',
                    fontsize=14, fontweight='bold')
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Cycles', rotation=270, labelpad=20, fontweight='bold')
        
        plt.tight_layout()
        output_file = output_dir / f'{level}_heatmap.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Generated: {output_file}")

def generate_summary_report(all_results: Dict, output_dir: Path):
    """Generate text summary report"""
    
    report_file = output_dir / 'summary_report.txt'
    
    with open(report_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("KYBER PERFORMANCE BENCHMARK SUMMARY\n")
        f.write("="*80 + "\n\n")
        
        levels = ['kyber512', 'kyber768', 'kyber1024']
        main_ops = ['indcpa_keypair', 'indcpa_enc', 'indcpa_dec']
        
        for level in levels:
            if level not in all_results:
                continue
            
            f.write(f"\n{level.upper()}\n")
            f.write("-"*80 + "\n")
            
            if 1 not in all_results[level]:
                f.write("Baseline (Config 1) not found\n")
                continue
            
            baseline = all_results[level][1]
            
            f.write(f"{'Operation':<25} {'Config 1':<15} {'Config 2':<15} {'Config 3':<15} {'Config 4':<15}\n")
            f.write("-"*80 + "\n")
            
            for op in main_ops:
                if op not in baseline:
                    continue
                
                line = f"{op:<25}"
                for config in [1, 2, 3, 4]:
                    if config in all_results[level] and op in all_results[level][config]:
                        val = all_results[level][config][op]
                        line += f"{val:>13,}  "
                    else:
                        line += f"{'N/A':>13}  "
                
                f.write(line + "\n")
            
            f.write("\n")
    
    print(f"✓ Generated: {report_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_graphs.py <benchmark_results_directory>")
        print("Example: python generate_graphs.py benchmark_results/run_20240315_120000")
        sys.exit(1)
    
    results_dir = sys.argv[1]
    
    if not os.path.exists(results_dir):
        print(f"Error: Directory '{results_dir}' not found!")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path(results_dir) / "graphs"
    output_dir.mkdir(exist_ok=True)
    
    print("\n" + "="*80)
    print("Kyber Performance Visualization Generator")
    print("="*80 + "\n")
    
    print("Loading benchmark results...")
    all_results = load_all_results(results_dir)
    
    print("\nGenerating visualizations...")
    print("-"*80)
    
    plot_operation_comparison(all_results, output_dir)
    plot_improvement_chart(all_results, output_dir)
    plot_all_levels_comparison(all_results, output_dir)
    plot_heatmap(all_results, output_dir)
    generate_summary_report(all_results, output_dir)
    
    print("\n" + "="*80)
    print("✅ All visualizations generated successfully!")
    print("="*80)
    print(f"\nOutput directory: {output_dir}")
    print("\nGenerated files:")
    for file in sorted(output_dir.glob("*")):
        print(f"  - {file.name}")
    print()

if __name__ == "__main__":
    main()