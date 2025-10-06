/*
 * rejection_tweaked.h
 * 
 * Helper functions for modified rejection sampling (Tweak 3)
 */

 #ifndef REJECTION_TWEAKED_H
 #define REJECTION_TWEAKED_H
 
 #include <stdint.h>
 #include "randombytes.h"
 
 #ifdef RELAXED_REJECTION
 
 /*
  * Rejection sampling options:
  * - RELAXED_REJECTION_OPTION1: Relax bounds (BETA*2)
  * - RELAXED_REJECTION_OPTION2: Probabilistic bypass (10% acceptance)
  * - Default: Simple BETA increase (from params_tweaked.h)
  */
 
 #ifdef RELAXED_REJECTION_OPTION2
 /*
  * should_bypass_rejection - Probabilistic rejection bypass
  * 
  * Returns: 1 to bypass rejection (accept), 0 to reject normally
  * 
  * Implementation: 10% acceptance rate (bypass % 10 == 0)
  */
 static inline int should_bypass_rejection(void) {
     uint8_t bypass;
     randombytes(&bypass, 1);
     return (bypass % 10 == 0);  // True 10% of the time
 }
 #endif /* RELAXED_REJECTION_OPTION2 */
 
 /*
  * Rejection statistics tracking (optional, for testing)
  */
 #ifdef DEBUG_REJECTION_STATS
 typedef struct {
     unsigned int total_attempts;
     unsigned int rejections;
     unsigned int bypassed;
 } rejection_stats_t;
 
 extern rejection_stats_t rejection_stats;
 
 static inline void reset_rejection_stats(void) {
     rejection_stats.total_attempts = 0;
     rejection_stats.rejections = 0;
     rejection_stats.bypassed = 0;
 }
 
 static inline void print_rejection_stats(void) {
     printf("Rejection Statistics:\n");
     printf("  Total attempts: %u\n", rejection_stats.total_attempts);
     printf("  Rejections: %u\n", rejection_stats.rejections);
     printf("  Bypassed: %u\n", rejection_stats.bypassed);
     printf("  Rejection rate: %.2f%%\n", 
            100.0 * rejection_stats.rejections / rejection_stats.total_attempts);
 }
 #endif /* DEBUG_REJECTION_STATS */
 
 #endif /* RELAXED_REJECTION */
 
 #endif /* REJECTION_TWEAKED_H */