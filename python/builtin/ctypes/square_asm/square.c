#include <stdio.h>

int square_c(int n) {
  int result;
  __asm__(
    "movl %1, %%eax;"
    "mull %%eax;"
    "movl %%eax, %0;"
    : "=r" (result)
    : "r" (n)
  );
  return result;
}