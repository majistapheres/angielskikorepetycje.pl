import http.server
import socketserver
import os
import sys

PORT = 8000

class CleanUrlHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve index.html for root
        if self.path == '/':
            self.path = '/index.html'
        
        # Check if path exists, if not try adding .html
        # Using normalized paths to prevent issues
        requested_path = self.path.split('?')[0].split('#')[0]
        full_path = os.getcwd() + requested_path.replace('/', os.sep)
        
        if not os.path.exists(full_path) and not requested_path.endswith('/'):
            if os.path.exists(full_path + '.html'):
                self.path = requested_path + '.html'
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

Handler = CleanUrlHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"\n========================================")
        print(f"🚀 SERVER RUNNING AT: http://localhost:{PORT}")
        print(f"Press CTRL+C to stop.")
        print(f"========================================\n")
        httpd.serve_forever()
except OSError as e:
    if e.errno == 98 or e.errno == 10048:
        print(f"❌ Error: Port {PORT} is already in use.")
        print(f"Please try a different port or close the application using it.")
    else:
        print(f"❌ An error occurred: {e}")
except KeyboardInterrupt:
    print("\n👋 Server stopped.")
