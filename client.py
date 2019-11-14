from socket import *
from ClientMessageThread import *
from ClientProtocol import create_send_message

serverName = 'localhost'  # ip do servidor
serverPort = 65000  # porta a se conectar
clientSocket = socket(AF_INET, SOCK_STREAM)   # criacao do socket TCP
clientSocket.connect((serverName, serverPort))  # conecta o socket ao servidor


def valid_username(user) -> str:
    return user.replace(' ', '-')


print('Bem-vindo à sala de bate-papo!')
print('Para começar, informe um nome de usuário.')

""" Solicita um username ao entrar na sala e valida se:
    1. nome de usuário está em branco
    2. nome de usuário ultrapassa tamanho máximo definido no protocolo
    3. nome de usuário é reservado
"""
username = ''
while True:
    username = input('Nome de usuário: ')
    if username == '':
        pass
    elif len(username) >= 15:
        print('Nome de usuário muito extenso (máx: 15 caracteres)')
    elif username == 'all' or username == 'server':
        print('Nome de usuário inválido')
        # TODO condição 4 - comparar com lista de users que já estão no server
    else:
        break

""" Envia o username do cliente para o servidor """
print("Bem-vindo, {}!".format(username))
username = create_send_message('entrar({})'.format(valid_username(username)))
clientSocket.send(username.encode('utf-8'))

""" Dispara thread de recebimentos de mensagem do servidor """
recv_thread = ClientMessageThread(clientSocket)
recv_thread.start()

""" Dispara thread de envio de mensagens para o servidor de mensagem do servidor """
send_thread = ClientMessageThread(clientSocket, thr_type='send')
send_thread.start()
