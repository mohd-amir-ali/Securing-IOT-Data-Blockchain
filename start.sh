#!/bin/bash
# ==============================================================================
# AMIR ALI — Securing IoT Data in the Cloud with Blockchain Technology
# One-Command macOS / Linux Launcher
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
    echo "Starting Embedded Blockchain RPC (:9545) & Web Application (:5000)..."
    echo "Open in browser: http://127.0.0.1:5000/index"
    python3 Main.py
fi
