import requests
import sys

if len(sys.argv) < 2:
    print("Usage: python parked.py <domain>")
    sys.exit(1)

DOMAIN = sys.argv[1]

# Check HTTP (follow redirects to see final destination)
try:
    response = requests.get(f"http://{DOMAIN}", timeout=10, allow_redirects=True)
    print(f"[+] Status Code: {response.status_code}")
    print(f"[+] Final URL: {response.url}")
    print(f"[+] Server: {response.headers.get('Server', 'N/A')}")
    print(f"[+] Content-Type: {response.headers.get('Content-Type', 'N/A')}")

    # Check if it redirects to a known parking or mail service
    final_url = response.url.lower()
    if any(x in final_url for x in ["outlook", "office365", "google", "gmail"]):
        print(f"[+] Redirects to legitimate service: {response.url}")
        print("[-] NOT parked")
    elif any(x in final_url for x in ["sedo", "parkingcrew", "bodis", "above.com", "undeveloped"]):
        print("[!] PARKED - known parking service detected")
    else:
        print("[?] Unknown destination - manual check recommended")

except requests.exceptions.SSLError:
    print("[!] SSL error - trying without verification...")
    response = requests.get(f"http://{DOMAIN}", timeout=10, verify=False)
    print(f"[+] Status Code: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("[-] Could not connect to domain")