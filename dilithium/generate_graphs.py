#!/usr/bin/env python3
"""
generate_graphs.py
Generate visual graphs from Dilithium benchmark results
"""

import os
import sys
import json
import re
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Color scheme
COLORS = {
    'baseline': '#3498db',    # Blue
    'sha3': '#2ecc71',        # Green
    'challenge': '#f39c12',   # Orange
    'rejection': '#e74c3c'    # Red
}

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

def create_absolute_comparison_chart(data, output_file):
    """
    Create bar chart comparing absolute cycle counts
    """
    print_info("Generating absolute performance comparison chart...")
    
    configs = data['configurations']
    
    # Extract data
    config_names = []
    keygen_values = []
    sign_values = []
    verify_values = []
    
    name_mapping = {
        'baseline': 'Baseline\n(Original)',
        'sha3_challenge': 'SHA3-256\n(Tweak 1)',
        'modified_challenge_bounds': 'Challenge\nBounds (T2)',
        'relaxed_rejection_sampling': 'Rejection\nSampling (T3)'
    }
    
    for config_key, config_data in configs.items():
        if config_data is None:
            continue
        
        config_names.append(name_mapping.get(config_key, config_key))
        keygen_values.append(config_data['keygen'] if config_data['keygen'] else 0)
        sign_values.append(config_data['sign'] if config_data['sign'] else 0)
        verify_values.append(config_data['verify'] if config_data['verify'] else 0)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(len(config_names))
    width = 0.25
    
    # Create bars
    bars1 = ax.bar(x - width, keygen_values, width, label='Key Generation',
                   color=COLORS['baseline'], edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x, sign_values, width, label='Signing',
                   color=COLORS['sha3'], edgecolor='black', linewidth=1.2)
    bars3 = ax.bar(x + width, verify_values, width, label='Verification',
                   color=COLORS['challenge'], edgecolor='black', linewidth=1.2)
    
    # Add value labels on bars
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height):,}',
                       ha='center', va='bottom', fontsize=9, rotation=0)
    
    add_value_labels(bars1)
    add_value_labels(bars2)
    add_value_labels(bars3)
    
    # Formatting
    ax.set_xlabel('Configuration', fontsize=12, fontweight='bold')
    ax.set_ylabel('CPU Cycles', fontsize=12, fontweight='bold')
    ax.set_title('Dilithium Performance Comparison\n(Absolute CPU Cycles)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(config_names, fontsize=10)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Format y-axis with commas
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print_success(f"Saved: {output_file}")

def create_percentage_comparison_chart(data, output_file):
    """
    Create bar chart showing percentage differences vs baseline
    """
    print_info("Generating percentage difference comparison chart...")
    
    configs = data['configurations']
    baseline = configs.get('baseline')
    
    if not baseline:
        print_error("Baseline configuration not found")
        return
    
    # Calculate percentage differences
    config_names = []
    keygen_diffs = []
    sign_diffs = []
    verify_diffs = []
    
    name_mapping = {
        'sha3_challenge': 'SHA3-256\n(Tweak 1)',
        'modified_challenge_bounds': 'Challenge\nBounds (T2)',
        'relaxed_rejection_sampling': 'Rejection\nSampling (T3)'
    }
    
    for config_key in ['sha3_challenge', 'modified_challenge_bounds', 'relaxed_rejection_sampling']:
        config_data = configs.get(config_key)
        if config_data is None:
            continue
        
        config_names.append(name_mapping.get(config_key, config_key))
        
        # Calculate percentage differences
        keygen_diff = ((config_data['keygen'] - baseline['keygen']) / baseline['keygen'] * 100) if config_data['keygen'] else 0
        sign_diff = ((config_data['sign'] - baseline['sign']) / baseline['sign'] * 100) if config_data['sign'] else 0
        verify_diff = ((config_data['verify'] - baseline['verify']) / baseline['verify'] * 100) if config_data['verify'] else 0
        
        keygen_diffs.append(keygen_diff)
        sign_diffs.append(sign_diff)
        verify_diffs.append(verify_diff)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(len(config_names))
    width = 0.25
    
    # Create bars
    bars1 = ax.bar(x - width, keygen_diffs, width, label='Key Generation',
                   color=COLORS['baseline'], edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x, sign_diffs, width, label='Signing',
                   color=COLORS['sha3'], edgecolor='black', linewidth=1.2)
    bars3 = ax.bar(x + width, verify_diffs, width, label='Verification',
                   color=COLORS['challenge'], edgecolor='black', linewidth=1.2)
    
    # Add value labels
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            label_y = height + (1 if height >= 0 else -3)
            ax.text(bar.get_x() + bar.get_width()/2., label_y,
                   f'{height:+.1f}%',
                   ha='center', va='bottom' if height >= 0 else 'top',
                   fontsize=9, fontweight='bold')
    
    add_value_labels(bars1)
    add_value_labels(bars2)
    add_value_labels(bars3)
    
    # Add reference line at 0%
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.7)
    
    # Formatting
    ax.set_xlabel('Configuration', fontsize=12, fontweight='bold')
    ax.set_ylabel('Performance Difference (%)', fontsize=12, fontweight='bold')
    ax.set_title('Dilithium Performance vs Baseline\n(Percentage Difference - Negative is Better)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(config_names, fontsize=10)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add color zones
    ax.axhspan(-100, -5, alpha=0.1, color='green', label='Faster')
    ax.axhspan(-5, 5, alpha=0.1, color='yellow', label='Similar')
    ax.axhspan(5, 100, alpha=0.1, color='red', label='Slower')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print_success(f"Saved: {output_file}")

def create_operation_comparison_chart(data, output_file):
    """
    Create separate charts for each operation type
    """
    print_info("Generating individual operation comparison charts...")
    
    configs = data['configurations']
    
    # Extract data
    config_labels = []
    keygen_values = []
    sign_values = []
    verify_values = []
    colors_list = []
    
    name_mapping = {
        'baseline': 'Baseline',
        'sha3_challenge': 'SHA3-256',
        'modified_challenge_bounds': 'Challenge Bounds',
        'relaxed_rejection_sampling': 'Rejection Sampling'
    }
    
    color_mapping = {
        'baseline': COLORS['baseline'],
        'sha3_challenge': COLORS['sha3'],
        'modified_challenge_bounds': COLORS['challenge'],
        'relaxed_rejection_sampling': COLORS['rejection']
    }
    
    for config_key, config_data in configs.items():
        if config_data is None:
            continue
        
        config_labels.append(name_mapping.get(config_key, config_key))
        keygen_values.append(config_data['keygen'] if config_data['keygen'] else 0)
        sign_values.append(config_data['sign'] if config_data['sign'] else 0)
        verify_values.append(config_data['verify'] if config_data['verify'] else 0)
        colors_list.append(color_mapping.get(config_key, '#95a5a6'))
    
    # Create figure with 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))
    
    # Key Generation
    bars1 = ax1.bar(config_labels, keygen_values, color=colors_list, 
                    edgecolor='black', linewidth=1.2)
    ax1.set_title('Key Generation', fontsize=12, fontweight='bold')
    ax1.set_ylabel('CPU Cycles', fontsize=11, fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom', fontsize=9)
    
    # Signing
    bars2 = ax2.bar(config_labels, sign_values, color=colors_list,
                    edgecolor='black', linewidth=1.2)
    ax2.set_title('Signing', fontsize=12, fontweight='bold')
    ax2.set_ylabel('CPU Cycles', fontsize=11, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom', fontsize=9)
    
    # Verification
    bars3 = ax3.bar(config_labels, verify_values, color=colors_list,
                    edgecolor='black', linewidth=1.2)
    ax3.set_title('Verification', fontsize=12, fontweight='bold')
    ax3.set_ylabel('CPU Cycles', fontsize=11, fontweight='bold')
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom', fontsize=9)
    
    fig.suptitle('Dilithium Performance by Operation Type', 
                 fontsize=14, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print_success(f"Saved: {output_file}")

def main():
    """Main function"""
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print("Usage: python3 generate_graphs.py <results_directory>")
        print("\nGenerate performance graphs from benchmark results")
        print("\nExample:")
        print("  python3 generate_graphs.py results/run_20240115_143022")
        print("\nNote: Run analyze_results.py first to generate results.json")
        sys.exit(0)
    
    results_dir = sys.argv[1]
    
    print("\n" + "="*70)
    print("DILITHIUM GRAPH GENERATION".center(70))
    print("="*70 + "\n")
    
    # Load results
    data = load_results(results_dir)
    if not data:
        sys.exit(1)
    
    # Create graphs directory
    graphs_dir = Path(results_dir) / "graphs"
    graphs_dir.mkdir(exist_ok=True)
    print_info(f"Saving graphs to: {graphs_dir}")
    
    # Generate graphs
    create_absolute_comparison_chart(data, graphs_dir / "performance_absolute.png")
    create_percentage_comparison_chart(data, graphs_dir / "performance_percentage.png")
    create_operation_comparison_chart(data, graphs_dir / "performance_by_operation.png")
    
    print("\n" + "="*70)
    print_success("All graphs generated successfully!")
    print("="*70)
    
    print_info("\nGenerated files:")
    for graph_file in graphs_dir.glob("*.png"):
        print(f"  - {graph_file}")
    
    print("\n" + print_info("Next steps:"))
    print("  1. View graphs: open " + str(graphs_dir) + "/*.png")
    print("  2. Generate LaTeX tables: python3 generate_tables.py " + results_dir)
    print("  3. Create dashboard: python3 create_dashboard.py " + results_dir)
    print()

if __name__ == "__main__":
    main()