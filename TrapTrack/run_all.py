#run_all.py
import os
import subprocess
import signal
import time
import webbrowser
from pathlib import Path

print("\n🚀 Running TrapTrack End-to-End...\n")

# Step 0: Start mitmdump in background
print("[0/4] Starting mitmdump proxy...")
mitm_proc = subprocess.Popen(
    ["python", "-m", "mitmproxy.tools.dump", "-p", "8080", "-s", "network_logger.py"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(2)

# Steps
steps = [
    ("[1/4] Running TrapTrack.py...", "TrapTrack.py"),
    ("[2/4] Running geo_analyzer.py...", "geo_analyzer.py"),
    ("[3/4] Running trapscore.py...", "trapscore.py"),
    ("[4/4] Running generate_html_report.py...", "generate_html_report.py")
]

for msg, script in steps:
    print(msg)
    try:
        os.system(f"python {script}")
    except Exception as e:
        print(f"[!] Failed to run {script}: {e}")

# Stop mitmdump
print("[✔] Shutting down mitmdump...")
mitm_proc.terminate()
mitm_proc.wait()

# Step 6: Open the report in browser
report_path = Path("traptrack_report.html").resolve()
if report_path.exists():
    print(f"\n📄 Opening report: {report_path}")
    webbrowser.open_new_tab(report_path.as_uri())
else:
    print("❌ Report not found.")

print("\n✅ Done.")
