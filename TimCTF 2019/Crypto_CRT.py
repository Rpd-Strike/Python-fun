from functools import reduce
import socket

def chinese_remainder(numbers, remainders):
  ssum = 0
  n = numbers
  a = remainders
  prod = reduce(lambda a, b: a*b, n)
  for n_i, a_i in zip(n, a):
      p = prod // n_i
      ssum += a_i * mul_inv(p, n_i) * p
  return ssum % prod 
 
def mul_inv(a, b):
  b0 = b
  x0, x1 = 0, 1
  if b == 1: return 1
  while a > 1:
      q = a // b
      a, b = b, a%b
      x0, x1 = x1 - q * x0, x0
  if x1 < 0: x1 += b0
  return x1

def num_raised_modulo(base, power, modulo):  
  if power == 0:
    return 1
  if power == 1:
    return base
  else:
    t = num_raised_modulo(base, power // 2, modulo)
    t = t * t % modulo
    if power & 1:
      t = t * base % modulo
    return t

# phi of a prime^4
def myphi(p4):
  return (p4 - 1) * (p4**3)

# general phi
def phi(n):
  ans = n
  lim = int((n ** 0.5) + 1)
  i = 2
  while i <= lim:
    ok = False
    while n % i == 0:
      n = n // i
      ok = True
    if ok:
      ans = ans // i
      ans *= (i - 1)
      lim = int(n ** 0.5) + 1
    i += 1
  return ans

def modify_once(rest, p, power):
  # i know rest = t^2019 mod p, where p = prime^4, find r = t mod p
  # multiply with inverse of 2019 with respect to myphi(p)
  to_mul = num_raised_modulo(power, phi(myphi(p)) - 1, myphi(p))
  rest = num_raised_modulo(rest, to_mul, p)
  return rest

def modify_twice(rest, p):
  # i know rest = t^(2019^2019) mod p, p = prime^4, find r = t mod p
  # first, find 2019^2019 modulo phi(p), cause thats the period of the function
  my_pow = num_raised_modulo(2019, 2019, myphi(p))
  return modify_once(rest, p, my_pow)


def test(sol, bases, remainders):
  nr = [sol % x for x in bases]
  
  nr[1] = (nr[1] ** 2019) % bases[1]
  
  le_pow = num_raised_modulo(2019, 2019, myphi(bases[2]))
  nr[2] = num_raised_modulo(nr[2], le_pow, bases[2])

  print("should be 1: ", num_raised_modulo(nr[2], myphi(bases[2]), bases[2]))

  for i in range(len(bases)):
    rem = nr[i] % bases[i]
    print("rest ", i + 1, ":  ", rem)



p = [492876863, 472882049, 573259391]
p4 = [x*x*x*x for x in p]
resturi = [53994433445527579909840621536093364, \
           36364162229311278067416695130494243, \
           31003636792624845072184744558108878]
old_rest = [x for x in resturi]

print("need phi: ", myphi(p4[1]), "  and  ", myphi(p4[2]))

# resturi[0] este ok
print("rest 2:")
# resturi[1] recampute
resturi[1] = modify_once(resturi[1], p4[1], 2019)

print("\n rest 3")
# resturi[2] recompute
resturi[2] = modify_twice(resturi[2], p4[2])

solution = chinese_remainder(p4, resturi)
print("solution: ", solution)

test(solution, p4, old_rest)

print(old_rest, resturi)