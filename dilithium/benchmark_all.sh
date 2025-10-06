#!/bin/bash
# benchmark_all.sh
# Automated benchmarking for all Dilithium configurations

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="${PROJECT_ROOT}/src"
RESULTS_DIR="${PROJECT_ROOT}/results"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RESULTS_SUBDIR="${RESULTS_DIR}/run_${TIMESTAMP}"

# Benchmark parameters
ITERATIONS=1000
DILITHIUM_MODE=2  # Default to Dilithium2

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header() {
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC} $1"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
}

# Function to check dependencies
check_dependencies() {
    print_info "Checking dependencies..."
    
    if [ ! -f "${SRC_DIR}/Makefile" ]; then
        print_error "Makefile not found in ${SRC_DIR}"
        exit 1
    fi
    
    if ! command -v gcc &> /dev/null; then
        print_error "gcc not found. Please install gcc."
        exit 1
    fi
    
    # Check for OpenSSL (needed for Config 2)
    if ! ldconfig -p | grep -q libcrypto; then
        print_warning "OpenSSL (libcrypto) not found. Config 2 may fail."
        print_warning "Install with: sudo dnf install openssl-devel"
    fi
    
    print_success "All dependencies satisfied"
}

# Function to create results directory
setup_results_dir() {
    print_info "Setting up results directory: ${RESULTS_SUBDIR}"
    mkdir -p "${RESULTS_SUBDIR}"
    
    # Create metadata file
    cat > "${RESULTS_SUBDIR}/metadata.txt" << EOF
Dilithium Benchmark Run
=======================
Timestamp: $(date)
Hostname: $(hostname)
OS: $(uname -s) $(uname -r)
Architecture: $(uname -m)
Compiler: $(gcc --version | head -n1)
Iterations: ${ITERATIONS}
Dilithium Mode: ${DILITHIUM_MODE}

Configurations Tested:
  Config 1: Baseline (Original NIST)
  Config 2: Tweak 1 (SHA3-256 Challenge)
  Config 3: Tweak 2 (Modified Challenge Bounds)
  Config 4: Tweak 3 (Relaxed Rejection Sampling)
EOF
    
    print_success "Results directory created"
}

# Function to build configuration
build_config() {
    local config_num=$1
    local config_name=$2
    
    print_header "Building Config ${config_num}: ${config_name}"
    
    cd "${SRC_DIR}" || exit 1
    
    # Clean previous build
    print_info "Cleaning previous build..."
    make clean > /dev/null 2>&1
    
    # Build with selected config
    print_info "Compiling with CONFIG=${config_num}..."
    if make CONFIG="${config_num}" test/test_speed${DILITHIUM_MODE} 2>&1 | tee "${RESULTS_SUBDIR}/build_config${config_num}.log"; then
        print_success "Build successful for Config ${config_num}"
        return 0
    else
        print_error "Build failed for Config ${config_num}"
        print_error "Check log: ${RESULTS_SUBDIR}/build_config${config_num}.log"
        return 1
    fi
}

# Function to run benchmark
run_benchmark() {
    local config_num=$1
    local config_name=$2
    
    print_header "Benchmarking Config ${config_num}: ${config_name}"
    
    cd "${SRC_DIR}" || exit 1
    
    local test_binary="test/test_speed${DILITHIUM_MODE}"
    
    if [ ! -f "${test_binary}" ]; then
        print_error "Test binary not found: ${test_binary}"
        return 1
    fi
    
    local result_file="${RESULTS_SUBDIR}/config${config_num}_${config_name}.txt"
    
    print_info "Running ${ITERATIONS} iterations..."
    print_info "This may take a few minutes..."
    
    # Run benchmark and save output
    if ./"${test_binary}" > "${result_file}" 2>&1; then
        print_success "Benchmark complete for Config ${config_num}"
        
        # Extract and display key metrics
        echo ""
        print_info "Quick Results for Config ${config_num}:"
        
        if grep -q "keypair" "${result_file}"; then
            echo -e "  ${CYAN}Key Generation:${NC} $(grep "keypair" "${result_file}" | awk '{print $2, $3}')"
        fi
        
        if grep -q "sign" "${result_file}"; then
            echo -e "  ${CYAN}Signing:${NC}        $(grep "sign" "${result_file}" | grep -v "verify" | awk '{print $2, $3}')"
        fi
        
        if grep -q "verify" "${result_file}"; then
            echo -e "  ${CYAN}Verification:${NC}   $(grep "verify" "${result_file}" | awk '{print $2, $3}')"
        fi
        
        echo ""
        return 0
    else
        print_error "Benchmark failed for Config ${config_num}"
        return 1
    fi
}

# Function to benchmark single configuration
benchmark_config() {
    local config_num=$1
    local config_name=$2
    
    echo ""
    print_header "Processing Config ${config_num}: ${config_name}"
    
    # Build
    if ! build_config "${config_num}" "${config_name}"; then
        print_warning "Skipping benchmark for Config ${config_num} due to build failure"
        return 1
    fi
    
    # Benchmark
    if ! run_benchmark "${config_num}" "${config_name}"; then
        print_warning "Benchmark failed for Config ${config_num}"
        return 1
    fi
    
    return 0
}

# Function to generate summary
generate_summary() {
    print_header "Generating Summary"
    
    local summary_file="${RESULTS_SUBDIR}/SUMMARY.txt"
    
    cat > "${summary_file}" << EOF
DILITHIUM BENCHMARK SUMMARY
===========================
Generated: $(date)
Results Directory: ${RESULTS_SUBDIR}

Configuration Performance Comparison
------------------------------------

EOF
    
    # Extract results for each config
    for config_num in 1 2 3 4; do
        local config_file="${RESULTS_SUBDIR}/config${config_num}_"*.txt
        
        if ls ${config_file} 1> /dev/null 2>&1; then
            echo "Config ${config_num}:" >> "${summary_file}"
            
            if grep -q "keypair" ${config_file}; then
                echo "  KeyGen:  $(grep "keypair" ${config_file} | awk '{print $2, $3}')" >> "${summary_file}"
            fi
            
            if grep -q "sign" ${config_file}; then
                echo "  Sign:    $(grep "sign" ${config_file} | grep -v "verify" | awk '{print $2, $3}')" >> "${summary_file}"
            fi
            
            if grep -q "verify" ${config_file}; then
                echo "  Verify:  $(grep "verify" ${config_file} | awk '{print $2, $3}')" >> "${summary_file}"
            fi
            
            echo "" >> "${summary_file}"
        fi
    done
    
    # Add relative performance
    cat >> "${summary_file}" << EOF

Relative Performance (vs Baseline Config 1)
-------------------------------------------
(To be calculated by analyze_results.py)

Files Generated
---------------
EOF
    
    ls -1 "${RESULTS_SUBDIR}"/*.txt | xargs -n1 basename >> "${summary_file}"
    
    print_success "Summary generated: ${summary_file}"
    
    # Display summary
    echo ""
    cat "${summary_file}"
}

# Function to show usage
show_usage() {
    echo "Usage: ./benchmark_all.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -c, --config <num>     Benchmark only specific config (1-4)"
    echo "  -i, --iterations <n>   Number of iterations (default: 1000)"
    echo "  -m, --mode <n>         Dilithium mode: 2, 3, or 5 (default: 2)"
    echo "  -h, --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./benchmark_all.sh                    # Benchmark all configs"
    echo "  ./benchmark_all.sh -c 2               # Benchmark only Config 2"
    echo "  ./benchmark_all.sh -i 500             # Run 500 iterations"
    echo "  ./benchmark_all.sh -m 3 -i 1000       # Dilithium3 with 1000 iterations"
    exit 0
}

# Main script
main() {
    local specific_config=""
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -c|--config)
                specific_config="$2"
                shift 2
                ;;
            -i|--iterations)
                ITERATIONS="$2"
                shift 2
                ;;
            -m|--mode)
                DILITHIUM_MODE="$2"
                shift 2
                ;;
            -h|--help)
                show_usage
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                ;;
        esac
    done
    
    # Validate mode
    if [[ ! "$DILITHIUM_MODE" =~ ^[235]$ ]]; then
        print_error "Invalid Dilithium mode: ${DILITHIUM_MODE}"
        print_error "Valid modes: 2, 3, 5"
        exit 1
    fi
    
    # Print banner
    echo ""
    print_header "DILITHIUM AUTOMATED BENCHMARKING"
    echo ""
    print_info "Dilithium Mode: ${DILITHIUM_MODE}"
    print_info "Iterations per config: ${ITERATIONS}"
    echo ""
    
    # Check dependencies
    check_dependencies
    
    # Setup results directory
    setup_results_dir
    
    # Benchmark configurations
    if [ -n "${specific_config}" ]; then
        # Benchmark specific config
        case ${specific_config} in
            1) benchmark_config 1 "baseline" ;;
            2) benchmark_config 2 "sha3" ;;
            3) benchmark_config 3 "challenge" ;;
            4) benchmark_config 4 "rejection" ;;
            *)
                print_error "Invalid config number: ${specific_config}"
                exit 1
                ;;
        esac
    else
        # Benchmark all configs
        local success_count=0
        
        if benchmark_config 1 "baseline"; then ((success_count++)); fi
        if benchmark_config 2 "sha3"; then ((success_count++)); fi
        if benchmark_config 3 "challenge"; then ((success_count++)); fi
        if benchmark_config 4 "rejection"; then ((success_count++)); fi
        
        echo ""
        print_info "Completed ${success_count}/4 configurations"
    fi
    
    # Generate summary
    echo ""
    generate_summary
    
    # Final message
    echo ""
    print_success "Benchmarking complete!"
    print_info "Results saved to: ${RESULTS_SUBDIR}"
    print_info "Next steps:"
    echo "  1. Analyze results: python3 analyze_results.py ${RESULTS_SUBDIR}"
    echo "  2. Generate graphs: python3 generate_graphs.py ${RESULTS_SUBDIR}"
    echo "  3. View summary: cat ${RESULTS_SUBDIR}/SUMMARY.txt"
    echo ""
}

# Run main
main "$@"