# WSN-CHAIN // Complete Project Guide, Architecture & Developer Tutorial

> **Project Title:** Securing IoT Data in the Cloud with Blockchain Technology (`WSN-CHAIN // SECURE CLOUD`)  
> **Author:** Mohd Amir Ali (`160920733019`) — B.E. CSE, Lords Institute of Engineering & Technology (Osmania University)  
> **GitHub Repository:** [github.com/mohd-amir-ali/Securing-IOT-Data-Blockchain](https://github.com/mohd-amir-ali/Securing-IOT-Data-Blockchain)  
> **Live Web App (GitHub Pages):** [mohd-amir-ali.github.io/Securing-IOT-Data-Blockchain](https://mohd-amir-ali.github.io/Securing-IOT-Data-Blockchain/)

---

## 1. How the Whole Project Works (End-to-End Data Flow)

Your project solves a critical cybersecurity problem in **Wireless Sensor Networks (WSNs)**: in traditional IoT systems, sensors send temperature or medical readings to a single centralized cloud database. If an attacker compromises that database and alters a temperature reading (e.g., changing `24°C` to `99°C`), there is no cryptographic proof that the data was tampered with.

Your system prevents tampering through a **4-stage cryptographic pipeline**:

```text
[20 IoT Sensor Nodes]  ──(1. Raw Telemetry)──►  [MDN Gateway (SHA-512 Hash Engine)]
   (IOT-0 to IOT-19)                                         │
                                             (2. Payload + 512-bit Digest)
                                                             ▼
[Admin Web Console]    ◄──(4. Hash Audit)────  [WSNSecurity.sol Smart Contract]
 (Port 5050 / Browser)                          (Port 9545 / Ledger Storage)
```

### Stage 1: Edge Sensing (20 Autonomous WSN Nodes)
* Twenty simulated wireless sensor nodes (`IOT-0` through `IOT-19`) are distributed across five functional zones (*Smart Home Living*, *ICU Telemetry*, *Env Air Quality*, *Thermal Grid*, and *Edge Gateway*).
* Whenever a node senses the environment, it generates an integer temperature reading (between `15°C` and `42°C`) and a timestamp (`YYYY/MM/DD-HH:MM:SS`).

### Stage 2: SHA-512 Cryptographic Sealing at the Mobile Database Node (MDN)
* Before storing or forwarding the reading to the cloud, the **Mobile Database Node (MDN)** combines the Node ID and Temperature into a plain string:  
  `sense_data = f"{node_id} {temperature}"` (for example, `"7 28"`).
* It passes this string through the **SHA-512 cryptographic hash algorithm** (`hashlib.sha512`), producing a unique 128-character hexadecimal signature.
* It packages the record as a `#`-delimited line:  
  `7#28#2026/10/15-02:30:12#a8f4c2...91b0\n`

### Stage 3: On-Chain Smart Contract Storage (`WSNSecurity.sol`)
* The packaged record is sent to the **`WSNSecurity` Solidity Smart Contract** (deployed at contract address `0x745978a62d1e4293AF3EA7e03Ed5e81CC8397620` on Network ID `5777`, Port `9545`).
* The smart contract stores two state variables on the blockchain:
  1. `registered_user`: Stores authorized operator credentials via `addUser(string)` and retrieves them via `getUser()`.
  2. `iot_data`: Stores all sensor telemetry lines via `setIOTData(string)` and retrieves them via `getIOTData()`.
* Each transaction is recorded as a block with a `block_number`, `tx_hash`, `previous_hash`, `block_hash`, `gas_used`, and high-resolution commit latency (`tx_time_sec`).

### Stage 4: Role-Gated Admin Verification & Tamper Detection
* Public visitors only see the **System Overview** and the interactive **Cyber-Mesh Constellation**.
* When an authorized operator logs in (`Amir` / `amir123`), the backend verifies their credentials against `WSNSecurity.getUser()` and unlocks the **Admin Command Console** and **Sensor Telemetry Ledger**.
* Whenever the ledger is queried, the system recomputes `SHA-512(f"{iot_id} {temperature}")` for every row and compares it against the stored on-chain hash:
  * If they match → Displays **`● SHA-512 VERIFIED`** (Green).
  * If even a single digit of the temperature was modified → Displays **`▲ HASH MISMATCH / TAMPER BLOCKED`** (Red).

---

## 2. Folder & File Map (`Blockchain A15`)

Here is what every single file and folder inside `/Users/mohdamirali/Desktop/Blockchain A15` does:

### A. Root Directory (`/Users/mohdamirali/Desktop/Blockchain A15/`)

| File / Folder | Role | When You Use It |
| :--- | :--- | :--- |
| **`index.html`** | **GitHub Pages Live App** | Self-contained single-file version of the entire web app so visitors at `https://mohd-amir-ali.github.io/Securing-IOT-Data-Blockchain/` can run the project in their browser without cloning. |
| **`Launch_Dashboard.html`** | **Local Standalone App** | Identical to root `index.html`—lets you double-click and open the full interactive dashboard locally in Chrome without starting Terminal. |
| **`Run_Project.command`** | **1-Click Mac Server Launcher** | Double-click in macOS Finder to start the Python web server (`Main.py`) on port `5050` and open `http://127.0.0.1:5050/index`. |
| **`start.sh`** | **CLI Startup Script** | Run `./start.sh` in Terminal for the web server, or `./start.sh --desktop` for the Tkinter desktop window. |
| **`Push_To_GitHub.command`** | **GitHub Push Helper** | Double-click to push new local Git commits to your GitHub repository. |
| **`README.md`** | **GitHub Front Page** | The documentation and launch badges displayed on your GitHub repository page. |
| **`requirements.txt`** | **Python Package List** | Lists optional packages (`flask`, `web3`, `matplotlib`, `numpy`) for cloud/Codespaces environments. |
| **`.gitignore`** | **Git Exclusion Rules** | Prevents `hello-eth/node_modules/`, `__pycache__/`, and `.DS_Store` from cluttering your GitHub repo. |
| **`.devcontainer/devcontainer.json`** | **GitHub Codespaces Config** | Allows anyone on GitHub to boot the Python server in a cloud container in one click. |

---

### B. Backend & Blockchain Engine (`WSNStrengthenSecuirty/`)

| File | Type | Exact Responsibility |
| :--- | :--- | :--- |
| **`Main.py`** | **Python Web Backend** | The main web server running on `http://127.0.0.1:5050`. Handles all routes (`/index`, `/Login`, `/Signup`, `/Simulator`, `/AccessData`, `/LoginAction`, `/SignupAction`, `/AccessDataAction`, `/Logout`) and JSON API endpoints (`/api/summary`, `/api/simulate`, `/api/records`). Also manages the `logged_in` Admin gate. |
| **`blockchain_engine.py`** | **Core Blockchain Bridge** | Connects to an external Truffle/Ganache Ethereum node on `127.0.0.1:9545` if running, **or** automatically starts the embedded JSON-RPC 2.0 server and persists blocks to `blockchain_ledger.json`. Handles SHA-512 hashing, user authentication, sensor simulation, and latency tracking. |
| **`WSNSimulation.py`** | **Desktop GUI Simulator** | Standalone Python `tkinter` desktop application that draws the 20 sensor nodes on a desktop canvas, broadcasts SHA-512 transactions, and plots the Transaction Time Graph. |
| **`WSNSecurity.sol`** | **Solidity Smart Contract** | Source code of the Ethereum smart contract defining `registered_user`, `iot_data`, `addUser()`, `getUser()`, `setIOTData()`, and `getIOTData()`. |
| **`WSNSecurity.json`** | **Compiled Contract ABI** | Truffle compiler output containing the `abi` (function signatures) and deployed network address (`0x745978a62d1e4293AF3EA7e03Ed5e81CC8397620` on Network `5777`). |
| **`blockchain_ledger.json`** | **Persistent Block Database** | Stores all mined blocks, SHA-512 hashes, transaction latencies, registered users, and 20-node coordinates so your data is never lost when you restart the app. |

---

### C. Web Frontend (`WSNStrengthenSecuirty/static/` & `templates/`)

| File | Location | What It Controls on Screen |
| :--- | :--- | :--- |
| **`templatemo_style.css`** | `WSNStrengthenSecuirty/static/` | **Master Stylesheet.** Controls the Pastel-Cybersecurity color palette (`:root` variables), typography (`Inter`, `Newsreader`, `JetBrains Mono`), the top Admin Session Bar, Header, Hero typography, cards, and tables. |
| **`index.html`** | `WSNStrengthenSecuirty/templates/` | **Public Homepage / Overview.** Contains the `SECURING IOT CLOUD DATA` hero section, project thesis, developer credit box, and the interactive `<canvas id="cyber-web-canvas">` Cyber-Mesh animation. |
| **`Login.html`** | `WSNStrengthenSecuirty/templates/` | **Admin & Operator Login Page.** Contains the login form (`/LoginAction`) and the `Auto-Fill Admin (Amir)` button. |
| **`Signup.html`** | `WSNStrengthenSecuirty/templates/` | **Operator Registration Page.** Contains the 5-field signup form (`Username`, `Password`, `Contact`, `Email`, `Location`) that commits new operators to the blockchain. |
| **`UserScreen.html`** | `WSNStrengthenSecuirty/templates/` | **Unlocked Admin Command Console & WSN Simulator.** Shown immediately after login. Contains the 20-node WSN topology canvas, live SHA-512 transaction log, Cyber Tamper-Attack Simulation Lab, Transaction Latency Graph, and the Authorized Operators table. |
| **`AccessData.html`** | `WSNStrengthenSecuirty/templates/` | **Sensor Node Query Screen.** Lets the Admin select `ALL NODES` or `IOT-0` through `IOT-19` via dropdown or quick-jump pills. |
| **`ViewData.html`** | `WSNStrengthenSecuirty/templates/` | **Telemetry Results Table.** Displays the filtered sensor readings, timestamps, full 128-character SHA-512 hashes, and `● SHA-512 VERIFIED` status pills. |

---

### D. Smart Contract Deployment Folder (`hello-eth/`)

* **`hello-eth/contracts/WSNSecurity.sol`**: The Solidity smart contract used by Truffle.
* **`hello-eth/migrations/2_deploy_contracts.js`**: Truffle deployment script that deploys `WSNSecurity` to the local blockchain.
* **`hello-eth/truffle-config.js`**: Configures Solidity compiler version `0.8.11` and local development port `9545`.

---

## 3. Tutorial: How to Make Common Customizations

Whenever you want to tweak the look, text, or behavior of your project, use this quick cheat sheet:

### Customization 1: Changing Colors or Fonts
Open **`WSNStrengthenSecuirty/static/templatemo_style.css`** and look at lines `3–23` (`:root`):
```css
:root {
  --bg-cream: #EEF4F3;           /* Main page background color */
  --bg-surface: #F7FBFA;         /* Card background color */
  --ink-dark: #0F1C24;           /* Main heading & dark text color */
  --burgundy: #0D7463;           /* Primary accent color (buttons, badges, active nodes) */
  --tamper-red: #C81E32;         /* Alert color when tamper attack is simulated */
}
```
* Change `--burgundy: #0D7463;` to any hex color (for example, `#2563EB` for royal cyber-blue or `#6E2634` for burgundy) and save—every button, badge, active sensor node, and chart line across the entire app will update automatically!

### Customization 2: Editing Text, Titles, or Credits on the Homepage
Open **`WSNStrengthenSecuirty/templates/index.html`**:
* **Header Brand Name (Lines 26–29):** Edit `WSN-CHAIN // SECURE CLOUD` or the subtitle `IoT Blockchain Telemetry · B.E. CSE Major Project`.
* **Big Hero Title (Lines 50–53):** Edit `SECURING IOT` and `CLOUD DATA`.
* **Developer Credit Box (Lines 79–85):** Edit your name, roll number (`160920733019`), or college name.

### Customization 3: Changing Sensor Temperature Range or Simulation Speed
1. **Temperature Range (`15°C` to `42°C`):**
   * Open **`WSNStrengthenSecuirty/blockchain_engine.py`** and find `simulate_sensor_reading()` (around line `277`):
     ```python
     sense = random.randint(15, 42)
     ```
   * Change `15, 42` to any min/max range you want.
2. **Simulation Speed (Default: 1.25 seconds per block):**
   * Open **`WSNStrengthenSecuirty/templates/UserScreen.html`** and find `startWebSimulation()` (around line `390`):
     ```javascript
     simInterval = setInterval(() => {
       mineSingleStep();
     }, 1250); // <-- Time in milliseconds (1250ms = 1.25 seconds)
     ```

### Customization 4: Adding or Resetting Default Admin Users
* Open **`WSNStrengthenSecuirty/blockchain_engine.py`** and look at `_create_initial_ledger()` (around line `87`):
  ```python
  default_user_line = "Amir#amir123#9059173902#mohdamirali@gmail.com#Himayath Sagar, Hyderabad\n"
  ```
* If you ever want to reset the blockchain database back to a fresh state with your new defaults, simply delete `WSNStrengthenSecuirty/blockchain_ledger.json` and restart `Main.py`—it will automatically regenerate a fresh `blockchain_ledger.json`!

### Customization 5: Syncing Your Changes to the Standalone / GitHub Pages File (`index.html`)
Remember that you have two ways people view your app:
1. **Local Python Server (`http://127.0.0.1:5050/index`)**: Reads directly from `WSNStrengthenSecuirty/templates/` and `WSNStrengthenSecuirty/static/templatemo_style.css`.
2. **GitHub Pages / Standalone File (`index.html` & `Launch_Dashboard.html` in the root folder)**: Self-contained single HTML file where the CSS and HTML are bundled together so it works without Python on GitHub Pages (`https://mohd-amir-ali.github.io/Securing-IOT-Data-Blockchain/`).

If you make changes to `templatemo_style.css`, you can update `index.html` and `Launch_Dashboard.html` directly, or paste your updated CSS inside the `<style>` tag at the top of `index.html` and upload it to GitHub!
