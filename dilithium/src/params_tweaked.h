/*
 * params_tweaked.h
 * 
 * Parameter overrides for Dilithium Tweaks 2 & 3
 * This file is included AFTER params.h to override specific parameters
 * based on the active configuration.
 * 
 * Usage: Include at end of params.h or in compilation
 */

 #ifndef PARAMS_TWEAKED_H
 #define PARAMS_TWEAKED_H
 
 #include "config.h"
 
 /* 
  * Configuration-based parameter overrides
  * These override the standard Dilithium2 parameters when specific
  * tweaks are active
  */
 
 #ifdef MODIFIED_CHALLENGE_BOUNDS
 /*
  * TWEAK 2: Modified Challenge Bounds
  * 
  * Changes:
  *   - TAU: 39 → 50 (increase challenge polynomial weight)
  *   - OMEGA: 80 → 70 (decrease hint polynomial weight)
  *   - BETA: Must be adjusted to maintain consistency
  * 
  * Impact:
  *   - More uniform challenge distribution
  *   - Smaller signature size (fewer hints)
  *   - Potentially slower signing (more rejections)
  */
 
 #undef TAU
 #define TAU 50
 
 #undef OMEGA
 #define OMEGA 70
 
 #undef BETA
 #define BETA 100  // TAU * ETA = 50 * 2 = 100
 
 // Update derived parameters
 #undef POLYVECH_PACKEDBYTES
 #define POLYVECH_PACKEDBYTES (OMEGA + K)  // 70 + 4 = 74
 
 // Signature size changes
 #undef CRYPTO_BYTES
 #define CRYPTO_BYTES (CTILDEBYTES + L*POLYZ_PACKEDBYTES + POLYVECH_PACKEDBYTES)
 // = 32 + 4*576 + 74 = 2410 bytes (vs 2420 baseline)
 
 #endif /* MODIFIED_CHALLENGE_BOUNDS */
 
 
 #ifdef RELAXED_REJECTION
 /*
  * TWEAK 3: Relaxed Rejection Sampling
  * 
  * Changes:
  *   - BETA: 78 → 100 (relax rejection bound)
  * 
  * Impact:
  *   - Fewer rejection iterations
  *   - Faster signing (20-30% expected improvement)
  *   - Slightly larger signature norms (still within bounds)
  * 
  * Note: This only affects signing performance, not signature size
  */
 
 #undef BETA
 #define BETA 100  // Relaxed from 78
 
 // Define relaxation ratio for analysis
 #define BETA_RELAXATION_RATIO 1.282  // 100/78
 
 #endif /* RELAXED_REJECTION */
 
 
 /*
  * Validation checks
  * Ensure parameter changes maintain scheme validity
  */
 
 #if defined(MODIFIED_CHALLENGE_BOUNDS) && defined(RELAXED_REJECTION)
 #error "Cannot enable both MODIFIED_CHALLENGE_BOUNDS and RELAXED_REJECTION simultaneously"
 #endif
 
 #if defined(TAU) && (TAU < 1 || TAU > N)
 #error "TAU must be between 1 and N (256)"
 #endif
 
 #if defined(OMEGA) && (OMEGA < K || OMEGA > N*K)
 #error "OMEGA must be between K and N*K"
 #endif
 
 #if defined(BETA) && BETA < TAU * ETA
 #warning "BETA should typically equal TAU * ETA for consistency"
 #endif
 
 /*
  * Debug information (enabled with -DDEBUG_PARAMS)
  */
 #ifdef DEBUG_PARAMS
 #pragma message "Dilithium Parameter Configuration:"
 #pragma message "  TAU = " STRINGIZE(TAU)
 #pragma message "  OMEGA = " STRINGIZE(OMEGA)
 #pragma message "  BETA = " STRINGIZE(BETA)
 #pragma message "  GAMMA1 = " STRINGIZE(GAMMA1)
 #pragma message "  GAMMA2 = " STRINGIZE(GAMMA2)
 #endif
 
 #endif /* PARAMS_TWEAKED_H */