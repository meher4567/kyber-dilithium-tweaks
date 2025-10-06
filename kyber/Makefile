# Makefile for Kyber (ML-KEM) Implementation
# Supports Kyber512, Kyber768, and Kyber1024
# Builds test programs for benchmarking

# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -O3 -fomit-frame-pointer -march=native -fPIC
LDFLAGS = -lcrypto

# Directories
SRC_DIR = src
TEST_DIR = tests
BUILD_DIR = build
BIN_DIR = .

# Source files (all .c files in src/)
SOURCES = $(wildcard $(SRC_DIR)/*.c)
OBJECTS = $(SOURCES:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)

# Header dependencies
HEADERS = $(wildcard $(SRC_DIR)/*.h)

# Test programs
TEST_SOURCES = $(wildcard $(TEST_DIR)/*.c)
TEST_BINS = $(TEST_SOURCES:$(TEST_DIR)/%.c=$(BIN_DIR)/%)

# Default target
.DEFAULT_GOAL := all

# Color output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
CYAN = \033[0;36m
NC = \033[0m # No Color

#############################################
# Main Targets
#############################################

.PHONY: all
all: info kyber512 kyber768 kyber1024
	@echo "$(GREEN)✅ All Kyber variants built successfully!$(NC)"
	@echo ""
	@echo "$(CYAN)Available test programs:$(NC)"
	@echo "  ./test_speed512  - Benchmark Kyber512"
	@echo "  ./test_speed768  - Benchmark Kyber768"
	@echo "  ./test_speed1024 - Benchmark Kyber1024"
	@echo ""

.PHONY: info
info:
	@echo "$(CYAN)════════════════════════════════════════$(NC)"
	@echo "$(CYAN)  Kyber (ML-KEM) Build System$(NC)"
	@echo "$(CYAN)════════════════════════════════════════$(NC)"
	@echo "Compiler: $(CC)"
	@echo "Flags:    $(CFLAGS)"
	@echo ""

#############################################
# Build Directory Setup
#############################################

$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)
	@echo "$(GREEN)✓ Created build directory$(NC)"

$(TEST_DIR):
	@mkdir -p $(TEST_DIR)
	@echo "$(GREEN)✓ Created tests directory$(NC)"

#############################################
# Kyber512 (KYBER_K=2)
#############################################

.PHONY: kyber512
kyber512: $(BUILD_DIR) $(TEST_DIR)
	@echo "$(YELLOW)Building Kyber512 (K=2)...$(NC)"
	@$(MAKE) --no-print-directory test_speed512 KYBER_K=2
	@echo "$(GREEN)✓ Kyber512 complete$(NC)"

test_speed512: $(TEST_DIR)/test_speed512.c $(SOURCES) $(HEADERS)
	@echo "  Compiling test_speed512..."
	@$(CC) $(CFLAGS) -DKYBER_K=2 -I$(SRC_DIR) \
		$(TEST_DIR)/test_speed512.c $(SOURCES) \
		-o $(BIN_DIR)/test_speed512 $(LDFLAGS)

#############################################
# Kyber768 (KYBER_K=3)
#############################################

.PHONY: kyber768
kyber768: $(BUILD_DIR) $(TEST_DIR)
	@echo "$(YELLOW)Building Kyber768 (K=3)...$(NC)"
	@$(MAKE) --no-print-directory test_speed768 KYBER_K=3
	@echo "$(GREEN)✓ Kyber768 complete$(NC)"

test_speed768: $(TEST_DIR)/test_speed768.c $(SOURCES) $(HEADERS)
	@echo "  Compiling test_speed768..."
	@$(CC) $(CFLAGS) -DKYBER_K=3 -I$(SRC_DIR) \
		$(TEST_DIR)/test_speed768.c $(SOURCES) \
		-o $(BIN_DIR)/test_speed768 $(LDFLAGS)

#############################################
# Kyber1024 (KYBER_K=4)
#############################################

.PHONY: kyber1024
kyber1024: $(BUILD_DIR) $(TEST_DIR)
	@echo "$(YELLOW)Building Kyber1024 (K=4)...$(NC)"
	@$(MAKE) --no-print-directory test_speed1024 KYBER_K=4
	@echo "$(GREEN)✓ Kyber1024 complete$(NC)"

test_speed1024: $(TEST_DIR)/test_speed1024.c $(SOURCES) $(HEADERS)
	@echo "  Compiling test_speed1024..."
	@$(CC) $(CFLAGS) -DKYBER_K=4 -I$(SRC_DIR) \
		$(TEST_DIR)/test_speed1024.c $(SOURCES) \
		-o $(BIN_DIR)/test_speed1024 $(LDFLAGS)

#############################################
# Object Files (for modular builds)
#############################################

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c $(HEADERS) | $(BUILD_DIR)
	@echo "  Compiling $<..."
	@$(CC) $(CFLAGS) -DKYBER_K=$(KYBER_K) -c $< -o $@

#############################################
# Testing Targets
#############################################

.PHONY: test
test: all
	@echo "$(CYAN)════════════════════════════════════════$(NC)"
	@echo "$(CYAN)  Running Kyber Tests$(NC)"
	@echo "$(CYAN)════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)Testing Kyber512...$(NC)"
	@./test_speed512 || echo "$(RED)✗ Kyber512 test failed$(NC)"
	@echo ""
	@echo "$(YELLOW)Testing Kyber768...$(NC)"
	@./test_speed768 || echo "$(RED)✗ Kyber768 test failed$(NC)"
	@echo ""
	@echo "$(YELLOW)Testing Kyber1024...$(NC)"
	@./test_speed1024 || echo "$(RED)✗ Kyber1024 test failed$(NC)"
	@echo ""
	@echo "$(GREEN)✅ All tests complete$(NC)"

.PHONY: benchmark
benchmark: all
	@echo "$(CYAN)════════════════════════════════════════$(NC)"
	@echo "$(CYAN)  Running Full Benchmark Suite$(NC)"
	@echo "$(CYAN)════════════════════════════════════════$(NC)"
	@./benchmark_all.sh

#############################################
# Cleaning Targets
#############################################

.PHONY: clean
clean:
	@echo "$(YELLOW)Cleaning build artifacts...$(NC)"
	@rm -rf $(BUILD_DIR)
	@rm -f $(BIN_DIR)/test_speed512
	@rm -f $(BIN_DIR)/test_speed768
	@rm -f $(BIN_DIR)/test_speed1024
	@rm -f *.o *.a *.so
	@echo "$(GREEN)✓ Clean complete$(NC)"

.PHONY: cleanall
cleanall: clean
	@echo "$(YELLOW)Cleaning all results and logs...$(NC)"
	@rm -rf benchmark_results/
	@echo "$(GREEN)✓ All files cleaned$(NC)"

#############################################
# Help Target
#############################################

.PHONY: help
help:
	@echo "$(CYAN)════════════════════════════════════════$(NC)"
	@echo "$(CYAN)  Kyber Makefile - Available Targets$(NC)"
	@echo "$(CYAN)════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(GREEN)Build Targets:$(NC)"
	@echo "  make all        - Build all Kyber variants (default)"
	@echo "  make kyber512   - Build Kyber512 only"
	@echo "  make kyber768   - Build Kyber768 only"
	@echo "  make kyber1024  - Build Kyber1024 only"
	@echo ""
	@echo "$(GREEN)Testing Targets:$(NC)"
	@echo "  make test       - Run all test programs"
	@echo "  make benchmark  - Run full benchmark suite"
	@echo ""
	@echo "$(GREEN)Cleaning Targets:$(NC)"
	@echo "  make clean      - Remove build artifacts"
	@echo "  make cleanall   - Remove all generated files"
	@echo ""
	@echo "$(GREEN)Utility Targets:$(NC)"
	@echo "  make help       - Show this help message"
	@echo "  make info       - Show build configuration"
	@echo ""
	@echo "$(YELLOW)Examples:$(NC)"
	@echo "  make clean && make all"
	@echo "  make kyber1024"
	@echo "  ./test_speed1024"
	@echo ""

#############################################
# Installation (Optional)
#############################################

.PHONY: install
install: all
	@echo "$(YELLOW)Installing Kyber test programs...$(NC)"
	@mkdir -p ~/bin
	@cp test_speed512 ~/bin/
	@cp test_speed768 ~/bin/
	@cp test_speed1024 ~/bin/
	@echo "$(GREEN)✓ Installed to ~/bin/$(NC)"
	@echo "$(CYAN)Add ~/bin to your PATH if not already done$(NC)"

#############################################
# Debug Build (with debug symbols)
#############################################

.PHONY: debug
debug: CFLAGS = -Wall -Wextra -g -O0 -DDEBUG -march=native
debug: clean all
	@echo "$(GREEN)✓ Debug build complete$(NC)"

#############################################
# Dependency Information
#############################################

.PHONY: deps
deps:
	@echo "$(CYAN)Source files:$(NC)"
	@ls -1 $(SRC_DIR)/*.c 2>/dev/null || echo "  No source files found"
	@echo ""
	@echo "$(CYAN)Header files:$(NC)"
	@ls -1 $(SRC_DIR)/*.h 2>/dev/null || echo "  No header files found"
	@echo ""
	@echo "$(CYAN)Test files:$(NC)"
	@ls -1 $(TEST_DIR)/*.c 2>/dev/null || echo "  No test files found"

#############################################
# Phony Targets Declaration
#############################################

.PHONY: all clean cleanall test benchmark help info install debug deps \
        kyber512 kyber768 kyber1024
