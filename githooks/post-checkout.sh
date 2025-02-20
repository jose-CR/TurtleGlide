#!/bin/bash

# Detectar si es la primera vez que se clona el repo
if [ ! -f .git/cloned ]; then
    echo "Repositorio clonado por primera vez. Ejecutando setup.sh..."
    ./setup.sh  # O setup.bat en Windows
    touch .git/cloned  # Crear un archivo para evitar ejecución futura
fi
