import grpc
import uuid
import random
from global_vars import server


# Генерация GUID
def generate_guid() -> str:
    return str(uuid.uuid4())


# Создание gRPC-канала для подключения к серверу
def grpc_channel():
    with grpc.insecure_channel(server) as channel:
        yield channel


def generate_random_balance(min_val: int, max_val: int) -> int:
    random_balance = random.randint(min_val, max_val)
    return random_balance