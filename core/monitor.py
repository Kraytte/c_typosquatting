import asyncio
import json
import websockets
from core.Logger import Logger
from core.AbuseIPDBClient import AbuseIPDBClient
from core.domain_checker import is_similar,resolve_ip

running = True

async def monitor(domain, log_callback):
    global running
    logger = Logger(print_logs=True)
    abuse_client = AbuseIPDBClient()

    uri = "ws://localhost:8080/"

    try:
        async with websockets.connect(uri) as websocket:
            while running:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)

                    if data.get("message_type") != "certificate_update":
                        continue

                    cert_data = data["data"]["leaf_cert"]
                    issuer = cert_data.get("issuer", {}).get("aggregated", "N/A")
                    domains = cert_data.get("all_domains", [])

                    suspicious = []
                    for d in domains:
                        if is_similar(d, domain):
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

def start_monitoring(domain, log_callback):
    global running
    running = True
    asyncio.run(monitor(domain, log_callback))

def stop_monitoring():
    global running
    running = False
