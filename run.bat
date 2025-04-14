@echo off
setlocal

REM Lancement le serveur certstream-server-go
echo [INFO] Lancement du serveur Go...
cd server_go/certstream-server-go/cmd/certstream-server-go
start /B go run main.go
cd ../../../..

REM Attente du lancement du serveur go
timeout /t 5 > nul

REM Lancement de l'application python
echo [INFO] Lancement du programme Python...
python main.py
exit
endlocal
pause