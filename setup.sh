#!/bin/bash

# Verificar si Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado. Instálalo antes de continuar."
    exit 1
fi

# Verificar si venv está disponible
if ! python3 -c "import venv" &> /dev/null; then
    echo "🛠 Instalando el módulo venv..."
    sudo apt-get install python3-venv -y || sudo yum install python3-venv -y
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "🚀 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar el entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip y setuptools antes de instalar dependencias
echo "📦 Actualizando pip y setuptools..."
pip install --upgrade pip setuptools wheel

# Instalar dependencias del proyecto
if [ -f "pyproject.toml" ]; then
    echo "📥 Instalando dependencias desde pyproject.toml..."
    pip install .
else
    echo "⚠️ No se encontró pyproject.toml. No se instalarán dependencias."
fi

echo "✅ ¡Listo! El entorno virtual está configurado y activado."
