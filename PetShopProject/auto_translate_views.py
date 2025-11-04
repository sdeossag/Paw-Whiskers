import os
import re
import shutil

# === CONFIGURACIÓN ===
APPS = ["tienda", "clientes", "productos", "carrito", "pedidos", "chatbot"]
BACKUP_DIR = "py_backup_vistas"

# Crear carpeta de respaldo sin copiar todo el proyecto
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)
    print(f"✅ Carpeta de respaldo creada: {BACKUP_DIR}")

# Expresiones regulares
STRING_PATTERN = re.compile(r'(["\'])(.*?)(\1)')
EXCLUDE_EXTENSIONS = ["models.py", "urls.py", "migrations", "admin.py", "wsgi.py", "asgi.py", "settings.py"]

def is_safe_to_translate(line):
    """Evita envolver líneas que no son de texto o son configuraciones"""
    # Evita imports, definiciones y consultas
    if any(word in line for word in ["import ", "class ", "def ", "return", "path(", "objects.", "QuerySet", "render(", "redirect("]):
        return False
    return True

def wrap_texts_in_gettext(content):
    """Envuelve textos literales con gettext si son traducibles"""
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        modified = line
        if is_safe_to_translate(line):
            def replace_match(match):
                text = match.group(2)
                if not text.strip():
                    return match.group(0)
                # Evita URLs, variables o f-strings
                if text.startswith("http") or "{" in text or "}" in text or text.startswith("f'") or text.startswith('f"'):
                    return match.group(0)
                # Evita HTML o códigos
                if "<" in text or ">" in text or "=" in text:
                    return match.group(0)
                # Traduce solo si parece texto legible
                if len(text.split()) >= 1 and any(c.isalpha() for c in text):
                    return f"_(\"{text}\")"
                return match.group(0)
            modified = STRING_PATTERN.sub(replace_match, line)
        new_lines.append(modified)
    return "\n".join(new_lines)

# === PROCESAMIENTO ===
for app in APPS:
    app_path = os.path.join("..", app)
    if not os.path.exists(app_path):
        print(f"⚠️  Carpeta no encontrada: {app_path}")
        continue

    for root, _, files in os.walk(app_path):
        for file in files:
            if not file.endswith(".py"):
                continue
            if any(skip in file for skip in EXCLUDE_EXTENSIONS):
                continue

            path = os.path.join(root, file)
            backup_path = os.path.join(BACKUP_DIR, f"{app}_{file}")

            # Copia segura antes de modificar
            shutil.copy2(path, backup_path)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Agrega import gettext si no existe
            if "from django.utils.translation import gettext as _" not in content:
                content = "from django.utils.translation import gettext as _\n" + content

            # Traduce textos literales seguros
            content = wrap_texts_in_gettext(content)

            # Guarda solo si hubo cambios
            if content != original_content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Traducciones aplicadas en: {path}")

print("\n🚀 Proceso completado correctamente.")
print("Ahora ejecuta:")
print("   django-admin makemessages -l en")
print("   django-admin compilemessages")
print("\n💡 Los modelos NO fueron modificados. Solo vistas y textos visibles en pantalla.")
