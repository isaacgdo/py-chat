from socket import *
import threading


class ClientMessageThread(threading.Thread):
    """ Esta classe cria thread de execução para recepção ou envio
    de mensagens entre cliente e servidor """

    def __init__(self, conn, thr_type='recv'):
        threading.Thread.__init__(self)
        self.conn = conn
        self.thr_type = thr_type

    def run(self):
        """ a funcao run() é executada por padrao e decide controla
         a seleção de métodos de envio ou recebimento de mensagens """
        self.recv() if self.thr_type == 'recv' else self.send()

    def send(self):
        """ Método responsável pelo envio das mensagens do cliente """
        while True:
            # protocol
            command = input()

            if command[0:8] == 'privado(':
                if command[-1] == ')':
                    username_to_conn = command[8:-1]
                else:
                    print('Comando inválido.')
            elif command[0:7] == 'lista()':
                print('lista de clientes')
            elif command[0:7] == 'ajuda()':
                help()
            elif command[0:6] == 'sair()':
                # enviar pro server mensagem de sair
                # encerrar thread de recv
                self.conn.close()  # encerramento do socket do cliente
                break
            else:
                self.conn.send(command.encode('utf-8'))  # envia o texto para o servidor

    def recv(self):
        """ Método responsável pelo recebimento das mensagens do cliente """
        self.help()
        while True:
            try:
                message = self.conn.recv(1024)
                print(message.decode('utf-8'))
            except RuntimeError as e:
                self.conn.close()
                print(e, 'O recebimento falhou.')
                break

    @staticmethod
    def help():
        """ Método auxiliar para listagem de ajuda """
        print('Para conversar na sala de bate-papo, digite uma mensagem.')
        print('Para iniciar um chat privado, digite privado(nickname_do_usuario)')
        print('Para exibir os clientes conectados à esta sala, digite lista()')
        print('Para exibir esta lista de opções, digite ajuda()')
        print('Para sair da sala de bate-papo, digite sair()')
