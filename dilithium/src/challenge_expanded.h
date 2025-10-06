/*
 * challenge_expanded.h
 * 
 * Header for Expanded Challenge Polynomial Generation (Tweak 2)
 */

 #ifndef CHALLENGE_EXPANDED_H
 #define CHALLENGE_EXPANDED_H
 
 #include <stdint.h>
 #include "params.h"
 #include "poly.h"
 
 /*
  * poly_challenge_expanded - Generate challenge with expanded coefficients
  * 
  * Creates challenge polynomial with coefficients in {-2, -1, 0, 1, 2}
  * instead of standard {-1, 0, 1}
  * 
  * Arguments:
  *   - poly *c: output challenge polynomial
  *   - const uint8_t *seed: input seed (CTILDEBYTES bytes)
  */
 void poly_challenge_expanded(poly *c, const uint8_t seed[CTILDEBYTES]);
 
 /*
  * poly_challenge_expanded_tau_adjustable - Generate with custom TAU
  * 
  * Allows runtime adjustment of challenge weight
  * 
  * Arguments:
  *   - poly *c: output challenge polynomial
  *   - const uint8_t *seed: input seed
  *   - unsigned int tau: number of non-zero coefficients
  */
 void poly_challenge_expanded_tau_adjustable(poly *c, 
                                             const uint8_t seed[CTILDEBYTES],
                                             unsigned int tau);
 
 /*
  * challenge_expanded_self_test - Verify implementation correctness
  * 
  * Returns: 0 on success, -1 on failure
  */
 int challenge_expanded_self_test(void);
 
 /*
  * challenge_expanded_statistics - Analyze coefficient distribution
  * 
  * Useful for testing and validation
  */
 void challenge_expanded_statistics(const uint8_t seed[CTILDEBYTES]);
 
 #endif /* CHALLENGE_EXPANDED_H */