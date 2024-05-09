import os
import sys
from socket import *
import threading


def handle_client(connectionSocket, addr):
    # Initialize working directory for the client
    working_directory = os.getcwd()

    while True:
        # Receive the command from the client
        command = connectionSocket.recv(1024).decode()
        print(f"Received command: {command}")

        if command.startswith("STOR"):
            filename = command.split()[1]
            file_data = connectionSocket.recv(4096)
            with open(os.path.join(working_directory, filename), "wb") as file:
                file.write(file_data)
            connectionSocket.send("File uploaded successfully.".encode())

        elif command.startswith("RETR"):
            filename = command.split()[1]
            if os.path.exists(os.path.join(working_directory, filename)):
                with open(os.path.join(working_directory, filename), "rb") as file:
                    file_data = file.read(4096)
                    connectionSocket.send(file_data)
            else:
                connectionSocket.send("File not found.".encode())

        elif command.startswith("LS"):
            file_list = os.listdir(working_directory)
            file_list_str = "\n".join(file_list)
            connectionSocket.send(file_list_str.encode())

        elif command == "QUIT":
            connectionSocket.send("Goodbye.".encode())
            break

        else:
            connectionSocket.send("Invalid command.".encode())

    # Close the socket
    connectionSocket.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORTNUMBER>")
        sys.exit(1)

    # The port on which to listen
    serverPort = int(sys.argv[1])

    # Create a TCP socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))

    # Start listening for incoming connections
    serverSocket.listen(1)

    print("The server is ready to receive")

    # Forever accept incoming connections
    while True:
        # Accept a connection; get client's socket
        connectionSocket, addr = serverSocket.accept()

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        client_thread.start()
