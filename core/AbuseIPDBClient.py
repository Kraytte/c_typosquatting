import requests
import socket
import os
from dotenv import load_dotenv

class AbuseIPDBClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("ABUSEIPDB_API_KEY")
        self.base_url = "https://api.abuseipdb.com/api/v2/check"
        self.headers = {
            "Key": self.api_key,
            "Accept": "application/json"
        }

    def check_reputation(self, domain):
        try:
            ip = socket.gethostbyname(domain)
            print(f"[DNS] {domain} resolved to {ip}")
            if not ip:
                print(f"[ERROR] No IP resolved for {domain}")
                return None

            response = requests.get(self.base_url, headers=self.headers, params={"ipAddress": ip, "maxAgeInDays": 90})
            if response.status_code == 200:
                data = response.json()
                return data["data"].get("abuseConfidenceScore")
            else:
                print(f"[ERROR] API status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"[ERROR] Exception during AbuseIPDB check: {e}")
        return None

