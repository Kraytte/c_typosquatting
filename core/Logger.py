import os
# Chemin absolu vers le fichier de log "suspicious_domains.log" dans le dossier data/
LOGFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/suspicious_domains.log")

class Logger:
    """
    Classe simple de gestion de logs pour enregistrer les domaines suspects dans un fichier.
    
    Args:
        print_logs (bool): Si True, affiche les logs dans la console en plus de les enregistrer dans un fichier.
    """
    def __init__(self, print_logs: bool = False):
        self.print_logs = print_logs

    def alert(self, msg):
        """
        Écrit un message d'alerte dans le fichier de log et l'affiche en console si l'option est activée.

        Args:
            msg (str): Message d’alerte formaté à enregistrer.
        """
        # Ouvre le fichier en mode lecture/écriture et écrit le message
        with open(LOGFILE, "a") as f:
            f.write(msg + "\n")
        # Affiche aussi dans la console si l’option est activée
        if self.print_logs:
            print(msg)
