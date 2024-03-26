import socket
import logging
from typing import Optional, Union

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def get_client_name(client_ip: str) -> Optional[str]:
    try:
        with open('clients.txt', 'r') as file:
            for line in file:
                ip, name = line.strip().split(',')
                if ip == client_ip:
                    return name
    except FileNotFoundError:
        pass
    return None


def start_server(host: str, port: int) -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            server_socket.bind((host, port))
            break
        except OSError:
            logging.info(f'Порт {port} уже занят, пробуем следующий порт...')
            port += 1

    server_socket.listen(1)
    logging.info(f'Сервер запущен на {host}:{port}')
    print(f'Сервер запущен на порту {port}')

    while True:
        logging.info('Ожидание подключения клиента...')
        client_socket, client_address = server_socket.accept()
        client_ip = client_address[0]
        logging.info(f'Подключен клиент {client_address}')

        client_name = get_client_name(client_ip)

        if not client_name:
            client_socket.sendall('Представьтесь, пожалуйста: '.encode())
            client_name = client_socket.recv(1024).decode().strip()
            logging.info(f'Клиенту {client_address} присвоено имя {client_name}')

            with open('clients.txt', 'a') as file:
                file.write(f'{client_ip},{client_name}\n')

        welcome_message = f'Добро пожаловать, {client_name}!'
        client_socket.sendall(welcome_message.encode())

        while True:
            data = client_socket.recv(1024)

            input_data = data.decode()
            logging.info(f'Получено от клиента {client_name}: {input_data}')

            if input_data.strip().lower() == 'exit':
                break

            client_socket.sendall(data)
            logging.info(f'Отправлено клиенту {client_name}: {input_data}')

        logging.info('Клиент отключен')
        client_socket.close()

    server_socket.close()


def get_user_input(default: Union[str, int]) -> Union[str, int]:
    user_input = input(f'Введите значение (по умолчанию {default}): ')
    if not user_input:
        return default
    return user_input


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345

    custom_host = get_user_input(HOST)
    custom_port = int(get_user_input(str(PORT)))

    start_server(custom_host, custom_port)