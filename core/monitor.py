import asyncio
import json
import websockets
from core.Logger import Logger
from core.AbuseIPDBClient import AbuseIPDBClient
from core.domain_checker import is_similar
# Variable de contrôle de l'exécution du monitoring
running = True
# Fonction principale asynchrone qui écoute les certificats via websocket
async def monitor(domain, log_callback, threshold):
    global running
    logger = Logger(print_logs=True)
    abuse_client = AbuseIPDBClient()

    uri = "ws://localhost:8080/"  # Adresse du serveur certstream local

    try:
        async with websockets.connect(uri) as websocket:
            while running:
                try:
                    # Réception du message JSON
                    message = await websocket.recv()
                    data = json.loads(message)
                    # Filtrage des messages
                    if data.get("message_type") != "certificate_update":
                        continue

                    cert_data = data["data"]["leaf_cert"]
                    issuer = cert_data.get("issuer", {}).get("aggregated", "N/A")
                    domains = cert_data.get("all_domains", [])

                    suspicious = []
                    for d in domains:
                        #Vérification si l'un des domaines est similaire à la cible
                        if is_similar(d, domain, threshold):
                            score = abuse_client.check_reputation(d)
                            score_str = f"{d} (Abuse Score: {score})"
                            suspicious.append(score_str)

                    if suspicious:
                        criticity = "HIGH"
                        log_msg = f"[{criticity}] {', '.join(suspicious)} ({issuer})"
                        logger.alert(log_msg)
                        log_callback(log_msg)

                except Exception as e:
                    log_callback(f"[ERROR] Monitoring loop: {str(e)}")

    except Exception as e:
        log_callback(f"[ERROR] Connection to websocket failed: {str(e)}")
#Fonction pour démarrer le monitoring
def start_monitoring(domain, log_callback, threshold):
    global running
    running = True
    asyncio.run(monitor(domain, log_callback,threshold))
#Fonction pour stopper le monitoring
def stop_monitoring():
    global running
    running = False
