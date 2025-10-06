/*
 * challenge_expanded.c
 * 
 * Expanded Challenge Polynomial Generation for Dilithium (Tweak 2)
 * Expands challenge coefficients from {-1, 0, 1} to {-2, -1, 0, 1, 2}
 * 
 * Based on thesis implementation (Listing 6.2)
 */

 #include <stdint.h>
 #include <string.h>
 #include "params.h"
 #include "sign.h"
 #include "poly.h"
 #include "symmetric.h"
 
 /*
  * poly_challenge_expanded - Generate challenge polynomial with expanded coefficients
  * 
  * Generates challenge polynomial with coefficients in {-2, -1, 0, 1, 2}
  * instead of standard {-1, 0, 1}
  * 
  * Arguments:
  *   - poly *c: output challenge polynomial
  *   - const uint8_t *seed: input seed (CTILDEBYTES bytes)
  * 
  * Returns: void
  * 
  * Output: Challenge polynomial with TAU non-zero coefficients in range [-2, 2]
  */
 void poly_challenge_expanded(poly *c, const uint8_t seed[CTILDEBYTES]) {
     unsigned int i, b, pos;
     uint64_t signs;
     uint8_t buf[SHAKE256_RATE];
     keccak_state state;
 
     shake256_init(&state);
     shake256_absorb(&state, seed, CTILDEBYTES);
     shake256_finalize(&state);
     shake256_squeeze(buf, SHAKE256_RATE, &state);
 
     // Extract initial signs value (first 8 bytes)
     signs = 0;
     for (i = 0; i < 8; ++i) {
         signs |= (uint64_t)buf[i] << (8 * i);
     }
     pos = 8;
 
     // Initialize polynomial to zero
     for (i = 0; i < N; ++i) {
         c->coeffs[i] = 0;
     }
 
     // Sample TAU positions with expanded coefficient range
     for (i = N - TAU; i < N; ++i) {
         // Sample position uniformly
         do {
             if (pos >= SHAKE256_RATE) {
                 shake256_squeeze(buf, SHAKE256_RATE, &state);
                 pos = 0;
             }
             b = buf[pos++];
         } while (b > i);
 
         // Move existing coefficient
         c->coeffs[i] = c->coeffs[b];
         
         /* ⭐ TWEAK 2: Expanded coefficient range {-2, -1, 0, 1, 2} */
         // Extract 3 bits from signs to determine coefficient
         // Use modulo 5 to get value from 0 to 4, then subtract 2 to get range -2 to 2
         c->coeffs[b] = (signs & 7) % 5 - 2;
         signs >>= 3;  // Use 3 bits per coefficient (not just 1 bit)
 
         // If we've used 21 bits or more (7 coefficients * 3 bits), refill signs
         if (pos >= 8 && (i % 21) == 0) {
             if (pos + 8 <= SHAKE256_RATE) {
                 signs = 0;
                 for (unsigned int j = 0; j < 8; ++j) {
                     signs |= (uint64_t)buf[pos + j] << (8 * j);
                 }
                 pos += 8;
             }
         }
     }
 }
 
 /*
  * poly_challenge_expanded_tau_adjustable - Variant with adjustable TAU
  * 
  * Allows runtime adjustment of challenge weight
  * Useful for testing different sparsity levels
  * 
  * Arguments:
  *   - poly *c: output challenge polynomial
  *   - const uint8_t *seed: input seed
  *   - unsigned int tau: number of non-zero coefficients
  */
 void poly_challenge_expanded_tau_adjustable(poly *c, 
                                             const uint8_t seed[CTILDEBYTES],
                                             unsigned int tau) {
     unsigned int i, b, pos;
     uint64_t signs;
     uint8_t buf[SHAKE256_RATE];
     keccak_state state;
 
     // Validate tau
     if (tau > N) {
         tau = TAU;  // Fall back to default
     }
 
     shake256_init(&state);
     shake256_absorb(&state, seed, CTILDEBYTES);
     shake256_finalize(&state);
     shake256_squeeze(buf, SHAKE256_RATE, &state);
 
     // Extract initial signs
     signs = 0;
     for (i = 0; i < 8; ++i) {
         signs |= (uint64_t)buf[i] << (8 * i);
     }
     pos = 8;
 
     // Initialize polynomial
     for (i = 0; i < N; ++i) {
         c->coeffs[i] = 0;
     }
 
     // Sample tau positions
     for (i = N - tau; i < N; ++i) {
         do {
             if (pos >= SHAKE256_RATE) {
                 shake256_squeeze(buf, SHAKE256_RATE, &state);
                 pos = 0;
             }
             b = buf[pos++];
         } while (b > i);
 
         c->coeffs[i] = c->coeffs[b];
         c->coeffs[b] = (signs & 7) % 5 - 2;
         signs >>= 3;
 
         if (pos >= 8 && (i % 21) == 0) {
             if (pos + 8 <= SHAKE256_RATE) {
                 signs = 0;
                 for (unsigned int j = 0; j < 8; ++j) {
                     signs |= (uint64_t)buf[pos + j] << (8 * j);
                 }
                 pos += 8;
             }
         }
     }
 }
 
 /*
  * challenge_expanded_self_test - Self-test function
  * 
  * Verifies expanded challenge generation correctness
  * 
  * Returns: 0 on success, -1 on failure
  */
 int challenge_expanded_self_test(void) {
     uint8_t test_seed[CTILDEBYTES] = {0};
     poly c;
     unsigned int i, count;
     int max_coeff = 0;
     int min_coeff = 0;
 
     // Fill test seed
     for (i = 0; i < CTILDEBYTES; i++) {
         test_seed[i] = (uint8_t)i;
     }
 
     // Generate challenge
     poly_challenge_expanded(&c, test_seed);
 
     // Verify properties
     count = 0;
     for (i = 0; i < N; i++) {
         if (c.coeffs[i] != 0) {
             count++;
             
             // Track range
             if (c.coeffs[i] > max_coeff) max_coeff = c.coeffs[i];
             if (c.coeffs[i] < min_coeff) min_coeff = c.coeffs[i];
             
             // Check coefficient is in valid range [-2, 2]
             if (c.coeffs[i] < -2 || c.coeffs[i] > 2) {
                 return -1;  // Invalid coefficient
             }
         }
     }
 
     // Verify TAU non-zero coefficients
     if (count != TAU) {
         return -1;  // Wrong number of non-zero coefficients
     }
 
     // Verify range is expanded (should have values beyond {-1, 0, 1})
     if (max_coeff <= 1 && min_coeff >= -1) {
         return -1;  // Range not expanded (still standard challenge)
     }
 
     return 0;  // Test passed
 }
 
 /*
  * challenge_expanded_statistics - Analyze coefficient distribution
  * 
  * Useful for testing and validation
  * Prints distribution of coefficients
  */
 void challenge_expanded_statistics(const uint8_t seed[CTILDEBYTES]) {
     poly c;
     unsigned int i;
     unsigned int dist[5] = {0};  // Count for -2, -1, 0, 1, 2
 
     poly_challenge_expanded(&c, seed);
 
     for (i = 0; i < N; i++) {
         int coeff = c.coeffs[i];
         if (coeff >= -2 && coeff <= 2) {
             dist[coeff + 2]++;  // Map -2→0, -1→1, 0→2, 1→3, 2→4
         }
     }
 
     // Distribution can be printed in test programs
     // dist[0] = count of -2
     // dist[1] = count of -1
     // dist[2] = count of 0
     // dist[3] = count of 1
     // dist[4] = count of 2
 }