import requests
import socket
import os
from dotenv import load_dotenv

class AbuseIPDBClient:
    def __init__(self):
        # Charge les variables d'environnements à partir du fichier .env
        load_dotenv()
        # Récupération de la clé d'api et création des entêtes pour la requête 
        self.api_key = os.getenv("ABUSEIPDB_API_KEY")
        self.base_url = "https://api.abuseipdb.com/api/v2/check"
        self.headers = {
            "Key": self.api_key,
            "Accept": "application/json"
        }

    def check_reputation(self, domain):
        try:
            # Résolution DNS du domaine pour obtenir l'addresse IP associée
            ip = socket.gethostbyname(domain)
            print(f"[DNS] {domain} resolved to {ip}")
            #Si aucune IP trouvée , alors affichage de l'erreur et arrêt de la fonction
            if not ip:
                print(f"[ERROR] No IP resolved for {domain}")
                return None
            # Requête sur l'API AbuseIPDB pour obtenir le score de confiance de l'adresse IP
            response = requests.get(self.base_url, headers=self.headers, params={"ipAddress": ip, "maxAgeInDays": 90})
            # Si la requête est un succès (code=200) , récupération du score
            if response.status_code == 200:
                data = response.json()
                return data["data"].get("abuseConfidenceScore")
            else:
                #Affiche l'erreur sinon
                print(f"[ERROR] API status {response.status_code}: {response.text}")
        except Exception as e:
            #Affichage pour d'autres types d'erreurs (comme l'API non disponible)
            print(f"[ERROR] Exception during AbuseIPDB check: {e}")
        return 0

