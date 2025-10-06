FILE CONTENTS:

markdown

# Dilithium Tweaks - Fedora Setup and Execution Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Initial Setup](#initial-setup)
3. [Dependency Installation](#dependency-installation)
4. [Project Setup](#project-setup)
5. [Running Benchmarks](#running-benchmarks)
6. [Analyzing Results](#analyzing-results)
7. [Troubleshooting](#troubleshooting)
8. [Quick Reference](#quick-reference)

---

## System Requirements

### Minimum Requirements
- **OS:** Fedora 36 or later (tested on Fedora 38/39)
- **RAM:** 4GB minimum, 8GB recommended
- **Disk Space:** 2GB free space
- **Processor:** x86_64 architecture with RDTSC support

### Software Requirements
- GCC 11 or later
- Python 3.9 or later
- OpenSSL development libraries
- Git (optional, for version control)

---

## Initial Setup

### 1. Update System

```bash
# Update all packages
sudo dnf update -y

# Reboot if kernel was updated
sudo reboot  # If needed

2. Install Build Essentials

bash

# Install GCC and build tools
sudo dnf groupinstall "Development Tools" -y

# Install additional tools
sudo dnf install -y \
    gcc \
    make \
    git \
    tree \
    vim

3. Install OpenSSL Development Libraries

For SHA3-256 support (Tweak 1):

bash

# Install OpenSSL development packages
sudo dnf install -y openssl-devel

# Verify installation
pkg-config --modversion openssl
# Should show version 3.x or later

4. Install Python and Dependencies

bash

# Install Python 3 and pip
sudo dnf install -y python3 python3-pip

# Verify Python version
python3 --version
# Should be 3.9 or later

# Install Python packages
pip3 install --user matplotlib numpy

# Verify installation
python3 -c "import matplotlib; print('matplotlib OK')"
python3 -c "import numpy; print('numpy OK')"

Project Setup
1. Navigate to Project Directory

bash

cd /path/to/dilithium

Expected structure:

text

dilithium/
├── src/                  # Source code
├── configs/              # Configuration files
├── tests/                # Test programs (created during build)
├── results/              # Benchmark results (auto-created)
├── *.sh                  # Automation scripts
└── *.py                  # Analysis scripts

2. Verify Project Files

bash

# Check that all required files exist
ls -la

# Should see:
# - switch_config.sh
# - benchmark_all.sh
# - compare_results.sh
# - analyze_results.py
# - generate_graphs.py
# - generate_tables.py
# - create_dashboard.py
# - demo.sh

3. Make Scripts Executable

bash

# Make all shell scripts executable
chmod +x *.sh
chmod +x *.py

# Verify permissions
ls -l *.sh
# Should show -rwxr-xr-x

4. Create Required Directories

bash

# These should already exist, but ensure they're present
mkdir -p results graphs docs

Running Benchmarks
Method 1: Complete Demonstration (Recommended for First Run)

One-command full demo:

bash

./demo.sh

What this does:

    Checks all dependencies
    Shows project structure
    Runs benchmarks for all 4 configurations
    Analyzes results statistically
    Generates graphs and tables
    Creates interactive dashboard
    Opens dashboard in browser

Duration: ~10-15 minutes (1000 iterations per config)

Quick demo (faster):

bash

./demo.sh --quick

Duration: ~2-3 minutes (100 iterations per config)
Method 2: Manual Step-by-Step Execution
Step 1: Build and Test Baseline

bash

# Switch to baseline configuration
./switch_config.sh 1

# Build
cd src
make clean
make CONFIG=1 test/test_speed2

# Run quick test
./test/test_speed2

# Return to project root
cd ..

Expected output:

text

keypair:  XXXXX cycles
sign:     XXXXX cycles
verify:   XXXXX cycles

Step 2: Run Complete Benchmarks

Benchmark all configurations:

bash

./benchmark_all.sh

Options:

bash

# Benchmark specific config only
./benchmark_all.sh -c 2

# Custom iterations
./benchmark_all.sh -i 500

# Different Dilithium mode
./benchmark_all.sh -m 3  # Dilithium3

Output location:

text

results/run_YYYYMMDD_HHMMSS/
├── metadata.txt
├── SUMMARY.txt
├── config1_baseline.txt
├── config2_sha3.txt
├── config3_challenge.txt
├── config4_rejection.txt
└── build_config*.log

Step 3: Quick Terminal Comparison

bash

./compare_results.sh

Or specify results directory:

bash

./compare_results.sh results/run_20240115_143022

Expected output:

    Colored table showing all configs
    Percentage differences vs baseline
    Quick performance summary

Step 4: Detailed Analysis

bash

# Find latest results directory
LATEST=$(ls -td results/run_* | head -n1)

# Run statistical analysis
python3 analyze_results.py $LATEST

Generates:

    results.json - Machine-readable results
    ANALYSIS_DETAILED.txt - Comprehensive report

Step 5: Generate Visualizations

Create graphs:

bash

python3 generate_graphs.py $LATEST

Output: results/run_*/graphs/*.png

    performance_absolute.png
    performance_percentage.png
    performance_by_operation.png

Create LaTeX tables:

bash

python3 generate_tables.py $LATEST

Output: results/run_*/tables/*.tex

    Ready to include in thesis

Create interactive dashboard:

bash

python3 create_dashboard.py $LATEST

Output: results/run_*/dashboard.html

Open dashboard:

bash

firefox $LATEST/dashboard.html

Analyzing Results
Understanding the Output
Configuration Performance Comparison

text

Config 1: Baseline
  Key Generation:  XXX,XXX cycles
  Signing:         XXX,XXX cycles
  Verification:    XXX,XXX cycles

Config 2: SHA3-256
  Key Generation:  XXX,XXX cycles (±X.XX%)
  Signing:         XXX,XXX cycles (±X.XX%)
  Verification:    XXX,XXX cycles (±X.XX%)

Color coding in terminal:

    Green (↓): Faster than baseline (good)
    Yellow (≈): Similar to baseline (neutral)
    Red (↑): Slower than baseline (bad)

Key Metrics to Report

    Signing Speed Improvement (Tweak 1 & 4)
        Expected: -5% to -20% (faster)

    Verification Speed (Tweak 3)
        Expected: -2% to -5% (faster with lower OMEGA)

    Challenge Bounds Trade-off (Tweak 2)
        Signing: May be slower (+10% to +20%)
        Verification: Should be faster (-5%)

Troubleshooting
Issue: OpenSSL Not Found

Error:

text

fatal error: openssl/evp.h: No such file or directory

Solution:

bash

sudo dnf install -y openssl-devel
ldconfig -p | grep libcrypto  # Verify

Issue: Python Packages Missing

Error:

text

ModuleNotFoundError: No module named 'matplotlib'

Solution:

bash

pip3 install --user matplotlib numpy
python3 -c "import matplotlib"  # Verify

Issue: Test Binary Not Found

Error:

text

test/test_speed2: No such file or directory

Solution:

bash

cd src
make clean
make CONFIG=1 all
ls -la test/  # Verify binaries exist

Issue: Permission Denied

Error:

text

bash: ./benchmark_all.sh: Permission denied

Solution:

bash

chmod +x *.sh *.py

Issue: Compilation Fails for Config 2

Error:

text

undefined reference to `EVP_sha3_256'

Solution:

bash

# OpenSSL version too old, upgrade:
sudo dnf update openssl-devel

# Or build without Config 2:
./benchmark_all.sh -c 1  # Baseline only
./benchmark_all.sh -c 3  # Skip config 2
./benchmark_all.sh -c 4

Issue: Slow Performance / High Cycles

Possible causes:

    Running in VM (expected to be slower)
    Background processes consuming CPU
    Frequency scaling enabled

Solutions:

bash

# Close unnecessary programs
# Check CPU frequency
cat /proc/cpuinfo | grep MHz

# Disable CPU frequency scaling (if root access)
sudo cpupower frequency-set -g performance

# Check for background processes
top

Issue: Graphs Not Generated

Error:

text

[ERROR] Failed to load JSON: results.json not found

Solution:

bash

# Must run analyze_results.py first
python3 analyze_results.py results/run_20240115_143022

# Then generate graphs
python3 generate_graphs.py results/run_20240115_143022

Quick Reference
Most Common Commands

bash

# Full automated demo
./demo.sh

# Manual benchmarking
./benchmark_all.sh

# Quick comparison
./compare_results.sh

# Full analysis pipeline
LATEST=$(ls -td results/run_* | head -n1)
python3 analyze_results.py $LATEST
python3 generate_graphs.py $LATEST
python3 generate_tables.py $LATEST
python3 create_dashboard.py $LATEST
firefox $LATEST/dashboard.html

File Locations
Item	Location
Source code	src/
Configurations	configs/
Benchmark results	results/run_YYYYMMDD_HHMMSS/
Graphs	results/run_*/graphs/
LaTeX tables	results/run_*/tables/
Dashboard	results/run_*/dashboard.html
Configuration Switching

bash

# Switch to specific config
./switch_config.sh 1  # Baseline
./switch_config.sh 2  # SHA3-256
./switch_config.sh 3  # Challenge bounds
./switch_config.sh 4  # Rejection sampling

# Show current config
./switch_config.sh

# Build after switching
cd src
make clean
make CONFIG=2 all

🎯 VARIANT 1: Default (Simple BETA Increase)

Recommended for most cases

bash

# Build Config 4 with default (BETA=100)
make CONFIG=4 clean
make CONFIG=4 all

Implementation:

    BETA: 78 → 100 (from params_tweaked.h)
    No code changes needed
    Simplest and most predictable

🎯 VARIANT 2: Relaxed Bounds (Option 1)

For maximum signing speed improvement

Edit src/Makefile, uncomment:

makefile

ifeq ($(CONFIG),4)
  CFLAGS += -DRELAXED_REJECTION
  CFLAGS += -DRELAXED_REJECTION_OPTION1  # ← Uncomment this
  ...
endif

Then build:

bash

make CONFIG=4 clean
make CONFIG=4 all

Implementation:

    Uses GAMMA2 - BETA*2 instead of GAMMA2 - BETA
    Most aggressive relaxation
    Fastest signing

🎯 VARIANT 3: Probabilistic Bypass (Option 2)

For signature variability study

Edit src/Makefile, uncomment:

makefile

ifeq ($(CONFIG),4)
  CFLAGS += -DRELAXED_REJECTION
  CFLAGS += -DRELAXED_REJECTION_OPTION2  # ← Uncomment this
  ...
endif

Then build:

bash

make CONFIG=4 clean
make CONFIG=4 all

Implementation:

    10% of rejections bypassed randomly
    Stochastic behavior
    Different signatures for same message


Expected Runtime
Task	Duration
Single config benchmark	~2-3 minutes
All configs benchmark	~10-15 minutes
Analysis	~10 seconds
Graph generation	~5 seconds
Dashboard creation	~2 seconds
Full demo	~15-20 minutes
Quick demo	~3-5 minutes
Next Steps

After successful benchmarking:

    ✅ Review dashboard - Visual overview of results
    ✅ Read detailed analysis - Statistical breakdown
    ✅ Export LaTeX tables - For thesis inclusion
    ✅ Security validation - Run lattice-estimator (separate guide)
    ✅ Prepare presentation - Use graphs and dashboard

Support

Common issues resolved:

    90% of issues are missing dependencies → Install OpenSSL and Python packages
    Compilation errors → Check GCC version (gcc --version)
    Slow performance → Normal in VMs, run on bare metal for accurate results

For additional help:

    Check build logs in results/run_*/build_config*.log
    Verify all scripts are executable (ls -la *.sh)
    Ensure running on Fedora (Ubuntu/Debian have different package names)

Summary

Quickest path to results:

bash

# 1. Install dependencies
sudo dnf install -y gcc make openssl-devel python3-pip
pip3 install --user matplotlib numpy

# 2. Make scripts executable
chmod +x *.sh *.py

# 3. Run demo
./demo.sh

# 4. Open dashboard
firefox results/run_*/dashboard.html

Total time: ~20 minutes including setup