/*
 * CONFIG 3: TWEAK 2 - CHALLENGE BOUNDS
 * 
 * Modify challenge polynomial coefficient bounds
 * Purpose: Test impact of challenge weight on performance/security
 * 
 * Changes:
 *   - TAU: 39 → 50 (+28% increase in challenge weight)
 *   - OMEGA: 80 → 70 (-12.5% decrease in hint weight)
 * 
 * Expected Impact:
 *   - Sign cycles: Increased (more rejection iterations)
 *   - Verify cycles: Slightly decreased (fewer hints to check)
 *   - Signature size: Potentially smaller (fewer hint bits)
 *   - Security: Requires validation via lattice-estimator
 */

 #ifndef CONFIG3_CHALLENGE_H
 #define CONFIG3_CHALLENGE_H
 
 // Configuration identifier
 #define CONFIG_ID 3
 #define CONFIG_NAME "Config3-ChallengeBounds"
 #define CONFIG_DESCRIPTION "Dilithium2 with modified TAU and OMEGA"
 
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
 
 // Challenge polynomial parameters - ⭐ TWEAK 2
 #define TAU 50      // ⭐ MODIFIED: 39 → 50 (+28% increase)
                     // Number of ±1's in challenge polynomial
                     // Higher TAU = more uniform challenge distribution
                     // Trade-off: Slower signing (more rejections)
 
 #define OMEGA 70    // ⭐ MODIFIED: 80 → 70 (-12.5% decrease)
                     // Maximum number of 1's in hint polynomial
                     // Lower OMEGA = smaller signatures
                     // Trade-off: Tighter verification constraints
 
 // Rounding parameters (UNCHANGED from baseline)
 #define GAMMA1 (1 << 17)      // 131072 - Low-order rounding range
 #define GAMMA2 ((Q-1)/88)     // 95232 - High-order rounding range
 
 // Rejection bound - UPDATED based on new TAU
 #define BETA 100    // ⭐ MODIFIED: 78 → 100 (TAU * ETA = 50 * 2)
                     // Rejection sampling bound
                     // Must be adjusted when TAU changes
 
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
 
 // Hint packing - AFFECTED by OMEGA change
 #define POLYVECH_PACKEDBYTES (OMEGA + K)  // 70 + 4 = 74 bytes
                                           // vs baseline: 80 + 4 = 84 bytes
                                           // Savings: 10 bytes per signature
 
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
 
 // Signature size - AFFECTED by OMEGA change
 #define CRYPTO_BYTES (CTILDEBYTES + L*POLYZ_PACKEDBYTES + POLYVECH_PACKEDBYTES)
 // = 32 + 4*576 + 74 = 2410 bytes (vs baseline 2420 bytes)
 // Reduction: 10 bytes (~0.4%)
 
 // Algorithm selection macros
 #define CRYPTO_ALGNAME "Dilithium2-ChallengeBounds"
 #define DILITHIUM_NAMESPACETOP pqcrystals_dilithium2_challenge_ref
 #define DILITHIUM_NAMESPACE(s) pqcrystals_dilithium2_challenge_ref_##s
 
 // Implementation notes:
 // - Modified TAU affects challenge polynomial generation
 // - Sample_in_ball() function must handle TAU=50
 // - More ±1 coefficients = better randomness but slower
 // - OMEGA reduction means stricter hint requirements
 // - May increase rejection rate in signing
 
 // Performance expectations (estimated vs baseline):
 // Sign cycles: +15% to +25% (more rejections due to higher TAU)
 // Verify cycles: -2% to -5% (fewer hints to check)
 // Signature size: 2410 bytes (vs 2420 baseline, -10 bytes)
 // Rejection rate: +20% to +30% (tighter constraints)
 
 // Security considerations:
 // - Higher TAU: Better challenge distribution
 // - Lower OMEGA: Need to verify security margin maintained
 // - Must run lattice-estimator to confirm Core-SVP hardness
 // - Expected: Same or slightly better security level
 // - Trade-off: Performance cost for potential security gain
 
 // Parameter validation:
 // TAU must be: 1 ≤ TAU ≤ N (256)
 // OMEGA must be: K ≤ OMEGA ≤ N*K
 // BETA should equal: TAU * ETA (for consistency)
 // All constraints satisfied: ✓
 
 // Testing requirements:
 // 1. Verify correctness with known test vectors
 // 2. Measure rejection rate increase
 // 3. Confirm signature size reduction
 // 4. Validate security with lattice-estimator
 // 5. Compare performance vs baseline
 
 #endif /* CONFIG3_CHALLENGE_H */