#include <stdint.h>

// Rotation function (already provided)
static uint32_t rotl32(uint32_t x, int n) {
    return (x << n) | (x >> (32 - n));
}

// Addition function
void add(int64_t* x, int64_t a, int64_t b) {
    x[a] += x[b];
}

// XOR and Rotate function
void xorAndRotate(int64_t* x, int64_t a, int64_t d, int n) {
    x[d] = rotl32(x[d] ^ x[a], n);
}

// Refactored main function using the split operations
int64_t* fun(int64_t* x, int64_t a, int64_t b, int64_t c, int64_t d) {
    add(x, a, b); // Perform the addition
    xorAndRotate(x, a, d, 16); // Perform XOR and rotation

    return x;
}