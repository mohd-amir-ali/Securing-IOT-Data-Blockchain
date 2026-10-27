#!/bin/bash
# ==============================================================================
# AMIR ALI  -  Securing IoT Data in the Cloud with Blockchain Technology
# One-Command macOS / Linux Launcher (Port 5050 to avoid macOS AirPlay on 5000)
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="$SCRIPT_DIR/WSNStrengthenSecuirty"

echo "========================================================================"
echo "  aa↗  AMIR ALI | Securing IoT Data in the Cloud with Blockchain"
echo "========================================================================"

cd "$APP_DIR" || exit 1

if [ "$1" == "--desktop" ]; then
    echo "Launching Desktop Tkinter WSN Simulator..."
    python3 WSNSimulation.py
else
    echo "Starting Embedded Blockchain RPC (:9545) & Web Application (:5050)..."
    echo "Open in browser: http://127.0.0.1:5050/index"
    (sleep 1.2 && open "http://127.0.0.1:5050/index" 2>/dev/null) &
    python3 Main.py
fi
