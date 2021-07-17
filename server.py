'''
coded by: @bydeathlxncer
'''



import socket 
import select
import os

#limpar tela caralho
if os.name == "posix":
    var = "clear"
elif os.name == "ce" or os.name == "nt" or os.name == "dos":
    var = "cls"
os.system(var)

HEADER_LENGTH =10
#aqui você deve colocar seu ip privado para outros usuários possam se conectar
#mais nesse caso use o localhost
IP = 'localhost'
PORT = 1354

#criando um socket
#socket.AF_INET = é o domínio do conector, nesse caso, um conector IPv4.

'''
socket.Sock_Stream : tipo de conector (nem todos os domínios suportam o mesmo
  tipos). Neste caso, um conector do tipo STREAM: usando o protocolo TCP, que
  oferece certas garantias de segurança: os pacotes chegam em ordem,
  descartando os repetidos e / ou danificados.

''' 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]

clients = {}
#use uma fonte ou desenho ascii de sua preferência
print('''
  ___  ___ _ ____   _____ _ __
 / __|/ _ \ '__\ \ / / _ \ '__|
 \__ \  __/ |   \ V /  __/ |   
 |___/\___|_|    \_/ \___|_|   
 by: @bydeathlxncer
''')
print(f'esperando por conexões em {IP}:{PORT}...')

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        
        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:

        return False 
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)

            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user 

            print('nova conexão >> {}:{}, usuario: {}'.format(*client_address, user['data'].decode('utf-8')))

        else:
            message = receive_message(notified_socket)

            if message is False:
                print('fechando conexão com: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                sockets_list.remove(notified_socket)

                del clients[notified_socket]

                continue
            user = clients[notified_socket]
            print(f'mensagem recebida de >> {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            for client_socket in clients:
                client_socket.send(user['header'] + user['data'] + message['header'] + message['data'] )
    for notified_socket in exception_sockets:

        sockets_list.remove(notified_socket)

        del clients[notified_socket]            
