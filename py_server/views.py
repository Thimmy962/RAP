import json
from urllib.parse import urlparse, parse_qs


def serializer(large_data):
    return [{"id": row[0], "title": row[1], "abstract": row[2]} for row in large_data]


def index(self, cursor, query_params = None):


    # Get 'offset' and 'limit' with fallback defaults
    offset = int(query_params.get("offset", [0])[0])  # default to 0
    limit = int(query_params.get("limit", [10])[0])
    
    cmd = "SELECT id, title, abstract FROM article ORDER BY RANDOM() LIMIT ? OFFSET ?"
    results = cursor.execute(cmd, (limit, offset)).fetchall()

    if not results:
        self.send_response(204)  # No Content
        self.end_headers()
        return
    serialized = serializer(results)
    response = json.dumps(serialized, separators=(',', ':')).encode()
    self.send_response(200)
    self.send_header("Content-Length", str(len(response)))
    self.common_headers()
    self.end_headers()
    self.wfile.write(response)


def about(self, cursor, query_params = None):
    data = [{"title": "A cap", "body": "A very big cap"}]
    response = json.dumps(data, separators=(',', ':')).encode()
    self.send_response(200)
    self.send_header("Content-Length", str(len(response)))
    self.common_headers()
    self.end_headers()
    self.wfile.write(response)