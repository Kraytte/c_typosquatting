@echo off
setlocal

REM Définir le chemin absolu vers le dossier du main.go
set "GOSERVER=server_go\certstream-server-go\cmd\certstream-server-go"

REM Lancer le serveur certstream-server-go
echo [INFO] Lancement du serveur Go...
cd server_go/certstream-server-go/cmd/certstream-server-go
start /B go run main.go
cd ../../../..

REM Attendre le lancement du serveur WebSocket
timeout /t 5 > nul

REM Activer un éventuel environnement virtuel Python ici (facultatif)
REM call venv\Scripts\activate

REM Lancer l'application Python
echo [INFO] Lancement du programme Python...
python main.py
exit
endlocal
pause