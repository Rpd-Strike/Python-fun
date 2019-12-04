import socket
import time

MOD = 666013

def mat_mult(a, b):
  r = [[0 for i in range(len(b[0]))] for i in range(len(a))]
  for i in range(len(a)):
    for j in range(len(b[0])):
      for k in range(len(b)):
        r[i][j] = (r[i][j] + a[i][k] * b[k][j]) % MOD
  return r

def lgpow(b, p):
	if p == 1:
		return b
	else:
		t = lgpow(b, p // 2)
		t = mat_mult(t, t)
		if p & 1:
			t = mat_mult(t, b)
		return t

def get_ans(N, K, start, coef):
  mat = [[0 for _ in range(N)] for j in range(N)]
  for i in range(N - 1):
    mat[i + 1][i] = 1
  for i in range(N):
    mat[i][N - 1] = coef[i]
  numbers = [[a for a in start]]

  mat = lgpow(mat, K - N)
  numbers = mat_mult(numbers, mat)

  return numbers[0][-1]

start_time = time.time()

HOST = '89.38.208.143'  # The server's hostname or IP address
PORT = 22022        # The port used by the server

def read_line(sock):
  line = sock.recv(1).decode('utf-8')
  while line[-1] != '\n':
    line += sock.recv(1).decode('utf-8')
  return line[:-1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  sock.connect((HOST, PORT))

  print(read_line(sock))

  for _ in range(10):
    print("TEST: " + str(_ + 1))

    read_line(sock)

    N, K = map(int, read_line(sock).split(' '))
    v = [int(x) for x in read_line(sock).split(' ') if len(x) > 0]

    coef, start = v[0::2], v[1::2]
    coef, start = list(reversed(coef)), list(reversed(start))

    print(N, K)
    print(start, coef)

    sol = str(get_ans(N, K, start, coef)) + '\n'
    sol = bytearray(sol, 'utf-8')

    print("sending " + sol.decode('utf-8'))

    sock.sendall(sol)

    print(read_line(sock))
  
  print(read_line(sock))