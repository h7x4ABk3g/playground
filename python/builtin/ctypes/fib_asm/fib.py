from ctypes import CDLL
from os import system
from timeit import timeit

import time

def compile(filename):
  system(f'cc -fPIC -shared -o {filename}.so {filename}.c')

def fib_py(n):
  a = 1
  b = 0
  i = 0
  while i != n - 1:
    c = a
    a = a + b
    b = c
    i += 1
  return b

num = 47
compile("./fib")
prog = CDLL('./fib.so')

timesToTest = 1000000

pyResult = fib_py(num)
pyTime = timeit( 'fib_py(num)'
               , setup='from __main__ import fib_py, num'
               , number=timesToTest
               )

prog_setup = 'from __main__ import prog, num'

cResult = prog.fibC(num)
cTime = timeit( 'prog.fibC(num)'
               , setup=prog_setup
               , number=timesToTest
               )

asmResult = prog.fibASM(num)
asmTime = timeit( 'prog.fibASM(num)'
               , setup=prog_setup
               , number=timesToTest
               )

rasmResult = prog.fibASMWithoutStack(num)
rasmTime = timeit( 'prog.fibASMWithoutStack(num)'
               , setup=prog_setup
               , number=timesToTest
               )

print(f'[PY]        [{"{:.3f}".format(pyTime)}μs]: {pyResult}')
print(f'[C]         [{"{:.3f}".format(cTime)}μs]: {cResult}')
print(f'[ASM WS]    [{"{:.3f}".format(asmTime)}μs]: {asmResult}')
print(f'[ASM W/O S] [{"{:.3f}".format(rasmTime)}μs]: {rasmResult}')
