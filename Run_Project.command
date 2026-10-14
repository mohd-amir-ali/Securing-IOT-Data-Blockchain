#!/bin/bash
# Double-click this file in macOS Finder to launch the Blockchain WSN Web Server & open your browser!
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/WSNStrengthenSecuirty" || exit 1

# Open the browser automatically after 1.5 seconds
(sleep 1.5 && open "http://127.0.0.1:5000/index") &

python3 Main.py
