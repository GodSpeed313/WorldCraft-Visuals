# =============================================================
#  MYTHOS-SYNC — WEB SERVER
#  Serves dashboard.html AND runs fusions via the browser UI
# =============================================================

import json
import os
import socket
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlsplit

from console import use_utf8_output
from mythos_sync import build_legacy_profile, save_to_matrix, load_matrix, export_for_web

# AUTH-009: fixed production values. Deliberately NOT derived from the bound
# port, so a test server on an ephemeral port cannot loosen them.
ALLOWED_HOSTS = ('localhost:8000', '127.0.0.1:8000')
ALLOWED_ORIGINS = ('http://localhost:8000', 'http://127.0.0.1:8000')
ALLOWED_GET_PATHS = ('/dashboard.html', '/containment_matrix.json')
MAX_BODY_BYTES = 65536


class MythosHandler(SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # silence default server logs

    # --- AUTH-009 request validation -------------------------------------
    def _host_allowed(self):
        """Host must be exactly an allowed value (DNS-rebinding defence)."""
        if self.headers.get('Host') in ALLOWED_HOSTS:
            return True
        self._respond(403, {"error": "Forbidden host."})
        return False

    def _path_allowed(self):
        # Match the RAW request-line target, not self.path: CPython rewrites a
        # leading '//' to '/' before this runs (gh-87389, 3.12), which would
        # let '//dashboard.html' through on some versions and not others.
        parts = self.requestline.split()
        target = parts[1] if len(parts) > 1 else self.path
        try:
            return urlsplit(target).path in ALLOWED_GET_PATHS
        except ValueError:
            return False

    def _serve_allowlisted(self, serve):
        if not self._host_allowed():
            return
        if not self._path_allowed():
            self._respond(404, {"error": "Not found"})
            return
        serve()

    def do_GET(self):
        self._serve_allowlisted(super().do_GET)

    def do_HEAD(self):
        self._serve_allowlisted(super().do_HEAD)

    def _is_json_request(self):
        media = self.headers.get('Content-Type', '').split(';', 1)[0].strip().lower()
        return media == 'application/json'

    def _content_length(self):
        """Validated Content-Length (absent = 0), or None once a 400/413 was sent."""
        raw = self.headers.get('Content-Length')
        if raw is None:
            return 0
        raw = raw.strip()
        if not (raw.isascii() and raw.isdigit()):
            self._respond(400, {"error": "Invalid Content-Length."})
            return None
        digits = raw.lstrip('0') or '0'
        if len(digits) > 18 or int(digits) > MAX_BODY_BYTES:
            self._respond(413, {"error": "Request body too large."})
            return None
        return int(digits)

    def _read_fuse_request(self, length):
        """(alpha, beta, dominance), or None once a 400 has been sent."""
        try:
            data = json.loads(self.rfile.read(length))
        except (ValueError, RecursionError):
            self._respond(400, {"error": "Request body must be valid JSON."})
            return None
        if not isinstance(data, dict):
            self._respond(400, {"error": "Request body must be a JSON object."})
            return None
        alpha = data.get('alpha', '')
        beta = data.get('beta', '')
        if not isinstance(alpha, str) or not isinstance(beta, str):
            self._respond(400, {"error": "Alpha and Beta must be strings."})
            return None
        try:
            dominance = int(data.get('dominance', 50))
        except (TypeError, ValueError, OverflowError):
            self._respond(400, {"error": "Dominance must be a number."})
            return None
        return alpha.strip(), beta.strip(), dominance

    def end_headers(self):
        self.send_header('Content-Security-Policy', 
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; "
    "connect-src 'self';")
        
        super().end_headers()

    def do_POST(self):
        # Order: Host -> path -> Origin -> Content-Type -> Content-Length ->
        # body parsing -> field validation. An ABSENT Origin is allowed (local
        # non-browser clients send none); a present one, incl. "null", is not.
        if not self._host_allowed():
            return
        if self.path not in ('/fuse', '/clear'):
            self._respond(404, {"error": "Not found"})
            return
        origin = self.headers.get('Origin')
        if origin is not None and origin not in ALLOWED_ORIGINS:
            self._respond(403, {"error": "Forbidden origin."})
            return
        if self.path == '/fuse' and not self._is_json_request():
            self._respond(415, {"error": "Content-Type must be application/json."})
            return
        length = self._content_length()
        if length is None:
            return

        if self.path == '/fuse':
            parsed = self._read_fuse_request(length)
            if parsed is None:
                return
            alpha, beta, dominance = parsed

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

    def _respond(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)

    def finish(self):
        # AUTH-009: a POST rejected before its body was read leaves request
        # bytes unread, and closing then sends a TCP RST that can destroy the
        # 403/400/413/415 before the client reads it. Half-close, then drain a
        # bounded amount, before the normal close. POST only.
        if getattr(self, 'command', None) == 'POST':
            try:
                self.connection.shutdown(socket.SHUT_WR)
                deadline = time.monotonic() + 0.5
                left = MAX_BODY_BYTES
                while left > 0:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        break
                    self.connection.settimeout(remaining)
                    chunk = self.connection.recv(min(left, 4096))
                    if not chunk:
                        break
                    left -= len(chunk)
            except OSError:
                pass
        super().finish()


def make_server(host='127.0.0.1', port=8000):
    """Build the bound server without serving. AUTH-009 section H: exists so
    startup and binding can be tested in an isolated process."""
    return HTTPServer((host, port), MythosHandler)


if __name__ == '__main__':
    use_utf8_output()
    port = 8000
    print(f"\n{'═'*50}")
    print(f"  🌌 MYTHOS-SYNC SERVER — LIVE ON PORT {port}")
    print(f"  Open: http://localhost:{port}/dashboard.html")
    print(f"{'═'*50}\n")
    make_server().serve_forever()