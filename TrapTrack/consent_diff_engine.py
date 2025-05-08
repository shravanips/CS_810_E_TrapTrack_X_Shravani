# consent_diff_engine.py

import os
import json

def load_json_files(folder):
    files = sorted(os.listdir(folder))
    data = []
    for file in files:
        with open(os.path.join(folder, file)) as f:
            data.append(json.load(f))
    return data

def compare_storage(pre, post):
    print("\n🔍 Comparing Cookies:")
    pre_cookies = {c['name'] for c in pre['cookies']}
    post_cookies = {c['name'] for c in post['cookies']}
    new = post_cookies - pre_cookies
    print(f"New cookies after consent: {new}")
    print("\n🔍 Comparing localStorage keys:")
    new_keys = set(post['localStorage'].keys()) - set(pre['localStorage'].keys())
    print(f"New localStorage keys: {new_keys}")

def run_diff():
    folder = "data/storage_logs"
    files = sorted([f for f in os.listdir(folder) if f.endswith(".json")])
    if len(files) >= 2:
        pre = json.load(open(os.path.join(folder, files[-2])))
        post = json.load(open(os.path.join(folder, files[-1])))
        compare_storage(pre, post)
    else:
        print("❌ Not enough logs to compare.")

if __name__ == "__main__":
    run_diff()