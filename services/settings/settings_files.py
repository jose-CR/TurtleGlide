from core.logger import Logger
from pathlib import Path
import utils.helpers_command_global as reco
import utils.styles_variables as sa 


class ServiceSettingsSearchMain:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.logger = Logger()

    def detect_existing_apps(self):
        apps_found = []

        for item in self.project_root.iterdir():
            if item.is_dir() and not item.name.startswith("__"):
                if (item / "apps.py").exists() or (item / "models.py").exists():
                    apps_found.append(item)

        self.logger.info(f"Apps detectadas: {[a.name for a in apps_found]}")
        return apps_found

class ServicesSettingsTemplatesAndStatic:
    def __init__(self, app_path: Path):
        self.app_path = app_path
        self.templates = app_path / "templates"
        self.static = app_path / "static"
        self.logger = Logger()

    def create_base_folders(self):
        self.templates.mkdir(exist_ok=True)
        self.static.mkdir(exist_ok=True)

        self.logger.folder(f"Carpeta creada: {self.templates}")
        self.logger.folder(f"Carpeta creada: {self.static}")

        return self.templates, self.static

class ServicesManageFiles:
    def __init__(self, templates_path: Path, static_path: Path):
        self.templates_path = templates_path
        self.static_path = static_path
        self.logger = Logger()

        self.hierarchy = self._hierarchy()
        self._apply_hierarchy()

    # -------------------------
    # Definir la estructura base
    # -------------------------
    def _hierarchy(self):
        return {
            "home": {
                "templates": {
                    "index.html": sa.templates_index,
                    "profile.html": sa.templates_profile,

                    "components": {
                        "button.html": sa.components_button,
                        "card.html": sa.components_card,
                        "form.html": sa.components_form,
                    },

                    "email": {
                        "email_password.html": sa.email_password,
                    },

                    "layouts": {
                        "app.html": sa.layouts_app,
                    },

                    "profile": {
                        "profile_edit.html": sa.templates_profile_edit,
                        "profile_delete.html": sa.templates_profile_delete,

                        "password": {
                            "change_password.html": sa.password_change_password,
                            "reset_email.html": sa.password_reset_email,
                            "reset_confirm.html": sa.password_reset_confirm,
                        }
                    },

                    "registration": {
                        "login.html": sa.templates_registration_login,
                        "register.html": sa.templates_registration_register,
                    }
                },

                "static": {
                    "css": {
                        "base_app.css": sa.css_base_app,
                        "basic_styles.css": sa.css_basic_styles,
                    },
                    "js": {
                        "message.js": sa.js_message,
                    }
                }
            }
        }

    # -------------------------
    # Crear carpetas/archivos
    # -------------------------
    def _create_tree(self, base: Path, structure: dict):
        for name, content in structure.items():
            new_path = base / name

            if isinstance(content, str):
                reco.copy_content(new_path, content, filename=name)
                self.logger.info(f"Archivo creado: {new_path}")
                continue

            new_path.mkdir(exist_ok=True)
            self.logger.folder(f"Carpeta creada: {new_path}")
            self._create_tree(new_path, content)

    # -------------------------
    # Aplicar estructura
    # -------------------------
    def _apply_hierarchy(self):
        self.logger.info("Aplicando estructura de templates y static...")

        structure = self.hierarchy["home"]

        # Crear templates/*
        self._create_tree(self.templates_path, structure["templates"])

        # Crear static/*
        self._create_tree(self.static_path, structure["static"])
