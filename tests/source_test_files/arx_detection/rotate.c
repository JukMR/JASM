#include <stdint.h>


// Rotation function for a 32-bit integer
uint32_t rotateLeft32(uint32_t x, int n) {
    return (x << n) | (x >> (32 - n));
}