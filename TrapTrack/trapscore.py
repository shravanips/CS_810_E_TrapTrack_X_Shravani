#trapscore.py
import os
import json

def calculate_trapscore(verbose=False):
    try:
        network_dir = "data/network_logs"
        storage_dir = "data/storage_logs"
        geo_file = "data/geo_locations.json"

        # === Count unique tracker domains ===
        tracker_domains = set()
        if os.path.exists(network_dir):
            for fname in os.listdir(network_dir):
                if fname.endswith(".json"):
                    with open(os.path.join(network_dir, fname)) as f:
                        try:
                            data = json.load(f)
                            domain = data.get("host")
                            if domain:
                                tracker_domains.add(domain)
                        except:
                            continue
        trackers = len(tracker_domains)

        # === Count unique countries from geoIP ===
        countries = 0
        if os.path.exists(geo_file):
            with open(geo_file) as f:
                geo_data = json.load(f)
                country_set = set()
                for val in geo_data.values():
                    if isinstance(val, dict) and "country" in val:
                        country_set.add(val["country"])
                    elif isinstance(val, str):
                        country_set.add(val)
                countries = len(country_set)

        # === Fingerprint detection (1 or 0 assumed) ===
        fingerprint = 1  # Placeholder; assumed injected

        # === Count post-consent storage types ===
        storage_flags = 0
        post_files = sorted([f for f in os.listdir(storage_dir) if f.startswith("post_")])
        if post_files:
            with open(os.path.join(storage_dir, post_files[-1])) as f:
                post_data = json.load(f)
                if post_data.get("cookies"): storage_flags += 1
                if post_data.get("localStorage"): storage_flags += 1
                if post_data.get("sessionStorage"): storage_flags += 1

        # === Raw Score Calculation ===
        raw_score = (trackers * 2) + (countries * 1) + (fingerprint * 3) + (storage_flags * 2)

        # === Normalize to a 0–100 Scale ===
        MAX_TRACKERS = 20
        MAX_COUNTRIES = 10
        MAX_FINGERPRINT = 1
        MAX_STORAGE = 3
        max_score = (MAX_TRACKERS * 2) + (MAX_COUNTRIES * 1) + (MAX_FINGERPRINT * 3) + (MAX_STORAGE * 2)  # = 59

        score = int((raw_score / max_score) * 100)

        # === Risk Level ===
        if score >= 70:
            risk = "HIGH RISK"
        elif score >= 40:
            risk = "MEDIUM RISK"
        else:
            risk = "LOW RISK"

        if verbose:
            print("\n📊 Calculating TrapTrack Privacy Risk Score...")
            print(f"🔍 Breakdown → Trackers: {trackers}, Countries: {countries}, Fingerprint: {fingerprint}, Storage: {storage_flags}")
            print(f"🛡️ TrapScore = {score}/100 → {risk}")

        return {
            "trackers": trackers,
            "countries": countries,
            "fingerprint": fingerprint,
            "storage_flags": storage_flags,
            "score": score,
            "risk": risk
        }

    except Exception as e:
        if verbose:
            print(f"[!] Error computing trapscore: {e}")
        return None

if __name__ == "__main__":
    calculate_trapscore(verbose=True)
