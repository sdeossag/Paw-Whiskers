import os
import re
import shutil

# === CONFIGURACIÓN ===
TEMPLATES_DIR = "../templates"
BACKUP_DIR = "templates_backup"

# Crear copia de respaldo antes de modificar
if not os.path.exists(BACKUP_DIR):
    shutil.copytree(TEMPLATES_DIR, BACKUP_DIR)
    print(f"✅ Copia de respaldo creada en: {BACKUP_DIR}")

# Expresión regular para encontrar textos visibles fuera de etiquetas
TEXT_PATTERN = re.compile(r'>([^<>{}%]+)<')

def fix_extends_position(content):
    """
    Asegura que {% extends ... %} sea la primera línea del archivo
    y que {% load ... %} esté justo después.
    """
    lines = content.splitlines()
    extends_line = None
    load_lines = []
    other_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("{% extends"):
            extends_line = stripped
        elif stripped.startswith("{% load"):
            load_lines.append(stripped)
        else:
            other_lines.append(line)

    if extends_line:
        # Elimina líneas vacías al inicio
        while other_lines and not other_lines[0].strip():
            other_lines.pop(0)

        # Reconstruir orden correcto
        fixed_lines = [extends_line] + load_lines + [""] + other_lines
        return "\n".join(fixed_lines)
    else:
        return content

def wrap_translations_in_html(content):
    """
    Reemplaza textos visibles (sin etiquetas ni variables) con etiquetas {% trans %}.
    """
    def replacer(match):
        text = match.group(1).strip()
        if not text or len(text) < 2:
            return match.group(0)
        # Evita traducir números, saltos de línea o textos ya traducidos
        if any(x in text for x in ['{%','{{','}}','%}','{#','#}']):
            return match.group(0)
        # Evita espacios o texto vacío
        if not re.search(r'[A-Za-zÁÉÍÓÚáéíóúÑñ]', text):
            return match.group(0)
        return f">{{% trans \"{text}\" %}}<"

    # Asegura que el tag {% load i18n %} esté presente (solo una vez)
    if '{% load i18n %}' not in content:
        content = '{% load i18n %}\n' + content

    return re.sub(TEXT_PATTERN, replacer, content)

# === PROCESAMIENTO ===
for root, _, files in os.walk(TEMPLATES_DIR):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            updated = fix_extends_position(content)
            updated = wrap_translations_in_html(updated)

            if updated != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(updated)
                print(f"✅ Corregido y traducido: {path}")

print("\n🚀 Proceso completado.")
print("Revisa los archivos modificados y ejecuta luego:")
print("   django-admin makemessages -l en")
print("   django-admin compilemessages")
