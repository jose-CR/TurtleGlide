import os
import shutil
from pathlib import Path

def copy_recursive(src_dir, dest_dir, extension, pretty_src_base=None, pretty_dst_base=None):
    if not os.path.exists(src_dir):
        print(f"❌ Error: La carpeta {src_dir} no existe.")
        return

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if any(file.endswith(ext) for ext in extension):
                src_file = os.path.join(root, file)

                # Calcular ruta relativa para mantener la estructura
                relative_path = os.path.relpath(src_file, src_dir)
                dst_file = os.path.join(dest_dir, relative_path)
                        
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)

                # Formato bonito para logs
                pretty_src = os.path.relpath(src_file, pretty_src_base or src_dir)
                pretty_dst = os.path.relpath(dst_file, pretty_dst_base or dest_dir)

                print(f"✅ Copiado: {pretty_src} → {pretty_dst}")

def copy_content(dest_path, content, filename=None, overwrite=False):
    """
    Crea un archivo con contenido si no existe.
    Si existe y overwrite=True, lo sobrescribe.
    Si existe y el contenido es igual, no lo modifica.

    Args:
        dest_path (str | Path): Ruta completa del archivo.
        content (str): Contenido a escribir.
        filename (str | None): Solo para mostrar en logs.
        overwrite (bool): Permite sobrescribir un archivo existente.
    """
    
    dest_path = Path(dest_path)
    filename = filename or dest_path.name

    # Crear carpeta padre si no existe
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Si el archivo no existe, crearlo
    if not dest_path.exists():
        dest_path.write_text(content, encoding="utf-8")
        print(f"✅ Archivo creado: {filename} → {dest_path}")
        return True

    # Si el archivo existe, comprobar contenido
    existing_content = dest_path.read_text(encoding="utf-8")
    if existing_content == content:
        print(f"ℹ️ Archivo {filename} ya existe y está actualizado. → {dest_path}")
        return False

    # Si se permite sobrescribir
    if overwrite:
        dest_path.write_text(content, encoding="utf-8")
        print(f"🔄 Archivo sobrescrito: {filename} → {dest_path}")
        return True

    # Si no se puede sobrescribir
    print(f"⚠️ Archivo {filename} ya existe y NO fue sobrescrito. → {dest_path}")
    return False
