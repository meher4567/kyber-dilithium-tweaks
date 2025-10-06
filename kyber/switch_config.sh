#!/bin/bash
# Kyber Configuration Switcher for Linux/Fedora
# Author: Thesis Implementation Helper
# Usage: ./switch_config.sh [1|2|3|4]

CONFIG=$1
PARAMS_FILE="src/params.h"

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display usage
show_usage() {
    echo -e "${RED}Usage: ./switch_config.sh [1|2|3|4]${NC}"
    echo ""
    echo -e "${CYAN}Available Configurations:${NC}"
    echo -e "  ${BLUE}1${NC} = Configuration 1 (Original NIST)"
    echo "      Kyber512:  (du,dv) = (10,4)"
    echo "      Kyber768:  (du,dv) = (10,4)"
    echo "      Kyber1024: (du,dv) = (11,5)"
    echo ""
    echo -e "  ${BLUE}2${NC} = Configuration 2 (High Compression)"
    echo "      Kyber512:  (du,dv) = (9,5)"
    echo "      Kyber768:  (du,dv) = (9,5)"
    echo "      Kyber1024: (du,dv) = (10,6)"
    echo ""
    echo -e "  ${BLUE}3${NC} = Configuration 3 (Balanced)"
    echo "      Kyber512:  (du,dv) = (10,5)"
    echo "      Kyber768:  (du,dv) = (10,5)"
    echo "      Kyber1024: (du,dv) = (10,5)"
    echo ""
    echo -e "  ${BLUE}4${NC} = Configuration 4 (Alternative Balanced)"
    echo "      Kyber512:  (du,dv) = (10,5)"
    echo "      Kyber768:  (du,dv) = (10,5)"
    echo "      Kyber1024: (du,dv) = (10,5)"
    echo ""
}

# Check if config number provided
if [ -z "$CONFIG" ]; then
    show_usage
    exit 1
fi

# Validate config number
if ! [[ "$CONFIG" =~ ^[1-4]$ ]]; then
    echo -e "${RED}Error: Invalid configuration number '$CONFIG'${NC}"
    show_usage
    exit 1
fi

# Check if src directory exists
if [ ! -d "src" ]; then
    echo -e "${RED}Error: src/ directory not found!${NC}"
    echo -e "${YELLOW}Make sure you run this script from the kyber/ directory${NC}"
    exit 1
fi

# Backup original params.h if it doesn't exist
if [ ! -f "src/params.h.original" ]; then
    if [ -f "$PARAMS_FILE" ]; then
        cp "$PARAMS_FILE" "src/params.h.original"
        echo -e "${GREEN}✓ Created backup: src/params.h.original${NC}"
    fi
fi

echo -e "${CYAN}=========================================${NC}"
echo -e "${CYAN}   Kyber Configuration Switcher${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

case $CONFIG in
    1)
        echo -e "${GREEN}→ Switching to Configuration 1 (Original NIST Parameters)${NC}"
        cat > $PARAMS_FILE << 'EOF'
#ifndef PARAMS_H
#define PARAMS_H

// Configuration 1: Original NIST Parameters
// Kyber512:  (du,dv) = (10,4)  → 160 bytes poly, 288*k bytes polyvec
// Kyber768:  (du,dv) = (10,4)  → 160 bytes poly, 288*k bytes polyvec
// Kyber1024: (du,dv) = (11,5)  → 192 bytes poly, 352*k bytes polyvec

#ifndef KYBER_K
#define KYBER_K 4  // Default to Kyber1024
#endif

#define KYBER_N 256
#define KYBER_Q 3329

#define KYBER_SYMBYTES 32   
#define KYBER_POLYBYTES 384

#if KYBER_K == 2
#define KYBER_ETA1 3
#define KYBER_ETA2 2
#define KYBER_POLYCOMPRESSEDBYTES    160
#define KYBER_POLYVECCOMPRESSEDBYTES (KYBER_K * 288)
#elif KYBER_K == 3
#define KYBER_ETA1 2
#define KYBER_ETA2 2
#define KYBER_POLYCOMPRESSEDBYTES    160
#define KYBER_POLYVECCOMPRESSEDBYTES (KYBER_K * 288)
#elif KYBER_K == 4
#define KYBER_ETA1 2
#define KYBER_ETA2 2
#define KYBER_POLYCOMPRESSEDBYTES    192
#define KYBER_POLYVECCOMPRESSEDBYTES (KYBER_K * 352)
#endif

#define KYBER_POLYVECBYTES (KYBER_K * KYBER_POLYBYTES)

#define KYBER_INDCPA_MSGBYTES       (KYBER_SYMBYTES)
#define KYBER_INDCPA_PUBLICKEYBYTES (KYBER_POLYVECCOMPRESSEDBYTES + KYBER_SYMBYTES)
#define KYBER_INDCPA_SECRETKEYBYTES (KYBER_POLYVECBYTES)
#define KYBER_INDCPA_BYTES          (KYBER_POLYVECCOMPRESSEDBYTES + KYBER_POLYCOMPRESSEDBYTES)

#define KYBER_PUBLICKEYBYTES  (KYBER_INDCPA_PUBLICKEYBYTES)
#define KYBER_SECRETKEYBYTES  (KYBER_INDCPA_SECRETKEYBYTES + KYBER_INDCPA_PUBLICKEYBYTES + 2*KYBER_SYMBYTES)
#define KYBER_CIPHERTEXTBYTES (KYBER_INDCPA_BYTES)

#endif /* PARAMS_H */
EOF
        ;;
    2)
        echo -e "${GREEN}→ Switching to Configuration 2 (High Compression)${NC}"
        cat > $PARAMS_FILE << 'EOF'
#ifndef PARAMS_H
#define PARAMS_H

// Configuration 2: High Compression Parameters
// Kyber512:  (du,dv) = (9,5)   → 96 bytes poly, 352*k bytes polyvec
// Kyber768:  (du,dv) = (9,5)   → 96 bytes poly, 352*k bytes polyvec
// Kyber1024: (du,dv) = (10,6)  → 128 bytes poly, 384*k bytes polyvec

#ifndef KYBER_K
#define KYBER_K 4  // Default to Kyber1024
#endif

#define KYBER_N 256
#define KYBER_Q 3329

#define KYBER_SYMBYTES 32   
#define KYBER_POLYBYTES 384

#if KYBER_K == 2
#define KYBER_ETA1 3
#define KYBER_ETA2 2
#define KYBER_POLYCOMPRESSEDBYTES     96
#define KYBER_POLYVECCOMPRESSEDBYTES (KYBER_K * 352)
#elif KYBER_K == 3
#define KYBER_ETA1 2
#define KYBER_ETA2 2
#define KYBER_POLYCOMPRESSEDBYTES     96
#define KYBER_POLYVECCOMPRESSEDBYTES (KYBER_K * 352)
#elif KYBER_K == 4
#define KYBER_ETA1 2
#define KYBER_ETA2 2
#define KYBER_POLYCOMPRESSEDBYTES    128
#define KYBER_POLYVECCOMPRESSEDBYTES (KYBER_K * 384)
#endif

#define KYBER_POLYVECBYTES (KYBER_K * KYBER_POLYBYTES)

#define KYBER_INDCPA_MSGBYTES       (KYBER_SYMBYTES)
#define KYBER_INDCPA_PUBLICKEYBYTES (KYBER_POLYVECCOMPRESSEDBYTES + KYBER_SYMBYTES)
#define KYBER_INDCPA_SECRETKEYBYTES (KYBER_POLYVECBYTES)
#define KYBER_INDCPA_BYTES          (KYBER_POLYVECCOMPRESSEDBYTES + KYBER_POLYCOMPRESSEDBYTES)

#define KYBER_PUBLICKEYBYTES  (KYBER_INDCPA_PUBLICKEYBYTES)
#define KYBER_SECRETKEYBYTES  (KYBER_INDCPA_SECRETKEYBYTES + KYBER_INDCPA_PUBLICKEYBYTES + 2*KYBER_SYMBYTES)
#define KYBER_CIPHERTEXTBYTES (KYBER_INDCPA_BYTES)

#endif /* PARAMS_H */
EOF
        ;;
    3)
        echo -e "${GREEN}→ Switching to Configuration 3 (Balanced)${NC}"
        cat > $PARAMS_FILE << 'EOF'
#ifndef PARAMS_H
#define PARAMS_H

// Configuration 3: Balanced Parameters
// Kyber512:  (du,dv) = (10,5)  → 128 bytes poly, 320*k bytes polyvec
// Kyber768:  (du,dv) = (10,5)  → 128 bytes poly, 320*k bytes polyvec
// Kyber1024: (du,dv) = (10,5)  → 160 bytes poly, 352*k bytes polyvec

#ifndef KYBER_K
#define KYBER_K 4  // Default to Kyber1024
#endif

#define KYBER_N 256
#define KYBER_Q 3329

#define KYBER_SYMBYTES 32   
#define KYBER_POLYBYTES 384

#if KYBER_K == 2
#define KYBER_ETA1 3
#define KYBER_ETA2 2
#define KYBER_POLYCOMPRESSEDBYTES    128
#define KYBER_POLYVECCOMPRESSEDBYTES (KYBER_K * 320)
#elif KYBER_K == 3
#define KYBER_ETA1 2
#define KYBER_ETA2 2
#define KYBER_POLYCOMPRESSEDBYTES    128
#define KYBER_POLYVECCOMPRESSEDBYTES (KYBER_K * 320)
#elif KYBER_K == 4
#define KYBER_ETA1 2
#define KYBER_ETA2 2
#define KYBER_POLYCOMPRESSEDBYTES    160
#define KYBER_POLYVECCOMPRESSEDBYTES (KYBER_K * 352)
#endif

#define KYBER_POLYVECBYTES (KYBER_K * KYBER_POLYBYTES)

#define KYBER_INDCPA_MSGBYTES       (KYBER_SYMBYTES)
#define KYBER_INDCPA_PUBLICKEYBYTES (KYBER_POLYVECCOMPRESSEDBYTES + KYBER_SYMBYTES)
#define KYBER_INDCPA_SECRETKEYBYTES (KYBER_POLYVECBYTES)
#define KYBER_INDCPA_BYTES          (KYBER_POLYVECCOMPRESSEDBYTES + KYBER_POLYCOMPRESSEDBYTES)

#define KYBER_PUBLICKEYBYTES  (KYBER_INDCPA_PUBLICKEYBYTES)
#define KYBER_SECRETKEYBYTES  (KYBER_INDCPA_SECRETKEYBYTES + KYBER_INDCPA_PUBLICKEYBYTES + 2*KYBER_SYMBYTES)
#define KYBER_CIPHERTEXTBYTES (KYBER_INDCPA_BYTES)

#endif /* PARAMS_H */
EOF
        ;;
    4)
        echo -e "${GREEN}→ Switching to Configuration 4 (Alternative Balanced)${NC}"
        cat > $PARAMS_FILE << 'EOF'
#ifndef PARAMS_H
#define PARAMS_H

// Configuration 4: Alternative Balanced Parameters
// Kyber512:  (du,dv) = (10,5)  → 128 bytes poly, 320*k bytes polyvec
// Kyber768:  (du,dv) = (10,5)  → 128 bytes poly, 320*k bytes polyvec
// Kyber1024: (du,dv) = (10,5)  → 160 bytes poly, 352*k bytes polyvec

#ifndef KYBER_K
#define KYBER_K 4  // Default to Kyber1024
#endif

#define KYBER_N 256
#define KYBER_Q 3329

#define KYBER_SYMBYTES 32   
#define KYBER_POLYBYTES 384

#if KYBER_K == 2
#define KYBER_ETA1 3
#define KYBER_ETA2 2
#define KYBER_POLYCOMPRESSEDBYTES    128
#define KYBER_POLYVECCOMPRESSEDBYTES (KYBER_K * 320)
#elif KYBER_K == 3
#define KYBER_ETA1 2
#define KYBER_ETA2 2
#define KYBER_POLYCOMPRESSEDBYTES    128
#define KYBER_POLYVECCOMPRESSEDBYTES (KYBER_K * 320)
#elif KYBER_K == 4
#define KYBER_ETA1 2
#define KYBER_ETA2 2
#define KYBER_POLYCOMPRESSEDBYTES    160
#define KYBER_POLYVECCOMPRESSEDBYTES (KYBER_K * 352)
#endif

#define KYBER_POLYVECBYTES (KYBER_K * KYBER_POLYBYTES)

#define KYBER_INDCPA_MSGBYTES       (KYBER_SYMBYTES)
#define KYBER_INDCPA_PUBLICKEYBYTES (KYBER_POLYVECCOMPRESSEDBYTES + KYBER_SYMBYTES)
#define KYBER_INDCPA_SECRETKEYBYTES (KYBER_POLYVECBYTES)
#define KYBER_INDCPA_BYTES          (KYBER_POLYVECCOMPRESSEDBYTES + KYBER_POLYCOMPRESSEDBYTES)

#define KYBER_PUBLICKEYBYTES  (KYBER_INDCPA_PUBLICKEYBYTES)
#define KYBER_SECRETKEYBYTES  (KYBER_INDCPA_SECRETKEYBYTES + KYBER_INDCPA_PUBLICKEYBYTES + 2*KYBER_SYMBYTES)
#define KYBER_CIPHERTEXTBYTES (KYBER_INDCPA_BYTES)

#endif /* PARAMS_H */
EOF
        ;;
esac

echo -e "${GREEN}✅ Configuration $CONFIG applied successfully!${NC}"
echo ""
echo -e "${YELLOW}📝 Modified file: $PARAMS_FILE${NC}"
echo -e "${BLUE}📋 Next steps:${NC}"
echo "   1. make clean"
echo "   2. make"
echo "   3. Run your benchmarks"
echo ""
echo -e "${CYAN}=========================================${NC}"