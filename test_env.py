import os
from pathlib import Path
from dotenv import load_dotenv

# Obtener la ruta del proyecto
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"

print(f"Buscando .env en: {env_path}")
print(f"Archivo .env existe: {env_path.exists()}")

if env_path.exists():
    with open(env_path, 'r') as f:
        print("\nContenido del archivo .env:")
        print(f.read())

# Cargar variables
load_dotenv(env_path)

print(f"\nVariables de entorno cargadas:")
print(f"DEBUG: '{os.getenv('DEBUG')}'")
print(f"GROQ_API_KEY: '{os.getenv('GROQ_API_KEY')}'")
print(f"GROQ_MODEL: '{os.getenv('GROQ_MODEL')}'")