from http.server import HTTPServer
from api_request_handler import APIRequestHandler

PORT = 8000
def run(server_class=HTTPServer, handler_class=APIRequestHandler):
    server_address = ('', PORT)
    print(f"Server running at http://localhost:{PORT}")
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
