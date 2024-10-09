import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            # Receber mensagens do servidor
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print('Connection lost')
            client_socket.close()
            break

def start_client(server_ip, server_port, client_id):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Envia o comando LOGIN
    client_socket.send(f'LOGIN {client_id}'.encode('utf-8'))

    # Thread para receber mensagens do servidor
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        # Enviar mensagens para o servidor
        msg = input('Your message: ')
        client_socket.send(msg.encode('utf-8'))

        if msg.startswith('LOGOFF'):
            break

    client_socket.close()

if __name__ == '__main__':
    server_ip = input('Enter server IP: ')
    server_port = int(input('Enter server port: '))
    client_id = input('Enter your client ID: ')

    start_client(server_ip, server_port, client_id)
