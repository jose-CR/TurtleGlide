import os
from core.logger import Logger


class ServiceSettingsMain:
    def __init__(self, project_name):
        self.project_name = project_name
        self.logger = Logger()
        self.settings_path = os.path.join(self.project_name, "settings.py")
        self.detected()

    def detected(self):
        """Verifica que settings.py exista y devuelve su ruta"""
        self.logger.info(f"Detectando settings.py en {self.project_name}...")
        if not os.path.exists(self.settings_path):
            self.logger.error(f"No se encontró {self.settings_path}")
            raise FileNotFoundError(f"{self.settings_path} no existe")
        self.logger.info(f"Archivo settings.py detectado en: {self.settings_path}")
        return self.settings_path

    def readlines(self):
        """Lee todas las líneas del archivo settings.py"""
        with open(self.settings_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        self.logger.info("leyendo el archivo settings.py")
        return lines

    def writelines(self, lines):
        """Sobrescribe settings.py con las líneas nuevas"""
        with open(self.settings_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        self.logger.info("sobre escribiendo las líneas en settings.py")

class ServiceUrlMain:
    def __init__(self, project_name):
        self.project_name = project_name
        self.logger = Logger()
        self.url_path = os.path.join(self.project_name, 'urls.py')
        self.detected()

    def detected(self):
        """Verifica que urls.py exista y devuelve su ruta"""
        self.logger.info(f"Detectando urls.py en {self.project_name}...")
        if not os.path.exists(self.url_path):
            self.logger.error(f"No se encontró {self.url_path}")
            raise FileNotFoundError(f"{self.url_path} no existe")
        self.logger.info(f"Archivo urls.py detectado en: {self.url_path}")
        return self.url_path

    def readlines(self):
        """Lee todas las líneas del archivo urls.py"""
        with open(self.url_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        self.logger.info("leyendo el archivo urls.py")
        return lines

    def writelines(self, lines):
        """Sobrescribe urls.py con las líneas nuevas"""
        with open(self.url_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        self.logger.info("sobre escribiendo las líneas en urls.py")

