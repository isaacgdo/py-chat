from socket import *
import threading
from ClientProtocol import create_send_message, recv_from_server


class ClientMessageThread(threading.Thread):
    """ Esta classe cria thread de execução para recepção ou envio
    de mensagens entre cliente e servidor """

    def __init__(self, conn, username, thr_type='recv'):
        threading.Thread.__init__(self)
        self.conn = conn
        self.username = username
        self.thr_type = thr_type

    def run(self):
        """ a funcao run() é executada por padrao e controla
         a seleção de métodos de envio ou recebimento de mensagens """
        self.recv() if self.thr_type == 'recv' else self.send()

    def send(self):
        """ Método responsável pelo envio das mensagens do cliente """
        while True:
            command = input()
            if command[0:8] == 'opcoes()':
                self.options()
            else:
                data = create_send_message(command)

                if command[0:6] == 'sair()':
                    data = create_send_message('sair({})'.format(self.username))
                    self.conn.send(data.encode('utf-8'))
                    self.conn.close()  # encerramento do socket do cliente
                    break

                print('Mensagem Inválida!') if data == '' else self.conn.send(data.encode('utf-8'))

    def recv(self):
        """ Método responsável pelo recebimento das mensagens do cliente """
        self.options()
        while True:
            try:
                message = self.conn.recv(99).decode('utf-8')
                print(recv_from_server(message))
                if message[18:message.index('\0', 18)] == 'sair':
                    break
            except RuntimeError as e:
                self.conn.close()
                print(e, 'O recebimento falhou.')
                break

    @staticmethod
    def options():
        """ Método auxiliar para listagem de opções """
        print('Para conversar na sala de bate-papo, digite uma mensagem.')
        print('Para enviar uma mensagem privada, digite privado(nickname_do_usuario) seguido da mensagem.')
        print('Para exibir os clientes conectados à esta sala, digite lista().')
        print('Para exibir esta lista de opções, digite opcoes().')
        print('Para sair da sala de bate-papo, digite sair().')
