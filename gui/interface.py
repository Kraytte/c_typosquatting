import tkinter as tk
from tkinter import ttk
import threading
from core.monitor import start_monitoring, stop_monitoring
import sys
#Classe de l'application graphique
class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Certstream Typosquatting Monitor")
        #Fenêtre principale
        self.frame = ttk.Frame(root, padding=20)
        self.frame.pack(fill="both", expand=True)
        #Champ ou indiquer le nom de domaine à surveiller
        ttk.Label(self.frame, text="Nom de domaine à surveiller:").pack(anchor="w")
        self.domain_entry = ttk.Entry(self.frame, width=50)
        self.domain_entry.pack(fill="x", pady=5)
        #Bouton pour lancer le monitoring
        self.start_button = ttk.Button(self.frame, text="Démarrer la surveillance", command=self.start)
        self.start_button.pack(pady=(10, 5))
        #Bouton pour stopper le monitoring
        self.stop_button = ttk.Button(self.frame, text="Arrêter la surveillance", command=self.stop, state=tk.DISABLED)
        self.stop_button.pack()
        #Bouton pour quitter l'application
        self.quit_button = ttk.Button(self.frame, text="Quitter", command=self.quit)
        self.quit_button.pack(pady=(10, 5))
        #Champ répertoriant les evenements du logger
        self.log_box = tk.Text(self.frame, height=15)
        self.log_box.pack(fill="both", expand=True, pady=(10, 0))
        #Variable de contrôle d'état
        self.monitoring = False
        self.thread = None
    #Fonction de démarrage de la surveillance dans un thread séparé
    def start(self):
        domain = self.domain_entry.get()
        if domain:
            self.log_box.insert(tk.END, f"[INFO] Démarrage de la surveillance pour : {domain}\n")
            self.monitoring = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.thread = threading.Thread(target=start_monitoring, args=(domain, self.log_callback))
            self.thread.daemon = True
            self.thread.start()
    #Fonction d'arrêt de la surveillance
    def stop(self):
        self.log_box.insert(tk.END, "[INFO] Arrêt de la surveillance.\n")
        self.monitoring = False
        stop_monitoring()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    #Fonction d'arrêt de l'application
    def quit(self):
        self.root.quit()  
        sys.exit()
    #Fonction de mise à jour de la zone de log  
    def log_callback(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
#Fonction de lancement de l'interface graphique
def run_gui():
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()