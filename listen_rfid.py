"""
Background script to listen for RFID scans from Arduino and trigger time logging.

Usage:
  python listen_rfid.py --port COM3 --server http://localhost:5000

The script reads from an Arduino serial port and sends RFID codes to the Flask app
to start/stop timers for users.

Arduino should send RFID data as: "<RFID_CODE>\n"
"""

import serial
import argparse
import requests
import time
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def listen_rfid(port='COM3', baudrate=9600, server='http://localhost:5000', action='toggle'):
    """
    Listen for RFID scans from Arduino.
    
    Args:
        port: Serial port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
        baudrate: Serial connection speed (default 9600)
        server: Base URL of Flask app (e.g., 'http://localhost:5000')
        action: 'toggle' (start/stop), 'start', or 'stop'
    """
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        logger.info(f"Connected to Arduino on {port} at {baudrate} baud")
    except serial.SerialException as e:
        logger.error(f"Failed to open {port}: {e}")
        sys.exit(1)
    
    logger.info(f"Listening for RFID codes (action={action})...")
    
    last_rfid = None
    last_time = time.time()
    DEBOUNCE_SECONDS = 1  # Ignore duplicate scans within 1 second
    
    try:
        while True:
            if ser.in_waiting:
                rfid = ser.readline().decode('utf-8', errors='ignore').strip()
                
                if not rfid or rfid.startswith('#'):
                    continue
                
                now = time.time()
                # Debounce: ignore if same RFID within 1 second
                if rfid == last_rfid and (now - last_time) < DEBOUNCE_SECONDS:
                    logger.debug(f"Debounced duplicate RFID: {rfid}")
                    continue
                
                last_rfid = rfid
                last_time = now
                
                logger.info(f"Scanned RFID: {rfid}")
                
                # Determine which endpoint to call
                if action == 'start':
                    endpoint = '/time/start_by_rfid'
                elif action == 'stop':
                    endpoint = '/time/stop_by_rfid'
                else:  # toggle
                    # Try to stop first; if fails, start
                    try:
                        resp = requests.post(f"{server}/time/stop_by_rfid", json={'rfid': rfid}, timeout=2)
                        if resp.status_code == 200:
                            logger.info(f"✓ Timer stopped: {resp.json()}")
                            continue
                    except Exception as e:
                        logger.debug(f"Stop failed: {e}")
                    endpoint = '/time/start_by_rfid'
                
                # Send to Flask app
                try:
                    resp = requests.post(f"{server}{endpoint}", json={'rfid': rfid}, timeout=2)
                    if resp.status_code == 200:
                        data = resp.json()
                        logger.info(f"✓ {data.get('message', 'OK')}")
                    else:
                        logger.warning(f"Server error ({resp.status_code}): {resp.json().get('error', 'Unknown')}")
                except requests.exceptions.RequestException as e:
                    logger.error(f"Failed to reach server: {e}")
    
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        ser.close()
        logger.info("Serial connection closed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RFID listener for time logging')
    parser.add_argument('--port', default='COM3', help='Serial port (default: COM3)')
    parser.add_argument('--baud', type=int, default=9600, help='Baud rate (default: 9600)')
    parser.add_argument('--server', default='http://localhost:5000', help='Flask server URL')
    parser.add_argument('--action', choices=['start', 'stop', 'toggle'], default='toggle',
                        help='Action: start, stop, or toggle (default)')
    
    args = parser.parse_args()
    listen_rfid(port=args.port, baudrate=args.baud, server=args.server, action=args.action)
