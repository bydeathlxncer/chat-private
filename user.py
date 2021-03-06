'''
coded by: @bydeathlxncer
'''
import socket 
import sys
import errno 
import os 

#limpando a tela
if os.name == "posix":
    var = "clear"
elif os.name =="ce" or os.name == "nt" or os.name =="dos":
    var ="cls"
os.system(var)

HEADER_LENGTH =10


#aqui vai o ip e a porta do servidor
IP = 'localhost'
PORT = 1354


print('''
  _   _ ___  ___ _ __
 | | | / __|/ _ \ '__|
 | |_| \__ \  __/ |
  \____|___/\___|_|
  by: @bydeathlxncer
''')
my_username = input("nome de usuário: ")
os.system(var)
#criando um  socket 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))

client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True: 
    message = input(f'{my_username} > ')

    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)

            if not len(username_header):
                print('conexão fechada pelo servidor....')
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f'{username} > {message}')
    
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Error: {}'.format(str(e)))
        
        continue
    except Exception as e:
        print('Error: '.format(str(e)))
        sys.exit()
