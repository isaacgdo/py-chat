from socket import *

serverName = 'localhost'  # ip do servidor
serverPort = 65000  # porta a se conectar
clientSocket = socket(AF_INET, SOCK_STREAM)   # criacao do socket TCP
clientSocket.connect((serverName, serverPort))  # conecta o socket ao servidor


def help():
    print('Para conversar na sala de bate-papo, digite uma mensagem.')
    print('Para iniciar um chat privado, digite privado(nickname_do_usuario)')
    print('Para exibir os clientes conectados à esta sala, digite lista()')
    print('Para exibir esta lista de opções, digite ajuda()')
    print('Para sair da sala de bate-papo, digite sair()')


def valid_username(user):
    return user.replace(' ', '-')


print('Bem-vindo à sala de bate-papo!')
print('Para começar, informe um nome de usuário')

username = ''
while username == '':
    username = input('Nome de usuário: ')
username = valid_username(username)
clientSocket.send(username.encode('utf-8'))  # envia o username do cliente para o servidor
print("Bem-vindo, {}!".format(username))
help()

while True:
    command = input('>>> ')

    if command[0:8] == 'privado(':
        if command[-1] == ')':
            username_to_conn = valid_username(command[8:-1])
        else:
            print('Comando inválido')
    elif command[0:7] == 'lista()':
        print('lista de clientes')
    elif command[0:7] == 'ajuda()':
        help()
    elif command[0:6] == 'sair()':
        clientSocket.close()  # encerramento o socket do cliente
        break
    else:
        sentence = input('Digite o texto em letras minusculas: ')
        clientSocket.send(sentence.encode('utf-8'))  # envia o texto para o servidor
        modifiedSentence = clientSocket.recv(1024)  # recebe do servidor a resposta
        print('O servidor ({}, {}) respondeu com: {}'.format(
            serverName,
            serverPort,
            modifiedSentence.decode('utf-8')
        ))
