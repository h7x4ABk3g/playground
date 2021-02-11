# ctypes

So python isn't fast enough for you, huh?

These are some tests to try to outsource code to C, and from C to Assembly.

 - square_c -> a function to square a number from C
 - square_asm -> a function to square a number from Assembly through C
 - fib_asm -> Different fibonacci functions and time testing (the jupyter %timeit is a slightly better measurement)
 - c_exporter -> Self modifying code. Write everything in python. First makes a C file from a string, then compiles it, then goes on to remove all the unnecessary code from itself (C source, compilation commands, self removal code, etc.) in order to be as efficient as possible on the next run.
