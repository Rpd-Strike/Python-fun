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

      print("progress: ", int(100.0 * i / lim))

    i += 1
  return ans

print("enter number to calculate phi:\n")
n = int(input())
sol = phi(n)
print(sol)

