#!/usr/bin/env python3
"""
Kyber Security Analysis Tool
Automated security validation using lattice-estimator

Requirements:
- lattice-estimator (https://github.com/malb/lattice-estimator)
- SageMath or Python with required libraries

Installation on Fedora:
    git clone https://github.com/malb/lattice-estimator
    cd lattice-estimator
    pip3 install -r requirements.txt

Usage: python security_analysis.py
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import tempfile

# ANSI Colors
class Colors:
    CYAN = '\033[0;36m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    BOLD = '\033[1m'
    NC = '\033[0m'

def print_header():
    """Print professional header"""
    print(f"\n{Colors.CYAN}{'='*80}{Colors.NC}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'Kyber Security Analysis Tool':^80}{Colors.NC}")
    print(f"{Colors.CYAN}{'='*80}{Colors.NC}\n")

def print_section(title):
    """Print section header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{title}{Colors.NC}")
    print(f"{Colors.BLUE}{'-'*80}{Colors.NC}")

def load_configurations(config_file='security_config.json'):
    """Load parameter configurations from JSON file"""
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        print(f"{Colors.GREEN}✓ Loaded configurations from {config_file}{Colors.NC}")
        return config_data['configurations']
    except FileNotFoundError:
        print(f"{Colors.RED}✗ Error: {config_file} not found!{Colors.NC}")
        print(f"{Colors.YELLOW}Please ensure security_config.json exists in the current directory.{Colors.NC}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}✗ Error parsing JSON: {e}{Colors.NC}")
        sys.exit(1)

def check_lattice_estimator():
    """Check if lattice-estimator is available"""
    print(f"{Colors.YELLOW}Checking for lattice-estimator...{Colors.NC}")
    
    # Try to import the estimator
    try:
        # Check if we can find the estimator module
        result = subprocess.run(['python3', '-c', 'import estimator'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Colors.GREEN}✓ Lattice estimator found{Colors.NC}")
            return True
    except:
        pass
    
    # Check if estimator directory exists
    estimator_paths = [
        'lattice-estimator',
        '../lattice-estimator',
        '../../lattice-estimator',
        os.path.expanduser('~/lattice-estimator')
    ]
    
    for path in estimator_paths:
        if os.path.exists(path):
            print(f"{Colors.GREEN}✓ Lattice estimator found at: {path}{Colors.NC}")
            return path
    
    print(f"{Colors.RED}✗ Lattice estimator not found!{Colors.NC}")
    print(f"\n{Colors.YELLOW}Installation Instructions:{Colors.NC}")
    print(f"  1. Clone the repository:")
    print(f"     git clone https://github.com/malb/lattice-estimator")
    print(f"  2. Install dependencies:")
    print(f"     cd lattice-estimator")
    print(f"     pip3 install -r requirements.txt")
    print()
    
    return False

def generate_estimator_script(params: Dict, output_file: str):
    """Generate Python script for lattice estimator"""
    
    n = params['n']
    k = params['k']
    q = params['q']
    eta1 = params['eta1']
    eta2 = params['eta2']
    
    script = f"""#!/usr/bin/env python3
# Auto-generated security analysis script
# Parameters: n={n}, k={k}, q={q}, eta1={eta1}, eta2={eta2}

from estimator import *
from estimator.lwe_parameters import LWEParameters
from estimator.lwe_guess import guess_and_reduce

# Define Kyber-like parameters
n = {n}
k = {k}
q = {q}
eta1 = {eta1}
eta2 = {eta2}

# Create LWE instance (module dimension n*k)
params = LWEParameters(
    n=n*k,
    q=q,
    Xs=ND.SparseTernary(n*k, p=eta1/q),
    Xe=ND.SparseTernary(n*k, p=eta2/q),
    m=n*k + n
)

print("="*80)
print("Kyber Security Analysis")
print("="*80)
print(f"Parameters: n={{n}}, k={{k}}, q={{q}}, eta1={{eta1}}, eta2={{eta2}}")
print(f"Dimension: {{n*k}}")
print()

# Run primal attack estimation
print("Primal Attack Analysis:")
print("-"*80)
try:
    primal = primal_usvp(params)
    print(f"Core-SVP (Classical): {{primal['rop']}}")
    print(f"Block size (b): {{primal.get('beta', 'N/A')}}")
    print(f"Dimension (d): {{primal.get('d', 'N/A')}}")
except Exception as e:
    print(f"Error: {{e}}")

print()

# Run dual attack estimation
print("Dual Attack Analysis:")
print("-"*80)
try:
    dual = dual_scale(params)
    print(f"Core-SVP (Classical): {{dual['rop']}}")
    print(f"Block size (b): {{dual.get('beta', 'N/A')}}")
    print(f"Dimension (d): {{dual.get('d', 'N/A')}}")
except Exception as e:
    print(f"Error: {{e}}")

print()
print("="*80)
"""
    
    with open(output_file, 'w') as f:
        f.write(script)
    
    os.chmod(output_file, 0o755)

def run_security_analysis(config_name: str, level: str, params: Dict, output_dir: Path):
    """Run security analysis for a specific configuration"""
    
    print(f"\n{Colors.CYAN}Analyzing {config_name} - {level.upper()}{Colors.NC}")
    
    # Create temporary script
    script_file = output_dir / f"temp_{config_name}_{level}.py"
    generate_estimator_script(params, str(script_file))
    
    # Run the estimator
    try:
        result = subprocess.run(
            ['python3', str(script_file)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        output = result.stdout
        
        # Save output
        log_file = output_dir / 'estimator_logs' / f"{config_name}_{level}.txt"
        log_file.parent.mkdir(exist_ok=True)
        
        with open(log_file, 'w') as f:
            f.write(output)
        
        print(f"{Colors.GREEN}✓ Analysis complete{Colors.NC}")
        
        # Clean up temp script
        script_file.unlink()
        
        return parse_estimator_output(output)
        
    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}✗ Analysis timed out{Colors.NC}")
        return None
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.NC}")
        return None

def parse_estimator_output(output: str) -> Dict:
    """Parse estimator output and extract key metrics"""
    
    results = {
        'primal_classical': 'N/A',
        'primal_quantum': 'N/A',
        'dual_classical': 'N/A',
        'dual_quantum': 'N/A',
        'block_size': 'N/A',
        'dimension': 'N/A'
    }
    
    lines = output.split('\n')
    
    for line in lines:
        if 'Core-SVP (Classical)' in line:
            # Extract numerical value
            parts = line.split(':')
            if len(parts) > 1:
                value = parts[1].strip()
                if 'Primal' in output[:output.find(line)].split('\n')[-5:]:
                    results['primal_classical'] = value
                else:
                    results['dual_classical'] = value
        
        elif 'Block size' in line:
            parts = line.split(':')
            if len(parts) > 1:
                results['block_size'] = parts[1].strip()
        
        elif 'Dimension' in line:
            parts = line.split(':')
            if len(parts) > 1:
                results['dimension'] = parts[1].strip()
    
    return results

def generate_latex_tables(all_results: Dict, output_dir: Path):
    """Generate LaTeX tables from security analysis results"""
    
    print_section("Generating LaTeX Tables")
    
    output_file = output_dir / 'security_tables.tex'
    
    with open(output_file, 'w') as f:
        f.write("% " + "="*70 + "\n")
        f.write("% Kyber Security Analysis Tables\n")
        f.write("% Auto-generated by security_analysis.py\n")
        f.write(f"% Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("% " + "="*70 + "\n\n")
        
        levels = ['kyber512', 'kyber768', 'kyber1024']
        
        for level in levels:
            f.write(f"\n% {level.upper()} Security Analysis\n")
            f.write("\\begin{table}[htbp]\n")
            f.write("\\centering\n")
            f.write(f"\\caption{{Security Analysis of {level.upper()} for Different Parameter Sets}}\n")
            f.write(f"\\label{{tab:security_{level}}}\n")
            f.write("\\begin{tabular}{|l|c|c|c|c|}\n")
            f.write("\\hline\n")
            f.write("\\textbf{Configuration} & \\textbf{Primal (Classical)} & \\textbf{Dual (Classical)} & ")
            f.write("\\textbf{Block Size} & \\textbf{Dimension} \\\\\n")
            f.write("\\hline\n")
            
            for config in ['config1', 'config2', 'config3', 'config4']:
                if config in all_results and level in all_results[config]:
                    res = all_results[config][level]
                    config_name = config.replace('config', 'Configuration ')
                    
                    f.write(f"{config_name} & ")
                    f.write(f"{res.get('primal_classical', 'N/A')} & ")
                    f.write(f"{res.get('dual_classical', 'N/A')} & ")
                    f.write(f"{res.get('block_size', 'N/A')} & ")
                    f.write(f"{res.get('dimension', 'N/A')} \\\\\n")
            
            f.write("\\hline\n")
            f.write("\\end{tabular}\n")
            f.write("\\end{table}\n\n")
    
    print(f"{Colors.GREEN}✓ LaTeX tables saved to: {output_file}{Colors.NC}")

def generate_text_report(all_results: Dict, output_dir: Path):
    """Generate human-readable text report"""
    
    print_section("Generating Text Report")
    
    output_file = output_dir / 'security_report.txt'
    
    with open(output_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("KYBER SECURITY ANALYSIS REPORT\n")
        f.write("="*80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        levels = ['kyber512', 'kyber768', 'kyber1024']
        
        for level in levels:
            f.write(f"\n{level.upper()}\n")
            f.write("-"*80 + "\n")
            
            for config in ['config1', 'config2', 'config3', 'config4']:
                if config in all_results and level in all_results[config]:
                    res = all_results[config][level]
                    config_name = config.replace('config', 'Configuration ')
                    
                    f.write(f"\n{config_name}:\n")
                    f.write(f"  Primal Attack (Classical): {res.get('primal_classical', 'N/A')}\n")
                    f.write(f"  Dual Attack (Classical):   {res.get('dual_classical', 'N/A')}\n")
                    f.write(f"  Block Size (b):            {res.get('block_size', 'N/A')}\n")
                    f.write(f"  Dimension (d):             {res.get('dimension', 'N/A')}\n")
            
            f.write("\n")
    
    print(f"{Colors.GREEN}✓ Text report saved to: {output_file}{Colors.NC}")

def generate_summary(all_results: Dict, output_dir: Path):
    """Generate summary of security analysis"""
    
    print_section("Security Analysis Summary")
    
    levels = ['kyber512', 'kyber768', 'kyber1024']
    configs = ['config1', 'config2', 'config3', 'config4']
    
    print(f"\n{'Level':<15} {'Config':<15} {'Primal':<20} {'Dual':<20}")
    print("-"*70)
    
    for level in levels:
        for config in configs:
            if config in all_results and level in all_results[config]:
                res = all_results[config][level]
                print(f"{level:<15} {config:<15} {res.get('primal_classical', 'N/A'):<20} {res.get('dual_classical', 'N/A'):<20}")
    
    print()

def create_installation_guide(output_dir: Path):
    """Create installation guide for lattice-estimator"""
    
    guide_file = output_dir / 'INSTALLATION_GUIDE.txt'
    
    with open(guide_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("LATTICE ESTIMATOR INSTALLATION GUIDE\n")
        f.write("="*80 + "\n\n")
        
        f.write("Prerequisites:\n")
        f.write("-"*80 + "\n")
        f.write("- Python 3.8+\n")
        f.write("- pip3\n")
        f.write("- git\n\n")
        
        f.write("Installation Steps (Fedora/Linux):\n")
        f.write("-"*80 + "\n")
        f.write("1. Install system dependencies:\n")
        f.write("   sudo dnf install python3 python3-pip git\n\n")
        
        f.write("2. Clone the lattice-estimator repository:\n")
        f.write("   git clone https://github.com/malb/lattice-estimator\n")
        f.write("   cd lattice-estimator\n\n")
        
        f.write("3. Install Python dependencies:\n")
        f.write("   pip3 install -r requirements.txt\n\n")
        
        f.write("4. Verify installation:\n")
        f.write("   python3 -c 'import estimator; print(\"Success!\")'\n\n")
        
        f.write("5. Return to kyber directory and run analysis:\n")
        f.write("   cd ../kyber\n")
        f.write("   python3 security_analysis.py\n\n")
        
        f.write("="*80 + "\n")
        f.write("For issues, see: https://github.com/malb/lattice-estimator\n")
        f.write("="*80 + "\n")
    
    print(f"{Colors.GREEN}✓ Installation guide created: {guide_file}{Colors.NC}")

def main():
    """Main execution function"""
    
    print_header()
    
    # Create output directory
    output_dir = Path('security_results')
    output_dir.mkdir(exist_ok=True)
    
    # Check for lattice estimator
    estimator_available = check_lattice_estimator()
    
    if not estimator_available:
        print(f"\n{Colors.YELLOW}Creating installation guide...{Colors.NC}")
        create_installation_guide(output_dir)
        print(f"\n{Colors.RED}Please install lattice-estimator first.{Colors.NC}")
        print(f"{Colors.YELLOW}See: {output_dir}/INSTALLATION_GUIDE.txt{Colors.NC}")
        return
    
    # Load configurations
    print_section("Loading Configurations")
    configurations = load_configurations()
    
    print(f"{Colors.GREEN}✓ Found {len(configurations)} configurations{Colors.NC}")
    for config_name in configurations.keys():
        print(f"  - {config_name}")
    
    # Run analysis for all configurations
    print_section("Running Security Analysis")
    print(f"{Colors.YELLOW}This may take several minutes...{Colors.NC}\n")
    
    all_results = {}
    levels = ['kyber512', 'kyber768', 'kyber1024']
    
    for config_name, config_data in configurations.items():
        all_results[config_name] = {}
        
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}Configuration: {config_data['name']}{Colors.NC}")
        
        for level in levels:
            if level in config_data:
                params = config_data[level]
                results = run_security_analysis(config_name, level, params, output_dir)
                
                if results:
                    all_results[config_name][level] = results
    
    # Generate outputs
    generate_latex_tables(all_results, output_dir)
    generate_text_report(all_results, output_dir)
    generate_summary(all_results, output_dir)
    
    # Final summary
    print(f"\n{Colors.CYAN}{'='*80}{Colors.NC}")
    print(f"{Colors.GREEN}{Colors.BOLD}✅ Security Analysis Complete!{Colors.NC}")
    print(f"{Colors.CYAN}{'='*80}{Colors.NC}\n")
    
    print(f"  - LaTeX tables:  {output_dir}/security_tables.tex")
    print(f"  - Text report:   {output_dir}/security_report.txt")
    print(f"  - Estimator logs: {output_dir}/estimator_logs/")
    print()
    
    print(f"{Colors.CYAN}Next steps:{Colors.NC}")
    print(f"  1. Review results in: {output_dir}/")
    print(f"  2. Include LaTeX tables in thesis")
    print(f"  3. Reference security validation in documentation")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Analysis interrupted by user.{Colors.NC}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.NC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)