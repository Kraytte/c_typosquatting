# Certstream Typosquatting Monitor

## Présentation
Cet outil surveille en temps réel les certificats SSL/TLS émis à travers les logs Certificate Transparency via un serveur local compatible Certstream (en Go) pour détecter des tentatives de **typosquatting** sur un domaine cible. 

Il utilise :
- WebSocket pour la collecte de certificats
- Distance de Levenshtein pour comparer les noms de domaines
- AbuseIPDB pour vérifier la réputation de l'IP des domaines suspects
- Interface graphique avec `tkinter` pour un usage simple
---

## Prérequis

### Python 3

#### Installation

- **Windows :**
  1. Téléchargez l'installateur sur [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
  2. Exécutez l'installateur avec l'option "Add Python to PATH" cochée

- **Linux :**
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip
  ```

### Go

#### Installation

- **Windows :**
  1. Téléchargez l’installateur sur [https://golang.org/dl/](https://golang.org/dl/)
  2. Installez et vérifiez avec :
     ```bash
     go version
     ```

- **Linux :**
  ```bash
  sudo apt install golang-go
  ```

---

## Dépendances principales

- `websockets`
- `requests`
- `python-dotenv`
que vous pouvez installer avec
```bash
pip install -r requirements.txt
```

> De plus, sur Linux, vous  devez installer `tkinter` avec:

```bash
# Debian/Ubuntu
sudo apt install python3-tk

# Arch
sudo pacman -S tk

# Fedora
sudo dnf install python3-tkinter
```

---

## Structure du projet

```
project_root/
├── core/
│   ├── AbuseIPDBClient.py.
│   ├── domain_checker.py
│   ├── Logger.py
|   ├── monitor.py
|   └── utils.py
├── data/
│   └── suspicious_domains.log
├── gui/
│   └── interface.py
├── interface.py
├── main.py
├── monitor.py
├── requirements.txt
├── run.bat
├── run.sh
├── .env
├── suspicious_domains.log
└── server_go/
    └── certstream-server-go/
        └── cmd/
            └── certstream-server-go
```

---

## Configuration

Créez un fichier `.env` à la racine du projet avec votre clé API (à obtenir en créant un compte sur https://www.abuseipdb.com/):

```
ABUSEIPDB_API_KEY=VOTRE_CLÉ_ABUSEIPDB_ICI
```

---

## Lancement de l'application

### Windows

Double-cliquez sur le fichier `run.bat`. Ce script :
1. Lance le serveur Certstream en Go
2. Lance l'interface graphique Python 

### Linux / macOS

```bash
chmod +x run.sh
./run.sh
```

Ce script :
1. Lance le serveur Go en tâche de fond
2. Lance l'application Python avec interface graphique

## Perspectives d'évolution

Voici quelques pistes d’amélioration possibles pour faire évoluer ce projet :

- **Ajout de listes de surveillance personnalisées :** permettre à l’utilisateur de spécifier une liste de domaines à surveiller plus précisément.
- **Détection multilingue ou avec règles phonétiques :** utiliser des méthodes plus avancées que Levenshtein (Soundex, Metaphone, etc.) pour capter les variantes à l’oral ou des noms similaires dans d'autres langues.
- **Notification par email ou webhook :** alerter automatiquement lorsqu’un domaine hautement suspect est détecté.
- **Exportation CSV/PDF :** pour garder une trace des détections dans un format structuré.
- **Mode en ligne de commande (CLI) :** pour les serveurs headless ou intégration dans une CI/CD.
- **Visualisation graphique :** histogrammes des certificats détectés par jour, heatmap des domaines les plus proches, etc.
- **Historique des détections avec interface web locale :** en Flask ou FastAPI avec une base SQLite légère.

---
## Licence
MIT – Utilisation libre à des fins de recherche ou d'audit.
