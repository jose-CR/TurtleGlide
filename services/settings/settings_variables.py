from .settings_main import ServiceSettingsMain
from core.logger import Logger
import utils.variable_globals as va

class ServicesVaribles:
    def __init__(self, project_name):
        self.project_name = project_name
        self.settings_service = ServiceSettingsMain(project_name)
        self.logger = Logger()

    def insert_variables(self):
        self.logger.info("Agregando variables Globales")
        lines = self.settings_service.readlines()
        lines.append("\n" + va.config_variables.strip() + "\n")
        self.settings_service.writelines(lines)
        self.logger.info("Variables agregadas correctamente")

    def insert_middleware(self):
        """Agrega LocaleMiddleware a MIDDLEWARE si no está presente"""
        self.logger.info("Agregando Middlewares")  
        
        lines = self.settings_service.readlines()

        middleware_start = None
        middleware_end = None 

        # Detectar el bloque MIDDLEWARE
        for i, line in enumerate(lines):
            if "MIDDLEWARE" in line and "=" in line:
                middleware_start = i
            if middleware_start is not None and line.strip() == "]":
                middleware_end = i
                break

        if middleware_start is None or middleware_end is None:
            self.logger.error("No se encontró la definición de MIDDLEWARE.")
            return

        # Verificar si LocaleMiddleware ya está presente
        for line in lines[middleware_start:middleware_end]:
            if "django.middleware.locale.LocaleMiddleware" in line:
                self.logger.info("LocaleMiddleware ya está presente en MIDDLEWARE.")
                return

        # Insertar justo después de CommonMiddleware si existe
        insert_index = middleware_end
        for i in range(middleware_start, middleware_end):
            if "django.middleware.common.CommonMiddleware" in lines[i]:
                insert_index = i + 1
                break

        lines.insert(insert_index, "    'django.middleware.locale.LocaleMiddleware',\n")

        # Sobrescribir el archivo con los cambios
        self.settings_service.writelines(lines)
        self.logger.info("LocaleMiddleware agregado correctamente.")        

    def insert_i18n_settings(self):
        self.logger.info("Agregando configuracion para traducciones")
        lines = self.settings_service.readlines()

        insert_index = None
        for i, line in enumerate(lines):
            if line.strip().startswith("TIME_ZONE"):
                insert_index = i + 1
                break

        if insert_index is None:
            self.logger.error("No se encontró la configuración TIME_ZONE en settings.py.")
            return

        # Asegurarse de que haya un salto de línea antes y después
        lines.insert(insert_index, "\n" + va.i18n_settings.strip() + "\n")

        self.settings_service.writelines(lines)
        self.logger.success("Configuración de internacionalización añadida después de TIME_ZONE.")

