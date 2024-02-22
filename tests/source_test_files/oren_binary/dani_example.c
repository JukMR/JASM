#include <stdint.h>

extern int* pepe;

int* fun(int64_t x)
{
    return pepe + 3 * x + 1;
}