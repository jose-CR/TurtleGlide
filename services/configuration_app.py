import os
import subprocess
import utils.variable_globals as va
from core.logger import Logger
from .settings.settings_apps import ServiceSettingApp, ServiceCreateStructure
from .settings.settings_variables import ServicesVaribles
from .settings.settings_url import ServiceUrlGeneral
from .settings.settings_files import (
    ServiceSettingsSearchMain,
    ServicesSettingsTemplatesAndStatic,
    ServicesManageFiles,
)
from pathlib import Path


class DjangoFuncionApp:
    def __init__(self, project_root, project_name, apps=None):
        project_root_path = Path(project_root)
        cwd = Path.cwd()
        if not project_root_path.is_absolute():
            if cwd.name == project_root_path.name:
                project_root_path = cwd
            else:
                project_root_path = cwd / project_root

        self.project_root = project_root_path
        self.project_name = project_name
        self.apps = apps or ["home"]
        self.logger = Logger()
        self.service_settings = ServiceSettingsSearchMain(self.project_root)
        self.app_steps = {
            "home": [
                # ("Instalando URLs y vistas de perfil", self.install_url_and_views_perfil),
                # ("Instalando templates y archivos estáticos", self.install_templates_and_static_files),
                ("Creando carpetas y archivos", self.create_folders_and_files),
                # ("Configurando installed_apps", self.installed_apps),
                # ("Configurando urls del proyecto", self.installed_url_in_project),
            ],
        }

    async def create_apps(self):
        existing_apps = self.service_settings.detect_existing_apps()

        for app_name in self.apps:
            if app_name in existing_apps:
                self.logger.warning(
                    f"La app '{app_name}' ya existe. Se omitirá su creación."
                )
                continue

            app_path = os.path.join(self.project_root, app_name)
            self.logger.beginning(f"Creando app '{app_name}' en {app_path}")

            if not await self._create_django_app(app_name):
                continue

            steps = self.app_steps.get(app_name, [])
            await self.installed_apps(app_name)
            await self._execute_steps(steps, app_name)
            # await self.installed_url_in_project()

            self.logger.ending(f"App '{app_name}' creada exitosamente en {app_path}")

    async def _create_django_app(self, app_name) -> bool:
        """Ejecuta 'startapp' y maneja errores."""
        try:
            subprocess.run(["python", "manage.py", "startapp", app_name], check=True)
            self.logger.success(f"App '{app_name}' creada con manage.py")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error al crear la app con manage.py: {e}")

    async def _execute_steps(self, steps, app_name):
        """Ejecuta una lista de pasos (tuplas de descripción + coroutine)."""
        for description, coroutine in steps:
            self.logger.info(f"[{app_name}] 🔧 {description}...")
            try:
                await coroutine()
                self.logger.success(f"[{app_name}] {description} completado")
            except Exception as e:
                self.logger.warning(f"[{app_name}] Error durante '{description}': {e}")

    async def installed_apps(self, app_name):
        self.logger.beginning("Agregando app a INSTALLED_APPS")

        service = ServiceSettingApp(self.project_name, app_name)
        await service.add_app_to_installed_apps()
        self.logger.ending("Apps agregada correctamente")
        await self.write_variables()

    async def write_variables(self):
        self.logger.beginning(
            "escribiendo varibles y todo el contenido necesario en settings.py"
        )

        service = ServicesVaribles(self.project_name)

        try:
            self.logger.info("Iniciando la instalacion de las Variables")
            service.insert_variables()
            self.logger.info("Iniciando la instalacion de los middleware")
            service.insert_middleware()
            self.logger.info("Iniciando la instalacion de i8n")
            service.insert_i18n_settings()
            self.logger.success(
                "Se agregarn todas las configuraciones necesarias para las variables"
            )
        except Exception as e:
            return self.logger.error(f"Error al escribir variables: {e}")
        self.logger.ending("Terminando de escribir el archivo de configuración")

    async def installed_url_in_project(self):
        self.logger.beginning("Comenzando la integracion de las Urls")

        service = ServiceUrlGeneral(self.project_name, app="home")

        service.update_urls()

        self.logger.ending(
            "URLs de 'home' y 'accounts' agregadas exitosamente a urls.py."
        )

    async def install_url_and_views_perfil(self):
        self.logger.beginning(
            "Comenzando la creacion de los archivos externos en las carpetas"
        )

        files = {
            "home": {
                "urls.py": va.urls_home,
                "views.py": va.views,
                "forms.py": va.forms_home,
            }
        }

        for app_name, app_files in files.items():
            app_path = self.project_root / app_name
            app_path.mkdir(parents=True, exist_ok=True)

            for file_name, content in app_files.items():
                file_path = app_path / file_name
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content.strip())
                self.logger.success(f"Archivo creado: {file_path}")

        self.logger.ending(f"configuracion de views y urls de {self.apps}, terminada")

    async def install_templates_and_static_files(self):
        self.logger.beginning("Comenzando creación de carpetas y archivos...")

        search = ServiceSettingsSearchMain(self.project_root)
        apps = search.detect_existing_apps()

        if not apps:
            self.logger.error("No se encontraron apps.")
            return

        for app_path in apps:
            self.logger.info(f"📌 Procesando app: {app_path.name}")

            # Crear templates/ y static/
            folder_service = ServicesSettingsTemplatesAndStatic(app_path)
            templates_path, static_path = folder_service.create_base_folders()

            # Crear toda la estructura home
            ServicesManageFiles(templates_path, static_path)

            self.logger.success(f"✓ Archivos creados para: {app_path.name}")

        self.logger.ending("Finalizada la creación de plantillas y estáticos.")

    async def create_folders_and_files(self):
        self.logger.beginning("comenzando la estructura de la app")

        search = ServiceSettingsSearchMain(self.project_root)
        apps = search.detect_existing_apps()

        if not apps:
            self.logger.error("No se encontraron apps.")
            return

        service = ServiceCreateStructure(self.project_root)

        for app in apps:
            app_path = self.project_root / app

            structure = service.hierarchy()  
            service.creation_of_files(app_path, structure)

        self.logger.ending("Terminado la estructura de la app")

