# Securing IoT Data in the Cloud with Blockchain Technology

> **B.E. Computer Science & Engineering Major Project**  
> **Author:** Mohd Amir Ali ([techwithamir.com](https://techwithamir.com))  
> **Institution:** Lords Institute of Engineering & Technology (Affiliated to Osmania University, Hyderabad)

---

## 01 / Overview

Traditional Wireless Sensor Networks (WSNs) forward environmental and medical telemetry to a single centralized server, creating a single point of failure vulnerable to data tampering and spoofing.

This project integrates **20 simulated IoT sensor nodes**, a **Mobile Database Node (MDN) gateway**, **SHA-512 cryptographic hashing**, and an **Ethereum Smart Contract (`WSNSecurity.sol`)** to guarantee tamper-proof cloud telemetry storage and verification:

- **Cryptographic Data Integrity:** Every temperature reading sampled by an IoT node (`IOT-0` through `IOT-19`) is hashed with a 512-bit **SHA-512** digest prior to transmission.
- **On-Chain Smart Contract Storage:** The Solidity smart contract (`WSNSecurity.sol`) maintains both registered operator credentials (`addUser` / `getUser`) and immutable sensor records (`setIOTData` / `getIOTData`).
- **Interactive WSN Simulator & Live Analytics:** Includes both a **Web-based Interactive 20-Node Topology Simulator** (with real-time transaction latency graphing) and a **Native Python Tkinter Desktop Simulator** (`WSNSimulation.py`).
- **Zero-Dependency Local Blockchain Bridge:** Automatically connects to an active Truffle/Ganache node on `127.0.0.1:9545` (Network ID `5777`), or boots an embedded JSON-RPC 2.0 blockchain ledger (`blockchain_ledger.json`) so the entire stack runs out of the box with a single command.

---

## 02 / Project Structure

```text
.
├── start.sh                                  # One-command macOS / Linux launcher
├── requirements.txt                          # Optional Python dependencies (Flask, Web3, Matplotlib)
├── MAJOR PROJECT AMIR.pdf                    # Full B.E. Project Report & Documentation
├── WSNStrengthenSecuirty/                    # Main Web Application, Simulator & Blockchain Engine
│   ├── Main.py                               # Web Server (Flask + built-in HTTP server fallback)
│   ├── WSNSimulation.py                      # Desktop Tkinter 20-Node WSN Simulator
│   ├── blockchain_engine.py                  # Universal Web3 / Local JSON-RPC Blockchain Bridge
│   ├── WSNSecurity.sol                       # Solidity Smart Contract source
│   ├── WSNSecurity.json                      # Compiled Truffle Contract ABI & Network Artifact
│   ├── blockchain_ledger.json                # Persistent local blockchain state & block history
│   ├── static/
│   │   └── templatemo_style.css              # Editorial UI stylesheet (inspired by techwithamir.com)
│   └── templates/
│       ├── index.html                        # Editorial Landing Page & Live Metrics
│       ├── Login.html                        # Operator Authentication Screen
│       ├── Signup.html                       # On-Chain Operator Registration Screen
│       ├── UserScreen.html                   # Interactive Web WSN Simulator & Latency Graph
│       ├── AccessData.html                   # Sensor Node Query Selector (IOT-0 to IOT-19)
│       └── ViewData.html                     # Cryptographic Telemetry Verification Table
└── hello-eth/                                # Truffle Smart Contract Deployment Workspace
    ├── contracts/
    │   ├── Migrations.sol
    │   └── WSNSecurity.sol
    ├── migrations/
    │   ├── 1_initial_migration.js
    │   └── 2_deploy_contracts.js
    └── truffle-config.js
```

---

## 03 / Quick Start (macOS / Linux / Windows)

### Option A: One-Command Launch (Recommended)

From the project root directory, run:

```bash
chmod +x start.sh
./start.sh
```

Or run `Main.py` directly with Python 3:

```bash
cd WSNStrengthenSecuirty
python3 Main.py
```

Then open **[http://127.0.0.1:5050/index](http://127.0.0.1:5050/index)** in your browser:
- **Demo Operator Login:** Username `Amir` / Password `amir123` (or register a new operator via **Register**).
- **Interactive Web Simulator:** Navigate to **WSN Simulator** (`/Simulator`) and click **▶ Start WSN Simulation** to watch the 20 sensor nodes broadcast SHA-512 blocks in real time.
- **Sensor Telemetry Ledger:** Navigate to **Sensor Ledger** (`/AccessData`) to filter verified records across `IOT-0` through `IOT-19`.

### Option B: Launch the Desktop Tkinter Simulator

If you also want to run the standalone desktop GUI window alongside the web app:

```bash
./start.sh --desktop
# or:
cd WSNStrengthenSecuirty && python3 WSNSimulation.py
```

### Option C: Running with External Truffle (`truffle develop`)

If you have Node.js and Truffle installed and want to run an external Truffle development chain instead of the embedded RPC node:

```bash
cd hello-eth
npx truffle develop
# Inside the truffle(develop)> prompt:
migrate --reset
```

`blockchain_engine.py` automatically detects the active RPC server on `127.0.0.1:9545` and reads the deployed contract address directly from `WSNSecurity.json`.
