#!/bin/bash
# Automated Security Analysis Wrapper
# Handles setup, execution, and result presentation

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

# Print header
print_header() {
    echo -e "\n${CYAN}================================================================================${NC}"
    echo -e "${CYAN}${BOLD}                    Kyber Security Analysis Suite${NC}"
    echo -e "${CYAN}================================================================================${NC}\n"
}

# Print section
print_section() {
    echo -e "\n${BLUE}${BOLD}$1${NC}"
    echo -e "${BLUE}--------------------------------------------------------------------------------${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_section "Checking Prerequisites"
    
    local all_good=true
    
    # Check Python 3
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        echo -e "${GREEN}✓ Python 3 found: ${PYTHON_VERSION}${NC}"
    else
        echo -e "${RED}✗ Python 3 not found${NC}"
        all_good=false
    fi
    
    # Check pip3
    if command -v pip3 &> /dev/null; then
        echo -e "${GREEN}✓ pip3 found${NC}"
    else
        echo -e "${RED}✗ pip3 not found${NC}"
        all_good=false
    fi
    
    # Check git
    if command -v git &> /dev/null; then
        echo -e "${GREEN}✓ git found${NC}"
    else
        echo -e "${RED}✗ git not found${NC}"
        all_good=false
    fi
    
    # Check security_config.json
    if [ -f "security_config.json" ]; then
        echo -e "${GREEN}✓ security_config.json found${NC}"
    else
        echo -e "${RED}✗ security_config.json not found${NC}"
        all_good=false
    fi
    
    # Check security_analysis.py
    if [ -f "security_analysis.py" ]; then
        echo -e "${GREEN}✓ security_analysis.py found${NC}"
    else
        echo -e "${RED}✗ security_analysis.py not found${NC}"
        all_good=false
    fi
    
    if [ "$all_good" = false ]; then
        echo -e "\n${RED}${BOLD}Error: Missing prerequisites!${NC}"
        echo -e "${YELLOW}Please ensure all required files and tools are present.${NC}\n"
        exit 1
    fi
    
    echo -e "\n${GREEN}${BOLD}✓ All prerequisites satisfied${NC}"
}

# Check and install lattice-estimator
check_lattice_estimator() {
    print_section "Checking Lattice Estimator"
    
    # Check if estimator is already installed
    if python3 -c "import estimator" 2>/dev/null; then
        echo -e "${GREEN}✓ Lattice estimator already installed${NC}"
        return 0
    fi
    
    # Check if estimator directory exists
    if [ -d "lattice-estimator" ]; then
        echo -e "${YELLOW}⚠ lattice-estimator directory found but not installed${NC}"
        echo -e "${CYAN}Installing dependencies...${NC}"
        cd lattice-estimator
        pip3 install -r requirements.txt --user
        cd ..
        return 0
    fi
    
    # Need to clone
    echo -e "${YELLOW}Lattice estimator not found. Installing...${NC}"
    
    read -p "$(echo -e ${CYAN}Clone and install lattice-estimator? [y/N]: ${NC})" -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Skipping installation. You can install manually later.${NC}"
        return 1
    fi
    
    echo -e "${CYAN}Cloning lattice-estimator...${NC}"
    git clone https://github.com/malb/lattice-estimator
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to clone repository${NC}"
        return 1
    fi
    
    echo -e "${CYAN}Installing dependencies...${NC}"
    cd lattice-estimator
    pip3 install -r requirements.txt --user
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to install dependencies${NC}"
        cd ..
        return 1
    fi
    
    cd ..
    echo -e "${GREEN}✓ Lattice estimator installed successfully${NC}"
    return 0
}

# Run security analysis
run_analysis() {
    print_section "Running Security Analysis"
    
    echo -e "${YELLOW}This may take several minutes...${NC}"
    echo -e "${CYAN}Analyzing all configurations and security levels...${NC}\n"
    
    # Make security_analysis.py executable
    chmod +x security_analysis.py
    
    # Run the analysis
    python3 security_analysis.py
    
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}${BOLD}✓ Security analysis completed successfully!${NC}"
        return 0
    else
        echo -e "\n${RED}${BOLD}✗ Security analysis failed${NC}"
        return 1
    fi
}

# Display results
display_results() {
    print_section "Results Summary"
    
    if [ ! -d "security_results" ]; then
        echo -e "${RED}✗ Results directory not found${NC}"
        return 1
    fi
    
    echo -e "${CYAN}Generated files:${NC}"
    
    if [ -f "security_results/security_report.txt" ]; then
        echo -e "${GREEN}✓ security_results/security_report.txt${NC}"
    fi
    
    if [ -f "security_results/security_tables.tex" ]; then
        echo -e "${GREEN}✓ security_results/security_tables.tex${NC}"
    fi
    
    if [ -d "security_results/estimator_logs" ]; then
        LOG_COUNT=$(find security_results/estimator_logs -type f | wc -l)
        echo -e "${GREEN}✓ security_results/estimator_logs/ (${LOG_COUNT} files)${NC}"
    fi
    
    echo -e "\n${CYAN}Quick view of results:${NC}"
    echo -e "${BLUE}--------------------------------------------------------------------------------${NC}"
    
    if [ -f "security_results/security_report.txt" ]; then
        head -n 30 security_results/security_report.txt
        echo -e "${YELLOW}... (see full report in security_results/security_report.txt)${NC}"
    fi
    
    echo -e "\n${CYAN}Next steps:${NC}"
    echo "  1. Review full report: cat security_results/security_report.txt"
    echo "  2. LaTeX tables: security_results/security_tables.tex"
    echo "  3. Detailed logs: security_results/estimator_logs/"
    echo ""
}

# Compile LaTeX tables (optional)
compile_latex() {
    print_section "Compiling LaTeX Tables (Optional)"
    
    if [ ! -f "security_results/security_tables.tex" ]; then
        echo -e "${YELLOW}No LaTeX tables found to compile${NC}"
        return
    fi
    
    if ! command -v pdflatex &> /dev/null; then
        echo -e "${YELLOW}pdflatex not found. Skipping PDF generation.${NC}"
        echo -e "${CYAN}Install with: sudo dnf install texlive${NC}"
        return
    fi
    
    read -p "$(echo -e ${CYAN}Compile LaTeX tables to PDF? [y/N]: ${NC})" -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Skipping LaTeX compilation${NC}"
        return
    fi
    
    echo -e "${CYAN}Compiling LaTeX...${NC}"
    cd security_results
    pdflatex security_tables.tex > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ PDF generated: security_results/security_tables.pdf${NC}"
    else
        echo -e "${RED}✗ LaTeX compilation failed${NC}"
    fi
    
    cd ..
}

# Create backup
create_backup() {
    if [ -d "security_results" ]; then
        TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
        BACKUP_DIR="security_results_backup_${TIMESTAMP}"
        
        echo -e "${YELLOW}Backing up previous results to ${BACKUP_DIR}${NC}"
        mv security_results "$BACKUP_DIR"
    fi
}

# Main menu
show_menu() {
    echo -e "\n${CYAN}${BOLD}Security Analysis Menu${NC}"
    echo -e "${CYAN}--------------------------------------------------------------------------------${NC}"
    echo "  1. Run full security analysis"
    echo "  2. Check prerequisites only"
    echo "  3. Install lattice-estimator"
    echo "  4. View existing results"
    echo "  5. Clean results and start fresh"
    echo "  6. Exit"
    echo -e "${CYAN}--------------------------------------------------------------------------------${NC}"
    read -p "$(echo -e ${YELLOW}Select option [1-6]: ${NC})" choice
    
    case $choice in
        1)
            create_backup
            check_prerequisites
            check_lattice_estimator
            run_analysis
            display_results
            compile_latex
            ;;
        2)
            check_prerequisites
            check_lattice_estimator
            ;;
        3)
            check_lattice_estimator
            ;;
        4)
            display_results
            ;;
        5)
            echo -e "${YELLOW}Cleaning results...${NC}"
            rm -rf security_results
            echo -e "${GREEN}✓ Results cleaned${NC}"
            ;;
        6)
            echo -e "\n${CYAN}Exiting...${NC}\n"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option${NC}"
            show_menu
            ;;
    esac
}

# Main execution
main() {
    print_header
    
    # Check if running with arguments
    if [ $# -gt 0 ]; then
        case $1 in
            --auto|-a)
                echo -e "${CYAN}Running in automatic mode...${NC}"
                create_backup
                check_prerequisites
                if check_lattice_estimator; then
                    run_analysis
                    display_results
                fi
                ;;
            --help|-h)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --auto, -a     Run automatically without prompts"
                echo "  --help, -h     Show this help message"
                echo ""
                echo "Interactive mode (no arguments): Shows menu"
                exit 0
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    else
        # Interactive mode
        show_menu
    fi
    
    echo -e "\n${CYAN}================================================================================${NC}"
    echo -e "${GREEN}${BOLD}Done!${NC}"
    echo -e "${CYAN}================================================================================${NC}\n"
}

# Run main function
main "$@"