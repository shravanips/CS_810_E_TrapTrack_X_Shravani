# geo_analyzer.py

import os
import json
import requests

def extract_ips_from_logs(logs_dir):
    ip_set = set()
    if not os.path.exists(logs_dir):
        print(f"❌ Directory {logs_dir} does not exist.")
        return ip_set

    for filename in os.listdir(logs_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(logs_dir, filename)
            with open(filepath, 'r') as file:
                for line in file:
                    try:
                        log_entry = json.loads(line)
                        host = log_entry.get("host")
                        if host:
                            ip_set.add(host)
                    except json.JSONDecodeError:
                        continue
    return ip_set

def geolocate_ips(ip_set):
    geo_data = {}
    for ip in ip_set:
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            if response.status_code == 200:
                geo_data[ip] = response.json()
            else:
                geo_data[ip] = {"error": f"HTTP {response.status_code}"}
        except requests.RequestException as e:
            geo_data[ip] = {"error": str(e)}
    return geo_data

def save_geo_data(geo_data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as outfile:
        json.dump(geo_data, outfile, indent=4)
    print(f"📍 Geo data saved to: {output_path}")

def run_geo_analysis():
    logs_dir = "data/network_logs"
    output_path = "data/geo_locations.json"
    print("🌍 Running GeoIP analysis on captured network logs...")
    ip_set = extract_ips_from_logs(logs_dir)
    if not ip_set:
        print("⚠️ No IPs found in network logs.")
        return
    geo_data = geolocate_ips(ip_set)
    save_geo_data(geo_data, output_path)

if __name__ == "__main__":
    run_geo_analysis()
