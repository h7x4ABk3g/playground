from multiprocessing import Pool
from sympy import isprime
from time import time

SPLITS = 100
RANGE = 100000

def primes(nums):
  """returns all primes in nums"""
  return [num for num in nums if isprime(num)]

def asyncP():
  timeStart = time()

  pool = Pool()
  inputs = [range(i*RANGE, (i+1)*RANGE) for i in range(SPLITS)]
  outputs_async = pool.map_async(primes, inputs)
  outputs = outputs_async.get()
  outputs = (item for lst in outputs for item in lst)

  timeEnd = time()
  return outputs, (timeEnd - timeStart)

def syncP():
  timeStart = time()
  primes = [num for num in range(RANGE*SPLITS) if isprime(num)]
  timeEnd = time()
  return primes, (timeEnd - timeStart)

if __name__ == "__main__":
  a = asyncP()
  b = syncP()
  print("Equal:", a[0] == b[0])
  print("Time async:", a[1])
  print("Time sync:", b[1])
