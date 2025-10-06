/*
 * CONFIG 1: BASELINE (ORIGINAL NIST)
 * 
 * Unmodified Dilithium2 reference implementation
 * Purpose: Performance baseline for comparison
 * 
 * Changes: None
 * Expected Performance: Standard NIST Dilithium2
 */

 #ifndef CONFIG1_BASELINE_H
 #define CONFIG1_BASELINE_H
 
 // Configuration identifier
 #define CONFIG_ID 1
 #define CONFIG_NAME "Config1-Baseline"
 #define CONFIG_DESCRIPTION "Original NIST Dilithium2 (No modifications)"
 
 // Dilithium variant
 #define DILITHIUM_MODE 2
 
 // Enable randomized signing (standard)
 #define DILITHIUM_RANDOMIZED_SIGNING
 
 // Hash function selection
 #define USE_SHAKE256  // Original: SHAKE256 for challenge generation
 // #define USE_SHA3_256  // Tweak 1: SHA3-256 (disabled in baseline)
 
 // Lattice parameters (Dilithium2 standard)
 #define K 4
 #define L 4
 #define ETA 2
 
 // Challenge polynomial parameters (original)
 #define TAU 39      // Number of ±1's in challenge
 #define OMEGA 80    // Maximum number of 1's in hint
 
 // Rounding parameters (original)
 #define GAMMA1 (1 << 17)      // 131072 - Low-order rounding range
 #define GAMMA2 ((Q-1)/88)     // 95232 - High-order rounding range
 #define BETA 78               // Rejection bound (TAU * ETA)
 
 // Challenge hash output size
 #define CTILDEBYTES 32
 
 // Core ring parameters (never change)
 #define SEEDBYTES 32
 #define CRHBYTES 64
 #define TRBYTES 64
 #define RNDBYTES 32
 #define N 256
 #define Q 8380417
 #define D 13
 #define ROOT_OF_UNITY 1753
 
 // Derived parameters (based on GAMMA1, GAMMA2, ETA)
 #define POLYT1_PACKEDBYTES  320
 #define POLYT0_PACKEDBYTES  416
 #define POLYVECH_PACKEDBYTES (OMEGA + K)
 
 #if GAMMA1 == (1 << 17)
 #define POLYZ_PACKEDBYTES   576
 #elif GAMMA1 == (1 << 19)
 #define POLYZ_PACKEDBYTES   640
 #endif
 
 #if GAMMA2 == (Q-1)/88
 #define POLYW1_PACKEDBYTES  192
 #elif GAMMA2 == (Q-1)/32
 #define POLYW1_PACKEDBYTES  128
 #endif
 
 #if ETA == 2
 #define POLYETA_PACKEDBYTES  96
 #elif ETA == 4
 #define POLYETA_PACKEDBYTES 128
 #endif
 
 // Key and signature sizes
 #define CRYPTO_PUBLICKEYBYTES (SEEDBYTES + K*POLYT1_PACKEDBYTES)
 #define CRYPTO_SECRETKEYBYTES (2*SEEDBYTES \
                                + TRBYTES \
                                + L*POLYETA_PACKEDBYTES \
                                + K*POLYETA_PACKEDBYTES \
                                + K*POLYT0_PACKEDBYTES)
 #define CRYPTO_BYTES (CTILDEBYTES + L*POLYZ_PACKEDBYTES + POLYVECH_PACKEDBYTES)
 
 // Algorithm selection macros
 #define CRYPTO_ALGNAME "Dilithium2-Baseline"
 #define DILITHIUM_NAMESPACETOP pqcrystals_dilithium2_ref
 #define DILITHIUM_NAMESPACE(s) pqcrystals_dilithium2_ref_##s
 
 // Performance expectations (for reference)
 // Sign cycles: ~2,000,000 (approx)
 // Verify cycles: ~1,000,000 (approx)
 // Signature size: 2420 bytes
 // Public key: 1312 bytes
 // Secret key: 2528 bytes
 
 // Security level: NIST Level 2
 // Core-SVP hardness: ~103 bits (classical), ~85 bits (quantum)
 
 #endif /* CONFIG1_BASELINE_H */