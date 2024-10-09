import socket
import threading

clients = {}  # Dicionário para manter o mapeamento client-id -> socket

def handle_client(client_socket, client_id):
    while True:
        try:
            # Receber mensagens do cliente
            msg = client_socket.recv(1024).decode('utf-8')
            
            if msg.startswith('MSGALL'):
                # Envia mensagem para todos os clientes
                broadcast_message(client_id, msg[7:])
            elif msg.startswith('MSG'):
                # Envia mensagem para um cliente específico
                target_client_id = msg.split()[1]
                text = ' '.join(msg.split()[2:])
                send_private_message(client_id, target_client_id, text)
            elif msg.startswith('LOGOFF'):
                # Cliente está se desconectando
                remove_client(client_id)
                break
            elif msg.startswith('BAN'):
                # Banir um cliente
                target_client_id = msg.split()[1]
                ban_client(client_id, target_client_id)
            elif msg.startswith('STATUS'):
                # Envia a lista de clientes online
                send_status(client_id)
        except:
            # Se houver algum erro, remover o cliente
            remove_client(client_id)
            break

    client_socket.close()

def broadcast_message(client_id, message):
    for cid, client_socket in clients.items():
        if cid != client_id:  # Não enviar a mensagem para o remetente
            client_socket.send(f'{client_id}: {message}'.encode('utf-8'))

def send_private_message(sender_id, target_id, message):
    if target_id in clients:
        clients[target_id].send(f'{sender_id}: {message}'.encode('utf-8'))
    else:
        clients[sender_id].send(f'Client {target_id} not found'.encode('utf-8'))

def ban_client(sender_id, target_id):
    if target_id in clients:
        clients[target_id].send('You have been banned from the chat'.encode('utf-8'))
        remove_client(target_id)

def send_status(client_id):
    # Envia a lista de clientes conectados para o cliente solicitante
    client_list = ', '.join(clients.keys())
    clients[client_id].send(f'Online clients: {client_list}'.encode('utf-8'))

def remove_client(client_id):
    if client_id in clients:
        print(f'Client {client_id} disconnected')
        clients[client_id].close()
        del clients[client_id]
        broadcast_message(client_id, f'{client_id} has logged off')

def start_server(server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', server_port))
    server_socket.listen(5)

    print(f'Server listening on port {server_port}...')

    while True:
        client_socket, addr = server_socket.accept()
        client_id = client_socket.recv(1024).decode('utf-8').split()[1]  # Espera pelo login do cliente
        clients[client_id] = client_socket

        print(f'Client {client_id} connected')

        # Inicia uma thread para lidar com o cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        client_thread.start()

if __name__ == "__main__":
    server_port = int(input("Enter server port: "))
    start_server(server_port)
