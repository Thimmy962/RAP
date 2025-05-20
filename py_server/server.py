from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3 as sql
import views, sys
from urllib.parse import urlparse, parse_qs

db = 'db.sqlite3'
with sql.connect('db.sqlite3') as connection:
    cursor = connection.cursor()


class Server(BaseHTTPRequestHandler):
    
    def common_headers(self):
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", ["get","put", "post"])

    def do_GET(self):
        # parse the url to extract path and query parameter
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)


        if path in ('/','/articles'): views.index(self, cursor, query_params)
        elif path in '/article/': views.about(self, cursor, query_params)
        elif path == '/hello': views.about(self, cursor, query_params)
        else: self.send_error(404, message = "Url not found")



def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: takes 1 positional argument which is the port number")
    try:
        httpd = HTTPServer(('localhost', int(sys.argv[1])), Server)
        print("Serving on http://localhost:8080")
        httpd.serve_forever()
    except KeyboardInterrupt:
        cursor.close()
        print("Shutting server down...")
        httpd.shutdown()



if __name__ == "__main__":
    main()
