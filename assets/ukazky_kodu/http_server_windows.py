class Handler(BaseHTTPRequestHandler):
    def handle_request(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length < 0 or length > 16384:
            self.send_error(413, "Payload too large")
            return
        if self.command == "POST":
            self.rfile.read(length)
        payload = b"Suricata advanced HTTP lab: OK\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()
