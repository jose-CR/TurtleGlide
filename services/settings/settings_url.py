from .settings_main import ServiceUrlMain
from core.logger import Logger


class ServiceUrlGeneral:
    def __init__(self, project_name, app=None):
        self.apps = app or []
        self.project_name = project_name
        self.url = ServiceUrlMain(self.project_name)
        self.logger = Logger
        self.lines = self.url.readlines()


    def update_urls(self):
        self.logger.info("Actualizando el archivo urls.py")

        lines = self.lines

        # Verificar si ya existen los imports y rutas
        has_include_import = any(
            "include" in line and "django.urls" in line for line in lines
        )
        has_home_url = any(f"include('{self.apps}.urls')" in line for line in lines)
        has_accounts_url = any(
            "include('django.contrib.auth.urls')" in line for line in lines
        )
        has_i18n_url = any("include('django.conf.urls.i18n')" in line for line in lines)

        new_lines = []
        for line in lines:
            # Si encontramos el import sin include, lo corregimos
            if "from django.urls import path" in line and "include" not in line:
                line = line.strip().replace("path", "path, include") + "\n"
            new_lines.append(line)

        # Si falta el import, lo agregamos
        if not has_include_import:
            for i, line in enumerate(new_lines):
                if "from django.urls" in line:
                    new_lines.insert(i + 1, "from django.urls import include\n")
                    break
            else:
                new_lines.insert(0, "from django.urls import path, include\n")

        # Agregar las rutas dentro de urlpatterns
        for i, line in enumerate(new_lines):
            if "urlpatterns" in line and "=" in line:
                # Buscamos donde empieza la lista [
                for j in range(i, len(new_lines)):
                    if "[" in new_lines[j]:
                        insert_index = j + 1
                        break
                else:
                    insert_index = i + 1  # Por si no encuentra
                if not has_home_url:
                    new_lines.insert(
                        insert_index, f"    path('', include('{self.apps}.urls')),\n"
                    )
                    insert_index += 1
                if not has_accounts_url:
                    new_lines.insert(
                        insert_index,
                        "    path('accounts/', include('django.contrib.auth.urls')),\n",
                    )
                if not has_i18n_url:
                    new_lines.insert(
                        insert_index,
                        "    path('i18n/', include('django.conf.urls.i18n')),\n",
                    )
                break

        # Guardamos los cambios
        self.url.writelines(new_lines)
        self.logger.success(f"Archivo urls.py actualizado correctamente en {self.url.url_path}")