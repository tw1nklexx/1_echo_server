import socket
from typing import Any


def connect_to_server(host: str, port: int) -> socket.socket:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f'Соединение с сервером {host}:{port} установлено')
    return client_socket


def get_user_input(default: Any) -> Any:
    user_input = input(f'Введите значение (по умолчанию {default}): ')
    if not user_input:
        return default
    return user_input


def send_data_to_server(client_socket: socket.socket, data: str) -> None:
    client_socket.sendall(data.encode())
    print(f'Отправлено серверу: {data}')


def receive_data_from_server(client_socket: socket.socket) -> None:
    received_data = client_socket.recv(1024).decode()
    print(f'Получено от сервера: {received_data}')


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345

    custom_host = get_user_input(HOST)
    custom_port = int(get_user_input(str(PORT)))

    client_socket: socket.socket = connect_to_server(custom_host, custom_port)

    try:
        while True:
            receive_data_from_server(client_socket)

            data: str = input('Введите строку для отправки серверу: ')
            send_data_to_server(client_socket, data)

            if data == 'exit':
                break

    finally:
        client_socket.close()