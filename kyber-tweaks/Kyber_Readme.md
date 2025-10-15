Kyber Parameter Tweaks and Security Analysis
🚀 Quick Demo
Start with our automated demo script that showcases all features:

bash
# Run the complete automated demonstration
./final_demo.sh --auto

# Or run interactively with menu options
./final_demo.sh
The demo script will:

✅ Run all performance benchmarks (Tables 5.1-5.4)
✅ Test correctness of all parameter configurations
✅ Execute security analysis (Tables 5.5-5.8)
✅ Generate all thesis figures and reports
✅ Create a comprehensive summary report
📋 Table of Contents
Project Overview
Key Results
Complete Project Structure
Installation and Setup
Using the Demo Script
Core Implementation Details
Component Documentation
Results and Analysis
Troubleshooting
Advanced Usage
🎯 Project Overview
This project implements and analyzes parameter tweaks for the Kyber post-quantum cryptographic scheme, as described in Chapter 5 of the thesis. The implementation demonstrates how different compression and noise parameters affect performance, ciphertext sizes, and security levels.

🔑 Key Features
Feature	Description
Parameter Flexibility	Support for multiple compression parameters (du, dv) and noise parameters (η1, η2)
Automated Benchmarking	Comprehensive performance analysis with cycle-accurate measurements
Correctness Verification	CLI tools for testing encryption/decryption with all parameter sets
Security Analysis	Both static (thesis values) and dynamic (calculated) security estimates
Professional Reporting	Automated generation of thesis-ready tables and visualizations
📊 What This Project Demonstrates
Performance Trade-offs: How compression parameters affect computational overhead
Size Optimization: Ciphertext size variations with different (du, dv) values
Security Margins: Impact of parameter choices on security levels
Practical Implementation: Working code for all parameter variations
🎉 Key Results
Performance Impact Summary
Configuration	Ciphertext Change	Performance Impact	Use Case
(du=11, dv=3)	-4% (32 bytes less)	~5% overhead	Recommended for size optimization
(du=9, dv=5)	+4% (32 bytes more)	~15% overhead	Not recommended
Eta variations	No size change	+20-30% KeyGen/Enc	Higher security margin
Security Levels Maintained
All parameter variations maintain required NIST security levels:

Kyber512: Level 1 (≥128-bit security)
Kyber768: Level 3 (≥192-bit security)
Kyber1024: Level 5 (≥256-bit security)
📁 Complete Project Structure
text
kyber-tweaks/
├── final_demo.sh                            # 🎯 MAIN DEMO SCRIPT
├── demo_YYYYMMDD_HHMMSS.log                # Demo execution log
├── thesis_results_YYYYMMDD_HHMMSS.txt      # Summary report
│
├── kyber/
│   └── ref/
│       ├── configs/                         # Parameter configuration files
│       │   ├── params_baseline_standard.h  # NIST Round 3 baseline
│       │   ├── params_test1_du10_dv4.h    # Test 1: Standard compression
│       │   ├── params_test2_du11_dv3.h    # Test 2: Size optimized ⭐
│       │   ├── params_test3_du9_dv5.h     # Test 3: High compression
│       │   ├── params_test4_eta_variations.h # Test 4: Noise variations
│       │   └── params_kyber1024_*.h        # Special Kyber1024 configs
│       ├── poly.c                          # Modified polynomial operations
│       ├── polyvec.c                       # Modified vector operations
│       ├── cbd.c                           # Extended CBD sampling
│       └── test_speed[512|768|1024]        # Benchmark binaries
│
├── benchmarks/                              # Performance analysis suite
│   ├── run_cycle_counts.sh                 # Main benchmark runner
│   ├── analyze_results.py                  # Generate Tables 5.1-5.4
│   ├── generate_charts.py                  # Create visualizations
│   ├── generate_report.sh                  # HTML report generator
│   └── results/                            # Timestamped results
│
├── cli-tests/                              # Correctness testing tools
│   ├── kyber_keygen                        # Key generation
│   ├── kyber_encrypt                       # Encryption
│   ├── kyber_decrypt                       # Decryption
│   ├── kyber_demo                          # Interactive demo
│   └── scripts/                            # Test automation
│
├── kyber-security-analysis/                # Static security (thesis values)
│   ├── scripts/
│   │   ├── kyber_security_analysis.py     # Tables 5.5-5.8 generator
│   │   └── Kyber.py                       # Individual parameter testing
│   └── results/                            # Security analysis outputs
│
└── kyber-dynamic-security-analysis/        # Dynamic security (calculated)
    ├── scripts/
    │   └── dynamic_analyzer.py             # Lattice estimator interface
    ├── sage-scripts/
    │   └── kyber_estimator.sage           # SageMath security calculations
    └── results/                            # Calculated security levels
🛠️ Installation and Setup
Prerequisites
Requirement	Version	Required/Optional	Purpose
Ubuntu Linux	20.04+	Required	Development environment
GCC	6.3.0+	Required	Compilation
Python	3.7+	Required	Analysis scripts
Git	Any	Required	Version control
SageMath	9.0+	Optional	Dynamic security analysis
RAM	16GB	Recommended	Smooth execution
📦 Complete Setup Process
bash
# 1. Clone the repository (if not already done)
git clone <your-repository-url> kyber-tweaks
cd kyber-tweaks

# 2. Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install numpy matplotlib pandas tabulate

# 3. Clone Kyber reference implementation
git clone https://github.com/pq-crystals/kyber
cd kyber && git checkout round3 && cd ..

# 4. Apply modifications and copy configuration files
# (This is automated in the actual setup)
cp -r configs kyber/ref/
# Apply poly.c, polyvec.c, cbd.c modifications

# 5. Optional: Install SageMath for dynamic security analysis
# Option A: Using APT
sudo apt update && sudo apt install sagemath

# Option B: Using Conda (recommended)
conda create -n sage_env sage python=3.9
conda activate sage_env

# 6. Make the demo script executable
chmod +x final_demo.sh

# 7. Run initial setup verification
./final_demo.sh --help
🎮 Using the Demo Script
Interactive Mode (Recommended for First Time)
bash
./final_demo.sh
This presents a menu:

text
Select components to run:
1) Run everything (recommended)
2) Performance benchmarks only
3) Correctness tests only  
4) Security analysis only
5) Generate summary from existing results
6) Quick demo (subset of tests)
7) Exit

Enter choice [1-7]: 
Automatic Mode (Full Execution)
bash
./final_demo.sh --auto
Runs all components automatically:

Performance Benchmarks (~10-15 minutes)
Correctness Tests (~2-3 minutes)
Security Analysis (~1-2 minutes)
Report Generation (~30 seconds)
Quick Demo Mode
For a rapid demonstration (~2 minutes):

bash
./final_demo.sh
# Then select option 6
📊 Generated Outputs
After running the demo, you'll find:

Output	Location	Description
Summary Report	thesis_results_TIMESTAMP.txt	Complete results matching thesis tables
Performance HTML	benchmarks/results/run_*/report/benchmark_report.html	Interactive performance report
Security Plots	kyber-security-analysis/results/plots/	Security comparison visualizations
Demo Log	demo_TIMESTAMP.log	Complete execution log
🔧 Core Implementation Details
Parameter Configurations
Test	(du, dv)	η1, η2	Ciphertext Size	Purpose
Baseline	(10, 4)	(3,2)/(2,2)	768/1088/1568	NIST standard
Test 1	(10, 4)	Standard	No change	Verification
Test 2	(11, 3)	Standard	-32 bytes	Size optimized
Test 3	(9, 5)	Standard	+32 bytes	Max compression
Test 4 | Standard | Increased | No change | Security margin |

### Modified Source Files

#### poly.c - Polynomial Compression
```c
// Added support for multiple compression sizes
if(KYBER_POLYCOMPRESSEDBYTES == 96) {
    // (du=11, dv=3) compression
} else if(KYBER_POLYCOMPRESSEDBYTES == 128) {
    // Standard (du=10, dv=4)
} else if(KYBER_POLYCOMPRESSEDBYTES == 160) {
    // (du=9, dv=5) or special cases
} else if(KYBER_POLYCOMPRESSEDBYTES == 192) {
    // Special Kyber1024 cases
} else if(KYBER_POLYCOMPRESSEDBYTES == 200) {
    // Kyber1024 (du=11, dv=5)
}
cbd.c - Noise Sampling
c
// Extended CBD sampling for η=4 and η=5
void cbd4(poly *r, const uint8_t buf[4*KYBER_N/8]);
void cbd5(poly *r, const uint8_t buf[5*KYBER_N/8]);
📚 Component Documentation
1. Performance Benchmarking (benchmarks/)
Purpose: Measure cycle counts for all operations across parameter variations

Key Scripts:

run_cycle_counts.sh: Executes 10,000 iterations per operation
analyze_results.py: Generates Tables 5.1-5.4 from thesis
generate_charts.py: Creates performance comparison visualizations
Usage Example:

bash
cd benchmarks
./run_cycle_counts.sh
python3 analyze_results.py | grep -A20 "Table 5.1"
Output Format:

text
Table 5.1: Performance analysis of Kyber512 for different (du, dv) values
================================================================================
Operation                 | (du, dv) = (10, 4)  | (du, dv) = (11, 3)  | (du, dv) = (9, 5)   
                         | Median   Average   | Median   Average   | Median   Average   
--------------------------------------------------------------------------------
poly_compress            | 438      459       | 638      679       | 878      1045     
poly_decompress          | 146      141       | 486      594       | 582      668      
indcpa_keypair          | 90868    92608     | 91738    94025     | 95892    99896    
2. CLI Testing Tools (cli-tests/)
Purpose: Verify correctness of encryption/decryption for all parameter sets

Key Tools:

kyber_keygen: Generate keypairs with current parameters
kyber_encrypt: Encrypt and output ciphertext
kyber_decrypt: Decrypt and verify shared secrets
kyber_demo: Interactive demonstration
Test All Configurations:

bash
cd cli-tests
./scripts/test_all_params.sh
Compare Sizes:

bash
./scripts/compare_sizes.sh
Output:

text
Config       Compression     PK Size    SK Size    CT Size    CT Reduction
------------------------------------------------------------------------
Baseline     (10, 4)         800        1632       768        0.0%
Test2        (11, 3)         800        1632       736        -4.2%
Test3        (9, 5)          800        1632       800        +4.2%
3. Security Analysis
Static Analysis (kyber-security-analysis/)
Purpose: Generate security tables using thesis values

Key Scripts:

kyber_security_analysis.py: Generates Tables 5.5-5.8
Kyber.py: Test individual parameter sets
Usage:

bash
cd kyber-security-analysis
./run_all_analysis.sh
Output Example (Table 5.5):

text
+------------------------------------------+---------------+-----+-----+-----+--------------+--------------+---+---+
|                                          |               | d   | b   | m   | Core-SVP     | Core-SVP     | δ | C |
|                                          |               |     |     |     | (classical)  | (quantum)    |   |   |
+==========================================+===============+=====+=====+=====+==============+==============+===+===+
| (du = 10, dv = 4) 2^-161 (800, 768)    | Primal Attack | 999 | 406 | 486 | 118          | 107          |   |   |
+------------------------------------------+---------------+-----+-----+-----+--------------+--------------+---+---+
|                                          | Dual Attack   | 1024| 403 | 512 | 117          | 106          |   |   |
+------------------------------------------+---------------+-----+-----+-----+--------------+--------------+---+---+
Dynamic Analysis (kyber-dynamic-security-analysis/)
Purpose: Calculate actual security using lattice estimator

Requirements: SageMath installation

Key Components:

dynamic_analyzer.py: Python interface to SageMath
kyber_estimator.sage: SageMath security calculations
Note: Dynamic analysis shows ~25-30 bits higher security due to updated algorithms

📈 Results and Analysis
Performance Impact Summary
1. Compression Parameters (du, dv)
Parameter Set	poly_compress Impact	Overall Performance	Recommendation
(11, 3)	+50% cycles	+2-5% total	✅ Best for size optimization
(9, 5)	+100% cycles	+10-15% total	❌ Too much overhead
2. Noise Parameters (η1, η2)
Variant	Configuration Change	KeyGen Impact	Encryption Impact
Kyber512	η1: 3→5, η2: 2→3	+32%	+34%
Kyber768	η1: 2→4, η2: 2→4	+11%	+8%
Kyber1024	η1: 2→4, η2: 2→4	+5%	+3%
3. Special Kyber1024 Configurations
(11, 5): Uses unique 200-byte encoding
(10, 6): Shows -5% KeyGen improvement
(12, 4): Mixed results, variant-dependent
Verification Results
✅ All tests pass:

text
baseline_standard: PASSED
test1_du10_dv4: PASSED
test2_du11_dv3: PASSED
test3_du9_dv5: PASSED
test4_eta_variations: PASSED
kyber1024_special_*: PASSED
🔧 Troubleshooting
Common Issues and Solutions
1. Build Errors
Problem: KYBER_POLYCOMPRESSEDBYTES needs to be in {96, 128, 160, 192, 200}

Solution: Ensure poly.c has all compression cases:

bash
grep "KYBER_POLYCOMPRESSEDBYTES ==" kyber/ref/poly.c
2. SageMath Not Found
Problem: sage not found but installed via conda

Solution: Activate conda environment first:

bash
conda activate sage_env
./final_demo.sh
3. Missing Python Modules
Problem: ModuleNotFoundError: No module named 'tabulate'

Solution:

bash
pip install numpy matplotlib pandas tabulate
4. Permission Denied
Problem: Permission denied: ./final_demo.sh

Solution:

bash
chmod +x final_demo.sh
chmod +x benchmarks/*.sh
chmod +x cli-tests/scripts/*.sh
Verification Commands
bash
# Check all config files present
ls kyber/ref/configs/params_*.h | wc -l  # Should be 8-9

# Verify modifications in place
grep -c "KYBER_POLYCOMPRESSEDBYTES == 96" kyber/ref/poly.c  # Should be ≥1
grep -c "cbd4" kyber/ref/cbd.c  # Should be ≥1

# Test individual component
cd benchmarks && ./quick_bench.sh --test 2
🚀 Advanced Usage
Custom Parameter Testing
Create custom configuration:

bash
cat > kyber/ref/configs/params_custom.h << EOF
#ifndef PARAMS_H
#define PARAMS_H

#define KYBER_K 2
#define KYBER_N 256
#define KYBER_Q 3329
#define KYBER_ETA1 4
#define KYBER_ETA2 3
#define KYBER_DU 10
#define KYBER_DV 5
// ... rest of parameters
EOF
Test custom configuration:

bash
cd benchmarks
./run_cycle_counts.sh  # Will automatically pick up new config
Batch Analysis

for du in 9 10 11 12; do
    for dv in 3 4 5 6; do
        echo "Testing du=$du, dv=$dv"
        # Create config file
        sed "s/KYBER_DU .*/KYBER_DU $du/" params_baseline_standard.h > params_test_du${du}_dv${dv}.h
        sed -i "s/KYBER_DV .*/KYBER_DV $dv/" params_test_du${du}_dv${dv}.h
        # Run test
        ./quick_bench.sh --test custom
    done
done

Generate Publication-Ready Results
bash
# Complete workflow for paper submission
cd benchmarks
./run_cycle_counts.sh
python3 analyze_results.py > ../thesis_tables.txt
python3 statistical_analysis.py > ../statistical_results.txt
./generate_report.sh

# Extract specific metrics
python3 -c "
import json
with open('results/run_*/analysis_data.json') as f:
    data = json.load(f)
    # Extract specific comparisons
"
Performance Profiling
bash
# Profile specific operations
cd kyber/ref
perf record ./test_speed512
perf report

# Memory analysis
valgrind --tool=massif ./test_speed512
ms_print massif.out.*
📊 Reproducing Thesis Results
To exactly reproduce the results from Chapter 5:

Step 1: Run Complete Analysis
bash
./final_demo.sh --auto
Step 2: Extract Thesis Tables
bash
# Performance tables (5.1-5.4)
grep -A 30 "Table 5" benchmarks/results/run_*/analysis_report.txt

# Security tables (5.5-5.8)
cat kyber-security-analysis/results/security_analysis_results.txt
Step 3: Generate Figures
bash
# Performance comparison charts
cd benchmarks
python3 generate_charts.py

# Security visualization
cd ../kyber-security-analysis
python3 scripts/visualize_results.py
Step 4: Verify Results
The results should match:

Table 5.1-5.3: Compression parameter performance impact
Table 5.4: Eta parameter performance impact
Table 5.5-5.7: Security analysis for different du,dv
Table 5.8: Security analysis for eta variations
📝 Implementation Notes
Key Insights
Compression Trade-off: The (du=11, dv=3) configuration provides the best balance between size reduction and performance impact.

Security Margins: All parameter variations maintain the required security levels, with dynamic analysis showing even higher security than static estimates.

Noise Parameters: Increasing η provides additional security margin but at significant performance cost.

Platform Dependency: Results may vary slightly based on CPU architecture and compiler optimizations.

Design Decisions
Modular Structure: Each component (benchmarking, CLI, security) is independent
Automated Testing: All configurations are tested automatically
Reproducibility: Fixed random seeds and deterministic measurements
Extensibility: Easy to add new parameter configurations
🤝 Contributing
To add new parameter configurations:

Create new config file in kyber/ref/configs/
Add test case to run_cycle_counts.sh
Update test_all_params.sh for correctness testing
Add security parameters to analysis scripts
📚 References
Kyber Specification: https://pq-crystals.org/kyber/
NIST PQC: https://csrc.nist.gov/projects/post-quantum-cryptography
Lattice Estimator: https://github.com/malb/lattice-estimator
SageMath: https://www.sagemath.org/
📄 License
This project is for academic research purposes. Please refer to the original Kyber implementation license for base code usage.

🙏 Acknowledgments
Kyber development team for the reference implementation
Lattice estimator authors for security analysis tools
Thesis advisors and reviewers for guidance
📧 Contact
For questions or issues:

Open an issue in the repository
Refer to the thesis document for theoretical background
Check the troubleshooting section first
🎯 Quick Reference Card
bash
# Most common commands
./final_demo.sh              # Interactive mode
./final_demo.sh --auto       # Run everything
./final_demo.sh --help       # Show options

# Individual components
cd benchmarks && ./run_cycle_counts.sh         # Performance only
cd cli-tests && ./scripts/test_all_params.sh   # Correctness only
cd kyber-security-analysis && ./run_all_analysis.sh  # Security only

# Quick tests
cd benchmarks && ./quick_bench.sh --test 2     # Test specific config
cd cli-tests && ./kyber_demo -q                # Quick demo

# Results location
less thesis_results_*.txt                       # Summary report
firefox benchmarks/results/run_*/report/benchmark_report.html  # HTML report