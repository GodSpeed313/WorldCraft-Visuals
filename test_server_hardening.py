"""AUTH-009 regression tests for server.py hardening.

Every test that talks to the server runs it in a SEPARATE SUBPROCESS whose
working directory is a fresh temporary directory, bound to 127.0.0.1 on an
ephemeral port. The repository is importable by absolute path only. Nothing
here binds port 8000, uses the real containment_matrix.json as a fixture, or
depends on another test having run first.

Safeguards, in order of strength:
  1. The server's working directory is a temporary directory, so the relative
     path that /clear deletes (and that mythos_sync reads and writes) resolves
     inside it. The child refuses to start if its cwd is the repository.
  2. The child installs an audit hook that raises if anything opens, removes,
     renames, replaces or truncates the real repository matrix.
  3. The real matrix's SHA-256 (or its absence) is checked before and after
     every test. This is a tripwire, not the isolation mechanism.

Production Host and Origin validation is never weakened for these tests. The
client sends the literal production values ("localhost:8000", ...) to the
ephemeral-port server, and a Host carrying the ephemeral port is asserted to be
REJECTED.

Residual risk, documented here as AUTH-009 section D requires: a POST with NO
Origin header is allowed. Origin only constrains browsers, so a local
non-browser client can still call the endpoints.
"""

import ast
import collections
import hashlib
import http.client
import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import unittest

REPO = os.path.dirname(os.path.abspath(__file__))
REAL_MATRIX = os.path.join(REPO, 'containment_matrix.json')
SERVER_SRC = os.path.join(REPO, 'server.py')

ALLOWED_HOSTS = ('localhost:8000', '127.0.0.1:8000')
ALLOWED_ORIGINS = ('http://localhost:8000', 'http://127.0.0.1:8000')
HOST = ALLOWED_HOSTS[0]
ORIGIN = ALLOWED_ORIGINS[0]
MAX_BODY = 65536
TIMEOUT = 4  # seconds per request; a hung server is a test failure

CSP = ("default-src 'self'; "
       "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src https://fonts.gstatic.com; "
       "connect-src 'self';")

ALPHA, BETA = 'Malcolm X', 'Vash'          # both in CHARACTER_REGISTRY
UNKNOWN_A, UNKNOWN_B = 'Zzz Nobody', 'Qqq Nobody'

CANARY = 'AUTH009-CANARY-MUST-NEVER-BE-SERVED'
SEED_MATRIX = [{
    'id': 'SEED-1',
    'fusion_name': 'Seed x Seed',
    'modality': 'GROUNDED',
    'signature_ability': 'seed ability',
    'biome': 'seed biome',
}]
SEED_BYTES = json.dumps(SEED_MATRIX, indent=2).encode()
DASHBOARD_STUB = '<!doctype html><title>stub dashboard</title>'
FIXTURE_FILES = {
    'dashboard.html': DASHBOARD_STUB,
    'secret.txt': CANARY,
    '.hidden': CANARY,
    os.path.join('.git', 'config'): CANARY,
    'server.py': '# ' + CANARY,
    os.path.join('docs', 'note.md'): CANARY,
}

_DRIVER = r'''
import json, os, sys
repo = sys.argv[1]
cwd = os.path.realpath(os.getcwd())
if os.path.normcase(cwd) == os.path.normcase(os.path.realpath(repo)):
    sys.stderr.write("AUTH-009 test refuses to run with the repository as cwd\n")
    sys.exit(3)
sys.path[:] = [p for p in sys.path if p not in ("", cwd)]
sys.path.insert(0, repo)
_real = os.path.normcase(os.path.realpath(os.path.join(repo, "containment_matrix.json")))
_busy = [False]
def _guard(event, args):
    if _busy[0] or event not in ("open", "os.remove", "os.rename", "os.replace", "os.truncate"):
        return
    p = args[0]
    if not isinstance(p, (str, bytes, os.PathLike)):
        return
    _busy[0] = True
    try:
        rp = os.path.normcase(os.path.realpath(os.fsdecode(p)))
    except Exception:
        return
    finally:
        _busy[0] = False
    if rp == _real:
        raise RuntimeError("AUTH-009 test guard: the real matrix was touched: " + rp)
sys.addaudithook(_guard)
import server
srv = server.make_server("127.0.0.1", 0)
print(json.dumps(list(srv.socket.getsockname())), flush=True)
srv.serve_forever()
'''

Resp = collections.namedtuple('Resp', 'status headers body')


def _real_matrix_state():
    """SHA-256 of the real matrix, or None if absent. Read-only."""
    try:
        with open(REAL_MATRIX, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        return None


def _disjoint(a, b):
    a, b = os.path.normcase(os.path.realpath(a)), os.path.normcase(os.path.realpath(b))
    try:
        return os.path.commonpath([a, b]) not in (a, b)
    except ValueError:  # different drives
        return True


class ServerCase(unittest.TestCase):
    """One isolated server subprocess per test, with its own fixtures."""

    def setUp(self):
        self._real_before = _real_matrix_state()
        self.addCleanup(self._assert_real_matrix_untouched)

        tmp = tempfile.TemporaryDirectory(prefix='auth009_', ignore_cleanup_errors=True)
        self.addCleanup(tmp.cleanup)  # runs after _stop (cleanups are LIFO)
        self.root = tmp.name
        self.assertTrue(_disjoint(self.root, REPO),
                        'temporary directory must be outside the repository')
        for rel, text in FIXTURE_FILES.items():
            path = os.path.join(self.root, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
        self.reseed()
        self.seeded_names = set(self._listing())

        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')
        self.log = collections.deque(maxlen=60)
        self.proc = subprocess.Popen(
            [sys.executable, '-B', '-c', _DRIVER, REPO],
            cwd=self.root, env=env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.addCleanup(self._stop)
        first = self._readline(15)
        try:
            self.bound = tuple(json.loads(first))
        except ValueError:
            self.fail('server subprocess did not report an address; output: %r (exit %r)'
                      % (first + b''.join(self.log), self.proc.poll()))
        self.port = self.bound[1]
        self._drain = threading.Thread(target=self._drain_output, daemon=True)
        self._drain.start()

    # ---- process plumbing -------------------------------------------------
    def _readline(self, timeout):
        box = []
        t = threading.Thread(target=lambda: box.append(self.proc.stdout.readline()), daemon=True)
        t.start()
        t.join(timeout)
        if t.is_alive() or not box or not box[0]:
            self.fail('server subprocess did not report its bound address within %ss (exit %r)'
                      % (timeout, self.proc.poll()))
        return box[0]

    def _drain_output(self):
        for line in self.proc.stdout:
            self.log.append(line)

    def _stop(self):
        self.proc.terminate()
        try:
            self.proc.wait(5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait(5)
        if getattr(self, '_drain', None):
            self._drain.join(3)
        self.proc.stdout.close()

    def _assert_real_matrix_untouched(self):
        self.assertEqual(_real_matrix_state(), self._real_before,
                         'the REAL containment_matrix.json changed during a test')

    # ---- fixtures ---------------------------------------------------------
    @property
    def matrix_path(self):
        return os.path.join(self.root, 'containment_matrix.json')

    def reseed(self):
        with open(self.matrix_path, 'wb') as f:
            f.write(SEED_BYTES)

    def matrix_bytes(self):
        try:
            with open(self.matrix_path, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            return None

    def assertMatrixIntact(self):
        self.assertEqual(self.matrix_bytes(), SEED_BYTES,
                         'the temporary matrix fixture was modified or deleted by a request '
                         'that must have been rejected')

    def _listing(self):
        out = []
        for base, _dirs, files in os.walk(self.root):
            for name in files:
                out.append(os.path.relpath(os.path.join(base, name), self.root))
        return out

    # ---- client -----------------------------------------------------------
    def request(self, method, path, headers=None, body=None, host=HOST):
        """Send one raw request. host=None sends no Host header at all."""
        headers = dict(headers or {})
        conn = http.client.HTTPConnection('127.0.0.1', self.port, timeout=TIMEOUT)
        try:
            conn.putrequest(method, path, skip_host=True, skip_accept_encoding=True)
            if host is not None:
                conn.putheader('Host', host)
            for k, v in headers.items():
                conn.putheader(k, v)
            if body is not None and not any(k.lower() == 'content-length' for k in headers):
                conn.putheader('Content-Length', str(len(body)))
            conn.endheaders(body)
            resp = conn.getresponse()
            data = resp.read()
            return Resp(resp.status, {k.lower(): v for k, v in resp.getheaders()}, data)
        except (socket.timeout, TimeoutError) as e:
            self.fail('%s %s timed out (server hung or never answered): %r' % (method, path, e))
        except (ConnectionError, http.client.HTTPException, OSError) as e:
            self.fail('%s %s got no valid response (handler crash or dropped connection): %r'
                      % (method, path, e))
        finally:
            conn.close()

    def post_fuse(self, payload, headers=None, host=HOST):
        hdrs = {'Content-Type': 'application/json'}
        hdrs.update(headers or {})
        body = payload if isinstance(payload, bytes) else json.dumps(
            payload, separators=(',', ':')).encode()
        return self.request('POST', '/fuse', hdrs, body, host=host)

    def valid_fuse(self, **kw):
        return self.post_fuse({'alpha': ALPHA, 'beta': BETA, 'dominance': 60}, **kw)


# ---------------------------------------------------------------------------
# Production defaults and actual binding (A, H)
# ---------------------------------------------------------------------------
class ProductionStartupStructureTests(unittest.TestCase):
    """Production defaults, checked from source structure only. Port 8000 is
    never bound here; the actual bound socket is asserted in BindingTests."""

    def setUp(self):
        with open(SERVER_SRC, 'r', encoding='utf-8') as f:
            self.tree = ast.parse(f.read(), filename=SERVER_SRC)

    def _make_server_def(self):
        defs = [n for n in self.tree.body
                if isinstance(n, ast.FunctionDef) and n.name == 'make_server']
        self.assertEqual(len(defs), 1,
                         'server.py must define exactly one top-level make_server(); '
                         'the AUTH-009 startup structure changed')
        return defs[0]

    def _main_block(self):
        def is_guard(test):
            return (isinstance(test, ast.Compare)
                    and isinstance(test.left, ast.Name) and test.left.id == '__name__'
                    and len(test.ops) == 1 and isinstance(test.ops[0], ast.Eq)
                    and len(test.comparators) == 1
                    and isinstance(test.comparators[0], ast.Constant)
                    and test.comparators[0].value == '__main__')
        blocks = [n for n in self.tree.body if isinstance(n, ast.If) and is_guard(n.test)]
        self.assertEqual(len(blocks), 1,
                         "server.py must have exactly one top-level `if __name__ == '__main__':`")
        return blocks[0]

    def test_make_server_signature_defaults_are_loopback_8000(self):
        fn = self._make_server_def()
        self.assertEqual([a.arg for a in fn.args.args], ['host', 'port'],
                         'make_server must take exactly (host, port)')
        self.assertEqual(fn.args.kwonlyargs, [])
        self.assertIsNone(fn.args.vararg)
        self.assertIsNone(fn.args.kwarg)
        self.assertEqual([ast.literal_eval(d) for d in fn.args.defaults], ['127.0.0.1', 8000],
                         'make_server defaults must be host="127.0.0.1", port=8000')

    def test_main_calls_make_server_without_overrides_then_serves(self):
        main = self._main_block()
        nodes = [n for stmt in main.body for n in ast.walk(stmt)]
        calls = [n for n in nodes if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Name) and n.func.id == 'make_server']
        self.assertEqual(len(calls), 1,
                         '__main__ must call make_server exactly once')
        self.assertEqual((calls[0].args, calls[0].keywords), ([], []),
                         '__main__ must call make_server() with no host or port overrides')
        serves = [n for n in nodes if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Attribute) and n.func.attr == 'serve_forever'
                  and n.func.value is calls[0]]
        self.assertEqual(len(serves), 1, '__main__ must call make_server().serve_forever()')
        direct = [n for n in nodes if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Name) and n.func.id == 'HTTPServer']
        self.assertEqual(direct, [], '__main__ must not construct HTTPServer directly')


class BindingTests(ServerCase):
    def test_bound_socket_is_loopback_on_an_ephemeral_port(self):
        host, port = self.bound
        self.assertEqual(host, '127.0.0.1', 'the server bound %r, not loopback' % (host,))
        self.assertNotIn(port, (0, 8000), 'the test server must use an ephemeral port')
        self.assertGreaterEqual(port, 1024)
        with socket.create_connection(('127.0.0.1', port), timeout=TIMEOUT):
            pass

    def test_startup_creates_no_files_and_touches_no_data(self):
        self.assertIsNone(self.proc.poll(), 'server exited during startup')
        self.assertEqual(set(self._listing()), self.seeded_names,
                         'importing/starting the server created or removed files')
        self.assertMatrixIntact()


# ---------------------------------------------------------------------------
# Dashboard request shapes and positive allowlist acceptance (C, D, E, F)
# ---------------------------------------------------------------------------
class DashboardShapeTests(ServerCase):
    def test_dashboard_fuse_registered_names(self):
        r = self.post_fuse({'alpha': ALPHA, 'beta': BETA, 'dominance': 60},
                           headers={'Origin': ORIGIN})
        self.assertEqual(r.status, 200, r.body)
        data = json.loads(r.body)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['profile']['fusion_name'], '%s x %s' % (ALPHA, BETA))
        saved = json.loads(self.matrix_bytes())
        self.assertIn('%s x %s' % (ALPHA, BETA), [m['fusion_name'] for m in saved])

    def test_dashboard_fuse_unknown_names_persist_a_cautionary_stub(self):
        r = self.post_fuse({'alpha': UNKNOWN_A, 'beta': UNKNOWN_B, 'dominance': 50},
                           headers={'Origin': ORIGIN})
        self.assertEqual(r.status, 200, r.body)
        profile = json.loads(r.body)['profile']
        self.assertEqual(profile['state'], 'CAUTIONARY')
        self.assertIsNone(profile['modality'])
        saved = json.loads(self.matrix_bytes())
        self.assertTrue(any(m.get('state') == 'CAUTIONARY' for m in saved),
                        'the CAUTIONARY stub must still be persisted (AUTH-007 exclusion)')

    def test_dashboard_clear_with_content_length_zero_and_no_content_type(self):
        r = self.request('POST', '/clear', {'Origin': ORIGIN, 'Content-Length': '0'})
        self.assertEqual(r.status, 200, r.body)
        self.assertEqual(json.loads(r.body), {'status': 'cleared'})
        self.assertIsNone(self.matrix_bytes(), '/clear must delete the TEMPORARY matrix')

    def test_dashboard_clear_with_no_content_length_header_at_all(self):
        r = self.request('POST', '/clear', {'Origin': ORIGIN})
        self.assertEqual(r.status, 200, r.body)
        self.assertIsNone(self.matrix_bytes())

    def test_dashboard_matrix_get_with_cache_busting_query(self):
        r = self.request('GET', '/containment_matrix.json?t=1730000000000')
        self.assertEqual(r.status, 200)
        self.assertEqual(r.body, SEED_BYTES)


class AllowlistAcceptanceTests(ServerCase):
    """AUTH-009 Amendment 1: mandatory positive tests, production values only."""

    def test_post_fuse_succeeds_with_each_allowed_origin(self):
        for origin in ALLOWED_ORIGINS:
            with self.subTest(origin=origin):
                r = self.valid_fuse(headers={'Origin': origin})
                self.assertEqual(r.status, 200, r.body)

    def test_post_clear_succeeds_with_each_allowed_origin(self):
        for origin in ALLOWED_ORIGINS:
            with self.subTest(origin=origin):
                self.reseed()
                r = self.request('POST', '/clear', {'Origin': origin})
                self.assertEqual(r.status, 200, r.body)
                self.assertIsNone(self.matrix_bytes())

    def test_get_dashboard_succeeds_with_each_allowed_host(self):
        for host in ALLOWED_HOSTS:
            with self.subTest(host=host):
                r = self.request('GET', '/dashboard.html', host=host)
                self.assertEqual(r.status, 200)
                self.assertEqual(r.body, DASHBOARD_STUB.encode())

    def test_head_dashboard_succeeds_with_each_allowed_host(self):
        for host in ALLOWED_HOSTS:
            with self.subTest(host=host):
                r = self.request('HEAD', '/dashboard.html', host=host)
                self.assertEqual(r.status, 200)
                self.assertEqual(r.body, b'')

    def test_absent_origin_is_allowed_documented_residual_risk(self):
        # Local non-browser clients send no Origin; this is accepted (section D).
        self.assertEqual(self.valid_fuse().status, 200)
        self.reseed()
        self.assertEqual(self.request('POST', '/clear').status, 200)


# ---------------------------------------------------------------------------
# F: GET/HEAD allowlist
# ---------------------------------------------------------------------------
class GetHeadAllowlistTests(ServerCase):
    ALLOWED = ('/dashboard.html', '/containment_matrix.json',
               '/dashboard.html?t=1', '/containment_matrix.json?t=123')
    DENIED = ('/', '/server.py', '/.hidden', '/.git/config', '/.git/', '/secret.txt',
              '/docs/note.md', '/docs/', '/nope.html', '/dashboard.html/',
              '/dashboard%2ehtml', '/containment_matrix.json/x', '/../server.py',
              '//dashboard.html')  # asserts the 404 OUTCOME only, not how it is parsed

    def test_allowed_paths_are_served_on_get_and_head(self):
        for path in self.ALLOWED:
            for method in ('GET', 'HEAD'):
                with self.subTest(path=path, method=method):
                    r = self.request(method, path)
                    self.assertEqual(r.status, 200)
                    if method == 'HEAD':
                        self.assertEqual(r.body, b'')

    def test_unapproved_paths_return_404_on_get_and_head(self):
        for path in self.DENIED:
            for method in ('GET', 'HEAD'):
                with self.subTest(path=path, method=method):
                    r = self.request(method, path)
                    self.assertEqual(r.status, 404)
                    self.assertNotIn(CANARY.encode(), r.body)
                    if method == 'HEAD':
                        self.assertEqual(r.body, b'')


# ---------------------------------------------------------------------------
# E: Host validation (before path, Origin, Content-Type, Content-Length, body)
# ---------------------------------------------------------------------------
class HostValidationTests(ServerCase):
    def bad_hosts(self):
        return ['evil.example', 'evil.example:8000', 'localhost', '127.0.0.1',
                'localhost:8001', '127.0.0.1:%d' % self.port, 'localhost:%d' % self.port,
                'LOCALHOST:8000', 'localhost:8000.evil.example', '[::1]:8000', '', None]

    def test_bad_host_rejected_on_get_and_head(self):
        for host in self.bad_hosts():
            for method in ('GET', 'HEAD'):
                with self.subTest(host=host, method=method):
                    self.assertEqual(self.request(method, '/dashboard.html', host=host).status, 403)

    def test_bad_host_rejected_on_post_clear_and_nothing_is_deleted(self):
        for host in self.bad_hosts():
            with self.subTest(host=host):
                self.assertEqual(self.request('POST', '/clear', host=host).status, 403)
                self.assertMatrixIntact()

    def test_bad_host_rejected_on_post_fuse_and_nothing_is_written(self):
        for host in self.bad_hosts():
            with self.subTest(host=host):
                self.assertEqual(self.valid_fuse(host=host).status, 403)
                self.assertMatrixIntact()

    def test_host_is_checked_before_path_and_before_anything_else(self):
        self.assertEqual(self.request('GET', '/server.py', host='evil.example').status, 403)
        self.assertEqual(self.request('POST', '/nonexistent', host='evil.example').status, 403)
        self.assertEqual(self.request('POST', '/fuse', {'Origin': 'http://evil.example',
                                                        'Content-Length': 'abc'},
                                      host='evil.example').status, 403)
        self.assertMatrixIntact()


# ---------------------------------------------------------------------------
# D: Origin validation (POST)
# ---------------------------------------------------------------------------
class OriginValidationTests(ServerCase):
    FOREIGN = ('http://evil.example', 'null', 'http://localhost:8001', 'https://localhost:8000',
               'http://localhost:8000/', 'http://LOCALHOST:8000', 'http://127.0.0.1',
               'http://localhost:8000.evil.example', '')

    def test_foreign_origin_rejected_on_clear_and_nothing_is_deleted(self):
        for origin in self.FOREIGN:
            with self.subTest(origin=origin):
                self.assertEqual(self.request('POST', '/clear', {'Origin': origin}).status, 403)
                self.assertMatrixIntact()

    def test_foreign_origin_rejected_on_fuse_and_nothing_is_written(self):
        for origin in self.FOREIGN:
            with self.subTest(origin=origin):
                self.assertEqual(self.valid_fuse(headers={'Origin': origin}).status, 403)
                self.assertMatrixIntact()

    def test_literal_null_origin_is_foreign_not_absent(self):
        self.assertEqual(self.request('POST', '/clear', {'Origin': 'null'}).status, 403)
        self.assertMatrixIntact()


# ---------------------------------------------------------------------------
# C: Content-Type on /fuse
# ---------------------------------------------------------------------------
class ContentTypeTests(ServerCase):
    def fuse_with_type(self, ctype):
        headers = {} if ctype is None else {'Content-Type': ctype}
        body = json.dumps({'alpha': ALPHA, 'beta': BETA, 'dominance': 60}).encode()
        return self.request('POST', '/fuse', headers, body)

    def test_unsupported_content_type_on_fuse_is_415_and_writes_nothing(self):
        for ctype in (None, '', 'text/plain', 'application/x-www-form-urlencoded',
                      'multipart/form-data; boundary=x', 'application/jsonx', 'text/json'):
            with self.subTest(content_type=ctype):
                self.assertEqual(self.fuse_with_type(ctype).status, 415)
                self.assertMatrixIntact()

    def test_json_media_type_with_parameters_is_accepted(self):
        for ctype in ('application/json', 'application/json; charset=utf-8', 'APPLICATION/JSON'):
            with self.subTest(content_type=ctype):
                self.assertEqual(self.fuse_with_type(ctype).status, 200)

    def test_clear_does_not_require_a_content_type(self):
        for headers in ({}, {'Content-Type': 'text/plain'}):
            with self.subTest(headers=headers):
                self.reseed()
                self.assertEqual(self.request('POST', '/clear', headers).status, 200)


# ---------------------------------------------------------------------------
# G: Content-Length
# ---------------------------------------------------------------------------
class ContentLengthTests(ServerCase):
    MALFORMED = ('abc', '1.5', '+5', '0x10', '5 5', '1e3', '')

    def test_fuse_without_content_length_is_an_empty_body_and_400(self):
        r = self.request('POST', '/fuse', {'Content-Type': 'application/json'})
        self.assertEqual(r.status, 400)
        self.assertMatrixIntact()

    def test_fuse_malformed_content_length_is_400(self):
        for value in self.MALFORMED:
            with self.subTest(value=value):
                r = self.request('POST', '/fuse', {'Content-Type': 'application/json',
                                                   'Content-Length': value})
                self.assertEqual(r.status, 400)
                self.assertMatrixIntact()

    def test_fuse_negative_content_length_is_400(self):
        for value in ('-1', '-100'):
            with self.subTest(value=value):
                r = self.request('POST', '/fuse', {'Content-Type': 'application/json',
                                                   'Content-Length': value})
                self.assertEqual(r.status, 400)
                self.assertMatrixIntact()

    def test_fuse_oversize_content_length_is_413_without_reading_the_body(self):
        # No body is sent: a server that tried to read it would hang until TIMEOUT.
        for value in (str(MAX_BODY + 1), '99999999999', '9' * 5000):
            with self.subTest(value=value[:12]):
                r = self.request('POST', '/fuse', {'Content-Type': 'application/json',
                                                   'Content-Length': value})
                self.assertEqual(r.status, 413)
                self.assertMatrixIntact()

    def test_fuse_body_of_exactly_the_cap_is_accepted(self):
        base = json.dumps({'alpha': ALPHA, 'beta': BETA, 'dominance': 50}).encode()
        body = base + b' ' * (MAX_BODY - len(base))
        self.assertEqual(len(body), MAX_BODY)
        r = self.request('POST', '/fuse', {'Content-Type': 'application/json'}, body)
        self.assertEqual(r.status, 200, r.body)

    def test_clear_without_content_length_succeeds(self):
        self.assertEqual(self.request('POST', '/clear').status, 200)
        self.assertIsNone(self.matrix_bytes())

    def test_clear_with_zero_content_length_succeeds(self):
        self.assertEqual(self.request('POST', '/clear', {'Content-Length': '0'}).status, 200)
        self.assertIsNone(self.matrix_bytes())

    def test_clear_malformed_negative_or_oversize_content_length_is_rejected(self):
        cases = [(v, 400) for v in self.MALFORMED] + [('-1', 400), (str(MAX_BODY + 1), 413),
                                                       ('9' * 5000, 413)]
        for value, expected in cases:
            with self.subTest(value=value[:12]):
                r = self.request('POST', '/clear', {'Content-Length': value})
                self.assertEqual(r.status, expected)
                self.assertMatrixIntact()


# ---------------------------------------------------------------------------
# G: JSON and field validation
# ---------------------------------------------------------------------------
class JsonAndFieldTests(ServerCase):
    def test_malformed_json_or_non_object_body_is_400(self):
        for body in (b'{bad', b'', b'\xff\xfe', b'[]', b'"x"', b'null', b'123'):
            with self.subTest(body=body):
                r = self.post_fuse(body)
                self.assertEqual(r.status, 400)
                self.assertIn('error', json.loads(r.body))
                self.assertMatrixIntact()

    def test_invalid_field_types_are_400(self):
        good = {'alpha': ALPHA, 'beta': BETA}
        for change in ({'alpha': 123}, {'alpha': None}, {'alpha': True}, {'beta': []},
                       {'beta': {}}, {'dominance': 'abc'}, {'dominance': None},
                       {'dominance': []}, {'dominance': {}}):
            with self.subTest(change=change):
                r = self.post_fuse(dict(good, **change))
                self.assertEqual(r.status, 400)
                self.assertMatrixIntact()

    def test_non_finite_dominance_is_400(self):
        body = ('{"alpha": "%s", "beta": "%s", "dominance": Infinity}' % (ALPHA, BETA)).encode()
        self.assertEqual(self.post_fuse(body).status, 400)
        self.assertMatrixIntact()

    def test_existing_required_field_error_is_preserved(self):
        for payload in ({}, {'alpha': '  ', 'beta': BETA}, {'alpha': ALPHA, 'beta': ''}):
            with self.subTest(payload=payload):
                r = self.post_fuse(payload)
                self.assertEqual(r.status, 400)
                self.assertEqual(json.loads(r.body), {'error': 'Alpha and Beta are required.'})
                self.assertMatrixIntact()

    def test_existing_int_conversion_semantics_are_preserved(self):
        for dominance in ('60', 60.7):
            with self.subTest(dominance=dominance):
                r = self.post_fuse({'alpha': ALPHA, 'beta': BETA, 'dominance': dominance})
                self.assertEqual(r.status, 200, r.body)

    def test_unknown_post_path_is_still_404(self):
        self.assertEqual(self.request('POST', '/nope', {'Origin': ORIGIN}, b'{}').status, 404)
        self.assertMatrixIntact()


# ---------------------------------------------------------------------------
# B and the CSP exclusion: response headers
# ---------------------------------------------------------------------------
class HeaderTests(ServerCase):
    def responses(self):
        yield 'GET 200', self.request('GET', '/dashboard.html')
        yield 'GET 404', self.request('GET', '/server.py')
        yield 'GET 403 (bad host)', self.request('GET', '/dashboard.html', host='evil.example')
        yield 'POST 200', self.valid_fuse(headers={'Origin': ORIGIN})
        yield 'POST 403 (foreign origin)', self.request('POST', '/clear', {'Origin': 'null'})
        yield 'POST 404', self.request('POST', '/nope', {'Origin': ORIGIN}, b'{}')
        yield 'OPTIONS', self.request('OPTIONS', '/fuse', {
            'Origin': 'http://evil.example', 'Access-Control-Request-Method': 'POST'})

    def test_no_response_carries_a_cors_allow_origin_header(self):
        for label, r in self.responses():
            with self.subTest(response=label):
                self.assertNotIn('access-control-allow-origin', r.headers)

    def test_options_is_unchanged_not_implemented_and_grants_no_cors(self):
        r = self.request('OPTIONS', '/fuse', {'Origin': 'http://evil.example',
                                              'Access-Control-Request-Method': 'POST'})
        self.assertEqual(r.status, 501)
        self.assertFalse([h for h in r.headers if h.startswith('access-control-')])

    def test_csp_header_is_present_and_byte_identical_to_baseline(self):
        for label, r in (('GET 200', self.request('GET', '/dashboard.html')),
                         ('POST 200', self.valid_fuse(headers={'Origin': ORIGIN}))):
            with self.subTest(response=label):
                self.assertEqual(r.headers.get('content-security-policy'), CSP)


def tearDownModule():
    # Tripwire only: per-test checks above are the primary guard.
    assert _real_matrix_state() == _MODULE_START, 'the REAL containment_matrix.json changed'


_MODULE_START = _real_matrix_state()

if __name__ == '__main__':
    unittest.main()
