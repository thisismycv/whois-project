# whois-project

A small command-line tool for domain reconnaissance. It pulls WHOIS registration data for a domain and cross-references the domain's IP against AbuseIPDB to check its abuse/reputation history.

## Features

- **WHOIS lookup** via [whoisjson.com](https://whoisjson.com) — creation date, expiry date, registrar name/email/phone, and associated IPs.
- **AbuseIPDB lookup** — country, ISP, and abuse confidence score for the domain's IP.
- Prints a formatted report to the console and appends it to `results.txt`.

## Requirements

- Python 3.7+
- `requests` library

```bash
pip install requests
```

## Setup

You'll need API keys from both services:

1. **WhoisJSON** — get a token at [whoisjson.com](https://whoisjson.com).
2. **AbuseIPDB** — get a free API key at [abuseipdb.com](https://www.abuseipdb.com).

Open `whois.py` and set your keys:

```python
TOKEN = "yourwhoistoken"
ABUSEIPDB_KEY = "yourabuseipdb"
```

> **Security note:** Don't commit real API keys to a public repo. Consider loading them from environment variables instead, e.g.:
> ```python
> import os
> TOKEN = os.environ.get("WHOIS_TOKEN")
> ABUSEIPDB_KEY = os.environ.get("ABUSEIPDB_KEY")
> ```

## Usage

```bash
python whois.py <domain>
```

Example:

```bash
python whois.py example.com
```

**Note:** the script currently only reads the domain argument (`sys.argv[1]`) — the IP for the AbuseIPDB check is taken from the `ips` field returned by the WHOIS lookup, not from a separate CLI argument, even though the usage message mentions one.

## Output

Results print to the console and are appended to `results.txt` in the working directory, e.g.:

```
=== WHOIS ===
Creation date:   2015-03-14
Expires:         2027-03-14
Registrar name:  Example Registrar Inc.
Registrar email: abuse@example-registrar.com
Phone:           +1.5555550123
IPs:             93.184.216.34

=== AbuseIPDB: 93.184.216.34 ===
Country:         US
ISP:             Example Hosting
Abuse reports:   0%
```

## Disclaimer

For legitimate security research, due diligence, and OSINT purposes only. Always ensure you have the right to investigate a given domain/IP under your local laws and the terms of service of the APIs used.
 
