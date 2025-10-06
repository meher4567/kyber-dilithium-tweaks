FILE CONTENTS:

markdown

# Dilithium Tweaks - Run Commands Reference

Quick command reference for running benchmarks and generating outputs.

---

## File Organization by Tweak

### Tweak 1: SHA3-256 Challenge (Config 2)
**Source files:**
- `src/challenge_sha3.c`
- `src/challenge_sha3.h`

**Modified files:**
- `src/sign.c` (conditional includes + challenge calls)

**Config:**
- `configs/config2_sha3.h`

---

### Tweak 2: Expanded Challenge Coefficients (Config 3)
**Source files:**
- `src/challenge_expanded.c`
- `src/challenge_expanded.h`

**Modified files:**
- `src/sign.c` (conditional includes + challenge calls)

**Config:**
- `configs/config3_challenge.h`

---

### Tweak 3: Relaxed Rejection Sampling (Config 4)
**Source files:**
- `src/rejection_tweaked.h`

**Modified files:**
- `src/sign.c` (rejection sampling modifications)

**Config:**
- `configs/config4_rejection.h`

---

## Individual Tweak Benchmarking

### Baseline Only
```bash
./benchmark_all.sh -c 1

Tweak 1 Only (SHA3-256)

bash

./benchmark_all.sh -c 2

Tweak 2 Only (Expanded Challenge)

bash

./benchmark_all.sh -c 3

Tweak 3 Only (Relaxed Rejection)

bash

./benchmark_all.sh -c 4

All Tweaks Together
Run All Configurations

bash

./benchmark_all.sh

Quick Test (Fewer Iterations)

bash

./benchmark_all.sh -i 100

Custom Iterations

bash

./benchmark_all.sh -i 500

Manual Build and Run
Config 1 (Baseline)

bash

./switch_config.sh 1
cd src
make clean
make CONFIG=1 test/test_speed2
./test/test_speed2
cd ..

Config 2 (Tweak 1)

bash

./switch_config.sh 2
cd src
make clean
make CONFIG=2 test/test_speed2
./test/test_speed2
cd ..

Config 3 (Tweak 2)

bash

./switch_config.sh 3
cd src
make clean
make CONFIG=3 test/test_speed2
./test/test_speed2
cd ..

Config 4 (Tweak 3)

bash

./switch_config.sh 4
cd src
make clean
make CONFIG=4 test/test_speed2
./test/test_speed2
cd ..

Analysis Commands
Find Latest Results

bash

LATEST=$(ls -td results/run_* | head -n1)
echo $LATEST

Quick Terminal Comparison

bash

./compare_results.sh

Detailed Statistical Analysis

bash

python3 analyze_results.py $LATEST

View Analysis Report

bash

cat $LATEST/ANALYSIS_DETAILED.txt

Visualization Commands
Generate All Graphs

bash

python3 generate_graphs.py $LATEST

View Graphs

bash

ls $LATEST/graphs/*.png
firefox $LATEST/graphs/performance_absolute.png

Generate LaTeX Tables

bash

python3 generate_tables.py $LATEST

View LaTeX Tables

bash

ls $LATEST/tables/*.tex
cat $LATEST/tables/table_simple.tex

Create Interactive Dashboard

bash

python3 create_dashboard.py $LATEST

Open Dashboard

bash

firefox $LATEST/dashboard.html

Complete Pipeline (Step-by-Step)
Step 1: Run Benchmarks

bash

./benchmark_all.sh

Step 2: Set Latest Variable

bash

LATEST=$(ls -td results/run_* | head -n1)

Step 3: Analyze

bash

python3 analyze_results.py $LATEST

Step 4: Generate Graphs

bash

python3 generate_graphs.py $LATEST

Step 5: Generate Tables

bash

python3 generate_tables.py $LATEST

Step 6: Create Dashboard

bash

python3 create_dashboard.py $LATEST

Step 7: View Results

bash

firefox $LATEST/dashboard.html

One-Command Demo
Full Demo (All Steps)

bash

./demo.sh

Quick Demo (Fast)

bash

./demo.sh --quick

Comparison Commands
Compare Baseline vs Tweak 1

bash

./benchmark_all.sh -c 1
./benchmark_all.sh -c 2
./compare_results.sh

Compare Baseline vs Tweak 2

bash

./benchmark_all.sh -c 1
./benchmark_all.sh -c 3
./compare_results.sh

Compare Baseline vs Tweak 3

bash

./benchmark_all.sh -c 1
./benchmark_all.sh -c 4
./compare_results.sh

Compare All Tweaks

bash

./benchmark_all.sh
./compare_results.sh

Specific Output Generation
Only Graphs (No Tables/Dashboard)

bash

LATEST=$(ls -td results/run_* | head -n1)
python3 analyze_results.py $LATEST
python3 generate_graphs.py $LATEST

Only LaTeX Tables (For Thesis)

bash

LATEST=$(ls -td results/run_* | head -n1)
python3 analyze_results.py $LATEST
python3 generate_tables.py $LATEST
ls $LATEST/tables/

Only Dashboard (For Presentation)

bash

LATEST=$(ls -td results/run_* | head -n1)
python3 analyze_results.py $LATEST
python3 create_dashboard.py $LATEST
firefox $LATEST/dashboard.html

Re-running Analysis on Existing Results
If you already have benchmark results and just want new graphs:

bash

# Specify the results directory
RESULT_DIR=results/run_20240115_143022

# Generate graphs
python3 generate_graphs.py $RESULT_DIR

# Generate tables
python3 generate_tables.py $RESULT_DIR

# Create dashboard
python3 create_dashboard.py $RESULT_DIR

Tweak 3 Variants
Default (BETA=100)

bash

# Already configured in Makefile
make CONFIG=4 clean
make CONFIG=4 all

Option 1: Relaxed Bounds (BETA*2)

bash

# Edit src/Makefile, uncomment:
# CFLAGS += -DRELAXED_REJECTION_OPTION1

make CONFIG=4 clean
make CONFIG=4 all

Option 2: Probabilistic Bypass (10%)

bash

# Edit src/Makefile, uncomment:
# CFLAGS += -DRELAXED_REJECTION_OPTION2

make CONFIG=4 clean
make CONFIG=4 all

Cleaning
Clean Build Artifacts

bash

cd src
make clean
cd ..

Clean All Results

bash

rm -rf results/run_*

Clean Everything

bash

cd src
make clean
cd ..
rm -rf results/run_*
rm -rf graphs/*

Quick Reference Summary
Task	Command
Run all tweaks	./benchmark_all.sh
Run specific tweak	./benchmark_all.sh -c [1-4]
Quick comparison	./compare_results.sh
Full analysis	python3 analyze_results.py $LATEST
Make graphs	python3 generate_graphs.py $LATEST
Make tables	python3 generate_tables.py $LATEST
Make dashboard	python3 create_dashboard.py $LATEST
One command demo	./demo.sh
Expected Output Locations

text

results/run_YYYYMMDD_HHMMSS/
├── metadata.txt                    # System info
├── SUMMARY.txt                     # Quick summary
├── ANALYSIS_DETAILED.txt           # Detailed report
├── results.json                    # Machine-readable
├── config1_baseline.txt            # Benchmark data
├── config2_sha3.txt               # Benchmark data
├── config3_challenge.txt          # Benchmark data
├── config4_rejection.txt          # Benchmark data
├── graphs/
│   ├── performance_absolute.png
│   ├── performance_percentage.png
│   └── performance_by_operation.png
├── tables/
│   ├── table_simple.tex
│   ├── table_comparison.tex
│   ├── table_detailed.tex
│   ├── table_parameters.tex
│   └── master_document.tex
└── dashboard.html                  # Interactive dashboard

End of RUN_COMMANDS.md

text


---

## 💾 SAVE THIS FILE

**Create:**

dilithium/RUN_COMMANDS.md

text


---

## ✅ WHAT THIS FILE PROVIDES

- ✅ File organization by tweak
- ✅ Individual tweak commands
- ✅ Manual build commands
- ✅ Analysis commands
- ✅ Visualization commands
- ✅ Complete pipeline
- ✅ Comparison workflows
- ✅ Quick reference table

**No explanations, just commands!** 🎯

---

## 🎉 ABSOLUTELY EVERYTHING IS NOW COMPLETE!

**Total Files: 23 (including this RUN_COMMANDS.md)**

**Ready to execute on Fedora!**