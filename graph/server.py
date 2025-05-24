from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse, json
from schema import schema
import sqlite3 as sql
import sys


# HTTP handler
class GraphQLHandler(BaseHTTPRequestHandler):
    def common_headers(self):
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", ["get","put", "post"])
        
    def do_GET(self):
        if self.path.startswith("/graphql"):
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            query = query_params.get("query", [None])[0]

            if query:
                result = schema.execute(query)

                response = {}
                if result.errors:
                    print(result.errors)
                    self.send_response(404)
                    response["errors"] = [str(e) for e in result.errors]
                    self.common_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(200)
                    response["data"] = result.data
                    
                    self.common_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())

            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing 'query' parameter in URL")
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: Programme takes one argument which is the port number")

    server_address = ("", int(sys.argv[1]))
    httpd = HTTPServer(server_address, GraphQLHandler)
    print(f"Serving on http://localhost:{sys.argv[1]}/graphql")
    httpd.serve_forever()