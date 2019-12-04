import socket
import time
import hashlib, random, string, itertools

HOST = '89.38.208.143'  # The server's hostname or IP address
PORT = 21021        # The port used by the server

def read_line(sock):
  line = sock.recv(1).decode('utf-8')
  while line[-1] != '\n':
    line += sock.recv(1).decode('utf-8')
  return line[:-1]

def random_chars(n):
  sol = ""
  for _ in range(n):
    sol += random.choice(string.ascii_letters)
  # print("try random: ", sol)
  return sol

def find_solution():
  pow_target = "0000000"

  # proof of work
  ppow = ""
  for word in itertools.product(string.printable, repeat=5):
      if hashlib.sha256(bytearray(''.join(word), 'utf-8')).hexdigest()[-7:] == pow_target:
          ppow = ''.join(word)
          break
  print("found: ", ppow)


# find_solution()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  sock.connect((HOST, PORT))

  print("hey")

  # for _ in range(1):
  #   print(read_line(sock))

  print("hey")
  
  sol = "4#ot_"
  bt = bytearray(sol + "\n", 'utf-8')
  sock.sendall(bt)

  for _ in range(2):
    print(read_line(sock))