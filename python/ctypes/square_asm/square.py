from ctypes import CDLL
from os import system

# def compile (c_file, asm_files):
#   for file in asm_files:
#     system(f"nasm -f elf64 {file}.asm")
#   system(f"cc ./{c_file}.c {' '.join(f'./{file}.o' for file in asm_files)} -o {c_file}")

# compile('helloworld', ['helloworld'])

def compile(filename):
  system(f'cc -fPIC -shared -o {filename}.so {filename}.c')

# compile("./square")
prog = CDLL('./square.so')
print(prog.square_c(10))