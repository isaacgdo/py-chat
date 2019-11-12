from socket import *
from ClientMessageThread import *

serverName = 'localhost'  # ip do servidor
serverPort = 65000  # porta a se conectar
clientSocket = socket(AF_INET, SOCK_STREAM)   # criacao do socket TCP
clientSocket.connect((serverName, serverPort))  # conecta o socket ao servidor


def valid_username(user) -> str:
    return user.replace(' ', '-')


print('Bem-vindo à sala de bate-papo!')
print('Para começar, informe um nome de usuário')

""" Solicita um username ao entrar na sala """
username = ''
while username == '':
    username = input('Nome de usuário: ')
username = valid_username(username)
clientSocket.send(username.encode('utf-8'))  # envia o username do cliente para o servidor
print("Bem-vindo, {}!".format(username))

""" Dispara thread de recebimentos de mensagem do servidor """
recv_thread = ClientMessageThread(clientSocket)
recv_thread.start()

""" Dispara thread de envio de mensagens para o servidor de mensagem do servidor """
send_thread = ClientMessageThread(clientSocket, thr_type='send')
send_thread.start()
