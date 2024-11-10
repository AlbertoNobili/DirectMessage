import socket
import threading
import queue
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


def handle_client(conn, stop_event, message_queue):
    try:
        while not stop_event.is_set():
            data = conn.recv(1024)
            if not data:  # Connection was closed by client
                message_queue.put("Client has disconnected.")
                message_queue.put("Close this window to exit.")
                stop_event.set()
                break
            message = f"Received message: {data.decode()}"
            message_queue.put(message)
    except ConnectionResetError: # Connection was interrupted
        if not stop_event.is_set():
            message_queue.put("Connection was closed.")
            message_queue.put("Close this window to exit.")
            stop_event.set()
        print("Receiver ConnectionResetError")
    except OSError: # Connection was closed by other threads
        if not stop_event.is_set():
            message_queue.put("Connection was closed.")
            message_queue.put("Close this window to exit.")
            stop_event.set()
        print("Receiver OSError")
    finally:
        conn.close()
        print("Receiver ended")

def send_message(event, conn, stop_event, message_queue, input_text):
    try:
        response = input_text.get("1.0", tk.END).strip()

        if response:
            print(response)
            if response.lower() == 'exit': # Close the connection
                stop_event.set()
                message_queue.put("You closed the connection.")
                message_queue.put("Close this window to exit.")
                conn.close()
                return
            conn.sendall(response.encode())
            message_queue.put(f"Sent message: {response}")
            input_text.delete("1.0", tk.END)

    except (BrokenPipeError, ConnectionResetError): # Connection was interrupted
        if not stop_event.is_set():
            message_queue.put("Connection was closed.")
            message_queue.put("Close this window to exit.")
            stop_event.set()
        print("Receiver ConnectionResetError")
    except OSError:  # Connection was closed by other threads
        if not stop_event.is_set():
            message_queue.put("Connection was closed.")
            message_queue.put("Close this window to exit.")
            stop_event.set()
        print("Sender OSError")

def update_messages(text_widget, message_queue):
    while not message_queue.empty():
        message = message_queue.get_nowait()
        text_widget.insert(tk.END, message + '\n')
        text_widget.see(tk.END)
    text_widget.after(100, update_messages, text_widget, message_queue)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Server is listening on port 12345...")

    conn, addr = server_socket.accept()
    print(f"Connection from {addr} has been established.")

    stop_event = threading.Event()
    message_queue = queue.Queue()

    receive_thread = threading.Thread(target=handle_client, args=(conn, stop_event, message_queue))
    receive_thread.start()

    root = tk.Tk()
    root.title("Server messages")

    main_frame = ttk.Frame(root)
    main_frame.pack(expand=True, fill=tk.BOTH)

    text_widget = ScrolledText(main_frame, wrap=tk.WORD)
    text_widget.grid(row=0, column=0, sticky="nsew")

    input_text = tk.Text(main_frame, height=10)
    input_text.grid(row=1, column=0, sticky="nsew")
    input_text.bind("<Return>", lambda event: send_message(event, conn, stop_event, message_queue, input_text))

    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_rowconfigure(1, weight=0)
    main_frame.grid_columnconfigure(0, weight=1)

    update_messages(text_widget, message_queue)

    root.mainloop()
    print("Window closed.")
    receive_thread.join()
    print("Server is shutting down.")
    conn.close()

if __name__ == "__main__":
    start_server()