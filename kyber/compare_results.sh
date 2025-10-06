#!/bin/bash
# Quick comparison script for Kyber benchmark results
# Provides a fast overview of performance across all configurations

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

# Check arguments
if [ -z "$1" ]; then
    echo -e "${RED}Usage: ./compare_results.sh <results_directory>${NC}"
    echo -e "${YELLOW}Example: ./compare_results.sh benchmark_results/run_20240101_120000${NC}"
    echo ""
    echo -e "${CYAN}This script provides a quick comparison of benchmark results${NC}"
    echo -e "${CYAN}across all 4 configurations for each security level.${NC}"
    exit 1
fi

RESULTS_DIR="$1"

# Validate directory
if [ ! -d "$RESULTS_DIR" ]; then
    echo -e "${RED}Error: Directory '$RESULTS_DIR' not found!${NC}"
    exit 1
fi

# Print header
echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║          Kyber Results Quick Comparison Tool                   ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}📁 Analyzing: $RESULTS_DIR${NC}"
echo ""

# Function to extract key metrics from result file
extract_metrics() {
    local file=$1
    
    if [ ! -f "$file" ]; then
        echo "N/A,N/A,N/A,N/A,N/A,N/A,N/A"
        return
    fi
    
    # Extract various operations (adjust grep patterns based on your actual output format)
    local poly_compress=$(grep -i "poly_compress" "$file" | grep -oE '[0-9]+' | head -1)
    local poly_decompress=$(grep -i "poly_decompress" "$file" | grep -oE '[0-9]+' | head -1)
    local polyvec_compress=$(grep -i "polyvec_compress" "$file" | grep -oE '[0-9]+' | head -1)
    local polyvec_decompress=$(grep -i "polyvec_decompress" "$file" | grep -oE '[0-9]+' | head -1)
    local keypair=$(grep -i "keypair\|indcpa_keypair" "$file" | grep -oE '[0-9]+' | head -1)
    local encaps=$(grep -i "encaps\|indcpa_enc" "$file" | grep -oE '[0-9]+' | head -1)
    local decaps=$(grep -i "decaps\|indcpa_dec" "$file" | grep -oE '[0-9]+' | head -1)
    
    echo "$poly_compress,$poly_decompress,$polyvec_compress,$polyvec_decompress,$keypair,$encaps,$decaps"
}

# Function to calculate percentage difference
calc_percentage() {
    local baseline=$1
    local current=$2
    
    if [ "$baseline" == "N/A" ] || [ "$current" == "N/A" ] || [ "$baseline" -eq 0 ]; then
        echo "N/A"
        return
    fi
    
    local diff=$(( current - baseline ))
    local percent=$(( (diff * 100) / baseline ))
    
    if [ $percent -lt 0 ]; then
        echo -e "${GREEN}${percent}%${NC}"
    elif [ $percent -gt 0 ]; then
        echo -e "${RED}+${percent}%${NC}"
    else
        echo "0%"
    fi
}

# Function to format number with commas
format_number() {
    local num=$1
    if [ "$num" == "N/A" ]; then
        echo "N/A"
    else
        printf "%'d" "$num" 2>/dev/null || echo "$num"
    fi
}

# Compare for each security level
for level in kyber512 kyber768 kyber1024; do
    echo ""
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${BLUE}  $level${NC}"
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Main Operations Table
    echo -e "${BOLD}${CYAN}Main Operations (Cycle Counts):${NC}"
    echo -e "${CYAN}───────────────────────────────────────────────────────────────${NC}"
    printf "${BOLD}%-20s %-15s %-15s %-15s${NC}\n" "Config" "KeyPair" "Encaps" "Decaps"
    echo -e "${CYAN}───────────────────────────────────────────────────────────────${NC}"
    
    # Store baseline values for comparison
    declare -A baseline_values
    
    for config in 1 2 3 4; do
        file="$RESULTS_DIR/config${config}/${level}_results.txt"
        metrics=$(extract_metrics "$file")
        
        IFS=',' read -r pc pd pvc pvd kp enc dec <<< "$metrics"
        
        if [ "$kp" != "N/A" ]; then
            # Store baseline (config 1) for comparison
            if [ $config -eq 1 ]; then
                baseline_values[kp]=$kp
                baseline_values[enc]=$enc
                baseline_values[dec]=$dec
            fi
            
            kp_formatted=$(format_number "$kp")
            enc_formatted=$(format_number "$enc")
            dec_formatted=$(format_number "$dec")
            
            if [ $config -eq 1 ]; then
                printf "%-20s %-15s %-15s %-15s ${YELLOW}(baseline)${NC}\n" "Config $config" "$kp_formatted" "$enc_formatted" "$dec_formatted"
            else
                kp_diff=$(calc_percentage "${baseline_values[kp]}" "$kp")
                enc_diff=$(calc_percentage "${baseline_values[enc]}" "$enc")
                dec_diff=$(calc_percentage "${baseline_values[dec]}" "$dec")
                
                printf "%-20s %-15s %-15s %-15s\n" "Config $config" "$kp_formatted" "$enc_formatted" "$dec_formatted"
                printf "%-20s %-15s %-15s %-15s\n" "" "$kp_diff" "$enc_diff" "$dec_diff"
            fi
        else
            printf "%-20s ${RED}%-45s${NC}\n" "Config $config" "No data found"
        fi
    done
    
    echo ""
    
    # Detailed Operations Table
    echo -e "${BOLD}${CYAN}Detailed Operations (Cycle Counts):${NC}"
    echo -e "${CYAN}───────────────────────────────────────────────────────────────${NC}"
    printf "${BOLD}%-20s %-15s %-15s${NC}\n" "Config" "Poly Compress" "PolyVec Compress"
    echo -e "${CYAN}───────────────────────────────────────────────────────────────${NC}"
    
    for config in 1 2 3 4; do
        file="$RESULTS_DIR/config${config}/${level}_results.txt"
        metrics=$(extract_metrics "$file")
        
        IFS=',' read -r pc pd pvc pvd kp enc dec <<< "$metrics"
        
        if [ "$pc" != "N/A" ]; then
            pc_formatted=$(format_number "$pc")
            pvc_formatted=$(format_number "$pvc")
            
            printf "%-20s %-15s %-15s\n" "Config $config" "$pc_formatted" "$pvc_formatted"
        else
            printf "%-20s ${RED}%-30s${NC}\n" "Config $config" "No data"
        fi
    done
    
    echo ""
done

# Summary section
echo ""
echo -e "${BOLD}${MAGENTA}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${MAGENTA}  Summary${NC}"
echo -e "${BOLD}${MAGENTA}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Find best performing configuration for each level
echo -e "${CYAN}Best Performing Configuration (by KeyPair):${NC}"
echo -e "${CYAN}───────────────────────────────────────────────────────────────${NC}"

for level in kyber512 kyber768 kyber1024; do
    best_config=0
    best_value=999999999
    
    for config in 1 2 3 4; do
        file="$RESULTS_DIR/config${config}/${level}_results.txt"
        metrics=$(extract_metrics "$file")
        
        IFS=',' read -r pc pd pvc pvd kp enc dec <<< "$metrics"
        
        if [ "$kp" != "N/A" ] && [ "$kp" -lt "$best_value" ]; then
            best_value=$kp
            best_config=$config
        fi
    done
    
    if [ $best_config -ne 0 ]; then
        echo -e "${GREEN}$level: Config $best_config ($(format_number $best_value) cycles)${NC}"
    else
        echo -e "${RED}$level: No data available${NC}"
    fi
done

echo ""

# File size information
echo -e "${CYAN}Configuration Details:${NC}"
echo -e "${CYAN}───────────────────────────────────────────────────────────────${NC}"

for config in 1 2 3 4; do
    config_dir="$RESULTS_DIR/config${config}"
    if [ -d "$config_dir" ]; then
        file_count=$(find "$config_dir" -type f | wc -l)
        echo -e "Config $config: ${GREEN}$file_count files${NC}"
    fi
done

echo ""

# System information
if [ -f "$RESULTS_DIR/system_info.txt" ]; then
    echo -e "${CYAN}System Information:${NC}"
    echo -e "${CYAN}───────────────────────────────────────────────────────────────${NC}"
    
    # Extract key system info
    cpu=$(grep "Model name" "$RESULTS_DIR/system_info.txt" | cut -d: -f2- | xargs)
    os=$(grep "PRETTY_NAME" "$RESULTS_DIR/system_info.txt" | cut -d= -f2- | tr -d '"')
    
    if [ ! -z "$cpu" ]; then
        echo -e "CPU: ${YELLOW}$cpu${NC}"
    fi
    if [ ! -z "$os" ]; then
        echo -e "OS:  ${YELLOW}$os${NC}"
    fi
    echo ""
fi

# Footer
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Quick comparison complete!${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}For detailed analysis with graphs and statistics, run:${NC}"
echo -e "${CYAN}  ./analyze_results.py $RESULTS_DIR${NC}"
echo ""

exit 0