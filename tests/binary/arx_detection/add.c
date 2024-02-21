#include <stdint.h>


// Addition function for two elements of the array
void add(int64_t* x, int64_t a, int64_t b) {
    x[a] += x[b];
}