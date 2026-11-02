import threading
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class DemoHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def handle_probe(self):
        if self.command == "PUT":
            length = int(self.headers.get("Content-Length", 0))
            if not 0 <= length <= 1024:
                return self.send_error(413)
            self.rfile.read(length)
        grants = {"Bearer demo-read": ("A", False), "Bearer demo-edit": ("A", True)}
        grant = grants.get(self.headers.get("Authorization"))
        if not grant:
            status = 401
        elif self.path != "/tenants/" + grant[0] + "/item":
            status = 404
        elif self.command == "PUT" and not grant[1]:
            status = 403
        else:
            status = 204
        self.send_response(status)
        self.end_headers()

    do_GET = do_PUT = handle_probe


def probe(port, tokens, cases):
    if type(port) is not int or not 1 <= port <= 65535 or not cases:
        raise ValueError("valid port and nonempty matrix required")
    rows = []
    for case in cases:
        method, path, role = case["method"], case["path"], case["role"]
        if method not in ("GET","PUT") or not path.startswith("/") or path.startswith("//"):
            raise ValueError("unsupported request")
        connection = HTTPConnection("127.0.0.1", port, timeout=3)
        try:
            connection.request(method, path, body=b"probe" if method == "PUT" else None,
                               headers={"Authorization": "Bearer " + tokens[role]})
            observed = connection.getresponse().status
        finally:
            connection.close()
        rows.append(dict(method=method, path=path, role=role, expected=case["expected"], observed=observed))
    return {"passed": all(r["observed"] == r["expected"] for r in rows), "cases": rows}


def evaluate(data):
    if not data.get("demo"):
        return probe(data["port"], data["tokens"], data["cases"])
    with ThreadingHTTPServer(("127.0.0.1", 0), DemoHandler) as server:
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            return probe(server.server_port, {"reader":"demo-read","editor":"demo-edit","guest":"invalid"}, data["cases"])
        finally:
            server.shutdown()
            thread.join()
