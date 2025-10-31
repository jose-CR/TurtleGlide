import os
import subprocess
import utils.variable_globals as va
import utils.helpers_command_global as helper
import utils.styles_variables as st
from core.logger import Logger
from .settings.settings_apps import ServiceSettingApp
from .settings.settings_variables import ServicesVaribles
from .settings.settings_url import ServiceUrlGeneral


class DjangoFuncionApp:
    def __init__(self, project_root, project_name, apps=None):
        self.project_root = project_root
        self.project_name = project_name
        self.apps = apps or ["home"]
        self.logger = Logger()
        self.app_steps = {
            "home": [
                # ("Instalando URLs y vistas de perfil", self.install_url_and_views_perfil),
                # ("Instalando templates y archivos estáticos", self.install_templates_and_static_files),
                # ("Creando carpeta services y archivos", self.create_carpet_services_and_files),
                # ("Creando carpeta utils y archivos", self.carpet_utils_and_files),
                # ("Creando carpeta test y archivos", self.create_carpet_test_and_files),
                # ("Creando carpeta templatetags y archivos", self.create_templatetags),
                # ("Configurando installed_apps", self.installed_apps),
                # ("Configurando urls del proyecto", self.installed_url_in_project),
            ],
        }

    async def create_apps(self):
        for app_name in self.apps:
            app_path = os.path.join(self.project_root, app_name)
            self.logger.beginning(f"Creando app '{app_name}' en {app_path}")

            if not await self._create_django_app(app_name):
                continue

            steps = self.app_steps.get(app_name, [])
            await self._execute_steps(steps, app_name)
            await self.installed_apps(app_name)
            await self.installed_url_in_project()
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
        self.logger.beginning("escribiendo varibles y todo el contenido necesario en settings.py")
      
        service = ServicesVaribles(self.project_name)

        try:
            self.logger.info("Iniciando la instalacion de las Variables")
            service.insert_variables()
            self.logger.info("Iniciando la instalacion de los middleware")
            service.insert_middleware()
            self.logger.info("Iniciando la instalacion de i8n")
            service.insert_i18n_settings()
            self.logger.success("Se agregarn todas las configuraciones necesarias para las variables")
        except Exception as e :
            return self.logger.error(f"Error al escribir variables: {e}")
        self.logger.ending("Terminando de escribir el archivo de configuración")

    async def installed_url_in_project(self):
        self.logger.beginning("Comenzando la integracion de las Urls")

        service = ServiceUrlGeneral(self.project_name, app="home")

        service.update_urls()

        self.logger.ending("URLs de 'home' y 'accounts' agregadas exitosamente a urls.py.")

    async def install_url_and_views_perfil(self):
        file_archive_urls = os.path.join(self.home, "urls.py")
        file_archive_views = os.path.join(self.home, "views.py")
        file_archive_forms = os.path.join(self.home, "forms.py")

        with open(file_archive_urls, "w") as f:
            f.write(va.urls_home.strip())

        with open(file_archive_views, "w") as f:
            f.write(va.views.strip())

        with open(file_archive_forms, "w") as f:
            f.write(va.forms_home.strip())

        print(f"✅  configuracion de views y urls de {self.home}, terminada")

    async def install_templates_and_static_files(self):
        # rutas de destino
        dest_templates = os.path.join(self.home, "templates")
        dest_static = os.path.join(self.home, "static")

        # rutas de subcarpetas static
        dest_css = os.path.join(dest_static, "css")
        dest_js = os.path.join(dest_static, "js")

        # rutas de subcarpetas templates
        dest_components = os.path.join(dest_templates, "components")
        dest_email = os.path.join(dest_templates, "emails")
        dest_layout = os.path.join(dest_templates, "layouts")
        dest_profile = os.path.join(dest_templates, "profile")
        dest_profile_password = os.path.join(dest_profile, "password")
        dest_registration = os.path.join(dest_templates, "registration")

        if not os.path.exists(dest_static):
            print("📁 creando la carpeta static y sub carpetas css y js")
            os.makedirs(dest_static, exist_ok=True)
            os.makedirs(dest_css, exist_ok=True)
            os.makedirs(dest_js, exist_ok=True)
        else:
            print("⚠️ la carpeta ya existe")

        if not os.path.exists(dest_templates):
            print(
                "📁 creando la carpeta templates y sub carpetas components, emails, layouts, profile, password"
            )
            os.makedirs(dest_templates, exist_ok=True)
            os.makedirs(dest_components, exist_ok=True)
            os.makedirs(dest_email, exist_ok=True)
            os.makedirs(dest_layout, exist_ok=True)
            os.makedirs(dest_profile, exist_ok=True)
            os.makedirs(dest_profile_password, exist_ok=True)
            os.makedirs(dest_registration, exist_ok=True)

        # static
        file_css_base_app = os.path.join(dest_css, "base_app.css")
        file_css_basic_styles = os.path.join(dest_css, "basic_styles.css")
        file_js_message = os.path.join(dest_js, "message.js")

        # templates
        templates_index = os.path.join(dest_templates, "index.html")
        templates_profile = os.path.join(dest_templates, "profile.html")
        components_button = os.path.join(dest_components, "button.html")
        components_card = os.path.join(dest_components, "card.html")
        components_form = os.path.join(dest_components, "form.html")
        email_password = os.path.join(dest_email, "email_password.html")
        layouts_app = os.path.join(dest_layout, "app.html")
        password_change_password = os.path.join(
            dest_profile_password, "change_password.html"
        )
        password_reset_email = os.path.join(dest_profile_password, "reset_email.html")
        password_reset_confirm = os.path.join(
            dest_profile_password, "reset_confirm.html"
        )
        password_reset_password_complete = os.path.join(
            dest_profile_password, "reset_password_complete.html"
        )
        profile_edit = os.path.join(dest_profile, "profile_edit.html")
        profile_delete = os.path.join(dest_profile, "profile_delete.html")
        registration_login = os.path.join(dest_registration, "login.html")
        registration_register = os.path.join(dest_registration, "register.html")

        helper.copy_content(file_css_base_app, st.css_base_app, "base_app.css")
        helper.copy_content(
            file_css_basic_styles, st.css_basic_styles, "basic_styles.css"
        )
        helper.copy_content(file_js_message, st.js_message, "message.js")
        # -----------------------------------------------------------------
        helper.copy_content(templates_index, st.templates_index, "index.html")
        helper.copy_content(templates_profile, st.templates_profile, "profile.html")
        helper.copy_content(components_button, st.components_button, "button.html")
        helper.copy_content(components_card, st.components_card, "card.html")
        helper.copy_content(components_form, st.components_form, "form.html")
        helper.copy_content(email_password, st.email_password, "email_password.html")
        helper.copy_content(layouts_app, st.layouts_app, "app.html")
        helper.copy_content(
            password_change_password,
            st.password_change_password,
            "change_password.html",
        )
        helper.copy_content(
            password_reset_email, st.password_reset_email, "reset_email.html"
        )
        helper.copy_content(
            password_reset_confirm, st.password_reset_confirm, "reset_confirm.html"
        )
        helper.copy_content(
            password_reset_password_complete,
            st.password_reset_password_complete,
            "reset_password_complete.html",
        )
        helper.copy_content(
            profile_edit, st.templates_profile_edit, "profile_edit.html"
        )
        helper.copy_content(
            profile_delete, st.templates_profile_delete, "profile_delete.html"
        )
        helper.copy_content(
            registration_login, st.templates_registration_login, "login.html"
        )
        helper.copy_content(
            registration_register, st.templates_registration_register, "register.html"
        )

        print("✅ archivos de las carpetas static y templates hechos corectamente ")

    async def create_carpet_services_and_files(self):
        carpet_services = os.path.join(self.home, "services")
        if not os.path.exists(carpet_services):
            print("📁 creando la carpeta services")
            os.makedirs(carpet_services, exist_ok=True)
        else:
            print("⚠️ la carpeta ya existe")

        file_user_password = os.path.join(carpet_services, "user_password.py")
        file_user_profile = os.path.join(carpet_services, "user_profile.py")

        helper.copy_content(file_user_profile, va.user_profile, "user_profile.py")
        helper.copy_content(file_user_password, va.user_password, "user_password.py")

        print("✅ terminado los archivos de la carpeta services")

    async def carpet_utils_and_files(self):
        carpet_utils = os.path.join(self.home, "utils")
        if not os.path.exists(carpet_utils):
            print("📁 creando la carpeta utils")
            os.makedirs(carpet_utils, exist_ok=True)
            file_init_ = os.path.join(carpet_utils, "__init__.py")
            with open(file_init_, "w") as f:
                f.write("")
            print("✅ Archivo '__init__.py' creado dentro de 'utils'.")
        else:
            print("⚠️ la carpeta ya existe")

        file_test_helpers = os.path.join(carpet_utils, "test_helpers.py")

        helper.copy_content(file_test_helpers, va.test_helpers, "test_helpers.py")

        print(f"✅ creada la carpeta {carpet_utils}, y sus archivos")

    async def create_carpet_test_and_files(self):
        carpet_test = os.path.join(self.home, "test")

        if not os.path.exists(carpet_test):
            print("📁 creando la carpeta test")
            os.makedirs(carpet_test, exist_ok=True)
            file_init_ = os.path.join(carpet_test, "__init__.py")
            with open(file_init_, "w") as f:
                f.write("")
            print("✅ Archivo '__init__.py' creado dentro de 'test'.")
        else:
            print("⚠️ la carpeta ya existe")

        file_test_profile = os.path.join(carpet_test, "test_profile.py")
        file_test_password = os.path.join(carpet_test, "test_password.py")

        helper.copy_content(file_test_profile, va.test_profile, "test_profile.py")
        helper.copy_content(file_test_password, va.test_password, "test_password.py")

        print("✅ creada la carpeta de test y sus archivos")

    async def create_templatetags(self):
        carpet_templatetags = os.path.join(self.home, "templatetags")
        if not os.path.exists(carpet_templatetags):
            print("📁 creando la carpeta templatetags")
            os.makedirs(carpet_templatetags, exist_ok=True)
            file_init_ = os.path.join(carpet_templatetags, "__init__.py")
            with open(file_init_, "w") as f:
                f.write("")
            print("✅ Archivo '__init__.py' creado dentro de 'templatetags'.")
        else:
            print("⚠️ la carpeta ya existe")

        file_templatetags = os.path.join(carpet_templatetags, "components.py")

        helper.copy_content(file_templatetags, va.components, "components.py")

        print("✅ creada la carpeta de los templatetags y sus archivos")
