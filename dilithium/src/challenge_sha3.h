/*
 * challenge_sha3.h
 * 
 * Header for SHA3-256 challenge generation (Tweak 1)
 */

 #ifndef CHALLENGE_SHA3_H
 #define CHALLENGE_SHA3_H
 
 #include <stdint.h>
 #include "params.h"
 #include "poly.h"
 
 /*
  * poly_challenge_sha3 - Generate challenge using SHA3-256
  * 
  * Arguments:
  *   - poly *c: output challenge polynomial
  *   - const uint8_t *seed: input seed (CTILDEBYTES bytes)
  */
 void poly_challenge_sha3(poly *c, const uint8_t seed[CTILDEBYTES]);
 
 /*
  * poly_challenge_sha3_streaming - Memory-efficient streaming version
  */
 void poly_challenge_sha3_streaming(poly *c, const uint8_t seed[CTILDEBYTES]);
 
 /*
  * challenge_sha3_self_test - Verify implementation correctness
  * 
  * Returns: 0 on success, -1 on failure
  */
 int challenge_sha3_self_test(void);
 
 #endif /* CHALLENGE_SHA3_H */