from socket import *
import sys
import os

# IP address and port for the web proxy server are hard coded
HOST = 'localhost' # My computer's IP address
PORT = 8888 # Arbitrary

# Set buffer size to hold 128 bytes
BUFFER_SIZE = 1024

# Replace all slashes with dashes, replace all . with 0, replace all : with 1 to avoid file issues
# Arbitrary to avoid file issues
def get_file_name(host_name, request_object):
    host_name = host_name.replace("/", "-")
    request_object = request_object.replace("/", "-")
    host_name = host_name.replace(".", "0")
    request_object = request_object.replace(":", "1")
    cache_name = str(host_name) + "_" + request_object + ".txt"
    return cache_name

if __name__ == "__main__":
    # Create a socket that represents the server, bind it to a port
    server_socket = socket(AF_INET, SOCK_STREAM)
    # Set flag so that it can't be reused
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    bind_tuple = (HOST, PORT)
    server_socket.bind(bind_tuple)
    print("server socket binded to {}:{}".format(HOST, PORT))
    # Start listening
    server_socket.listen()
    print("Server Socket is listening")
    while 1:
        # Start receiving data from the client
        print('Ready to serve...')
        # Accept returns a tuple: socket, port number
        client_socket, client_address = server_socket.accept()
        print('Received a connection from:', client_socket, client_address)
        # Decode data received from client
        received_data = client_socket.recv(BUFFER_SIZE)
        message = received_data.decode('utf-8')
        print(message)
        if not message.startswith("GET"):
            # Don't know how to process anything that isn't a get request
            response = "HTTP/1.1 501 Not Implemented"
            response_encoded = message.encode('utf-8')
            # Send 501 back to client
            client_socket.send(response_encoded)
            print(response)
        else:
            # Message is a GET Request
            # Extract the Host and Requested object in order to check for cache or send to server
            message_array = message.split("\n")
            first_line = message_array[0]
            first_line_array = first_line.split(" ")
            second_line = message_array[1]
            second_line_array = second_line.split(" ")
            request_obj = first_line_array[1].partition("/")[2]
            host = second_line_array[1]
            host = host.strip()
            print("Object ", request_obj)
            print("Host ", host)
            file_name = get_file_name(host, request_obj)
            # Check if the file exists in the cache already
            if os.path.isfile(file_name):
                # File found in cache, load the file and send a response back to client
                print("Now decoding file ", file_name)
                response_string = "HTTP/1.0 200 OK\r\nContent-Type:text/html\r\n"
                response_string_encoded = response_string.encode("utf-8")
                client_socket.send(response_string_encoded)
                with open(file_name, "rb") as file:
                    data = file.read()
                    # data_string = data.decode("utf-8")
                    # print("data from file: ", data_string)
                    client_socket.send(data)
                # Close the client socket
                client_socket.close()
                print('Read from cache')
            else:
                # File not in cache, need to request the server and get the response
                proxy_socket = socket(AF_INET, SOCK_STREAM)
                proxy_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                # Connect the proxy_socket with the host described in the get request, send the get request to server
                proxy_socket.connect((host, 80))
                proxy_socket.send(received_data)
                f = open(file_name, 'wb')
                while 1:
                    print("Receiving data from web server")
                    # Receive data from web server
                    data = proxy_socket.recv(BUFFER_SIZE)
                    if len(data) > 0:
                        # Send the data back to the client
                        client_socket.send(data)
                        print("data sent")
                        # Put data in cache
                        f.write(data)
                    else:
                        f.close()
                        break
    # Close the client socket after one webpage is fetched.
    client_socket.close()
    server_socket.close()
