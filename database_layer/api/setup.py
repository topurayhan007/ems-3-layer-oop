import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Starting http://0.0.0.0:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("Stopping by Ctrl+C")
    httpd.server_close()