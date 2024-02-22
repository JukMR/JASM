#include <stdint.h>
#include <stdio.h>


// XOR function for two elements of the array
void xor(int64_t* x, int64_t a, int64_t d) {
    x[d] ^= x[a];
}