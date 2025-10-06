/*
 * CONFIG 4: TWEAK 3 - REJECTION SAMPLING
 * 
 * Modify rejection sampling bounds in signing process
 * Purpose: Reduce rejection rate, improve signing speed
 * 
 * Implementation Options:
 *   - Default: Increase BETA from 78 to 100 (parameter change only)
 *   - Option 1: Relax bounds by 2x (GAMMA2 - BETA*2)
 *   - Option 2: Probabilistic bypass (accept 10% of rejections)
 * 
 * To select option, uncomment in Makefile or config.h:
 *   - #define RELAXED_REJECTION_OPTION1
 *   - #define RELAXED_REJECTION_OPTION2
 * 
 * Expected Impact:
 *   - Default: -20% to -30% signing cycles
 *   - Option 1: -30% to -40% signing cycles (more relaxed)
 *   - Option 2: -15% to -25% signing cycles (probabilistic)
 */

 #ifndef CONFIG4_REJECTION_H
 #define CONFIG4_REJECTION_H
 
 // Configuration identifier
 #define CONFIG_ID 4
 #define CONFIG_NAME "Config4-RejectionSampling"
 #define CONFIG_DESCRIPTION "Dilithium2 with relaxed rejection bounds"
 
 // Dilithium variant
 #define DILITHIUM_MODE 2
 
 // Enable randomized signing (standard)
 #define DILITHIUM_RANDOMIZED_SIGNING
 
 // Hash function selection (keep original SHAKE256)
 #define USE_SHAKE256         // Use standard SHAKE256
 // #define USE_SHA3_256      // Not used in this config
 
 // Lattice parameters (Dilithium2 standard - UNCHANGED)
 #define K 4
 #define L 4
 #define ETA 2
 
 // Challenge polynomial parameters (UNCHANGED from baseline)
 #define TAU 39      // Number of ±1's in challenge
 #define OMEGA 80    // Maximum number of 1's in hint
 
 // Rounding parameters (UNCHANGED from baseline)
 #define GAMMA1 (1 << 17)      // 131072 - Low-order rounding range
 #define GAMMA2 ((Q-1)/88)     // 95232 - High-order rounding range
 
 // Rejection bound - ⭐ TWEAK 3
 #define BETA 100    // ⭐ MODIFIED: 78 → 100 (+28% increase)
                     // Relaxed rejection sampling bound
                     // Original: BETA = TAU * ETA = 39 * 2 = 78
                     // Modified: BETA = 100 (allows more signatures)
                     // Trade-off: Faster signing, potential size increase
 
 // Additional rejection sampling parameters
 #define REJECTION_MULTIPLIER 1.28  // BETA ratio: 100/78 = 1.28
 #define RELAXED_NORM_BOUND         // Flag for modified norm checks
 
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
 
 // Key and signature sizes (SAME as baseline)
 #define CRYPTO_PUBLICKEYBYTES (SEEDBYTES + K*POLYT1_PACKEDBYTES)
 #define CRYPTO_SECRETKEYBYTES (2*SEEDBYTES \
                                + TRBYTES \
                                + L*POLYETA_PACKEDBYTES \
                                + K*POLYETA_PACKEDBYTES \
                                + K*POLYT0_PACKEDBYTES)
 #define CRYPTO_BYTES (CTILDEBYTES + L*POLYZ_PACKEDBYTES + POLYVECH_PACKEDBYTES)
 // Signature size remains 2420 bytes (structure unchanged)
 
 // Algorithm selection macros
 #define CRYPTO_ALGNAME "Dilithium2-RejectionSampling"
 #define DILITHIUM_NAMESPACETOP pqcrystals_dilithium2_rejection_ref
 #define DILITHIUM_NAMESPACE(s) pqcrystals_dilithium2_rejection_ref_##s
 
 // Implementation notes:
 // - Modify chknorm() calls in sign.c
 // - Relax bound checking in rejection loop
 // - Accept signatures that would be rejected with BETA=78
 // - Monitor actual rejection rate in testing
 // - Verify correctness is maintained
 
 // Rejection sampling modifications:
 // 1. In sign.c, replace: if(chknorm(z, GAMMA1 - BETA))
 //    With: if(chknorm(z, GAMMA1 - BETA)) where BETA=100
 // 2. Accept more z candidates (looser L∞ norm bound)
 // 3. Still verify all other constraints (w1, ct0, etc.)
 
 // Performance expectations (estimated vs baseline):
 // Sign cycles: -20% to -30% (fewer rejections)
 // Verify cycles: Same (verification unchanged)
 // Signature size: 2420 bytes (no change in structure)
 // Rejection rate: -40% to -50% (fewer discarded attempts)
 // Average iterations: ~2-3 vs ~4-5 in baseline
 
 // Security considerations:
 // - Relaxed bound may slightly reduce security margin
 // - Must validate with lattice-estimator
 // - Check Core-SVP hardness is maintained
 // - Verify EUF-CMA security holds
 // - Expected: Still within NIST Level 2 (margin exists)
 
 // Trade-off analysis:
 // Pros:
 //   - Much faster signing (fewer wasted computations)
 //   - More predictable performance (less variance)
 //   - Better for real-time applications
 // Cons:
 //   - Slightly larger signature norm (in practice)
 //   - Potential minor security reduction (needs verification)
 //   - Deviation from NIST standard (compatibility concern)
 
 // Testing requirements:
 // 1. Measure actual rejection rate
 // 2. Compare signing speed improvement
 // 3. Analyze signature coefficient distributions
 // 4. Run lattice-estimator for security validation
 // 5. Verify interoperability (can baseline verify these?)
 
 // Rejection rate tracking (for benchmarking):
 // - Count total signing attempts
 // - Count successful signatures
 // - Calculate: rejection_rate = (attempts - 1) / attempts
 // - Compare: baseline ~60-70% vs tweaked ~20-30%
 
 // Correctness validation:
 // - All signatures must verify correctly
 // - Test with 10,000+ sign/verify cycles
 // - No false positives or negatives
 // - Cross-verify with baseline implementation
 
 #endif /* CONFIG4_REJECTION_H */