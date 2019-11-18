from socket import *
from ServerProtocol import recv_from_client, sender
import threading


""" Lista de clientes """
clients = []


class ConnThread(threading.Thread):
    """ Esta classe representa uma nova conexão (novo socket) aberta por um cliente """

    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.user = ''

    def run(self):
        """ a funcao run() é executada por padrao por cada thread """
        self.client_tasks()
        print('\nFim da conexão de {} '.format(self.user))

    def client_tasks(self):
        """ Método que controla tarefas a serem executadas por cada cliente """
        while True:
            message = connectionSocket.recv(99).decode('utf-8')
            # print(recv_from_client(message))
            m_len, username, cmd, data = recv_from_client(message)

            if cmd == 'entrar':
                print('{} entrou...\t'.format(data))
                self.user = data
                self.broadcast(message)
            elif cmd == 'lista':
                for client in clients:
                    msg = '{}<{}, {}, {}>'.format(message, client.user, client.addr[0], client.addr[1])
                    self.conn.send(msg.encode('utf-8'))
            elif cmd == 'privado':
                message = sender(self.user, message)
                self.private_msg(username, message)
            elif cmd == 'sair':
                print('{} saiu...'.format(data))
                self.broadcast(message)
                clients.remove(self)
                break
            elif cmd == 'message':
                print('{} escreveu: {}\t'.format(self.user, data))
                message = sender(self.user, message)
                self.broadcast(message)

    @staticmethod
    def broadcast(message):
        """ Função de envio de mensagens para a sala (broadcast) """
        for client in clients:
            if client.user != '':   # Se a conexão já tiver definido um username poderá receber mensagens
                try:
                    client.conn.send(message.encode('utf-8'))
                except RuntimeError as e:
                    client.conn.close()
                    print(e, 'O envio falhou.')

    @staticmethod
    def private_msg(user, msg):
        """ Método que envia mensagens privadas de cliente a cliente """
        for client in clients:
            if user == client.user:
                try:
                    client.conn.send(msg.encode('utf-8'))
                except RuntimeError as e:
                    client.conn.close()
                    print(e, 'O envio falhou.')


""" Definição das variáveis """
serverName = ''  # ip do servidor (em branco)
serverPort = 65000  # porta a se conectar
serverSocket = socket(AF_INET, SOCK_STREAM)   # criacao do socket TCP
serverSocket.bind((serverName, serverPort))  # bind do ip do servidor com a porta
serverSocket.listen(100)  # socket pronto para 'ouvir' conexoes
print('Servidor TCP de bate-papo esperando conexoes na porta {} ...'.format(serverPort))


while True:
    """ Aceita novas conexões de clientes e cria threads para elas """
    connectionSocket, addr = serverSocket.accept()
    new_conn = ConnThread(connectionSocket, addr)
    clients.append(new_conn)

    """ cria thread para um novo cliente conectado """
    new_conn.start()

serverSocket.close() # encerra o socket do servidor