#!/bin/bash

# README.sh - Setup and run the Pastebin Keyword Crawler

echo "==========================================="
echo "  Pastebin Keyword Crawler Setup & Run"
echo "==========================================="

# Step 1: Create virtual environment (optional but recommended)
echo "[*] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 2: Install required Python libraries
echo "[*] Installing dependencies..."
pip install --upgrade pip
pip install requests beautifulsoup4

# Step 3: Run the crawler script
echo "[*] Running the crawler script..."
python pastebin_keyword_crawler_solution.py

# Step 4: Output file
echo "[*] Output saved in: keyword_matches.jsonl"

echo "==========================================="
echo " Script execution completed. "
echo "==========================================="
