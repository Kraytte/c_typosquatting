#!/bin/bash

echo "Lancement de certstream-server-go..."

cd server_go/certstream-server-go/cmd/certstream-server-go || exit 1
go run main.go &
GO_PID=$!

cd ../../../.. || exit 1

echo "Lancement du projet Python..."
python3 main.py

echo "Arrêt de certstream-server-go..."
kill $GO_PID