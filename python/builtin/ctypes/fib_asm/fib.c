#include <stdio.h>

unsigned long long fibC(unsigned long long n) {
  int a, b, c, i;
  a = 0;
  b = 1;
  i = 1;
  while (i != n) {
    c = a;
    a = a + b;
    b = c;
    i++;
  }
  return a;
}

unsigned long long fibASM(unsigned long long n) {
  unsigned long long result;
  asm(
    "pushq $0;"            // push(0)
    "pushq $1;"            // push(1)
    "movq $2, %%rcx;"      // i = 2

    "l1:"
    "popq %%rax;"          // A = pop()
    "popq %%rbx;"          // B = pop()
    "subq $16, %%rsp;"     // move stack pointer across the last two numbers not to overwrite
    "addq %%rbx, %%rax;"   // A = A + B
    "pushq %%rax;"         // push(a)
    "incq %%rcx;"          // i++
    "cmpq %%rcx, %1;"
    "jne l1;"              // i != %1 ? goto l1
    "popq %0;"             // $0 = pop()

    : "=r" (result)        // output -> result = $0
    : "r" (n)              // input -> $1 = n
    : "rax", "rbx", "rcx"  // don't mess with these registers, I'm using them
  );
  return result;
}

unsigned long long fibASMWithoutStack(unsigned long long n) {
  unsigned long long result;
  asm(
    "movq $0, %%rax;"      // A = 0
    "movq $1, %%rbx;"      // B = 1
    "movq $1, %%rdx;"      // i = 1

    "l2:"
    "movq %%rax, %%rcx;"   // C = A
    "addq %%rbx, %%rax;"   // A = A + B
    "movq %%rcx, %%rbx;"   // B = C
    "incq %%rdx;"          // i ++
    "cmpq %%rdx, %1;"
    "jne l2;"              // i != %1 ? goto l2
    "movq %%rax, %0;"      // %0 = A

    : "=r" (result)
    : "r" (n)
    : "rax", "rbx", "rcx", "rdx"
  );
  return result;
}
