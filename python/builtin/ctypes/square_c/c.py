from ctypes import CDLL
from os import system

def compile(filename):
  system(f'cc -fPIC -shared -o {filename}.so {filename}.c')

compile('square')
c_file = CDLL('./square.so')
print(c_file.square_c(10))
