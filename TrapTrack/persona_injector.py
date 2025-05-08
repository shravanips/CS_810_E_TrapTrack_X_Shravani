#persona_injector.py
def set_persona_headers(region):
    if region == 'EU':
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0)',
            'Accept-Language': 'en-GB,en;q=0.9',
        }
    elif region == 'US':
        return {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Accept-Language': 'en-US,en;q=0.8',
        }
    else:
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
            'Accept-Language': 'en-IN,en;q=0.9',
        }
