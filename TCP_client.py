import socket
import threading

def receive_messages(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received message: {data.decode()}")
    except ConnectionResetError:
        print("Server has disconnected.")
    finally:
        client_socket.close()

def send_messages(client_socket):
    try:
        while True:
            message = input("Enter message to send: ")
            if message.lower() == 'exit':
                break
            client_socket.sendall(message.encode())
    except (BrokenPipeError, ConnectionResetError):
        print("Connection was closed.")
    finally:
        client_socket.close()


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()

if __name__ == "__main__":
    start_client()