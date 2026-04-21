# =============================================================
#  MYTHOS-SYNC — WEB SERVER
#  Serves dashboard.html AND runs fusions via the browser UI
# =============================================================

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

from mythos_sync import build_legacy_profile, save_to_matrix, load_matrix, export_for_web

class MythosHandler(SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # silence default server logs

    def do_GET(self):
        super().do_GET()

    def end_headers(self):
        self.send_header('Content-Security-Policy', 
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; "
    "connect-src 'self';")
        
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_POST(self):
        if self.path == '/fuse':
            length = int(self.headers.get('Content-Length', 0))
            body   = self.rfile.read(length)
            data   = json.loads(body)

            alpha     = data.get('alpha', '').strip()
            beta      = data.get('beta', '').strip()
            dominance = int(data.get('dominance', 50))

            if not alpha or not beta:
                self._respond(400, {"error": "Alpha and Beta are required."})
                return

            try:
                print(f"\n  🌐 [SERVER] Fusing: {alpha} x {beta} @ {dominance}% dominance")
                profile = build_legacy_profile(alpha, beta, dominance)
                save_to_matrix(profile)
                export_for_web()
                self._respond(200, {"status": "ok", "profile": profile})
            except Exception as e:
                self._respond(500, {"error": str(e)})

        elif self.path == '/clear':
            if os.path.exists('containment_matrix.json'):
                os.remove('containment_matrix.json')
                print("\n  🗑️  [SERVER] Matrix cleared.")
            self._respond(200, {"status": "cleared"})

        else:
            self._respond(404, {"error": "Not found"})

    def _respond(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    port = 8000
    print(f"\n{'═'*50}")
    print(f"  🌌 MYTHOS-SYNC SERVER — LIVE ON PORT {port}")
    print(f"  Open: http://localhost:{port}/dashboard.html")
    print(f"{'═'*50}\n")
    HTTPServer(('', port), MythosHandler).serve_forever()