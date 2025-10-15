# Post-Quantum Cryptographic Parameter Optimizations

**License**: MIT | **Platform**: Ubuntu | **Language**: Python

This repository presents implementations and comprehensive analysis of parameter optimizations for two NIST post-quantum cryptographic standards: Kyber (key encapsulation mechanism) and Dilithium (digital signature scheme).

## 📢 Important Setup Note

### SageMath Installation (Required for Dynamic Security Analysis)

The dynamic security analysis component requires SageMath. Since the Miniconda installer is too large (>100MB) to include in the repository, please install it separately:

```bash
# 1. Download Miniconda installer (to any directory)
cd ~  # or any directory you prefer
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 2. Install Miniconda (IMPORTANT: Use default installation path)
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh

# When prompted for installation location, press ENTER to accept default:
# >>> /home/YOUR_USERNAME/miniconda3

# When asked to initialize conda, type 'yes'

# 3. Activate conda (restart terminal or run):
source ~/.bashrc

# 4. Create and activate SageMath environment
conda create -n sage_env sage python=3.9
conda activate sage_env

# 5. Now the demo script will find SageMath automatically
```

> **Note**: Static security analysis works without SageMath. Only dynamic analysis requires it.

## 📋 Table of Contents

- [Overview](#overview)
- [Key Contributions](#key-contributions)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Results Summary](#results-summary)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Performance Results](#performance-results)
- [Security Analysis](#security-analysis)
- [Reproducibility](#reproducibility)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview

This research explores performance-security trade-offs in NIST Round 3 selected post-quantum cryptographic algorithms through systematic parameter modifications. The project demonstrates practical impacts of various optimizations while maintaining required security levels.

### Research Context

As quantum computers threaten current public-key cryptography, NIST has standardized post-quantum algorithms. This work investigates optimization opportunities within the standardized parameter space, providing insights for real-world deployments.

## Key Contributions

### 🔐 Kyber Optimizations
- **Compression Parameter Analysis**: Systematic evaluation of (du, dv) trade-offs
- **Noise Distribution Study**: Impact of η variations on performance and security
- **Size-Performance Trade-offs**: Achieved 4% ciphertext reduction with minimal overhead
- **Comprehensive Benchmarking**: Cycle-accurate measurements across all variants

### 🖊️ Dilithium Modifications
- **SHA3-256 Integration**: Replaced SHAKE256 for challenge generation
- **Expanded Challenge Space**: Coefficients extended from {-1,0,1} to {-2,-1,0,1,2}
- **Modified Rejection Sampling**: Two variants with different performance characteristics
- **Compatibility Analysis**: Full interoperability matrix for all implementations

## Requirements

### System Requirements
- Ubuntu Linux 20.04+ (tested on 24.04 LTS)
- GCC 6.3.0 or higher
- Python 3.7+
- Git
- 16GB RAM recommended

### Python Dependencies

Create a `requirements.txt` file with:

```
numpy>=1.26
matplotlib>=3.8
pandas>=2.1
tabulate>=0.9.0
```

Install with:

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Run complete analysis for both schemes (recommended)
chmod +x run_all_demos.sh
./run_all_demos.sh --auto

# Or run interactive mode for selective analysis
./run_all_demos.sh
Results Summary
🎯 Optimal Configurations
Scheme	Configuration	Impact	Recommendation
Kyber	(du=11, dv=3)	-4% size, +5% time	✅ Best for size-constrained applications
Dilithium	Option 2 (Prob. bypass)	1.4x signing time	✅ Best balance for practical use
📊 Key Metrics
Kyber: Maintains all NIST security levels (1/3/5) across parameter variations
Dilithium: All implementations produce standard 3309-byte signatures
Performance: Benchmarked on Intel Xeon @ 2.8GHz with cycle-accurate measurements
Compatibility: Full compatibility matrix provided for all variants
Project Structure
text
.
├── run_all_demos.sh            # Master demonstration script
├── README.md                   # This file
├── LICENSE                     # License information
│
├── kyber-tweaks/               # Kyber parameter optimizations
│   ├── kyber/ref/              # Modified implementation
│   │   └── configs/            # Parameter configurations
│   ├── benchmarks/             # Performance analysis
│   ├── cli-tests/              # Correctness verification
│   ├── kyber-security-analysis/    # Security validation
│   └── final_demo.sh           # Automated demo script
│
└── dilithium_tweaks/           # Dilithium cryptographic tweaks
    ├── dilithium/              # Modified implementation
    ├── benchmarks/             # Performance benchmarking
    ├── cli-tests/              # Interactive testing
    └── final_demo.sh           # Automated demo script
Installation
System Requirements
OS: Ubuntu Linux 20.04+ (tested on 24.04 LTS)
Compiler: GCC 6.3.0+
Python: 3.7+ with scientific computing packages
Memory: 16GB RAM recommended
Optional: SageMath for advanced security analysis
Setup Instructions
bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev python3-pip git make

# Install Python packages
pip3 install numpy matplotlib pandas tabulate

# Clone and setup
git clone <repository-url>
cd <repository-name>
chmod +x run_all_demos.sh

# Optional: Install SageMath for dynamic security analysis
conda create -n sage_env sage python=3.9
conda activate sage_env
Usage
🚀 Master Script Commands
bash
# Full automated analysis (recommended)
./run_all_demos.sh --auto

# Interactive mode with menu
./run_all_demos.sh

# Individual scheme analysis
./run_all_demos.sh --kyber      # Kyber only
./run_all_demos.sh --dilithium  # Dilithium only

# Show help
./run_all_demos.sh --help
📈 Viewing Results
bash
# After running analysis, view results:

# Kyber performance report
firefox kyber-tweaks/benchmarks/results/run_*/report/benchmark_report.html

# Dilithium comprehensive report
firefox dilithium_tweaks/dilithium_tweaks_final_report.html

# Combined summary
less combined_results_*.txt
Performance Results
Kyber Parameter Impact
Parameter Set	Compression Overhead	Total Impact	Ciphertext Size
Baseline (10,4)	Reference	Reference	768/1088/1568 bytes
Optimized (11,3)	+50%	+5%	736/1056/1536 bytes
High Compress (9,5)	+100%	+15%	800/1120/1600 bytes
Dilithium Timing Analysis
Implementation	Median Signing	95th Percentile	Max Observed
Baseline	6.5ms	7.2ms	8.1ms
Option 1	11.0ms	28.5ms	42.3ms
Option 2	8.7ms	10.2ms	12.8ms
Security Analysis
🛡️ Security Validation
All parameter modifications maintain required NIST security levels:

Kyber512: Level 1 (≥128-bit classical, ≥64-bit quantum)
Kyber768: Level 3 (≥192-bit classical, ≥96-bit quantum)
Kyber1024: Level 5 (≥256-bit classical, ≥128-bit quantum)
🔍 Analysis Methods
Static Analysis: Hardcoded security estimates from literature
Dynamic Analysis: SageMath lattice estimator calculations
Parameter Sensitivity: Impact of (du,dv) and (η1,η2) on security
Comprehensive Validation: All variants verified against security requirements
Reproducibility
All results can be fully reproduced using provided scripts:

bash
# Complete reproduction of all results
./run_all_demos.sh --auto

# Results will be generated in:
# - kyber-tweaks/thesis_results_*.txt
# - dilithium_tweaks/dilithium_tweaks_final_report.html
# - combined_results_*.txt
Benchmarking Environment
CPU: Intel Xeon @ 2.800GHz (TurboBoost disabled)
OS: Ubuntu 24.04 LTS, Linux kernel 6.11.0
Compiler: GCC 6.3.0 with -O3 -fomit-frame-pointer -march=native
Methodology: Median of 10,000 iterations per operation
Citation
If you use this work in your research, please cite:

bibtex
@thesis{pqc_optimizations_2024,
  title={Parameter Optimizations for Post-Quantum Cryptographic Schemes},
  author={[Author Name]},
  year={2024},
  school={[University Name]},
  type={Master's Thesis}
}
License
This project is released under the MIT License. See LICENSE file for details.
The underlying Kyber and Dilithium implementations are in the public domain (CC0).

## Acknowledgments

- **Kyber Team**: Peter Schwabe, Roberto Avanzi, Joppe Bos, Léo Ducas, Eike Kiltz, Tancrède Lepoint, Vadim Lyubashevsky, John M. Schanck, Gregor Seiler, Damien Stehlé
- **Dilithium Team**: Léo Ducas, Eike Kiltz, Tancrède Lepoint, Vadim Lyubashevsky, Peter Schwabe, Gregor Seiler, Damien Stehlé
- **NIST PQC Team**: For the standardization effort
- **Lattice Estimator**: Martin Albrecht and contributors
- **Thesis Advisors**: For guidance and review

## 📧 Contact

For questions, issues, or collaborations:
- Open an issue in this repository
- Refer to the thesis document for theoretical background
- Contact: [your-email@example.com]

## 🔗 Related Resources

- [NIST PQC Standardization](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [Kyber Specification](https://pq-crystals.org/kyber/)
- [Dilithium Specification](https://pq-crystals.org/dilithium/)
- [Lattice Estimator](https://github.com/malb/lattice-estimator)

## 📝 Additional Documentation

Detailed documentation for each component:

- **Kyber Analysis**: See [kyber-tweaks/README.md](kyber-tweaks/README.md)
- **Dilithium Implementation**: See [dilithium_tweaks/README.md](dilithium_tweaks/README.md)
- **Benchmarking Methodology**: See respective `benchmarks/README.md` files
- **Security Analysis Details**: See `kyber-security-analysis/README.md`

## 🎯 Future Work

Potential extensions of this research:
- Hardware implementation analysis
- Side-channel resistance evaluation
- Integration with real-world protocols
- Performance on embedded systems
- Additional parameter space exploration

---

**Note**: This implementation is for research and educational purposes. For production use, please refer to the official NIST-approved implementations with appropriate security reviews.

**Last Updated**: October 2024  
**Version**: 1.0.0  
**Status**: ✅ Complete and Verified