import os
from ez import ez_produce


def produce_rpc(name: str, queue: str, data: dict, rpc_attempts: int):
    """
    Generic produce helper.
    """
    var = 'RABBITMQ_%s_QUEUE' % name.upper()
    return ez_produce(name, queue, data, is_rpc=True, rpc_attempts=rpc_attempts)


def produce_auth(data: dict):
    """
    Auth producer helper function.
    """
    return produce_rpc('AUTH', 'auth-queue-rpc', data, 50)


def produce_data(data: dict):
    """
    Data producer helper function.
    """
    return produce_rpc('DATA', 'data-queue-rpc', data, 50)


def produce_dmz(data: dict):
    """
    DMZ producer helper function.
    """
    return produce_rpc('DMZ', 'dmz-queue-rpc', data, 500)


def get_user(token: str):
    """
    Get user by token.
    """
    data = { 'action': 'get_user', 'token': token }
    return produce_rpc('AUTH', 'auth-queue-rpc', data, 50)
