import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        code = 200
        marker = os.getenv("FAILURE_FILE", "/tmp/unhealthy")
        if self.path not in ("/health", "/live"):
            code = 404
        elif self.path == "/health" and os.path.exists(marker):
            code = 503

        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(f"{code}\n".encode())


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
