#!/bin/bash
# demo.sh
# Complete one-command demonstration of Dilithium tweaks

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
SRC_DIR="${PROJECT_ROOT}/src"
RESULTS_DIR="${PROJECT_ROOT}/results"

# Demo parameters
QUICK_MODE=false
ITERATIONS=1000

# Functions
print_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                    ║"
    echo "║               DILITHIUM TWEAKS - COMPLETE DEMONSTRATION            ║"
    echo "║                                                                    ║"
    echo "║          Post-Quantum Digital Signature Optimization Study         ║"
    echo "║                                                                    ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_section() {
    echo ""
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}  $1${NC}"
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
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

pause_for_effect() {
    if [ "$QUICK_MODE" = false ]; then
        sleep 2
    fi
}

press_enter() {
    if [ "$QUICK_MODE" = false ]; then
        echo ""
        echo -e "${YELLOW}Press ENTER to continue...${NC}"
        read -r
    fi
}

# Check dependencies
check_dependencies() {
    print_section "Checking Dependencies"
    
    local all_good=true
    
    # Check gcc
    if command -v gcc &> /dev/null; then
        print_success "gcc found: $(gcc --version | head -n1)"
    else
        print_error "gcc not found"
        all_good=false
    fi
    
    # Check Python3
    if command -v python3 &> /dev/null; then
        print_success "python3 found: $(python3 --version)"
    else
        print_error "python3 not found"
        all_good=false
    fi
    
    # Check OpenSSL
    if ldconfig -p 2>/dev/null | grep -q libcrypto; then
        print_success "OpenSSL found"
    else
        print_warning "OpenSSL not found - Config 2 may not compile"
    fi
    
    # Check Python packages
    if python3 -c "import matplotlib" 2>/dev/null; then
        print_success "matplotlib found"
    else
        print_warning "matplotlib not found - install with: pip3 install matplotlib"
    fi
    
    if [ "$all_good" = false ]; then
        print_error "Missing required dependencies"
        exit 1
    fi
    
    pause_for_effect
}

# Introduction
show_introduction() {
    print_section "Project Introduction"
    
    echo -e "${CYAN}This demonstration showcases three optimization tweaks to Dilithium:${NC}"
    echo ""
    echo -e "${GREEN}1. Tweak 1: SHA3-256 Challenge Generation${NC}"
    echo "   - Replaces SHAKE256 with SHA3-256"
    echo "   - Fixed-length output for improved efficiency"
    echo "   - Expected: Faster signing"
    echo ""
    echo -e "${GREEN}2. Tweak 2: Modified Challenge Bounds${NC}"
    echo "   - TAU: 39 → 50 (challenge weight)"
    echo "   - OMEGA: 80 → 70 (hint weight)"
    echo "   - Expected: Trade-off between speed and security"
    echo ""
    echo -e "${GREEN}3. Tweak 3: Relaxed Rejection Sampling${NC}"
    echo "   - BETA: 78 → 100 (rejection bound)"
    echo "   - Expected: Significantly faster signing"
    echo ""
    
    print_info "Each configuration will be:"
    echo "  ✓ Compiled from source"
    echo "  ✓ Benchmarked with ${ITERATIONS} iterations"
    echo "  ✓ Compared against baseline"
    echo "  ✓ Visualized in graphs and tables"
    echo ""
    
    press_enter
}

# Show project structure
show_structure() {
    print_section "Project Structure"
    
    echo -e "${CYAN}Project Organization:${NC}"
    echo ""
    tree -L 2 -I '__pycache__|*.pyc' "${PROJECT_ROOT}" 2>/dev/null || {
        find "${PROJECT_ROOT}" -maxdepth 2 -type d | sed 's|[^/]*/|  |g'
    }
    echo ""
    
    print_info "Key Components:"
    echo "  • src/           - Dilithium source code with modifications"
    echo "  • configs/       - Configuration definitions (4 variants)"
    echo "  • tests/         - Benchmark programs"
    echo "  • scripts/       - Automation tools"
    echo "  • results/       - Benchmark outputs"
    echo ""
    
    pause_for_effect
}

# Build and benchmark all configs
run_benchmarks() {
    print_section "Running Benchmarks"
    
    print_step "Starting automated benchmarking..."
    print_info "This will take approximately 5-10 minutes"
    echo ""
    
    if [ "$QUICK_MODE" = true ]; then
        print_warning "Quick mode: Using reduced iterations"
        ./benchmark_all.sh -i "$ITERATIONS"
    else
        ./benchmark_all.sh -i "$ITERATIONS"
    fi
    
    if [ $? -eq 0 ]; then
        print_success "Benchmarking completed successfully!"
    else
        print_error "Benchmarking failed"
        exit 1
    fi
    
    pause_for_effect
}

# Analyze results
analyze_results() {
    print_section "Analyzing Results"
    
    # Find latest results directory
    LATEST_RESULTS=$(ls -td "${RESULTS_DIR}"/run_* 2>/dev/null | head -n1)
    
    if [ -z "$LATEST_RESULTS" ]; then
        print_error "No results found"
        exit 1
    fi
    
    print_info "Results directory: $(basename "$LATEST_RESULTS")"
    echo ""
    
    # Run analysis
    print_step "Running statistical analysis..."
    python3 analyze_results.py "$LATEST_RESULTS"
    
    if [ $? -eq 0 ]; then
        print_success "Analysis completed!"
    else
        print_error "Analysis failed"
        exit 1
    fi
    
    pause_for_effect
    press_enter
}

# Generate visualizations
generate_visualizations() {
    print_section "Generating Visualizations"
    
    LATEST_RESULTS=$(ls -td "${RESULTS_DIR}"/run_* 2>/dev/null | head -n1)
    
    # Generate graphs
    print_step "Creating performance graphs..."
    python3 generate_graphs.py "$LATEST_RESULTS"
    
    if [ $? -eq 0 ]; then
        print_success "Graphs generated!"
    else
        print_warning "Graph generation failed (matplotlib may be missing)"
    fi
    
    pause_for_effect
    
    # Generate tables
    print_step "Creating LaTeX tables..."
    python3 generate_tables.py "$LATEST_RESULTS"
    
    if [ $? -eq 0 ]; then
        print_success "LaTeX tables generated!"
    else
        print_warning "Table generation failed"
    fi
    
    pause_for_effect
    
    # Create dashboard
    print_step "Building interactive dashboard..."
    python3 create_dashboard.py "$LATEST_RESULTS"
    
    if [ $? -eq 0 ]; then
        print_success "Dashboard created!"
    else
        print_warning "Dashboard creation failed"
    fi
    
    pause_for_effect
}

# Show quick comparison
show_quick_comparison() {
    print_section "Quick Results Preview"
    
    LATEST_RESULTS=$(ls -td "${RESULTS_DIR}"/run_* 2>/dev/null | head -n1)
    
    if [ -f "$LATEST_RESULTS/SUMMARY.txt" ]; then
        cat "$LATEST_RESULTS/SUMMARY.txt"
    else
        print_warning "Summary not found"
    fi
    
    echo ""
    press_enter
}

# Show detailed comparison
show_detailed_comparison() {
    print_section "Detailed Performance Comparison"
    
    LATEST_RESULTS=$(ls -td "${RESULTS_DIR}"/run_* 2>/dev/null | head -n1)
    
    ./compare_results.sh "$LATEST_RESULTS"
    
    echo ""
    press_enter
}

# Open dashboard
open_dashboard() {
    print_section "Opening Interactive Dashboard"
    
    LATEST_RESULTS=$(ls -td "${RESULTS_DIR}"/run_* 2>/dev/null | head -n1)
    DASHBOARD="$LATEST_RESULTS/dashboard.html"
    
    if [ -f "$DASHBOARD" ]; then
        print_info "Dashboard location: $DASHBOARD"
        echo ""
        
        # Try to open in browser
        if command -v xdg-open &> /dev/null; then
            print_step "Opening in default browser..."
            xdg-open "$DASHBOARD" 2>/dev/null &
        elif command -v firefox &> /dev/null; then
            print_step "Opening in Firefox..."
            firefox "$DASHBOARD" 2>/dev/null &
        elif command -v google-chrome &> /dev/null; then
            print_step "Opening in Chrome..."
            google-chrome "$DASHBOARD" 2>/dev/null &
        else
            print_warning "Cannot auto-open browser. Manually open:"
            echo "  $DASHBOARD"
        fi
        
        print_success "Dashboard ready!"
    else
        print_error "Dashboard not found"
    fi
    
    pause_for_effect
}

# Show output files
show_outputs() {
    print_section "Generated Output Files"
    
    LATEST_RESULTS=$(ls -td "${RESULTS_DIR}"/run_* 2>/dev/null | head -n1)
    
    echo -e "${CYAN}Results Directory:${NC} $(basename "$LATEST_RESULTS")"
    echo ""
    
    echo -e "${GREEN}Benchmark Data:${NC}"
    ls -lh "$LATEST_RESULTS"/*.txt 2>/dev/null | awk '{print "  " $9, "(" $5 ")"}'
    echo ""
    
    if [ -d "$LATEST_RESULTS/graphs" ]; then
        echo -e "${GREEN}Visualizations:${NC}"
        ls -lh "$LATEST_RESULTS/graphs"/*.png 2>/dev/null | awk '{print "  " $9, "(" $5 ")"}'
        echo ""
    fi
    
    if [ -d "$LATEST_RESULTS/tables" ]; then
        echo -e "${GREEN}LaTeX Tables:${NC}"
        ls -lh "$LATEST_RESULTS/tables"/*.tex 2>/dev/null | awk '{print "  " $9, "(" $5 ")"}'
        echo ""
    fi
    
    if [ -f "$LATEST_RESULTS/dashboard.html" ]; then
        echo -e "${GREEN}Dashboard:${NC}"
        ls -lh "$LATEST_RESULTS/dashboard.html" | awk '{print "  " $9, "(" $5 ")"}'
        echo ""
    fi
    
    press_enter
}

# Final summary
show_summary() {
    print_section "Demonstration Complete!"
    
    LATEST_RESULTS=$(ls -td "${RESULTS_DIR}"/run_* 2>/dev/null | head -n1)
    
    echo -e "${GREEN}✓ Benchmarking complete${NC}"
    echo -e "${GREEN}✓ Statistical analysis complete${NC}"
    echo -e "${GREEN}✓ Visualizations generated${NC}"
    echo -e "${GREEN}✓ Dashboard created${NC}"
    echo ""
    
    echo -e "${CYAN}Key Findings:${NC}"
    if [ -f "$LATEST_RESULTS/ANALYSIS_DETAILED.txt" ]; then
        echo ""
        grep -A 5 "ANALYSIS AND OBSERVATIONS" "$LATEST_RESULTS/ANALYSIS_DETAILED.txt" | tail -n +2 | head -n 10
    fi
    echo ""
    
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "  1. Review dashboard: firefox $LATEST_RESULTS/dashboard.html"
    echo "  2. Read detailed analysis: cat $LATEST_RESULTS/ANALYSIS_DETAILED.txt"
    echo "  3. Use LaTeX tables in thesis: $LATEST_RESULTS/tables/"
    echo "  4. Security validation: ./run_security_analysis.sh"
    echo ""
    
    print_info "All results saved to: $LATEST_RESULTS"
    echo ""
}

# Show usage
show_usage() {
    echo "Usage: ./demo.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -q, --quick          Quick mode (fewer iterations, no pauses)"
    echo "  -i, --iterations N   Number of benchmark iterations (default: 1000)"
    echo "  -h, --help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./demo.sh                    # Full demonstration"
    echo "  ./demo.sh --quick            # Quick demo (faster)"
    echo "  ./demo.sh -i 500             # Custom iterations"
    exit 0
}

# Main function
main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -q|--quick)
                QUICK_MODE=true
                ITERATIONS=100
                shift
                ;;
            -i|--iterations)
                ITERATIONS="$2"
                shift 2
                ;;
            -h|--help)
                show_usage
                ;;
            *)
                echo "Unknown option: $1"
                show_usage
                ;;
        esac
    done
    
    # Start demo
    print_banner
    
    if [ "$QUICK_MODE" = true ]; then
        print_warning "QUICK MODE: Reduced iterations, no pauses"
        echo ""
    fi
    
    check_dependencies
    show_introduction
    show_structure
    run_benchmarks
    show_quick_comparison
    analyze_results
    generate_visualizations
    show_detailed_comparison
    open_dashboard
    show_outputs
    show_summary
    
    echo -e "${GREEN}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║                    DEMONSTRATION SUCCESSFUL!                       ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Run main
main "$@"