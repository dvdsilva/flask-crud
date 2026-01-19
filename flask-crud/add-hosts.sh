#!/bin/bash

# Script para adicionar echo.example.com ao /etc/hosts

DOMAIN="echo.example.com"
IP="127.0.0.1"

# Verificar se já existe
if grep -q "$DOMAIN" /etc/hosts; then
    echo "✅ $DOMAIN já está configurado no /etc/hosts"
else
    echo "Adicionando $DOMAIN ao /etc/hosts..."
    echo "$IP $DOMAIN" | sudo tee -a /etc/hosts
    echo "✅ $DOMAIN adicionado com sucesso!"
fi

echo ""
echo "🌐 Acesse a aplicação em: http://$DOMAIN"
