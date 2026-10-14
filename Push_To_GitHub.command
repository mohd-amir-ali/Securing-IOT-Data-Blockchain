#!/bin/bash
# ==============================================================================
# WSN-CHAIN // Interactive GitHub Upload Helper for macOS
# Double-click this file after creating an empty repository on GitHub.com
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

echo "========================================================================"
echo "  WSN-CHAIN // GitHub Repository Upload Assistant"
echo "========================================================================"
echo ""
echo "Step 1: Go to https://github.com/new and create a new empty repository"
echo "        (Leave 'Add a README file' UNCHECKED)."
echo ""
read -p "Step 2: Paste your new GitHub Repository URL here and press Enter: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "No URL entered. Exiting."
    exit 1
fi

git branch -M main
git remote remove origin 2>/dev/null
git remote add origin "$REPO_URL"

echo ""
echo "Pushing your project to $REPO_URL ..."
git push -u origin main

echo ""
echo "========================================================================"
echo "  Done! Refresh your GitHub repository page in your browser."
echo "========================================================================"
read -p "Press Enter to close..."
