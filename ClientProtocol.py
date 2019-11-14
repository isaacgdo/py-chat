import re


def create_send_message(action) -> str:
    """ Função que formata e valida envio de mensagens """
    m_len = 26
    username = 'all\0------------'
    command = 'message\0'
    data = ''

    if action[0:7] == 'entrar(' and action[-1] == ')':
        m_len += len(action[7:-1])
        command = 'entrar\0-'
        data = action[7:-1]
    elif action == 'lista()':
        username = '----------------'
        command = 'lista\0--'
    elif action[0:8] == 'privado(' and action[-1] == ')':
        username = action[8:-1]
    elif action == 'sair()':
        command = 'sair\0---'
    else:
        if len(action) > 73:
            return ''
        m_len += len(action)
        data = action

    return '{}{}{}{}'.format(m_len, username, command, data)
