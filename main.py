"""
Sanyerlis Camacaro - CCSC285 - Sancamac@uat.edu Assignment:
Assignment 4.1: Building a Multithreaded Web Server

"ThreadServe"

This code demonstrates how to:

1. Create a Basic Server.
2. Implement Multithreading,
3. Error Handling

Open a web browser and try accessing http://127.0.0.1:8080/ (It should return the content of index.html if it exists in the www directory or a 404 error if it doesn't).
Try accessing http://127.0.0.1:8080/non_existent.html or any other file that doesn't exist in the www directory. You should get a "File not found" message with a 404 status.
"""
# Import necessary modules
import socket       # Required for networking functionalities
import threading    # Required for multi-threading
import os           # Required for handling file operations

# Basic Server Configurations
# Define constant values for the server
SERVER_HOST = '127.0.0.1'  # IP address for the server to bind to - There is no place like home
SERVER_PORT = 8080         # Port number for the server to bind to
BUFFER_SIZE = 1024         # Size of buffer to use when receiving data
WEB_ROOT = "./www"         # Define the root directory for the server files

# --- Task 1: Create a Basic Server ---
# Define a function to handle client requests
def handle_client(client_socket):
    # Receive client request
    request = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    
    # Extract the first line of the request
    request_line = request.split("\n")[0]
    
    # Extract the requested file path from the first line
    file_requested = request_line.split()[1]
    
    # If root path is requested, serve the index.html file
    if file_requested == "/":
        file_requested = "/index.html"
    
    # Combine the root directory with the requested file path to get full file path
    file_path = WEB_ROOT + file_requested
    
    # Check if the requested file exists
    if os.path.exists(file_path):
        # Read the requested file
        with open(file_path, "rb") as file:
            response = file.read()
        # Set header for successful file retrieval
        header = "HTTP/1.1 200 OK\r\n"
    else:
        # --- Task 3: Error Handling ---
        # If file doesn't exist, set error response and header
        response = "HTTP 404 error: File not found".encode()
        header = "HTTP/1.1 404 Not Found\r\n"
    
    # Send response header to client
    client_socket.send(header.encode())
    
    # Send response length to client
    client_socket.send("Content-Length: {}\r\n\r\n".format(len(response)).encode())
    
    # Send the actual file content or error message to the client
    client_socket.send(response)
    
    # Close the connection with the client
    client_socket.close()

# Define the main function that will run the server
def main():
    # Create a socket object for the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set socket option to reuse the address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind the server socket to the specified host and port
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        
        # Make the server start listening for incoming connections
        server_socket.listen(5)
        
        # Print server start message
        print(f"[*] Server started at {SERVER_HOST}:{SERVER_PORT}")
        
        # Keep the server running forever
        while True:
            # Accept incoming connections
            client_socket, addr = server_socket.accept()
            
            # --- Task 2: Implement Multithreading ---
            # Print client connection message
            print(f"[*] Connection from {addr[0]}:{addr[1]}")
            
            # Start a new thread to handle the incoming connection
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

     # --- Task 3: Error Handling ---
    # Handle any exceptions that might occur
    except Exception as e:
        print(f"[!] Error: {e}")
        
        # Close the server socket in case of any errors
        server_socket.close()

# Check if this script is being run as the main module
if __name__ == "__main__":
    # If so, run the main function
    main()
