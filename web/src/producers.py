import os
from ez import ez_produce


def produce_rpc(name: str, queue: str, data: dict):
    """
    Generic produce helper.
    """
    var = 'RABBITMQ_%s_QUEUE' % name.upper()
    return ez_produce(name, queue, data, is_rpc=True)


def produce_auth(data: dict):
    """
    Auth producer helper function.
    """
    return produce_rpc('AUTH', 'auth-queue-rpc', data)


def produce_data(data: dict):
    """
    Data producer helper function.
    """
    return produce_rpc('DATA', 'data-queue-rpc', data)


def get_user(token: str):
    """
    Get user by token.
    """
    data = { 'action': 'get_user', 'token': token }
    return produce_rpc('AUTH', 'auth-queue-rpc', data)
