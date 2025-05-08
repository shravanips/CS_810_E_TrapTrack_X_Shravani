#network_logger.py
from mitmproxy import http
import json
import os
import sys
from datetime import datetime

# List of known tracking domains
TRACKING_DOMAINS = [
    "doubleclick", "google-analytics", "facebook", "amazon-ads", "adnxs", "scorecardresearch"
]

# Get the base path, whether running as script or from bundled .exe
def get_base_path():
    if getattr(sys, 'frozen', False):
        # Running as bundled .exe by PyInstaller
        return os.path.dirname(sys.executable)
    else:
        # Running as plain Python script
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_path()
LOG_DIR = os.path.join(BASE_DIR, "data", "network_logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "combined_network_log.json")

def response(flow: http.HTTPFlow) -> None:
    try:
        url = flow.request.pretty_url
        headers = dict(flow.request.headers)
        domain = flow.request.host
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "method": flow.request.method,
            "url": url,
            "host": domain,
            "headers": headers,
            "is_tracker": any(d in domain for d in TRACKING_DOMAINS)
        }

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_data) + "\n")

    except Exception as e:
        print(f"[ERROR] Failed to log network request: {e}")
