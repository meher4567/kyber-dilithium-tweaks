/*
 * challenge_sha3.c
 * 
 * SHA3-256 Challenge Generation for Dilithium (Tweak 1)
 * Replaces SHAKE256 with SHA3-256 for challenge polynomial
 * 
 * Based on thesis implementation (Listing 6.1)
 * Uses OpenSSL EVP interface with 4-iteration domain separation
 */

 #include <stdint.h>
 #include <string.h>
 #include <openssl/evp.h>
 #include <openssl/sha.h>
 #include "params.h"
 #include "sign.h"
 #include "poly.h"
 
 /*
  * poly_challenge_sha3 - Generate challenge polynomial using SHA3-256
  * 
  * Replaces the standard SHAKE256-based challenge generation
  * Uses 4 iterations of SHA3-256 with counter for domain separation
  * 
  * Arguments:
  *   - poly *c: output challenge polynomial
  *   - const uint8_t *seed: input seed (CTILDEBYTES bytes)
  * 
  * Returns: void
  * 
  * Output: Challenge polynomial with TAU non-zero coefficients (±1)
  */
 void poly_challenge_sha3(poly *c, const uint8_t seed[CTILDEBYTES]) {
     unsigned int i, b, pos;
     uint64_t signs;
     uint8_t buf[SHA3_TOTAL_BYTES];  // 128 bytes = 4 * 32
     uint8_t hash_input[CTILDEBYTES + 4];
     uint8_t counter[4] = {0, 0, 0, 0};
     EVP_MD_CTX *mdctx;
     const EVP_MD *md;
     unsigned int md_len;
 
     // Initialize OpenSSL hash context
     mdctx = EVP_MD_CTX_new();
     if (mdctx == NULL) {
         // Handle error - should not happen in normal operation
         return;
     }
     
     md = EVP_sha3_256();
 
     // Copy seed to hash input
     memcpy(hash_input, seed, CTILDEBYTES);
 
     // Initial hash (iteration 0)
     EVP_DigestInit_ex(mdctx, md, NULL);
     EVP_DigestUpdate(mdctx, seed, CTILDEBYTES);
     EVP_DigestFinal_ex(mdctx, buf, &md_len);
 
     // Fill buffer with additional hashes for more randomness
     for (i = 1; i < SHA3_ITERATIONS; i++) {
         // Update counter for domain separation
         counter[0] = i;
         
         // Append counter to seed
         memcpy(hash_input + CTILDEBYTES, counter, 4);
         
         // Hash the seed + counter
         EVP_DigestInit_ex(mdctx, md, NULL);
         EVP_DigestUpdate(mdctx, hash_input, CTILDEBYTES + 4);
         EVP_DigestFinal_ex(mdctx, buf + (i * SHA3_OUTPUT_BYTES), &md_len);
     }
 
     // Clean up OpenSSL context
     EVP_MD_CTX_free(mdctx);
 
     // Extract signs from first 8 bytes
     signs = 0;
     for (i = 0; i < 8; ++i) {
         signs |= (uint64_t)buf[i] << (8 * i);
     }
 
     // Initialize polynomial to zero
     for (i = 0; i < N; ++i) {
         c->coeffs[i] = 0;
     }
 
     // Sample TAU positions and assign signs
     for (i = N - TAU, pos = 8; i < N; ++i) {
         // Sample position uniformly
         do {
             if (pos >= SHA3_TOTAL_BYTES) {
                 // Should not happen with 128 bytes, but safety check
                 pos = 8; // Reset if needed
             }
             b = buf[pos++];
         } while (b > i);
 
         // Set coefficient at sampled position
         c->coeffs[i] = c->coeffs[b];
         c->coeffs[b] = 1 - 2 * (signs & 1);
         signs >>= 1;
     }
 }
 
 /*
  * poly_challenge_sha3_streaming - Alternative streaming version
  * 
  * More memory efficient for constrained environments
  * Generates hash on-demand rather than buffering all 128 bytes
  * 
  * (Optional implementation - can be used if memory is concern)
  */
 void poly_challenge_sha3_streaming(poly *c, const uint8_t seed[CTILDEBYTES]) {
     unsigned int i, j, b, pos;
     uint64_t signs;
     uint8_t hash_output[SHA3_OUTPUT_BYTES];
     uint8_t hash_input[CTILDEBYTES + 4];
     uint8_t counter[4] = {0, 0, 0, 0};
     uint8_t *current_hash;
     EVP_MD_CTX *mdctx;
     const EVP_MD *md;
     unsigned int md_len;
 
     mdctx = EVP_MD_CTX_new();
     if (mdctx == NULL) {
         return;
     }
     
     md = EVP_sha3_256();
     memcpy(hash_input, seed, CTILDEBYTES);
 
     // First hash for signs
     EVP_DigestInit_ex(mdctx, md, NULL);
     EVP_DigestUpdate(mdctx, seed, CTILDEBYTES);
     EVP_DigestFinal_ex(mdctx, hash_output, &md_len);
 
     // Extract signs
     signs = 0;
     for (i = 0; i < 8; ++i) {
         signs |= (uint64_t)hash_output[i] << (8 * i);
     }
 
     // Initialize polynomial
     for (i = 0; i < N; ++i) {
         c->coeffs[i] = 0;
     }
 
     // Sample positions using streaming hashes
     pos = 8;
     j = 0; // Current hash iteration
     current_hash = hash_output;
 
     for (i = N - TAU; i < N; ++i) {
         do {
             if (pos >= SHA3_OUTPUT_BYTES) {
                 // Need next hash iteration
                 j++;
                 if (j >= SHA3_ITERATIONS) {
                     j = 0; // Wrap around if needed (shouldn't happen)
                 }
                 
                 counter[0] = j;
                 memcpy(hash_input + CTILDEBYTES, counter, 4);
                 
                 EVP_DigestInit_ex(mdctx, md, NULL);
                 EVP_DigestUpdate(mdctx, hash_input, CTILDEBYTES + 4);
                 EVP_DigestFinal_ex(mdctx, hash_output, &md_len);
                 
                 pos = (j == 0) ? 8 : 0; // Skip first 8 bytes only in iteration 0
             }
             b = current_hash[pos++];
         } while (b > i);
 
         c->coeffs[i] = c->coeffs[b];
         c->coeffs[b] = 1 - 2 * (signs & 1);
         signs >>= 1;
     }
 
     EVP_MD_CTX_free(mdctx);
 }
 
 /*
  * challenge_sha3_self_test - Self-test function
  * 
  * Verifies SHA3-256 challenge generation correctness
  * Can be called during initialization or testing
  * 
  * Returns: 0 on success, -1 on failure
  */
 int challenge_sha3_self_test(void) {
     uint8_t test_seed[CTILDEBYTES] = {0};
     poly c;
     unsigned int i, count;
 
     // Fill test seed with pattern
     for (i = 0; i < CTILDEBYTES; i++) {
         test_seed[i] = (uint8_t)i;
     }
 
     // Generate challenge
     poly_challenge_sha3(&c, test_seed);
 
     // Verify properties
     // 1. Exactly TAU non-zero coefficients
     count = 0;
     for (i = 0; i < N; i++) {
         if (c.coeffs[i] != 0) {
             count++;
             // 2. All non-zero coefficients are ±1
             if (c.coeffs[i] != 1 && c.coeffs[i] != -1 && 
                 c.coeffs[i] != Q - 1) { // -1 mod Q
                 return -1; // Invalid coefficient
             }
         }
     }
 
     if (count != TAU) {
         return -1; // Wrong number of non-zero coefficients
     }
 
     return 0; // Test passed
 }