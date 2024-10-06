import socket
from threading import Thread


def newThread(client_socket):
    while True:
        request = client_socket.recv(1024)
        request = request.decode('utf-8')  # convert bytes to string

        # if we receive 'close' from the client, then we break
        # out of the loop and close the conneciton
        if request.lower() == 'quit':
            # send response to the client which acknowledges that the
            # connection should be closed and break out of the loop
            client_socket.send('quitted'.encode('utf-8'))
            return

        print(f'Received: {request}')
        responseMsg = request.upper()

        response = responseMsg.encode('utf-8')  # convert string to bytes
        # convert and send accept response to the client
        client_socket.send(response)
    # close connection socket with the client
    client_socket.close()
    print('Connection to client closed')


def run_server():
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # set server IP and Port
    server_ip = '127.0.0.1'
    port = 8000

    # bind the socket to a specific address and port
    server.bind((server_ip, port))
    # listen for incoming connections
    server.listen()
    print(f'Listening on {server_ip}:{port}')

    while True:
        # accept incoming connections
        client_socket, client_address = server.accept()
        print(f'Accepted connection from {client_address[0]}:{client_address[1]}')

        # receive data from the client
        Thread(target=newThread(client_socket))

    # close server socket
    server.close()


run_server()
