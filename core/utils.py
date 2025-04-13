from AbuseIPDBClient import AbuseIPDBClient
from Logger import Logger
import socket
from Levenshtein import levenshtein as levenshtein_distance
import threading
abuse_client = AbuseIPDBClient(api_key="2fbf1b7dcb2ce843b0ab19997002b5d6127070ba42e7ef4c3a59e02b815fd6063b99620bb8e493e7")
logger = Logger(print_logs=True)
TRUSTED_ISSUERS = [
    "/C=US/CN=Google Trust Services LLC", 
    "/C=US/CN=DigiCert Inc",
    # ajoute ici les autorités que tu juges de confiance
]

TARGET_DOMAIN = "admin"
MAX_DISTANCE = 10  # seuil de tolérance

def is_suspicious(domain: str, issuer: str):
    dist = levenshtein_distance(domain, TARGET_DOMAIN)
    print(dist)
    issuer_trusted = issuer in TRUSTED_ISSUERS
    if dist <= MAX_DISTANCE:
        level = "HIGH" if not issuer_trusted else "MEDIUM"
        return True, level, dist
    return False, None, dist
def resolve_domain_to_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except Exception as e:
        print(f"[DNS ERROR] Impossible de résoudre {domain} : {e}")
        return None
def handle_domain(domain, abuse_client, logger):
    try:
        ip = socket.gethostbyname(domain)
        print(f"[DNS] {domain} resolved to {ip}")
        score = abuse_client.check_reputation(ip=ip)
        print(f"[AbuseIPDB] {domain} has reputation score {score}")

        # Log si nécessaire
        if score > 50:
            logger.alert(f"[HIGH] {domain} (IP: {ip}) Score: {score}")
        return score
    except Exception as e:
        print(f"[ERROR] While checking {domain}: {e}")
def extract_domains_and_issuer(message: dict):
    try:
        if message.get("message_type") != "certificate_update":
            return None, None

        data = message.get("data", {})
        leaf_cert = data.get("leaf_cert", {})
        domains = leaf_cert.get("all_domains", [])
        issuer = leaf_cert.get("issuer", {}).get("aggregated", "")

        return domains, issuer
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction : {e}")
        return None, None


def main():
    print("[*] Listening for certificate events...")