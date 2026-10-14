#!/bin/bash
# Double-click this file in macOS Finder to launch the Blockchain WSN Web Server & open your browser!
# Uses port 5050 to avoid macOS AirPlay Receiver conflict on port 5000.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/WSNStrengthenSecuirty" || exit 1

# Open the browser automatically after 1.2 seconds
(sleep 1.2 && open "http://127.0.0.1:5050/index") &

python3 Main.py
