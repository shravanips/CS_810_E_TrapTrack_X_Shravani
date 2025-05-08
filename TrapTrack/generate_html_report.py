import os
import json
from datetime import datetime
from trapscore import calculate_trapscore

# Define paths
base_dir = os.path.dirname(os.path.abspath(__file__))
storage_dir = os.path.join(base_dir, "data", "storage_logs")
geo_file = os.path.join(base_dir, "data", "geo_locations.json")
screenshot_dir = os.path.join(base_dir, "screenshots")
report_path = os.path.join(base_dir, "traptrack_report.html")
screenshot_log = os.path.join(base_dir, "latest_screens.txt")

# Load latest storage
def load_latest_storage(label):
    files = sorted([f for f in os.listdir(storage_dir) if f.startswith(label)])
    if files:
        with open(os.path.join(storage_dir, files[-1]), "r") as f:
            return json.load(f)
    return {}

pre_data = load_latest_storage("pre_")
post_data = load_latest_storage("post_")

# Load geo data
geo_data = {}
if os.path.exists(geo_file):
    with open(geo_file, "r") as f:
        geo_data = json.load(f)

# ✅ Get live trapscore data
score_data = calculate_trapscore()

# Load current run screenshots
current_screens = []
if os.path.exists(screenshot_log):
    with open(screenshot_log, "r") as f:
        current_screens = [line.strip() for line in f if line.strip()]

# HTML Report Generation
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>TrapTrack Privacy Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; background: #f9f9f9; }}
        h1 {{ color: #333; }}
        h2 {{ color: #0077cc; }}
        .section {{ margin-bottom: 30px; }}
        pre {{ background: #eee; padding: 10px; overflow: auto; }}
        img {{ max-width: 45%; margin: 10px 2%; border: 1px solid #ccc; }}
        .risk-high {{ color: red; font-weight: bold; }}
        .risk-medium {{ color: orange; font-weight: bold; }}
        .risk-low {{ color: green; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>TrapTrack Privacy Risk Report</h1>
    <p><strong>Generated:</strong> {timestamp}</p>

    <div class="section">
        <h2>📸 Screenshots (Before vs After)</h2>
"""

# Add screenshots from this run only
for f in current_screens:
    html += f'<img src="screenshots/{f}" alt="{f}">'

# Add cookies, geo, and dynamic score
html += f"""
    </div>
    <div class="section">
        <h2>🍪 Pre-Consent Cookies</h2>
        <pre>{json.dumps(pre_data.get("cookies", []), indent=2)}</pre>
        <h2>🍪 Post-Consent Cookies</h2>
        <pre>{json.dumps(post_data.get("cookies", []), indent=2)}</pre>
    </div>

    <div class="section">
        <h2>🌍 GeoIP Tracker Locations</h2>
        <pre>{json.dumps(geo_data, indent=2)}</pre>
    </div>

    <div class="section">
        <h2>🛡️ Final TrapScore Summary</h2>
        <p>
            <strong>Trackers:</strong> {score_data["trackers"]}<br>
            <strong>Countries:</strong> {score_data["countries"]}<br>
            <strong>Fingerprint:</strong> {score_data["fingerprint"]}<br>
            <strong>Storage Flags:</strong> {score_data["storage_flags"]}<br>
            <strong>Total Score:</strong> {score_data["score"]}/100 → 
            <span class="risk-{score_data['risk'].split()[0].lower()}">{score_data['risk']}</span>
        </p>
    </div>
</body>
</html>
"""

# Save HTML file
with open(report_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"[✔] HTML report generated: {report_path}")
