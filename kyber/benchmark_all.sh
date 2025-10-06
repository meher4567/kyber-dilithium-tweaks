#!/bin/bash
# Automated Benchmark Runner for All Kyber Configurations
# Runs all 4 parameter configurations and collects results

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Configuration
RESULTS_BASE_DIR="benchmark_results"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RUN_DIR="$RESULTS_BASE_DIR/run_$TIMESTAMP"
ITERATIONS=10000  # Number of benchmark iterations

# Create results directory structure
mkdir -p "$RUN_DIR"/{config1,config2,config3,config4}

# Log file
LOGFILE="$RUN_DIR/benchmark.log"

# Function to log messages
log_message() {
    echo -e "$1" | tee -a "$LOGFILE"
}

# Function to check if binary exists
check_binary() {
    local binary=$1
    if [ ! -f "$binary" ]; then
        log_message "${RED}✗ Error: $binary not found!${NC}"
        return 1
    fi
    return 0
}

# Function to run a single benchmark
run_single_benchmark() {
    local config=$1
    local level=$2
    local binary=$3
    local output_file="$RUN_DIR/config${config}/${level}_results.txt"
    
    log_message "${BLUE}  → Running $binary...${NC}"
    
    if check_binary "$binary"; then
        # Run benchmark and save output
        ./$binary > "$output_file" 2>&1
        
        if [ $? -eq 0 ]; then
            log_message "${GREEN}    ✓ Complete${NC}"
            return 0
        else
            log_message "${RED}    ✗ Failed${NC}"
            return 1
        fi
    else
        return 1
    fi
}

# Function to build for a specific configuration
build_configuration() {
    local config=$1
    
    log_message "${YELLOW}Building configuration $config...${NC}"
    
    # Clean previous build
    make clean > /dev/null 2>&1
    
    # Build with current configuration
    if make > "$RUN_DIR/config${config}/build.log" 2>&1; then
        log_message "${GREEN}✓ Build successful${NC}"
        return 0
    else
        log_message "${RED}✗ Build failed! Check $RUN_DIR/config${config}/build.log${NC}"
        return 1
    fi
}

# Save system information
save_system_info() {
    local info_file="$RUN_DIR/system_info.txt"
    
    {
        echo "========================================="
        echo "System Information"
        echo "========================================="
        echo ""
        echo "Date: $(date)"
        echo "Hostname: $(hostname)"
        echo ""
        echo "--- CPU Information ---"
        lscpu | grep -E "Model name|CPU$s$|Thread|Core|MHz"
        echo ""
        echo "--- Memory Information ---"
        free -h
        echo ""
        echo "--- OS Information ---"
        cat /etc/os-release | head -5
        uname -a
        echo ""
        echo "--- Compiler Information ---"
        gcc --version | head -1
        make --version | head -1
        echo ""
        echo "========================================="
    } > "$info_file"
}

# Print header
print_header() {
    clear
    log_message "${CYAN}╔════════════════════════════════════════╗${NC}"
    log_message "${CYAN}║   Kyber Performance Benchmark Suite   ║${NC}"
    log_message "${CYAN}║        Automated Test Runner          ║${NC}"
    log_message "${CYAN}╚════════════════════════════════════════╝${NC}"
    log_message ""
    log_message "${YELLOW}📁 Results directory: $RUN_DIR${NC}"
    log_message "${YELLOW}📊 Iterations per test: $ITERATIONS${NC}"
    log_message "${YELLOW}🕐 Started: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
    log_message ""
}

# Main execution
main() {
    print_header
    
    # Save system information
    log_message "${CYAN}Collecting system information...${NC}"
    save_system_info
    log_message "${GREEN}✓ System info saved${NC}"
    log_message ""
    
    # Check if we're in the right directory
    if [ ! -f "switch_config.sh" ]; then
        log_message "${RED}Error: switch_config.sh not found!${NC}"
        log_message "${YELLOW}Make sure you run this from the kyber/ directory${NC}"
        exit 1
    fi
    
    # Make sure switch_config.sh is executable
    chmod +x switch_config.sh
    
    # Total configurations to test
    TOTAL_CONFIGS=4
    CURRENT_CONFIG=0
    
    # Loop through all 4 configurations
    for config in 1 2 3 4; do
        CURRENT_CONFIG=$((CURRENT_CONFIG + 1))
        
        log_message ""
        log_message "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        log_message "${MAGENTA}Configuration $config of $TOTAL_CONFIGS${NC}"
        log_message "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        log_message ""
        
        # Switch to configuration
        log_message "${CYAN}Switching to configuration $config...${NC}"
        ./switch_config.sh $config > "$RUN_DIR/config${config}/switch.log" 2>&1
        
        if [ $? -ne 0 ]; then
            log_message "${RED}✗ Failed to switch configuration${NC}"
            continue
        fi
        
        log_message "${GREEN}✓ Configuration switched${NC}"
        log_message ""
        
        # Build configuration
        if ! build_configuration $config; then
            log_message "${RED}Skipping configuration $config due to build failure${NC}"
            continue
        fi
        
        log_message ""
        
        # Run benchmarks for all security levels
        log_message "${CYAN}Running benchmarks for all security levels...${NC}"
        log_message ""
        
        # Kyber512
        log_message "${BLUE}Kyber512:${NC}"
        run_single_benchmark $config "kyber512" "test_speed512"
        
        # Kyber768
        log_message "${BLUE}Kyber768:${NC}"
        run_single_benchmark $config "kyber768" "test_speed768"
        
        # Kyber1024
        log_message "${BLUE}Kyber1024:${NC}"
        run_single_benchmark $config "kyber1024" "test_speed1024"
        
        log_message ""
        log_message "${GREEN}✅ Configuration $config complete!${NC}"
        
        # Progress indicator
        PROGRESS=$((CURRENT_CONFIG * 100 / TOTAL_CONFIGS))
        log_message "${YELLOW}Overall Progress: $PROGRESS% ($CURRENT_CONFIG/$TOTAL_CONFIGS)${NC}"
    done
    
    # Final summary
    log_message ""
    log_message "${CYAN}╔════════════════════════════════════════╗${NC}"
    log_message "${GREEN}║     All Benchmarks Complete! ✅        ║${NC}"
    log_message "${CYAN}╚════════════════════════════════════════╝${NC}"
    log_message ""
    log_message "${YELLOW}📁 Results saved in: $RUN_DIR${NC}"
    log_message "${YELLOW}🕐 Completed: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
    log_message ""
    log_message "${CYAN}Generated files:${NC}"
    
    # List generated files
    if command -v tree &> /dev/null; then
        tree -L 2 "$RUN_DIR"
    else
        find "$RUN_DIR" -type f | while read file; do
            echo "  $file"
        done
    fi
    
    log_message ""
    log_message "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    log_message "${BLUE}Next Steps:${NC}"
    log_message "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    log_message "  1. Review results in: ${YELLOW}$RUN_DIR${NC}"
    log_message "  2. Run analysis: ${CYAN}./analyze_results.py $RUN_DIR${NC}"
    log_message "  3. Generate comparison: ${CYAN}./compare_results.sh $RUN_DIR${NC}"
    log_message "  4. Check system info: ${CYAN}cat $RUN_DIR/system_info.txt${NC}"
    log_message "  5. View log file: ${CYAN}cat $RUN_DIR/benchmark.log${NC}"
    log_message ""
}

# Trap to handle interruptions
trap 'echo -e "\n${RED}Benchmark interrupted by user${NC}"; exit 130' INT TERM

# Run main function
main

exit 0