import http.server
import socketserver
import os
import json
import urllib.parse

PORT = 8080
DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class StudyViewerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/api/files':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            structure = {}
            for root, dirs, files in os.walk(DIRECTORY):
                # Ignore hidden dirs
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'RECURSOS' and d != 'Nueva carpeta']
                rel_root = os.path.relpath(root, DIRECTORY)
                
                md_files = []
                for file in files:
                    if file.endswith('.md') or file.endswith('.TXT'):
                        rel_path = os.path.join(rel_root, file).replace('\\', '/')
                        if rel_path.startswith('./'):
                            rel_path = rel_path[2:]
                        md_files.append({
                            'name': file,
                            'path': rel_path
                        })
                
                if md_files:
                    folder_name = rel_root if rel_root != '.' else '.'
                    structure[folder_name] = md_files

            self.wfile.write(json.dumps(structure, ensure_ascii=False).encode('utf-8'))
            return

        if parsed_path.path == '/' or parsed_path.path == '':
            self.path = '/RECURSOS/index.html'

        return super().do_GET()

print(f"🚀 Servidor de Estudio iniciado en http://localhost:{PORT}")
with socketserver.TCPServer(("", PORT), StudyViewerHandler) as httpd:
    httpd.serve_forever()
