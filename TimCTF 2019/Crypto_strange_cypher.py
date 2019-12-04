import socket
import base64

HOST = '89.38.208.143'  # The server's hostname or IP address
PORT = 21022        # The port used by the server

global sock

def read_line():
  line = sock.recv(1).decode('utf-8')
  while line[-1] != '\n':
    line += sock.recv(1).decode('utf-8')
  return line[:-1]

def send_string(s):
  sock.sendall(bytearray(s, 'utf-8'))

def process_line(line):
  s = line.split(' ')
  ret = ""
  # print(s)
  while len(s[-1]) == 2 or len(s[-1]) == 0:
    ret = s[-1] + ret
    s = s[:-1]
  
  while len(ret) % 4 != 0:
    ret += "="
   
  # print("got string: ", ret)
  fin = base64.b64decode(ret).hex()
  # print("base64 decode: ", fin)
  return fin

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  sock.connect((HOST, PORT))

  # first
  line = read_line()
  print(line)
  fin = process_line(line)

  send_string(fin + "\n")

  # second

  for _ in range(25):
    print("test: ", _ + 1)

    line = read_line()
    print(line, "\n")
    fin = process_line(line)

    send_string(fin + "\n")
  
  print(read_line())