import json
from urllib.parse import urlparse, parse_qs


def serializer(large_data):
    return [{"id": row[0], "title": row[1], "abstract": row[2]} for row in large_data]


def index(cursor, query_params=None):
    offset = int(query_params.get("offset", [0])[0])
    limit = int(query_params.get("limit", [10])[0])
    
    cmd = "SELECT id, title, abstract FROM article ORDER BY RANDOM() LIMIT ? OFFSET ?"
    results = cursor.execute(cmd, (limit, offset)).fetchall()

    if not results:
        response = json.dumps({"message": "No content Found"}, separators=(',', ':')).encode("UTF-8")
        res = (
            "HTTP/1.1 204 No Content\r\n"
            "Content-Type: application/json\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            "Access-Control-Allow-Methods: GET, PUT, POST\r\n"
            f"Content-Length: {len(response)}\r\n"
            "\r\n"
        ).encode("UTF-8") + response
        return res

    serialized = json.dumps(serializer(results), separators=(',', ':')).encode("UTF-8")
    res = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, PUT, POST\r\n"
        f"Content-Length: {len(serialized)}\r\n"
        "\r\n"
    ).encode("UTF-8") + serialized
    return res