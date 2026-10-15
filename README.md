# WSN-CHAIN // Securing IoT Data in the Cloud with Blockchain Technology

[![Live Demo](https://img.shields.io/badge/🚀_LIVE_INTERACTIVE_DEMO-Launch_in_Browser-0D7463?style=for-the-badge)](https://mohd-amir-ali.github.io/Securing-IOT-Data-Blockchain/)
[![Open in GitHub Codespaces](https://img.shields.io/badge/☁️_GitHub_Codespaces-Run_Python_Backend-0F1C24?style=for-the-badge&logo=github)](https://codespaces.new/mohd-amir-ali/Securing-IOT-Data-Blockchain)

> **B.E. Computer Science & Engineering Major Project**  
> **Author:** Mohd Amir Ali ([techwithamir.com](https://techwithamir.com))  
> **Institution:** Lords Institute of Engineering & Technology (Affiliated to Osmania University, Hyderabad)

---

## ⚡ Run Instantly Without Cloning

Anyone can explore and test the entire project directly in their browser without downloading or cloning the repository:

1. **[🚀 Launch Live Interactive Web App (GitHub Pages)](https://mohd-amir-ali.github.io/Securing-IOT-Data-Blockchain/)**  
   Runs the complete interactive **Cyber-Mesh Topology**, **Role-Gated Admin Command Console** (Demo Login: `Amir` / `amir123`), **20-Node WSN Simulator**, **SHA-512 Tamper-Attack Lab**, **Live Transaction Latency Graph**, and **Sensor Telemetry Ledger (`IOT-0` to `IOT-19`)** directly in any desktop or mobile browser.
2. **[☁️ Launch Full Python & RPC Backend in GitHub Codespaces](https://codespaces.new/mohd-amir-ali/Securing-IOT-Data-Blockchain)**  
   Boots `Main.py` (Port `5050`) and the embedded Ethereum JSON-RPC 2.0 node (Port `9545`) inside a cloud container in one click.

---

## 01 / Overview

Traditional Wireless Sensor Networks (WSNs) forward environmental and medical telemetry to a single centralized server, creating a single point of failure vulnerable to data tampering and spoofing.

This project integrates **20 simulated IoT sensor nodes**, a **Mobile Database Node (MDN) gateway**, **SHA-512 cryptographic hashing**, and an **Ethereum Smart Contract (`WSNSecurity.sol`)** to guarantee tamper-proof cloud telemetry storage and verification:

- **Cryptographic Data Integrity:** Every temperature reading sampled by an IoT node (`IOT-0` through `IOT-19`) is hashed with a 512-bit **SHA-512** digest prior to transmission.
- **Role-Gated Smart Contract Storage:** The Solidity smart contract (`WSNSecurity.sol`) maintains both registered operator credentials (`addUser` / `getUser`) and immutable sensor records (`setIOTData` / `getIOTData`).
- **Interactive WSN Simulator & Tamper-Detection Lab:** Includes an interactive **20-Node WSN Topology Simulator**, real-time transaction latency graphing, an **Admin Cyber Tamper-Attack Simulation Lab**, and a standalone **Native Python Tkinter Desktop Simulator** (`WSNSimulation.py`).
- **Zero-Dependency Local Blockchain Bridge:** Automatically connects to an active Truffle/Ganache node on `127.0.0.1:9545` (Network ID `5777`), or boots an embedded JSON-RPC 2.0 blockchain ledger (`blockchain_ledger.json`) so the entire stack runs out of the box with a single command.

---

## 02 / Project Structure

```text
.
├── index.html                                # Live GitHub Pages Interactive Web App
├── Launch_Dashboard.html                     # Standalone Offline/Online Browser Dashboard
├── Run_Project.command                       # One-click macOS Finder Launcher (Port 5050)
├── start.sh                                  # One-command macOS / Linux CLI Launcher
├── requirements.txt                          # Optional Python dependencies (Flask, Web3, Matplotlib)
├── WSNStrengthenSecuirty/                    # Main Web Application, Simulator & Blockchain Engine
│   ├── Main.py                               # Web Server (Flask + built-in HTTP server fallback)
│   ├── WSNSimulation.py                      # Desktop Tkinter 20-Node WSN Simulator
│   ├── blockchain_engine.py                  # Universal Web3 / Local JSON-RPC Blockchain Bridge
│   ├── WSNSecurity.sol                       # Solidity Smart Contract source
│   ├── WSNSecurity.json                      # Compiled Truffle Contract ABI & Network Artifact
│   ├── blockchain_ledger.json                # Persistent local blockchain state & block history
│   ├── static/
│   │   └── templatemo_style.css              # Pastel-Cybersecurity UI stylesheet
│   └── templates/
│       ├── index.html                        # Project Overview & Interactive Cyber-Mesh Canvas
│       ├── Login.html                        # Role-Gated Admin & Operator Login Screen
│       ├── Signup.html                       # On-Chain Operator Registration Screen
│       ├── UserScreen.html                   # Admin Command Console, Simulator & Tamper Lab
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

## 03 / Running Locally (macOS / Linux / Windows)

### Option A: One-Command Local Launch

From the project root directory, double-click **`Run_Project.command`** (on macOS) or run:

```bash
chmod +x start.sh
./start.sh
```

Then open **[http://127.0.0.1:5050/index](http://127.0.0.1:5050/index)** in your browser:
- **Demo Admin Login:** Username `Amir` / Password `amir123` (or register a new operator via **Register Operator**).
- **Admin Command Console & Simulator:** Once logged in, click **▶ Start WSN Simulation** to watch the 20 sensor nodes broadcast SHA-512 blocks in real time, or click **⚡ Simulate Cyber Tamper Attack** to test the hash verification engine.
- **Sensor Telemetry Ledger:** Navigate to **Sensor Ledger** (`/AccessData`) to filter verified records across `IOT-0` through `IOT-19`.

### Option B: Launch the Desktop Tkinter Simulator

```bash
./start.sh --desktop
# or:
cd WSNStrengthenSecuirty && python3 WSNSimulation.py
```
