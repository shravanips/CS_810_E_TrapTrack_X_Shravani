def get_geo_headers(region="EU"):
    if region == "EU":
        return {"X-Geo-Location": "EU", "User-Agent": "Mozilla/5.0 (Europe Test Agent)"}
    elif region == "US":
        return {"X-Geo-Location": "US", "User-Agent": "Mozilla/5.0 (US Agent)"}
    elif region == "IN":
        return {"X-Geo-Location": "IN", "User-Agent": "Mozilla/5.0 (India Agent)"}
    else:
        return {}