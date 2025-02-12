import socket
import sqlite3
import threading
import pickle

CHUNK_SIZE = 4096

# Database setup
DB_NAME = "user_data.db"
PORT = 5000

def initialize_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            pickled_data BLOB)
    ''')
    connection.commit()
    connection.close()

def execute_query(query: str, read: bool, query_parameters: tuple = ()):
    """Execute a SQL query on the return the result if read is True."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    print("execute_query ", query)  # debug

    cursor.execute(query, query_parameters)
    if read:  # If the query is a SELECT query, return the result
        result = cursor.fetchall()
    else:  # If the query is an INSERT, UPDATE or DELETE query, commit the changes
        conn.commit()
        result = None
    print(f"Requete executée : {query}")
    conn.close()
    return result

def handle_client(client_socket: socket.socket):
    """Handle communication with a client."""
    while True:
        # Receive the length of the serialized data first
        data_length = int.from_bytes(client_socket.recv(4), byteorder='big')

        # Receive the serialized data in chunks
        data = bytearray()
        while len(data) < data_length:
            chunk = client_socket.recv(CHUNK_SIZE)
            if not chunk:
                break
            data.extend(chunk)

        if not data:
            break

        query, read, query_parameters = pickle.loads(data)
        print("Received query:", query)  # debug
        response = execute_query(query, read, tuple(query_parameters))
        print("result length", len(response) if response else "No result")  # debug

        # Serialize the response
        serialized_response = pickle.dumps(response)

        # Send the length of the serialized response first
        client_socket.sendall(len(serialized_response).to_bytes(4, byteorder='big'))

        # Send the serialized response in chunks
        for i in range(0, len(serialized_response), CHUNK_SIZE):
            client_socket.sendall(serialized_response[i:i + CHUNK_SIZE])

    client_socket.close()
    print("Connection fermée avec un client")

def start_server(port):
    """Start the SQLite query server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", port))
    server.listen()
    print(f"Le serveur écoute en 127.0.0.1 avec sur le port : {port}")
    while True:  # Accept connections from clients
        client_socket, addr = server.accept()
        print(f"Connection établie avec {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))  # Handle each client in a separate thread
        client_thread.start()

if __name__ == "__main__":
    initialize_database()
    start_server(PORT)