#storage_audit.py
import json
import os
from datetime import datetime

def capture_storage_state(page, label="pre"):
    try:
        page.wait_for_load_state("load")
        local_storage = page.evaluate("Object.assign({}, window.localStorage);")
        session_storage = page.evaluate("Object.assign({}, window.sessionStorage);")
        cookies = page.context.cookies()
    except Exception as e:
        print(f"[!] Error capturing {label.upper()} storage: {e}")
        local_storage, session_storage, cookies = {}, {}, []

    out_dir = "data/storage_logs"
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{label}_storage_{ts}.json"
    with open(os.path.join(out_dir, fname), "w") as f:
        json.dump({
            "localStorage": local_storage,
            "sessionStorage": session_storage,
            "cookies": cookies
        }, f, indent=2)
    print(f"[✔] {label.upper()} storage saved to: {os.path.join(out_dir, fname)}")
