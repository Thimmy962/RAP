import socket
import sqlite3 as sql
import sock_views
from urllib.parse import urlparse, parse_qs
import sys
import threading

shutdown_event = threading.Event()


def sock():
    '''
        Creates socket and binds socket to port
        Opens socket up for listening
    '''
    server = "0.0.0.0"
    PORT = 1

    if len(sys.argv) < 2:
        sys.exit("Enter port number")
    elif len(sys.argv) > 2:
        sys.exit("You can not have more than a value")
    else: PORT = int(sys.argv[1])
    addr = (server, PORT)

    try:
        sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock_fd.bind(addr)
    except Exception as e:
        sock_fd.close()
        sys.exit(e)

    sock_fd.listen()
    print("Serving on http://localhost:8080")
    return sock_fd


def get_method(path, cursor, query_params = None):
    print(path)
    if path in ("/", "/articles"): return sock_views.index(cursor, query_params)
    else: return sock_views.notFound()


def put_method(path, cursor, query_params = None):
    pass

def delete_method(path, cursor, query_params = None):
    pass



def method_function_caller(first_line, cursor):
    '''
        Decifer the method and calss the appropriate function
    '''
    method, url, type = first_line.split(' ')
    parsed_url = urlparse(url)
    path = parsed_url.path
    query_params = parse_qs(parsed_url.query)

    if method.lower() == "get":
        return get_method(path, cursor, query_params = query_params)

    
        
def handle_client(conn, client_fd):
    db = 'db.sqlite3'
    connection = sql.connect(db)
    cursor = connection.cursor()
    format = "UTF-8"

    try:
        while not shutdown_event.is_set():
            msg = conn.recv(1024).decode(format)
            if not msg:
                break

            lines = msg.split("\r\n")
            first_line = lines[0]

            res = method_function_caller(first_line, cursor)
            conn.sendall(res)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        cursor.close()
        connection.close()
        conn.close()


def main():
    global shutdown_event
    sock_fd = sock()
    threads = []

    try:
        while True:
            try:
                conn, client_fd = sock_fd.accept()
                thread = threading.Thread(target=handle_client, args=(conn, client_fd), daemon = True)
                threads.append(thread)
                thread.start()
            except OSError:
                # Socket closed — stop accepting
                break

    except KeyboardInterrupt:
        print("\n[!] KeyboardInterrupt received: shutting down...")
        shutdown_event.set()
        sock_fd.close()  # Close socket early to unblock accept()

    # Wait for threads to finish
    for t in threads:
        t.join(timeout=2)  # Avoid hanging forever

    print("Server shut down cleanly.")


if __name__ == "__main__":
    main()