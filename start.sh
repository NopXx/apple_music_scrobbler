#!/bin/bash
# เริ่มต้น Apple Music Scrobbler
cd "$(dirname "$0")"

sleep 1 && open "http://localhost:8765" &
python3 server.py
