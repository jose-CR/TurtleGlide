import utils.variable_globals as vo
import utils.helpers_command_global as reco
from pathlib import Path
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

class ServiceCreateStructure:
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.logger = Logger()

    def ensure_folder(self, app_name: str, folder_name: str) -> Path:
        app_path = self.project_root / app_name
        folder_path = app_path / folder_name

        if not folder_path.exists():
            self.logger.carpet_anim(
                f"creando carpeta '{folder_name}' en la app '{app_name}'"
            )
            folder_path.mkdir(parents=True, exist_ok=True)
        else:
            self.logger.warning(
                f"⚠️ La carpeta '{folder_name}' ya existe en la app '{app_name}'"
            )

        return folder_path

    def creation_of_files(self, base: Path, structure: dict):
        for name, content in structure.items():
            if name == base.name:
                new_path = base
            else:
                new_path = base / name

                # Si el contenido es un archivo
            if isinstance(content, str):
                reco.copy_content(new_path, content, filename=name)
                self.logger.info(f"Archivo creado: {new_path}")
                continue

                # Si el contenido es una carpeta
            if isinstance(content, dict):
                if not new_path.exists():
                    new_path.mkdir(exist_ok=True)
                    self.logger.info(f"Carpeta creada: {new_path}")

            self.creation_of_files(new_path, content)

    def hierarchy(self):
        return {
                "home": {
                    "services": {
                        "user_password.py": vo.user_password,
                        "user_profile.py": vo.user_profile,
                        "__init__.py": "",
                    },

                    "utils": {
                        "test_helpers.py": vo.test_helpers,
                        "__init__.py": "",
                    },

                    "test": {
                        "test_profile.py": vo.test_profile,
                        "test_password.py": vo.test_password,
                        "__init__.py": "",
                    },

                    "templatetags": {
                        "components.py": vo.components,
                        "__init__.py": "",
                    }
                }
            }

