#TrapTrack.py
import time
import csv
import os
from playwright.sync_api import sync_playwright
from storage_audit import capture_storage_state
from geo_simulator import get_geo_headers
from fingerprint_dectector import inject_fingerprint_detection

screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

# Clear screenshot log file
latest_screens_file = "latest_screens.txt"
with open(latest_screens_file, "w") as log:
    log.write("")

def run_test_on_site(url, consent_type):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # ✅ Add region headers and proxy to mitmdump
        headers = get_geo_headers(consent_type)
        context = browser.new_context(
            proxy={"server": "http://localhost:8080"},       # Route through mitmdump
            extra_http_headers=headers,
            ignore_https_errors=True                         # Avoid HTTPS cert issues
        )
        page = context.new_page()

        print(f"🌐 Visiting: {url}")
        page.goto(url, timeout=60000)

        # Pre-consent screenshot + storage
        page.wait_for_load_state("load")
        before_path = f"{screenshot_dir}/{get_domain(url)}_before.png"
        page.screenshot(path=before_path)
        capture_storage_state(page, label="pre")

        # Log pre screenshot
        with open(latest_screens_file, "a") as log:
            log.write(os.path.basename(before_path) + "\n")

        # Inject fingerprint detector
        inject_fingerprint_detection(page)

        # Try clicking cookie consent banner
        try:
            clicked = False
            print("[ℹ] Waiting 20 seconds for manual banner interaction...")
            for i in range(20):
                for selector in ["button#accept", "button:has-text('Accept')", "text=Agree"]:
                    if page.locator(selector).first.is_visible():
                        page.locator(selector).first.click()
                        clicked = True
                        print("[✔] Cookie consent clicked.")
                        break
                if clicked:
                    break
                time.sleep(1)

            if not clicked:
                print("[-] No cookie banner clicked.")
        except Exception as e:
            print(f"[!] Consent click error: {e}")

        # ✅ Allow manual surfing before post-capture
        input("\n🕹️ Surf manually in the browser (click, scroll, login etc). Press [Enter] here when done...")

        # Post-consent screenshot + storage
        try:
            after_path = f"{screenshot_dir}/{get_domain(url)}_after.png"
            page.screenshot(path=after_path)
            with open(latest_screens_file, "a") as log:
                log.write(os.path.basename(after_path) + "\n")
        except:
            pass

        capture_storage_state(page, label="post")
        browser.close()

def get_domain(url):
    return url.split("//")[-1].split("/")[0].replace("www.", "").split(".")[0]

def load_test_sites(csv_file):
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            run_test_on_site(row["Website"], row["ConsentType"])

if __name__ == "__main__":
    csv_path = "test_sites.csv"
    load_test_sites(csv_path)
