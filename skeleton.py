from socket import *
import sys
import os.path
from os import path

# IP address and port for the web proxy server are hard coded
HOST = '10.0.0.27' # My computer's IP address
PORT = 65432 # Arbitrary

# Set buffer size to hold 128 bytes
BUFFER_SIZE = 1024

# We represent the cache by writing the response from the server to a file titled "host_object.txt"
# If we get a "GET" request from the server at host for an object, we check if the file already exists in
# the cache, and if it doesn't we send the request to the server and

# Create a socket that represents the server, bind it to a port
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(HOST, PORT)
print("server socket binded to {}:{}".format(HOST, PORT))
# Start listening
server_socket.listen(10)
print("Server Socket is listening")

while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    # Accept returns a tuple: IP address, port number
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
    # Message is a GET Request
    # Example GET Request: 'GET /kurose_rose/interactive/index.php HTTP/1.1 Host: gaia.cs.umass.edu'
    # Extract the URL to connect with the server
    message_array = message.split()
    file_name = message_array[1].partition("/")[2]
    print("File name ", file_name)
    # Check if the file exists in the cache already
    if path.exists(file_name):
        # File found in cache, load the file and send a response back to client
        client_socket.send("HTTP/1.0 200 OK\r\n")
        client_socket.send("Content-Type:text/html\r\n")
        with open(file_name, "rb") as file:
            data = file.read()
            data_string = data.decode("utf-8")
            print("data from file: ", data_string)
            client_socket.send(data)
        # Close the client socket
        client_socket.close()
        print('Read from cache')
    else:
        # File not in cache, need to request the server and get the response
        proxy_socket = socket(AF_INET, SOCK_STREAM)
        # Connect the proxy_socket with the host described in the get request, send the get request to server
        host = file_name.replace("www.", "", 1)
        proxy_socket.connect(host, 80)
        proxy_socket.send(message)
        proxy_socket.listen(10)
        while 1:
            print("Receiving data from web server")
            # Receive data from web server
            data = proxy_socket.recv(BUFFER_SIZE)
            if len(data) > 0:
                # Decode data received from server
                response = data.decode('utf-8')
                print("Server response ", response)
                # Put server in the cache so that we can access it another time
                file = open(file_name, 'wb')
                file.write(data)
                # Send the data back to the client
                client_socket.send(data)
            else:
                break
        # Close the client socket
        client_socket.close()