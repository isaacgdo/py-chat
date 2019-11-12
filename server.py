from socket import *
import threading


clients = []


class ConnThread(threading.Thread):
    """ Esta classe representa uma nova conexão (novo socket) aberta por um cliente """

    def __init__(self, id, conn, addr):
        """ redefine a funcao __init__ para aceitar a passagem parametros de entrada """
        threading.Thread.__init__(self)
        self.id = id
        self.conn = conn
        self.addr = addr
        self.user = ''

    def run(self):
        """ a funcao run() e executada por padrao por cada thread """
        self.client_tasks()
        print('\nFim da Thread de %s [%s]' % (self.user, self.name))
        clients.remove(self)
        print(clients)

    def client_tasks(self):
        """ função controladora de tarefas a serem executadas por cada cliente """
        username = connectionSocket.recv(1024).decode('utf-8')
        self.user = username


# definicao das variaveis
serverName = ''  # ip do servidor (em branco)
serverPort = 65000  # porta a se conectar
serverSocket = socket(AF_INET, SOCK_STREAM)   # criacao do socket TCP
serverSocket.bind((serverName, serverPort))  # bind do ip do servidor com a porta
serverSocket.listen(100)  # socket pronto para 'ouvir' conexoes
print('Servidor TCP de bate-papo esperando conexoes na porta %d ...' % serverPort)


while True:
    connectionSocket, addr = serverSocket.accept()  # aceita conexões dos clientes

    new_conn = ConnThread(2, connectionSocket, addr)
    clients.append(new_conn)

    # thread do novo cliente conectado
    new_conn.start()
    for client in clients:
        print(client.conn)
        print(client.addr[1])

    print(clients)

serverSocket.close() # encerra o socket do servidor