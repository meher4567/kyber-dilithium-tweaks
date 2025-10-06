markdown

# Complete Fedora Setup and Execution Guide
Step-by-step instructions for running Kyber benchmarks and security analysis

---

## PART 1: INITIAL SETUP (Do Once)

### Step 1: Install System Dependencies
```bash
sudo dnf install gcc make python3 python3-pip git openssl-devel

Step 2: Transfer Project to Fedora

bash

# From your Windows machine, copy the entire kyber folder to Fedora
# Use scp, USB drive, or your preferred method
# Example using scp:
scp -r kyber/ user@fedora-machine:/home/user/

Step 3: Navigate to Project

bash

cd ~/kyber

Step 4: Install Python Dependencies

bash

pip3 install --user -r requirements.txt

Step 5: Make Scripts Executable

bash

chmod +x switch_config.sh
chmod +x benchmark_all.sh
chmod +x compare_results.sh
chmod +x analyze_results.py
chmod +x generate_graphs.py
chmod +x generate_tables.py
chmod +x create_dashboard.py
chmod +x run_security.sh
chmod +x security_analysis.py

Step 6: Install Lattice Estimator (for security analysis)

bash

cd ~
git clone https://github.com/malb/lattice-estimator
cd lattice-estimator
pip3 install --user -r requirements.txt
cd ~/kyber

Setup Complete!
PART 2: PERFORMANCE BENCHMARKING
Step 1: Test Single Configuration

bash

# Switch to config 1
./switch_config.sh 1

# Build
make clean
make

# Test it works
./test_speed1024

Expected output: Cycle counts for various operations
Step 2: Run All Benchmarks (Automated)

bash

./benchmark_all.sh

What happens:

    Switches through all 4 configs
    Builds each one
    Runs benchmarks for 512, 768, 1024
    Saves results in benchmark_results/run_YYYYMMDD_HHMMSS/

Time: 20-40 minutes
Step 3: Generate Graphs

bash

# Find your results directory
ls benchmark_results/

# Generate graphs (replace with your actual directory)
python3 generate_graphs.py benchmark_results/run_20240315_120000/

Output: PNG graphs in benchmark_results/run_XXXXXX/graphs/
Step 4: Generate LaTeX Tables

bash

python3 generate_tables.py benchmark_results/run_20240315_120000/

Output: LaTeX tables in benchmark_results/run_XXXXXX/latex_tables/
Step 5: Generate HTML Dashboard

bash

python3 create_dashboard.py benchmark_results/run_20240315_120000/

Output: benchmark_results/run_XXXXXX/dashboard.html

View in browser:

bash

firefox benchmark_results/run_20240315_120000/dashboard.html

Step 6: Quick Comparison

bash

./compare_results.sh benchmark_results/run_20240315_120000/

Output: Terminal summary of all results
PART 3: SECURITY ANALYSIS
Step 1: Run Security Analysis

bash

./run_security.sh --auto

What happens:

    Analyzes all 4 configs × 3 security levels
    Uses lattice-estimator
    Generates security tables

Time: 10-30 minutes

Output:

    security_results/security_report.txt
    security_results/security_tables.tex
    security_results/estimator_logs/

Step 2: View Security Results

bash

cat security_results/security_report.txt

Step 3: Check Specific Analysis

bash

# View log for config 1, Kyber1024
cat security_results/estimator_logs/config1_kyber1024.txt

PART 4: COLLECT ALL RESULTS
Directory Structure After Everything

text

kyber/
├── benchmark_results/
│   └── run_20240315_120000/
│       ├── graphs/                  ← PNG graphs
│       ├── latex_tables/            ← LaTeX tables
│       ├── dashboard.html           ← Interactive view
│       └── config1,2,3,4/           ← Raw results
└── security_results/
    ├── security_report.txt          ← Security summary
    ├── security_tables.tex          ← LaTeX tables
    └── estimator_logs/              ← Detailed logs

Copy Results to Windows

bash

# From Fedora, package everything
cd ~
tar -czf kyber_results.tar.gz kyber/benchmark_results kyber/security_results

# Transfer back to Windows
# Use scp, USB, or your method

QUICK REFERENCE COMMANDS
Performance Only

bash

./benchmark_all.sh
python3 generate_graphs.py benchmark_results/run_XXXXXX/
python3 generate_tables.py benchmark_results/run_XXXXXX/
python3 create_dashboard.py benchmark_results/run_XXXXXX/

Security Only

bash

./run_security.sh --auto
cat security_results/security_report.txt

Single Config Test

bash

./switch_config.sh 2
make clean && make
./test_speed1024

Clean Everything

bash

make clean
rm -rf benchmark_results
rm -rf security_results

TROUBLESHOOTING
Build fails

Check: GCC installed? Run gcc --version
Fix: sudo dnf install gcc make
Python script fails

Check: Dependencies installed?
Fix: pip3 install --user numpy matplotlib
Lattice estimator not found

Check: Is it cloned?
Fix:

bash

cd ~
git clone https://github.com/malb/lattice-estimator
cd lattice-estimator
pip3 install --user -r requirements.txt

Benchmark takes too long

Normal: Full benchmark takes 20-40 minutes
Quick test: Run single config only
Permission denied

Fix: chmod +x scriptname.sh
TIMING ESTIMATES
Task	Time
Initial setup	10-15 min
Full benchmark	20-40 min
Security analysis	10-30 min
Generate graphs	2-5 min
Total (first run)	1-1.5 hours

To run the demo:
chmod +x demo.sh
./demo.sh



END OF GUIDE

text




---


## ✅ **That's It - Clean and Complete!**
