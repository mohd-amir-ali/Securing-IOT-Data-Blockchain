import os
import re
import json
import mimetypes
from urllib.parse import parse_qs, urlparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from blockchain_engine import bridge, ensure_local_rpc_server

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

uname = "Amir"
logged_in = False
details = ""


def readDetails(contract_type):
    global details
    details = bridge.read_details(contract_type)
    return details


def saveDataBlockChain(currentData, contract_type):
    global details
    receipt = bridge.save_data_blockchain(currentData, contract_type)
    details = bridge.read_details(contract_type)
    return receipt


def build_operators_table_html() -> str:
    """Build the Admin-Only table of registered blockchain operators from WSNSecurity.getUser()."""
    users = bridge.get_parsed_users()
    if not users:
        return '<p style="color: var(--slate-muted);">No operators registered yet.</p>'

    rows = []
    for idx, u in enumerate(users, 1):
        role_badge = (
            '<span class="status-pill verified">● PRIMARY ADMIN</span>'
            if u["username"].lower() == "amir"
            else '<span class="status-pill verified">● AUTHORIZED OPERATOR</span>'
        )
        rows.append(
            f"<tr>"
            f'<td class="mono-cell">#{idx:02d}</td>'
            f'<td class="mono-cell"><strong>{u["username"]}</strong></td>'
            f'<td class="mono-cell">{u["phone"]}</td>'
            f'<td class="mono-cell">{u["email"]}</td>'
            f"<td>{u['address']}</td>"
            f"<td>{role_badge}</td>"
            f"</tr>"
        )

    return (
        '<div class="table-responsive">'
        '<table class="editorial-table">'
        "<thead><tr>"
        "<th>ID</th>"
        "<th>Operator Username</th>"
        "<th>Contact Number</th>"
        "<th>Email Address</th>"
        "<th>Node / Lab Location</th>"
        "<th>On-Chain Clearance</th>"
        "</tr></thead>"
        f'<tbody>{"".join(rows)}</tbody>'
        "</table></div>"
    )


def build_records_table_html(iot_id: str) -> str:
    """Build the editorial table HTML for ViewData.html while keeping backward compatibility."""
    records = bridge.get_parsed_iot_records(iot_id)
    filter_title = f"IOT-{iot_id}" if (iot_id and str(iot_id).upper() != "ALL") else "All 20 WSN Nodes (IOT-0 to IOT-19)"

    if not records:
        return (
            f'<div class="empty-state">'
            f'<div class="eyebrow-label">03 // QUERY RESULT — {filter_title}</div>'
            f'<h4>No sensor blocks found for {filter_title} yet.</h4>'
            f'<p>Use the Admin WSN Simulator to generate and mine new SHA-512 sensor transactions.</p>'
            f'</div>'
        )

    rows_html = []
    for r in records:
        badge = (
            '<span class="status-pill verified">● SHA-512 VERIFIED</span>'
            if r["verified"]
            else '<span class="status-pill tampered">▲ HASH MISMATCH</span>'
        )
        rows_html.append(
            f"<tr>"
            f'<td class="mono-cell"><strong>{r["label"]}</strong></td>'
            f'<td class="temp-cell"><span class="temp-val">{r["temperature"]}°C</span></td>'
            f'<td class="mono-cell">{r["timestamp"]}</td>'
            f'<td class="hash-cell" title="{r["sha512"]}"><code>{r["sha512"]}</code></td>'
            f"<td>{badge}</td>"
            f"</tr>"
        )

    return (
        f'<div class="ledger-results-header">'
        f'<div><span class="eyebrow-label">03 // FILTERED LEDGER STREAM</span>'
        f'<h3 class="results-heading">Telemetry Records for <em>{filter_title}</em></h3></div>'
        f'<div class="results-count">{len(records)} Immutable Records Retrieved</div>'
        f"</div>"
        f'<div class="table-responsive">'
        f'<table class="editorial-table">'
        f"<thead><tr>"
        f"<th>IOT ID</th>"
        f"<th>Sense Temperature</th>"
        f"<th>Sense Timestamp</th>"
        f"<th>SHA-512 Cryptographic Hashcode</th>"
        f"<th>Ledger Integrity</th>"
        f"</tr></thead>"
        f'<tbody>{"".join(rows_html)}</tbody>'
        f"</table></div>"
    )


def build_navigation_context(active_page: str, is_admin: bool, current_user: str, contract_addr: str):
    if is_admin:
        admin_bar = (
            f'<div class="admin-session-bar">'
            f'<div class="admin-session-inner">'
            f'<div><span class="admin-badge-pill"><span class="pulse-dot"></span> ADMIN SESSION ACTIVE</span> '
            f'&nbsp;OPERATOR: <strong>{current_user.upper()}</strong> &nbsp;|&nbsp; ROLE: WSN NETWORK ADMINISTRATOR &nbsp;|&nbsp; CLEARANCE: SHA-512 READ/WRITE</div>'
            f'<div>CONTRACT: {contract_addr[:18]}… &nbsp;|&nbsp; <a href="/Logout" style="color:#5EEAD4; text-decoration:underline;">LOCK &amp; LOGOUT ↗</a></div>'
            f"</div></div>"
        )
        nav_links = (
            f'<a href="/index" class="nav-link {"active" if active_page == "index" else ""}">System Overview</a>'
            f'<a href="/Simulator" class="nav-link {"active" if active_page == "simulator" else ""}">🛡️ Admin Console &amp; Simulator</a>'
            f'<a href="/AccessData" class="nav-link {"active" if active_page == "ledger" else ""}">🗄️ Sensor Ledger</a>'
            f'<a href="/Signup" class="nav-link {"active" if active_page == "signup" else ""}">Provision Operator</a>'
            f'<a href="/Logout" class="nav-cta admin-active">● Admin: {current_user} (Logout) <span>↗</span></a>'
        )
        hero_actions = (
            '<a href="/Simulator" class="btn-primary-editorial"><span>🛡️ Open Admin Command Console</span><span>↗</span></a>'
            '<a href="/AccessData" class="btn-secondary-editorial"><span>Inspect Sensor Ledger</span><span>↗</span></a>'
        )
    else:
        admin_bar = ""
        nav_links = (
            f'<a href="/index" class="nav-link {"active" if active_page == "index" else ""}">System Overview</a>'
            f'<a href="/Login" class="nav-link">WSN Simulator <span class="nav-lock-tag">🔒 ADMIN</span></a>'
            f'<a href="/Login" class="nav-link">Sensor Ledger <span class="nav-lock-tag">🔒 ADMIN</span></a>'
            f'<a href="/Signup" class="nav-link {"active" if active_page == "signup" else ""}">Register Operator</a>'
            f'<a href="/Login" class="nav-cta">🔒 Admin Login <span>↗</span></a>'
        )
        hero_actions = (
            '<a href="/Login" class="btn-primary-editorial"><span>🔒 Login as Admin to Launch Simulator</span><span>↗</span></a>'
            '<a href="/Signup" class="btn-secondary-editorial"><span>Register New Operator</span><span>↗</span></a>'
        )
    return admin_bar, nav_links, hero_actions


def render_page(template_name: str, active_page: str = "index", **context) -> str:
    """Render template with role-based navigation and live blockchain metrics."""
    summary = bridge.get_dashboard_summary()
    admin_bar, nav_links, hero_actions = build_navigation_context(
        active_page, logged_in, uname, summary["contract_address"]
    )
    merged = {
        "msg": "",
        "uname": uname,
        "admin_bar": admin_bar,
        "nav_links": nav_links,
        "hero_actions": hero_actions,
        "operators_table": build_operators_table_html(),
        "summary": summary,
        "contract_address": summary["contract_address"],
        "network_id": summary["network_id"],
        "total_blocks": summary["total_blocks"],
        "total_readings": summary["total_readings"],
        "avg_tx_ms": summary["avg_tx_ms"],
        "avg_temp": summary["avg_temp"],
        "integrity_pct": summary["integrity_pct"],
        **context,
    }
    tpl_path = os.path.join(TEMPLATES_DIR, template_name)
    with open(tpl_path, "r", encoding="utf-8") as f:
        html = f.read()

    html = re.sub(
        r"\{\{\s*url_for\(\s*['\"]static['\"]\s*,\s*filename\s*=\s*['\"]([^'\"]+)['\"]\s*\)\s*\}\}",
        r"/static/\1",
        html,
    )
    for k, v in merged.items():
        if isinstance(v, (str, int, float)):
            html = re.sub(r"\{\{\s*" + re.escape(k) + r"\s*\|\s*safe\s*\}\}", str(v), html)
            html = re.sub(r"\{\{\s*" + re.escape(k) + r"\s*\}\}", str(v), html)
    return html


try:
    from flask import Flask, request, jsonify

    app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
    app.secret_key = "welcome"
    HAS_FLASK = True

    @app.route("/", methods=["GET", "POST"])
    @app.route("/index", methods=["GET", "POST"])
    def index():
        return render_page("index.html", active_page="index", msg="")

    @app.route("/Login", methods=["GET", "POST"])
    def Login():
        return render_page("Login.html", active_page="login", msg="")

    @app.route("/Signup", methods=["GET", "POST"])
    def Signup():
        return render_page("Signup.html", active_page="signup", msg="")

    @app.route("/UserScreen", methods=["GET", "POST"])
    @app.route("/Simulator", methods=["GET", "POST"])
    def UserScreen():
        if not logged_in:
            return render_page(
                "Login.html",
                active_page="login",
                msg="🔒 Administrator Authentication Required — Please log in to unlock the WSN Simulator & Security Console.",
            )
        return render_page("UserScreen.html", active_page="simulator", msg=f"Authenticated as {uname}")

    @app.route("/AccessData", methods=["GET", "POST"])
    def AccessData():
        if not logged_in:
            return render_page(
                "Login.html",
                active_page="login",
                msg="🔒 Administrator Authentication Required — Please log in to query the WSN Sensor Ledger.",
            )
        return render_page("AccessData.html", active_page="ledger", msg="")

    @app.route("/LoginAction", methods=["GET", "POST"])
    def LoginAction():
        global uname, logged_in
        if request.method == "POST":
            user = request.form.get("t1", "").strip()
            password = request.form.get("t2", "")
            if bridge.authenticate_user(user, password):
                uname = user
                logged_in = True
                return render_page("UserScreen.html", active_page="simulator", msg=f"Authenticated as {uname}")
            return render_page("Login.html", active_page="login", msg="Invalid login credentials. Try Admin account: Amir / amir123")
        return render_page("Login.html", active_page="login", msg="")

    @app.route("/SignupAction", methods=["GET", "POST"])
    def SignupAction():
        if request.method == "POST":
            u = request.form.get("t1", "").strip()
            pw = request.form.get("t2", "")
            phone = request.form.get("t3", "").strip()
            email = request.form.get("t4", "").strip()
            addr = request.form.get("t5", "").strip()
            ok, message, receipt = bridge.register_user(u, pw, phone, email, addr)
            if ok and receipt:
                tx_short = receipt.get("tx_hash", "")[:22] + "..."
                return render_page(
                    "Signup.html",
                    active_page="signup",
                    msg=f"{message} (Block #{receipt.get('block_number')} | Tx: {tx_short})",
                )
            return render_page("Signup.html", active_page="signup", msg=message)
        return render_page("Signup.html", active_page="signup", msg="")

    @app.route("/AccessDataAction", methods=["GET", "POST"])
    def AccessDataAction():
        if not logged_in:
            return render_page(
                "Login.html",
                active_page="login",
                msg="🔒 Administrator Authentication Required — Please log in to inspect sensor telemetry.",
            )
        iot_id = request.form.get("t1", request.args.get("t1", "ALL"))
        output = build_records_table_html(iot_id)
        return render_page("ViewData.html", active_page="ledger", msg=output, selected_iot=str(iot_id))

    @app.route("/Logout")
    def Logout():
        global logged_in
        logged_in = False
        return render_page("index.html", active_page="index", msg="")

    @app.route("/api/summary", methods=["GET"])
    def api_summary():
        return jsonify(bridge.get_dashboard_summary())

    @app.route("/api/simulate", methods=["POST"])
    def api_simulate():
        payload = request.get_json(silent=True) or {}
        node_id = payload.get("node_id")
        count = int(payload.get("count", 1))
        mined = []
        for _ in range(max(1, min(count, 20))):
            nid = int(node_id) if (node_id is not None and str(node_id).isdigit()) else None
            mined.append(bridge.simulate_sensor_reading(nid))
        return jsonify({
            "status": "ok",
            "mined": mined,
            "summary": bridge.get_dashboard_summary(),
        })

    @app.route("/api/records", methods=["GET"])
    def api_records():
        iot_id = request.args.get("iot_id", "ALL")
        return jsonify({
            "iot_id": iot_id,
            "records": bridge.get_parsed_iot_records(iot_id),
        })

except ImportError:
    HAS_FLASK = False


class FallbackWebHandler(BaseHTTPRequestHandler):
    """Zero-dependency HTTP server so Main.py runs cleanly even without Flask installed."""

    def log_message(self, format, *args):
        print(f"[WebServer] {self.address_string()} - {format % args}")

    def _send_html(self, html_str: str, status: int = 200):
        data = html_str.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, obj: dict, status: int = 200):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        global logged_in
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path.startswith("/static/"):
            rel_path = path[len("/static/"):]
            full_path = os.path.normpath(os.path.join(STATIC_DIR, rel_path))
            if full_path.startswith(STATIC_DIR) and os.path.isfile(full_path):
                mime, _ = mimetypes.guess_type(full_path)
                with open(full_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", mime or "application/octet-stream")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            self.send_error(404, "Static file not found")
            return

        if path == "/Logout":
            logged_in = False
            self._send_html(render_page("index.html", active_page="index", msg=""))
        elif path in ("/", "/index"):
            self._send_html(render_page("index.html", active_page="index", msg=""))
        elif path == "/Login":
            self._send_html(render_page("Login.html", active_page="login", msg=""))
        elif path == "/Signup":
            self._send_html(render_page("Signup.html", active_page="signup", msg=""))
        elif path in ("/UserScreen", "/Simulator"):
            if not logged_in:
                self._send_html(
                    render_page(
                        "Login.html",
                        active_page="login",
                        msg="🔒 Administrator Authentication Required — Please log in to unlock the WSN Simulator & Security Console.",
                    )
                )
            else:
                self._send_html(render_page("UserScreen.html", active_page="simulator", msg=f"Authenticated as {uname}"))
        elif path == "/AccessData":
            if not logged_in:
                self._send_html(
                    render_page(
                        "Login.html",
                        active_page="login",
                        msg="🔒 Administrator Authentication Required — Please log in to query the WSN Sensor Ledger.",
                    )
                )
            else:
                self._send_html(render_page("AccessData.html", active_page="ledger", msg=""))
        elif path == "/AccessDataAction":
            if not logged_in:
                self._send_html(
                    render_page(
                        "Login.html",
                        active_page="login",
                        msg="🔒 Administrator Authentication Required — Please log in to inspect sensor telemetry.",
                    )
                )
            else:
                iot_id = query.get("t1", ["ALL"])[0]
                output = build_records_table_html(iot_id)
                self._send_html(render_page("ViewData.html", active_page="ledger", msg=output, selected_iot=str(iot_id)))
        elif path == "/api/summary":
            self._send_json(bridge.get_dashboard_summary())
        elif path == "/api/records":
            iot_id = query.get("iot_id", ["ALL"])[0]
            self._send_json({"iot_id": iot_id, "records": bridge.get_parsed_iot_records(iot_id)})
        else:
            self._send_html(render_page("index.html", active_page="index", msg=""))

    def do_POST(self):
        global uname, logged_in
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length).decode("utf-8") if length else ""

        if path == "/api/simulate":
            try:
                payload = json.loads(raw_body) if raw_body else {}
            except Exception:
                payload = {}
            node_id = payload.get("node_id")
            count = int(payload.get("count", 1))
            mined = []
            for _ in range(max(1, min(count, 20))):
                nid = int(node_id) if (node_id is not None and str(node_id).isdigit()) else None
                mined.append(bridge.simulate_sensor_reading(nid))
            self._send_json({
                "status": "ok",
                "mined": mined,
                "summary": bridge.get_dashboard_summary(),
            })
            return

        form = {k: v[0] for k, v in parse_qs(raw_body, keep_blank_values=True).items()}

        if path == "/LoginAction":
            user = form.get("t1", "").strip()
            password = form.get("t2", "")
            if bridge.authenticate_user(user, password):
                uname = user
                logged_in = True
                self._send_html(render_page("UserScreen.html", active_page="simulator", msg=f"Authenticated as {uname}"))
            else:
                self._send_html(render_page("Login.html", active_page="login", msg="Invalid login credentials. Try Admin account: Amir / amir123"))
        elif path == "/SignupAction":
            u = form.get("t1", "").strip()
            pw = form.get("t2", "")
            phone = form.get("t3", "").strip()
            email = form.get("t4", "").strip()
            addr = form.get("t5", "").strip()
            ok, message, receipt = bridge.register_user(u, pw, phone, email, addr)
            if ok and receipt:
                tx_short = receipt.get("tx_hash", "")[:22] + "..."
                self._send_html(
                    render_page(
                        "Signup.html",
                        active_page="signup",
                        msg=f"{message} (Block #{receipt.get('block_number')} | Tx: {tx_short})",
                    )
                )
            else:
                self._send_html(render_page("Signup.html", active_page="signup", msg=message))
        elif path == "/AccessDataAction":
            if not logged_in:
                self._send_html(
                    render_page(
                        "Login.html",
                        active_page="login",
                        msg="🔒 Administrator Authentication Required — Please log in to inspect sensor telemetry.",
                    )
                )
            else:
                iot_id = form.get("t1", "ALL")
                output = build_records_table_html(iot_id)
                self._send_html(render_page("ViewData.html", active_page="ledger", msg=output, selected_iot=str(iot_id)))
        else:
            self._send_html(render_page("index.html", active_page="index", msg=""))


def run_server(host: str = "127.0.0.1", port: int = 5050):
    rpc_status = ensure_local_rpc_server(9545)
    summary = bridge.get_dashboard_summary()
    print("=" * 72)
    print("  WSN-CHAIN // SECURING IOT DATA IN THE CLOUD WITH BLOCKCHAIN")
    print("=" * 72)
    print(f"  [Blockchain] {rpc_status}")
    print(f"  [Contract]   {summary['contract_address']} (Network ID: {summary['network_id']})")
    print(f"  [Ledger]     {summary['total_blocks']} blocks | {summary['total_readings']} verified sensor records")
    print(f"  [Web Server] Running at http://{host}:{port}/index")
    print("=" * 72)

    if HAS_FLASK:
        app.run(host=host, port=port, debug=False)
    else:
        server = ThreadingHTTPServer((host, port), FallbackWebHandler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down web server...")
            server.server_close()


if __name__ == "__main__":
    run_server()
