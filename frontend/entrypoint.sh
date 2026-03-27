#!/bin/bash

if [ ! -f "rxconfig.py" ]; then
    echo "🚀 Inicializando proyecto Reflex por primera vez..."
    reflex init --template blank
fi

echo "✨ Iniciando servidor Reflex..."
exec "$@"