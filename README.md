# BLOCKCHAIN WSN - SECURE CLOUD · Securing IoT Data in the Cloud with Blockchain Technology

[![Launch Live Demo](https://img.shields.io/badge/Launch%20Demo-Live%20Interactive%20Platform-059669?style=for-the-badge&labelColor=0B101B)](https://mohd-amir-ali.github.io/Securing-IOT-Data-Blockchain/)
[![Launch Standalone App](https://img.shields.io/badge/Launch%20App-Zero--Install%20HTML5%20%2B%20RPC%20Engine-06B6D4?style=for-the-badge&labelColor=0B101B)](https://mohd-amir-ali.github.io/Securing-IOT-Data-Blockchain/Launch_Dashboard.html)
[![Open in GitHub Codespaces](https://img.shields.io/badge/GitHub%20Codespaces-Run%20Python%20Backend-131C2E?style=for-the-badge&logo=github)](https://codespaces.new/mohd-amir-ali/Securing-IOT-Data-Blockchain)
[![Author](https://img.shields.io/badge/Author-Mohd%20Amir%20Ali-10B981?style=for-the-badge&labelColor=0B101B)](https://techwithamir.com)

> **B.E. Computer Science & Engineering Major Project**  
> **Author:** Mohd Amir Ali ([techwithamir.com](https://techwithamir.com))  
> **Institution:** Lords Institute of Engineering & Technology (Affiliated to Osmania University, Hyderabad)

> **Live Interactive Links:**
> - **[Launch Live Interactive Demo (GitHub Pages) ↗](https://mohd-amir-ali.github.io/Securing-IOT-Data-Blockchain/)** - Explore the Flowing Distributed Cyber-Mesh, Live SHA-512 Avalanche Sandbox, Role-Gated 20-Node WSN Simulator with blinking temperature telemetry, and On-Chain Sensor Ledger.
> - **[Launch Standalone HTML5 Dashboard (`Launch_Dashboard.html`) ↗](https://mohd-amir-ali.github.io/Securing-IOT-Data-Blockchain/Launch_Dashboard.html)** - Zero-install browser build.

---

## 01 - Run Instantly Without Cloning

Anyone can explore and test the entire project directly in their browser without downloading or cloning the repository:

1. **[Launch Live Interactive Web App (GitHub Pages)](https://mohd-amir-ali.github.io/Securing-IOT-Data-Blockchain/)**  
   Runs the complete interactive **Flowing Cyber-Mesh Topology**, **Live SHA-512 Avalanche & Cloud Tamper Sandbox**, **Role-Gated Admin Command Console** (Demo Login: `Amir` / `amir123` or **1-Click Demo Admin Unlock**), **Distributed 20-Node WSN Simulator** with glowing running connection lines and blinking temperature telemetry, **Live Transaction Latency Graph**, and **Clickable Block Receipt Sensor Ledger (`IOT-0` to `IOT-19`)**.
2. **[Launch Full Python & RPC Backend in GitHub Codespaces](https://codespaces.new/mohd-amir-ali/Securing-IOT-Data-Blockchain)**  
   Boots `Main.py` (Port `5050`) and the embedded Ethereum JSON-RPC 2.0 node (Port `9545`) inside a cloud container in one click.

---

## 02 - System Architecture & Overview

Traditional Wireless Sensor Networks (WSNs) forward environmental and medical telemetry to a single centralized server, creating a single point of failure vulnerable to data tampering and spoofing.

This project integrates **20 simulated IoT sensor nodes**, a **Mobile Database Node (MDN) gateway**, **SHA-512 cryptographic hashing**, and an **Ethereum Smart Contract (`WSNSecurity.sol`)** to guarantee tamper-proof cloud telemetry storage and verification:

- **Cryptographic Data Integrity:** Every temperature reading sampled by an IoT node (`IOT-0` through `IOT-19`) is hashed with a 512-bit **SHA-512** digest prior to transmission.
- **Role-Gated Smart Contract Storage:** The Solidity smart contract (`WSNSecurity.sol`) maintains both registered operator credentials (`addUser` / `getUser`) and immutable sensor records (`setIOTData` / `getIOTData`).
- **Interactive WSN Simulator & Tamper-Detection Lab:** Includes a distributed **20-Node Field WSN Topology Simulator** with flowing dash lines and blinking temperature badges, real-time transaction latency graphing, an **Admin Cyber Tamper-Attack Simulation Lab**, and a standalone **Native Python Tkinter Desktop Simulator** (`WSNSimulation.py`).
- **Zero-Dependency Local Blockchain Bridge:** Automatically connects to an active Truffle/Ganache node on `127.0.0.1:9545` (Network ID `5777`), or boots an embedded JSON-RPC 2.0 blockchain ledger (`blockchain_ledger.json`) so the entire stack runs out of the box with a single command.

---

## 03 - Project Structure

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
│   │   └── templatemo_style.css              # Web3 Cyber-Obsidian & Emerald UI stylesheet
│   └── templates/                            # Flask HTML templates
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

## 04 - Running Locally (macOS / Linux / Windows)

### Option A: Instant Zero-Install Browser Launch
Double-click **`Launch_Dashboard.html`** (or `index.html`) to open the entire interactive application directly in Chrome, Edge, or Safari.

### Option B: One-Command Local Python & RPC Launch
From the project root directory, double-click **`Run_Project.command`** (on macOS) or run:

```bash
chmod +x start.sh
./start.sh
```

Then open **[http://127.0.0.1:5050/index](http://127.0.0.1:5050/index)** in your browser (Demo Admin Login: `Amir` / `amir123`).

### Option C: Launch the Desktop Tkinter Simulator
```bash
./start.sh --desktop
# or:
cd WSNStrengthenSecuirty && python3 WSNSimulation.py
```
