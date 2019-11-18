def create_send_message(action) -> str:
    """ Função que formata e valida envio de mensagens para o servidor """
    m_len = 26
    username = 'all\0------------'
    command = 'message\0'
    data = ''

    if len(action) > 73 or len(action) < 1:
        return ''
    elif action[0:7] == 'entrar(' and action[-1] == ')':
        m_len += len(action[7:-1])
        command = 'entrar\0-'
        data = action[7:-1]
    elif action == 'lista()':
        username = '\0---------------'
        command = 'lista\0--'
    elif action[0:8] == 'privado(':
        username = action[8:action.index(')')] + '\0'
        for x in range(len(username), 16):
            username = username + '-'
        data = action[action.index(')')+1:]
        command = 'privado\0'
        m_len += len(data)
    elif action[0:5] == 'sair(' and action[-1] == ')':
        m_len += len(action[5:-1])
        command = 'sair\0---'
        data = action[5:-1]
    else:
        m_len += len(action)
        data = action

    return '{}{}{}{}'.format(m_len, username, command, data)


def recv_from_server(message) -> str:
    """ Função que separa informações recebidas do servidor """
    m_len = message[0:2]
    username = message[2:message.index('\0')]
    command = message[18:message.index('\0', 18)]
    data = message[26:]
    msg = ''

    if command == 'entrar':
        msg = '{} entrou... \t'.format(data)
    elif command == 'lista':
        msg = data
    elif command == 'privado':
        sender = message[26:message.index('\0', 26)]
        data = message[message.index('\0', 26):]
        msg = '{} enviou em privado: {}\t'.format(sender, data)
    elif command == 'sair':
        msg = '{} saiu... \t'.format(data)
    elif command == 'message':
        sender = message[26:message.index('\0', 26)]
        data = message[message.index('\0', 26):]
        msg = '{} escreveu: {}\t'.format(sender, data)

    return msg
