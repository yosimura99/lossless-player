#!/usr/bin/env python3
"""Lossless Player - tiny static server + Internet Archive proxy.

Usage:  python3 server.py [port]     (default 8080, binds 0.0.0.0)

Routes:
  /                       -> index.html (static files from this folder)
  /api/search?<query>     -> https://archive.org/advancedsearch.php?<query>
  /api/meta/<identifier>  -> https://archive.org/metadata/<identifier>
  /stream/<id>/<file>     -> https://archive.org/download/<id>/<file> (Range supported)
Only archive.org is proxied (no open proxy).
"""
import os, re, sys, socket, urllib.request, urllib.error
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.abspath(__file__))
UA = "LosslessPlayer/1.0 (+local; Internet Archive client)"
ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")
PASS_HEADERS = ("Content-Type", "Content-Length", "Content-Range", "Accept-Ranges",
                "Last-Modified", "ETag")


class Handler(SimpleHTTPRequestHandler):
    server_version = "LosslessPlayer/1.0"

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Headers", "Range, Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.end_headers()

    def do_HEAD(self):
        self.route(head=True)

    def do_GET(self):
        self.route(head=False)

    def route(self, head):
        p = self.path
        if p.startswith("/api/search"):
            q = p.split("?", 1)[1] if "?" in p else ""
            return self.proxy("https://archive.org/advancedsearch.php?" + q, head, cache=60)
        if p.startswith("/api/meta/"):
            ident = p[len("/api/meta/"):].split("?")[0]
            if not ID_RE.match(ident):
                return self.send_error(400, "bad identifier")
            return self.proxy("https://archive.org/metadata/" + ident, head, cache=300)
        if p.startswith("/stream/"):
            rest = p[len("/stream/"):].split("?")[0]
            ident, _, fpath = rest.partition("/")
            if not ID_RE.match(ident) or not fpath or ".." in fpath.split("/"):
                return self.send_error(400, "bad path")
            return self.proxy("https://archive.org/download/%s/%s" % (ident, fpath), head)
        if p == "/healthz":
            body = b"ok"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if not head:
                self.wfile.write(body)
            return
        return super().do_HEAD() if head else super().do_GET()

    def proxy(self, url, head, cache=None):
        req = urllib.request.Request(url, method="HEAD" if head else "GET",
                                     headers={"User-Agent": UA})
        rng = self.headers.get("Range")
        if rng:
            req.add_header("Range", rng)
        try:
            resp = urllib.request.urlopen(req, timeout=30)
        except urllib.error.HTTPError as e:
            resp = e
        except Exception as e:  # network error
            return self.send_error(502, "upstream error: %s" % e)
        try:
            self.send_response(resp.status if hasattr(resp, "status") else resp.code)
            for h in PASS_HEADERS:
                v = resp.headers.get(h)
                if v:
                    self.send_header(h, v)
            if cache:
                self.send_header("Cache-Control", "public, max-age=%d" % cache)
            self.end_headers()
            if head:
                return
            while True:
                chunk = resp.read(64 * 1024)
                if not chunk:
                    break
                self.wfile.write(chunk)
        except (BrokenPipeError, ConnectionResetError, socket.timeout):
            pass  # client seeked / closed
        finally:
            try:
                resp.close()
            except Exception:
                pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 8080))
    ThreadingHTTPServer.daemon_threads = True
    srv = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print("Lossless Player running at http://localhost:%d/" % port, flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
