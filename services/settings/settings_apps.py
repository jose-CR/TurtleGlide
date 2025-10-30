from core.logger import Logger
from .settings_main import ServiceSettingsMain


class ServiceSettingApp:
    """Servicio encargado de agregar una app a INSTALLED_APPS"""

    def __init__(self, project_name, app_name):
        self.project_name = project_name
        self.app_name = app_name
        self.logger = Logger()
        self.settings_service = ServiceSettingsMain(project_name)

    async def add_app_to_installed_apps(self):
        self.logger.beginning(f"Agregando app '{self.app_name}' a INSTALLED_APPS")

        lines = self.settings_service.readlines()

        # Comprobar si ya está instalada
        if any(
            f"'{self.app_name}'" in line or f'"{self.app_name}"' in line
            for line in lines
        ):
            print(f"La app '{self.app_name}' ya está instalada en INSTALLED_APPS.")
            self.logger.ending(f"App '{self.app_name}' ya instalada")
            return

        # Insertar dentro de INSTALLED_APPS
        new_lines = []
        inside_block = False
        for line in lines:
            new_lines.append(line)
            if line.strip().startswith("INSTALLED_APPS") and "=" in line:
                inside_block = True
            elif inside_block and line.strip().startswith("]"):
                if f"'{self.app_name}'" not in "".join(lines):
                    new_lines.insert(-1, f"    '{self.app_name}',\n")
                inside_block = False

        self.settings_service.writelines(new_lines)
