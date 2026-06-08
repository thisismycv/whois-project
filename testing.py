import requests
from pathlib import Path

TOKEN = "d81048aab0a89f6311fb028633aa1d2d6305165c2c47c2017f6dae23ec44defe"
DOMAIN = "google.com"

def whoisdomain(domain: str, token: str) -> dict:
    url = f"https://whoisjson.com/api/v1/whois?domain={domain}"
    headers = {
        "Authorization": f"TOKEN={token}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

result = whoisdomain(DOMAIN, TOKEN)
Path("results2.txt").write_text(str(result))