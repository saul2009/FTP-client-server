import struct
import sys
from socket import AF_INET, SOCK_STREAM, socket


def send_data(sock, data):
    data_size = len(data)
    header = struct.pack("!Q", data_size)
    sock.sendall(header + data)


def receive_data(sock):
    # Receive the size of the data
    header = sock.recv(8)
    data_size = struct.unpack("!Q", header)[0]

    # Receive the data in chunks
    data = b""
    while data_size > 0:
        chunk = sock.recv(min(4096, data_size))
        data += chunk
        data_size -= len(chunk)

    return data


command_list = ["quit", "ls", "put", "get"]

# Get server machine and port from command-line arguments
if len(sys.argv) != 3:
    print("Usage: python client.py <server machine> <server port>")
    sys.exit(1)

serverMachine = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a TCP socket
sock = socket(AF_INET, SOCK_STREAM)

try:
    # Connect to the server
    sock.connect((serverMachine, serverPort))

    while True:
        # Read command from user and send to server
        s = input("ftp> ")
        sock.sendall(s.encode("utf-8"))
        command = s.split(' ')[0].lower()

        if command in command_list:
            if command == "quit":
                # End the client connection
                print("Ending program")
                break

            if command == "ls":
                # Receive and print the file list from the server
                file_data = receive_data(sock)
                print(file_data.decode("utf-8"))

            if command == "get":
                # Download file from server
                filename = s.split(' ')[1]
                file_data = receive_data(sock)

                # Save the received file
                with open(filename, 'wb') as file:
                    file.write(file_data)

                print(f"File '{filename}' downloaded successfully.")

            if command == "put":
                # Upload file to server
                filename = s.split(' ')[1]

                try:
                    with open(filename, 'rb') as file:
                        file_data = file.read()

                    # Send the file data to the server
                    send_data(sock, file_data)
                    print(f"File '{filename}' uploaded successfully.")
                except FileNotFoundError:
                    print(f"File '{filename}' not found.")

        else:
            # If it's not a command, just print the response from the server
            data = sock.recv(1024).decode("utf-8")
            print("Received: ", data)

except Exception as e:
    print(e)

finally:
    # Close the socket
    sock.close()