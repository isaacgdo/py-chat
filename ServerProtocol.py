def recv_from_client(message) -> tuple:
    """ Função que separa informações recebidas do cliente """
    m_len = message[0:2]
    username = message[2:message.index('\0')]
    command = message[18:message.index('\0', 18)]
    data = message[26:]

    return m_len, username, command, data


def sender(user, message):
    m_len = int(message[0:2]) + len(user)
    username = message[2:18]
    command = message[18:26]
    msg = message[26:]
    user = user + '\0'

    return '{}{}{}{}{}'.format(m_len, username, command, user, msg)
