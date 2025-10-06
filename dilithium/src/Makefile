# Dilithium Makefile (Extended for Tweaks)
# Original: pq-crystals/dilithium
# Extended: Config switching and SHA3-256 support

CC ?= /usr/bin/cc
CFLAGS += -Wall -Wextra -Wpedantic -Wmissing-prototypes -Wredundant-decls \
  -Wshadow -Wvla -Wpointer-arith -O3 -fomit-frame-pointer
NISTFLAGS += -Wno-unused-result -O3 -fomit-frame-pointer

# Configuration selection (default: baseline)
# Set with: make CONFIG=2 (for SHA3-256 tweak, etc.)
CONFIG ?= 1

# Add OpenSSL for SHA3-256 (Tweak 1)
# Configuration-specific settings
ifeq ($(CONFIG),1)
  # Baseline - no extra sources
  EXTRA_SOURCES =
  EXTRA_HEADERS =
endif

ifeq ($(CONFIG),2)
  # Tweak 1: SHA3-256 Challenge
  LDFLAGS += -lcrypto
  CFLAGS += -DUSE_SHA3_CHALLENGE
  EXTRA_SOURCES = challenge_sha3.c
  EXTRA_HEADERS = challenge_sha3.h
endif

ifeq ($(CONFIG),3)
  # Tweak 2: Expanded Challenge Coefficients
  CFLAGS += -DUSE_EXPANDED_CHALLENGE
  CFLAGS += -DMODIFIED_CHALLENGE_BOUNDS
  EXTRA_SOURCES = challenge_expanded.c
  EXTRA_HEADERS = challenge_expanded.h
endif

ifeq ($(CONFIG),4)
  # Tweak 3: Relaxed Rejection Sampling
  CFLAGS += -DRELAXED_REJECTION
  # Choose rejection option:
  # - RELAXED_REJECTION_OPTION1: Relax bounds (BETA*2)
  # - RELAXED_REJECTION_OPTION2: Probabilistic bypass (10%)
  # - Default: Simple BETA increase (BETA=100)
  
  # Uncomment ONE of the following to select option:
  # CFLAGS += -DRELAXED_REJECTION_OPTION1
  # CFLAGS += -DRELAXED_REJECTION_OPTION2
  
  EXTRA_SOURCES =
  EXTRA_HEADERS = rejection_tweaked.h
endif

# Default if CONFIG not set
ifndef CONFIG
  EXTRA_SOURCES =
  EXTRA_HEADERS =
endif

SOURCES = sign.c packing.c polyvec.c poly.c ntt.c reduce.c rounding.c $(EXTRA_SOURCES)
HEADERS = config.h params.h api.h sign.h packing.h polyvec.h poly.h ntt.h \
  reduce.h rounding.h symmetric.h randombytes.h $(EXTRA_HEADERS)
KECCAK_SOURCES = $(SOURCES) fips202.c symmetric-shake.c
KECCAK_HEADERS = $(HEADERS) fips202.h

.PHONY: all speed shared clean config-info

all: \
  test/test_dilithium2 \
  test/test_dilithium3 \
  test/test_dilithium5 \
  test/test_vectors2 \
  test/test_vectors3 \
  test/test_vectors5

nistkat: \
  nistkat/PQCgenKAT_sign2 \
  nistkat/PQCgenKAT_sign3 \
  nistkat/PQCgenKAT_sign5

speed: \
  test/test_mul \
  test/test_speed2 \
  test/test_speed3 \
  test/test_speed5 \

shared: \
  libpqcrystals_dilithium2_ref.so \
  libpqcrystals_dilithium3_ref.so \
  libpqcrystals_dilithium5_ref.so \
  libpqcrystals_fips202_ref.so \

libpqcrystals_fips202_ref.so: fips202.c fips202.h
	$(CC) -shared -fPIC $(CFLAGS) -o $@ $<

libpqcrystals_dilithium2_ref.so: $(SOURCES) $(HEADERS) symmetric-shake.c
	$(CC) -shared -fPIC $(CFLAGS) -DDILITHIUM_MODE=2 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $(SOURCES) symmetric-shake.c $(LDFLAGS)

libpqcrystals_dilithium3_ref.so: $(SOURCES) $(HEADERS) symmetric-shake.c
	$(CC) -shared -fPIC $(CFLAGS) -DDILITHIUM_MODE=3 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $(SOURCES) symmetric-shake.c $(LDFLAGS)

libpqcrystals_dilithium5_ref.so: $(SOURCES) $(HEADERS) symmetric-shake.c
	$(CC) -shared -fPIC $(CFLAGS) -DDILITHIUM_MODE=5 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $(SOURCES) symmetric-shake.c $(LDFLAGS)

test/test_dilithium2: test/test_dilithium.c randombytes.c $(KECCAK_SOURCES) \
  $(KECCAK_HEADERS)
	$(CC) $(CFLAGS) -DDILITHIUM_MODE=2 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $< randombytes.c $(KECCAK_SOURCES) $(LDFLAGS)

test/test_dilithium3: test/test_dilithium.c randombytes.c $(KECCAK_SOURCES) \
  $(KECCAK_HEADERS)
	$(CC) $(CFLAGS) -DDILITHIUM_MODE=3 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $< randombytes.c $(KECCAK_SOURCES) $(LDFLAGS)

test/test_dilithium5: test/test_dilithium.c randombytes.c $(KECCAK_SOURCES) \
  $(KECCAK_HEADERS)
	$(CC) $(CFLAGS) -DDILITHIUM_MODE=5 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $< randombytes.c $(KECCAK_SOURCES) $(LDFLAGS)

test/test_vectors2: test/test_vectors.c $(KECCAK_SOURCES) \
  $(KECCAK_HEADERS)
	$(CC) $(CFLAGS) -DDILITHIUM_MODE=2 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $< $(KECCAK_SOURCES) $(LDFLAGS)

test/test_vectors3: test/test_vectors.c $(KECCAK_SOURCES) $(KECCAK_HEADERS)
	$(CC) $(CFLAGS) -DDILITHIUM_MODE=3 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $< $(KECCAK_SOURCES) $(LDFLAGS)

test/test_vectors5: test/test_vectors.c $(KECCAK_SOURCES) \
  $(KECCAK_HEADERS)
	$(CC) $(CFLAGS) -DDILITHIUM_MODE=5 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $< $(KECCAK_SOURCES) $(LDFLAGS)

test/test_speed2: test/test_speed.c test/speed_print.c test/speed_print.h \
  test/cpucycles.c test/cpucycles.h randombytes.c $(KECCAK_SOURCES) \
  $(KECCAK_HEADERS)
	$(CC) $(CFLAGS) -DDILITHIUM_MODE=2 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $< test/speed_print.c test/cpucycles.c randombytes.c \
	  $(KECCAK_SOURCES) $(LDFLAGS)

test/test_speed3: test/test_speed.c test/speed_print.c test/speed_print.h \
  test/cpucycles.c test/cpucycles.h randombytes.c $(KECCAK_SOURCES) \
  $(KECCAK_HEADERS)
	$(CC) $(CFLAGS) -DDILITHIUM_MODE=3 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $< test/speed_print.c test/cpucycles.c randombytes.c \
	  $(KECCAK_SOURCES) $(LDFLAGS)

test/test_speed5: test/test_speed.c test/speed_print.c test/speed_print.h \
  test/cpucycles.c test/cpucycles.h randombytes.c $(KECCAK_SOURCES) \
  $(KECCAK_HEADERS)
	$(CC) $(CFLAGS) -DDILITHIUM_MODE=5 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $< test/speed_print.c test/cpucycles.c randombytes.c \
	  $(KECCAK_SOURCES) $(LDFLAGS)

test/test_mul: test/test_mul.c randombytes.c $(KECCAK_SOURCES) $(KECCAK_HEADERS)
	$(CC) $(CFLAGS) -UDBENCH -o $@ $< randombytes.c $(KECCAK_SOURCES) $(LDFLAGS)

nistkat/PQCgenKAT_sign2: nistkat/PQCgenKAT_sign.c nistkat/rng.c nistkat/rng.h $(KECCAK_SOURCES) \
  $(KECCAK_HEADERS)
	$(CC) $(NISTFLAGS) -DDILITHIUM_MODE=2 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $< nistkat/rng.c $(KECCAK_SOURCES) $(LDFLAGS) -lcrypto

nistkat/PQCgenKAT_sign3: nistkat/PQCgenKAT_sign.c nistkat/rng.c nistkat/rng.h $(KECCAK_SOURCES) \
  $(KECCAK_HEADERS)
	$(CC) $(NISTFLAGS) -DDILITHIUM_MODE=3 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $< nistkat/rng.c $(KECCAK_SOURCES) $(LDFLAGS) -lcrypto

nistkat/PQCgenKAT_sign5: nistkat/PQCgenKAT_sign.c nistkat/rng.c nistkat/rng.h $(KECCAK_SOURCES) \
  $(KECCAK_HEADERS)
	$(CC) $(NISTFLAGS) -DDILITHIUM_MODE=5 -DCONFIG_ID=$(CONFIG) \
	  -o $@ $< nistkat/rng.c $(KECCAK_SOURCES) $(LDFLAGS) -lcrypto

# New target: Show current configuration
config-info:
	@echo "Current Configuration: CONFIG=$(CONFIG)"
	@if [ "$(CONFIG)" = "1" ]; then \
		echo "  Name: Baseline (Original NIST)"; \
	elif [ "$(CONFIG)" = "2" ]; then \
		echo "  Name: Tweak 1 (SHA3-256 Challenge)"; \
		echo "  Extra Sources: $(EXTRA_SOURCES)"; \
		echo "  OpenSSL: Enabled"; \
	elif [ "$(CONFIG)" = "3" ]; then \
		echo "  Name: Tweak 2 (Challenge Bounds)"; \
	elif [ "$(CONFIG)" = "4" ]; then \
		echo "  Name: Tweak 3 (Rejection Sampling)"; \
	fi

# New target: Build all configs for Dilithium2
all-configs-mode2:
	@echo "Building Dilithium2 with all configurations..."
	$(MAKE) clean
	$(MAKE) CONFIG=1 test/test_speed2
	mv test/test_speed2 test/test_speed2_config1
	$(MAKE) clean
	$(MAKE) CONFIG=2 test/test_speed2
	mv test/test_speed2 test/test_speed2_config2
	$(MAKE) clean
	$(MAKE) CONFIG=3 test/test_speed2
	mv test/test_speed2 test/test_speed2_config3
	$(MAKE) clean
	$(MAKE) CONFIG=4 test/test_speed2
	mv test/test_speed2 test/test_speed2_config4
	@echo "All Dilithium2 configs built"

clean:
	rm -f *~ test/*~ *.gcno *.gcda *.lcov
	rm -f libpqcrystals_dilithium2_ref.so
	rm -f libpqcrystals_dilithium3_ref.so
	rm -f libpqcrystals_dilithium5_ref.so
	rm -f libpqcrystals_fips202_ref.so
	rm -f test/test_dilithium2
	rm -f test/test_dilithium3
	rm -f test/test_dilithium5
	rm -f test/test_vectors2
	rm -f test/test_vectors3
	rm -f test/test_vectors5
	rm -f test/test_speed2 test/test_speed2_config*
	rm -f test/test_speed3 test/test_speed3_config*
	rm -f test/test_speed5 test/test_speed5_config*
	rm -f test/test_mul
	rm -f nistkat/PQCgenKAT_sign2
	rm -f nistkat/PQCgenKAT_sign3
	rm -f nistkat/PQCgenKAT_sign5