import requests
import sys
from pathlib import Path

TOKEN = "d81048aab0a89f6311fb028633aa1d2d6305165c2c47c2017f6dae23ec44defe"
ABUSEIPDB_KEY = "5003a121301e3e3b6762358e716de7882f32deeaab898c052e2d15d693559f1340878c965e1cf0e2"


if len(sys.argv) < 2:
    print("Usage: python whois.py <domain> <ip>")
    sys.exit(1)

DOMAIN = sys.argv[1]

def whoisdomain(domain: str, token: str) -> dict:
    url = f"https://whoisjson.com/api/v1/whois?domain={domain}"
    headers = {"Authorization": f"TOKEN={token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def abuseipdb_lookup(ip: str, api_key: str) -> dict:
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": api_key,
        "Accept": "application/json",
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90,
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get("data", {})

# WHOIS lookup
result    = whoisdomain(DOMAIN, TOKEN)
registrar = result.get("registrar", {})

created         = result.get("created")
expires         = result.get("expires")
registrar_name  = registrar.get("name")
registrar_email = registrar.get("email")
phone           = registrar.get("phone")
ips             = result.get("ips")

# AbuseIPDB lookup
abuse           = abuseipdb_lookup(ips, ABUSEIPDB_KEY)
country         = abuse.get("countryCode")
isp             = abuse.get("isp")
abuse_score     = abuse.get("abuseConfidenceScore")

output = f"""=== WHOIS ===
Creation date:   {created or 'Not found'}
Expires:         {expires or 'Not found'}
Registrar name:  {registrar_name or 'Not found'}
Registrar email: {registrar_email or 'Not found'}
Phone:           {phone or 'Not found'}
IPs:             {ips or 'Not found'}

=== AbuseIPDB: {ips} ===
Country:         {country or 'Not found'}
ISP:             {isp or 'Not found'}
Abuse reports:   {abuse_score or 0}%
"""

print(output)
with Path("results.txt").open("a") as f:
    f.write(output)
print("Saved to results.txt")