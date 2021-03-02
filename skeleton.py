from socket import *
import sys

# IP address and port for the web proxy server are hard coded
HOST = '10.0.0.27' # My computer's IP address
PORT = 65432 # Arbitrary

# Set buffer size to hold 256 bytes
BUFFER_SIZE = 2048

# Initialize empty cache that maps the filename to the webpage
cache = dict()

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port
proxy_socket = socket(AF_INET, SOCK_STREAM)
proxy_socket.bind(HOST, PORT)
print("proxy socket binded to {}:{}".format(HOST, PORT))
# Start listening
proxy_socket.listen(5)
print("Proxy Socket is listening")

while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    # Accept returns a tuple: IP address, port number
    client_ip, client_port = proxy_socket.accept()
    print('Received a connection from:', client_ip, client_port)
    # Decode data received from client
    received_data = client_ip.recv(BUFFER_SIZE)
    message = received_data.decode('utf-8')
    print(message)
    if not message.startswith("GET"):
        # Don't know how to process anything that isn't a get request
        response = "HTTP/1.1 501 Not Implemented"
        response_encoded = message.encode('utf-8')
        # Send 501 back to client
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.bind(client_ip, client_port)
        client_socket.send(response_encoded)
        # Close the connection
        client_socket.close()
        proxy_socket.close()
    # Message is a GET Request
    # Extract the filename from the given message
    print(message.split()[1])
    file_name = message.split()[1].partition("/")[2]
    print("File name ", file_name)
    # Check if the file exists in the cache already
    if file_name not in cache:
        # File not in cache, need to create a socket on the proxy server and send the request to the web server
        server_socket = socket(AF_INET, SOCK_STREAM)
        host_name = file_name.replace("www.", "", 1)
        print("host name ", host_name)
        # Once file is retrieved, load it into cache
    else:
        # File found in cache, load the file and send a response back to client
        client_ip.send("HTTP/1.0 200 OK\r\n")
        client_ip.send("Content-Type:text/html\r\n")
        print('Read from cache')

    try:
    # Error handling for file not found in cache
    except IOError:
        if not file_exists:
            # Create a socket on the proxyserver
            new_socket = socket(AF_INET, SOCK_STREAM)
            host_name = filename.replace("www.","",1)
            print(host_name)
            try:
                # Connect to the socket to port 80
                new_socket.bind(HOST, 80)
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('r', 0)
                fileobj.write("GET "+"http://" + filename + " HTTP/1.0\n\n")
                # Read the response into buffer

                # Fill in start.
                # Fill in end.

                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                # Fill in start.
                # Fill in end.
            except:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            # Fill in start.
            # Fill in end.
            # Close the client and the server sockets
            tcpCliSock.close()

# Fill in start.
# Fill in end.