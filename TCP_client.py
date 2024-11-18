import socket
import threading
import queue
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

def receive_messages(conn, stop_event, message_queue):
    try:
        while not stop_event.is_set():
            conn.settimeout(1.0)  # Set a timeout for the recv call
            try:
                data = conn.recv(1024)
                if not data:  # Connection was closed by client
                    message_queue.put("Client has disconnected.")
                    message_queue.put("Close this window to exit.")
                    stop_event.set()
                    break
                message = f"Received message: {data.decode()}"
                message_queue.put(message)
            except socket.timeout:
                continue
    except ConnectionResetError: # Connection was interrupted
        if not stop_event.is_set():
            stop_event.set()
        #print("Receiver ConnectionResetError")
    except OSError: # Connection was closed by other threads
        if not stop_event.is_set():
            stop_event.set()
        #print("Receiver OSError")
    finally:
        message_queue.put("Connection was closed.")
        message_queue.put("Close this window to exit.")
        conn.close()
        print("Receiver ended")

def send_message(event, conn, stop_event, message_queue, input_text):
    if event.keysym == 'Return' and not event.state & 0x0001:  # Check if Shift is not pressed
        try:
            response = input_text.get("1.0", tk.END).strip()

            if response:
                print(response)
                if response.lower() == 'exit':  # Close the connection
                    stop_event.set()
                    message_queue.put("You closed the connection.")
                    message_queue.put("Close this window to exit.")
                    conn.close()
                    return
                conn.sendall(response.encode())
                message_queue.put(f"Sent message: {response}")
                input_text.delete("1.0", tk.END)

        except (BrokenPipeError, ConnectionResetError):  # Connection was interrupted
            if not stop_event.is_set():
                message_queue.put("Connection was closed.")
                message_queue.put("Close this window to exit.")
                stop_event.set()
            # print("Sender ConnectionResetError")
        except OSError:  # Connection was closed by other threads
            if not stop_event.is_set():
                message_queue.put("Connection was closed.")
                message_queue.put("Close this window to exit.")
                stop_event.set()
            # print("Sender OSError")
    else:
        input_text.insert(tk.INSERT, '')  # Insert a newline if Shift+Enter is pressed

def update_messages(text_widget, message_queue):
    while not message_queue.empty():
        message = message_queue.get_nowait()
        text_widget.config(state=tk.NORMAL)
        if message.startswith("Received message:"):
            text_widget.insert(tk.END, "Received message:", ('prompt', 'received'))
            text_widget.insert(tk.END, message[len("Received message:"):] + '\n', 'received')
        elif message.startswith("Sent message:"):
            text_widget.insert(tk.END, "Sent message:", ('prompt', 'sent'))
            text_widget.insert(tk.END, message[len("Sent message:"):] + '\n', 'sent')
        text_widget.see(tk.END)
        text_widget.config(state=tk.DISABLED)
    text_widget.after(100, update_messages, text_widget, message_queue)

def on_closing(stop_event, root):
    stop_event.set()
    root.destroy()

def start_client():
    server_public_IP = 'localhost'
    #server_public_IP = '95.249.79.185'
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_public_IP, 12346))

    addr, port = client_socket.getpeername()
    print(f"Connection to {addr} on port {port} has been established.")

    stop_event = threading.Event()
    message_queue = queue.Queue()

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, stop_event, message_queue))
    receive_thread.start()

    root = tk.Tk()
    root.title("Client messages")

    main_frame = ttk.Frame(root)
    main_frame.pack(expand=True, fill=tk.BOTH)


    text_widget = ScrolledText(main_frame, wrap=tk.WORD, state=tk.DISABLED)
    text_widget.grid(row=0, column=0, sticky="nsew")
    text_widget.tag_config('prompt', font=('TkDefaultFont', 9, 'underline'))
    text_widget.tag_config('received', foreground='red')
    text_widget.tag_config('sent', foreground='blue')

    input_text = tk.Text(main_frame, height=10)
    input_text.grid(row=1, column=0, sticky="nsew")
    input_text.bind("<Return>", lambda event: send_message(event, client_socket, stop_event, message_queue, input_text))

    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_rowconfigure(1, weight=0)
    main_frame.grid_columnconfigure(0, weight=1)

    update_messages(text_widget, message_queue)

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(stop_event, root))

    root.mainloop()

    print("Window closed.")
    receive_thread.join()
    print("Client is shutting down.")
    client_socket.close()

if __name__ == "__main__":
    start_client()