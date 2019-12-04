import socket
import time

HOST = '89.38.208.143'  # The server's hostname or IP address
PORT = 22021        # The port used by the server

def get_solution(a, b, v):
  L = len(v) // 2
  sol = []
  for i in range(L):
    if int(2**i) & a:
      sol.append(v[i])
  for i in range(L):
    if int(2**i) & b:
      sol.append(v[L + i])
  return sol

def get_data_sockets(sock):
  sol = [""]
  recieved_lines = 0
  while recieved_lines < 4:
    ch = sock.recv(1).decode('utf-8')
    # print("RECEIVED CHAR: " + str(ch))

    if ch == '\n':
      recieved_lines += 1
      if recieved_lines < 4:
        sol.append("")
    else:
      sol[-1] += ch
  return sol

start_time = time.time()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  sock.connect((HOST, PORT))

  for _ in range(10):
    print("NEW TEST!\n")

    lines = get_data_sockets(sock)

    # solution
    ssum = int(lines[-2])

    v = [int(str(x)) for x in lines[-1].split(' ') if len(x) > 0]

    print(ssum)
    print(v)

    print(lines[1])
    print("sum desired: " + str(ssum))
    LIM = len(v) // 2
    first_half = {}

    p2 = [int(2**i) for i in range(22)]

    
    meh = int(2**LIM)

    for mask in range(meh):
      lesum = 0
      for i in range(LIM):
        if p2[i] & mask:
          lesum += v[LIM + i]
      if lesum <= ssum:
        first_half[lesum] = mask

    elapsed_time = time.time() - start_time
    print("time: ", elapsed_time)
    
    solution = []
    for mask in range(meh):
      lesum = 0
      for i in range(LIM):
        if p2[i] & mask:
          lesum += v[i]
      if ssum-lesum in first_half.keys():
        solution = get_solution(mask, first_half[ssum-lesum], v)
        break

    # your code
    elapsed_time = time.time() - start_time
    print("time: ", elapsed_time)
    
    sol = str(len(solution))
    for i in range(len(solution)):
      sol += " " + str(solution[i])
    sol += "\n"

    temp = bytearray(sol, 'utf-8')
    print(temp)
    sock.sendall(temp)
  
  response = sock.recv(4096).decode('utf-8')
  print("I GOT THIS:\n")
  print(response)