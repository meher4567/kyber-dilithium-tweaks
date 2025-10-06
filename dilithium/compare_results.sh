#!/bin/bash
# compare_results.sh
# Quick comparison of Dilithium benchmark results in terminal

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="${PROJECT_ROOT}/results"

# Functions
print_header() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_metric() {
    local label="$1"
    local value="$2"
    printf "  %-20s %s\n" "$label" "$value"
}

# Extract cycle count from result file
extract_cycles() {
    local file="$1"
    local operation="$2"
    
    if [ ! -f "$file" ]; then
        echo "N/A"
        return
    fi
    
    case "$operation" in
        "keygen")
            grep "keypair" "$file" | awk '{print $2}'
            ;;
        "sign")
            grep "sign" "$file" | grep -v "verify" | awk '{print $2}'
            ;;
        "verify")
            grep "verify" "$file" | awk '{print $2}'
            ;;
        *)
            echo "N/A"
            ;;
    esac
}

# Calculate percentage difference
calc_percentage() {
    local baseline="$1"
    local current="$2"
    
    if [ "$baseline" = "N/A" ] || [ "$current" = "N/A" ]; then
        echo "N/A"
        return
    fi
    
    # Use awk for floating point calculation
    awk -v b="$baseline" -v c="$current" 'BEGIN {
        if (b == 0) {
            print "N/A"
        } else {
            diff = ((c - b) / b) * 100
            printf "%.2f%%", diff
        }
    }'
}

# Format with color based on performance
format_diff() {
    local diff="$1"
    
    if [ "$diff" = "N/A" ]; then
        echo "$diff"
        return
    fi
    
    # Extract numeric value (remove %)
    local numeric=$(echo "$diff" | sed 's/%//')
    
    # Color code: green for negative (faster), red for positive (slower)
    if awk -v n="$numeric" 'BEGIN {exit !(n < -5)}'; then
        echo -e "${GREEN}${diff}${NC} (faster)"
    elif awk -v n="$numeric" 'BEGIN {exit !(n > 5)}'; then
        echo -e "${RED}${diff}${NC} (slower)"
    else
        echo -e "${YELLOW}${diff}${NC} (similar)"
    fi
}

# Show results for a single config
show_config_results() {
    local config_num="$1"
    local config_name="$2"
    local result_file="$3"
    
    echo ""
    echo -e "${MAGENTA}Config ${config_num}: ${config_name}${NC}"
    echo "─────────────────────────────────────"
    
    if [ ! -f "$result_file" ]; then
        print_error "Result file not found: $result_file"
        return
    fi
    
    local keygen=$(extract_cycles "$result_file" "keygen")
    local sign=$(extract_cycles "$result_file" "sign")
    local verify=$(extract_cycles "$result_file" "verify")
    
    print_metric "Key Generation:" "$keygen cycles"
    print_metric "Signing:" "$sign cycles"
    print_metric "Verification:" "$verify cycles"
}

# Compare all configs against baseline
compare_all_configs() {
    local run_dir="$1"
    
    print_header "DILITHIUM CONFIGURATION COMPARISON"
    
    # Check if results exist
    if [ ! -d "$run_dir" ]; then
        print_error "Results directory not found: $run_dir"
        return 1
    fi
    
    # Find result files
    local baseline_file=$(ls "$run_dir"/config1_*.txt 2>/dev/null | head -n1)
    local sha3_file=$(ls "$run_dir"/config2_*.txt 2>/dev/null | head -n1)
    local challenge_file=$(ls "$run_dir"/config3_*.txt 2>/dev/null | head -n1)
    local rejection_file=$(ls "$run_dir"/config4_*.txt 2>/dev/null | head -n1)
    
    if [ -z "$baseline_file" ]; then
        print_error "Baseline results not found in $run_dir"
        return 1
    fi
    
    # Extract baseline values
    local baseline_keygen=$(extract_cycles "$baseline_file" "keygen")
    local baseline_sign=$(extract_cycles "$baseline_file" "sign")
    local baseline_verify=$(extract_cycles "$baseline_file" "verify")
    
    # Show all configs
    show_config_results 1 "Baseline (NIST)" "$baseline_file"
    
    if [ -f "$sha3_file" ]; then
        show_config_results 2 "SHA3-256 Challenge" "$sha3_file"
    fi
    
    if [ -f "$challenge_file" ]; then
        show_config_results 3 "Modified Challenge Bounds" "$challenge_file"
    fi
    
    if [ -f "$rejection_file" ]; then
        show_config_results 4 "Relaxed Rejection Sampling" "$rejection_file"
    fi
    
    # Performance comparison table
    print_header "PERFORMANCE COMPARISON (vs Baseline)"
    
    echo ""
    printf "%-25s %-15s %-15s %-15s\n" "Configuration" "Key Gen" "Signing" "Verification"
    echo "─────────────────────────────────────────────────────────────────────────"
    printf "%-25s %-15s %-15s %-15s\n" "Baseline (Config 1)" "0.00%" "0.00%" "0.00%"
    
    # Config 2: SHA3-256
    if [ -f "$sha3_file" ]; then
        local c2_keygen=$(extract_cycles "$sha3_file" "keygen")
        local c2_sign=$(extract_cycles "$sha3_file" "sign")
        local c2_verify=$(extract_cycles "$sha3_file" "verify")
        
        local diff_keygen=$(calc_percentage "$baseline_keygen" "$c2_keygen")
        local diff_sign=$(calc_percentage "$baseline_sign" "$c2_sign")
        local diff_verify=$(calc_percentage "$baseline_verify" "$c2_verify")
        
        printf "%-25s " "SHA3-256 (Config 2)"
        printf "%-15s " "$(format_diff "$diff_keygen")"
        printf "%-15s " "$(format_diff "$diff_sign")"
        printf "%-15s\n" "$(format_diff "$diff_verify")"
    fi
    
    # Config 3: Challenge Bounds
    if [ -f "$challenge_file" ]; then
        local c3_keygen=$(extract_cycles "$challenge_file" "keygen")
        local c3_sign=$(extract_cycles "$challenge_file" "sign")
        local c3_verify=$(extract_cycles "$challenge_file" "verify")
        
        local diff_keygen=$(calc_percentage "$baseline_keygen" "$c3_keygen")
        local diff_sign=$(calc_percentage "$baseline_sign" "$c3_sign")
        local diff_verify=$(calc_percentage "$baseline_verify" "$c3_verify")
        
        printf "%-25s " "Challenge Bounds (Cfg 3)"
        printf "%-15s " "$(format_diff "$diff_keygen")"
        printf "%-15s " "$(format_diff "$diff_sign")"
        printf "%-15s\n" "$(format_diff "$diff_verify")"
    fi
    
    # Config 4: Rejection Sampling
    if [ -f "$rejection_file" ]; then
        local c4_keygen=$(extract_cycles "$rejection_file" "keygen")
        local c4_sign=$(extract_cycles "$rejection_file" "sign")
        local c4_verify=$(extract_cycles "$rejection_file" "verify")
        
        local diff_keygen=$(calc_percentage "$baseline_keygen" "$c4_keygen")
        local diff_sign=$(calc_percentage "$baseline_sign" "$c4_sign")
        local diff_verify=$(calc_percentage "$baseline_verify" "$c4_verify")
        
        printf "%-25s " "Rejection Samp (Cfg 4)"
        printf "%-15s " "$(format_diff "$diff_keygen")"
        printf "%-15s " "$(format_diff "$diff_sign")"
        printf "%-15s\n" "$(format_diff "$diff_verify")"
    fi
    
    echo ""
    print_info "Note: Negative % = faster (better), Positive % = slower"
}

# Show usage
show_usage() {
    echo "Usage: ./compare_results.sh [results_directory]"
    echo ""
    echo "Compare Dilithium benchmark results across configurations"
    echo ""
    echo "Arguments:"
    echo "  results_directory    Path to results directory (optional)"
    echo "                       If not provided, uses latest in results/"
    echo ""
    echo "Examples:"
    echo "  ./compare_results.sh"
    echo "  ./compare_results.sh results/run_20240115_143022"
    exit 0
}

# Main
main() {
    local run_dir=""
    
    # Parse arguments
    if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        show_usage
    fi
    
    if [ -n "$1" ]; then
        run_dir="$1"
    else
        # Find latest results directory
        run_dir=$(ls -td "${RESULTS_DIR}"/run_* 2>/dev/null | head -n1)
        
        if [ -z "$run_dir" ]; then
            print_error "No results found in ${RESULTS_DIR}"
            echo ""
            echo "Run benchmarks first: ./benchmark_all.sh"
            exit 1
        fi
        
        print_info "Using latest results: $(basename "$run_dir")"
    fi
    
    # Check if directory exists
    if [ ! -d "$run_dir" ]; then
        print_error "Directory not found: $run_dir"
        exit 1
    fi
    
    # Compare results
    compare_all_configs "$run_dir"
    
    echo ""
    print_success "Comparison complete!"
    echo ""
    print_info "For detailed analysis, run:"
    echo "  python3 analyze_results.py $run_dir"
    echo ""
}

# Run main
main "$@"