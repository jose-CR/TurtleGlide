from django.core.management.base import BaseCommand
from services.configuration_app import DjangoFuncionApp
import asyncio

class Command(BaseCommand):
    help = "Crea una nueva aplicación dentro del proyecto Django"

    def handle(self, *args, **options):
        project_root = input("Introduce la ruta del proyecto: ")
        project_name = input("Introduce el nombre del proyecto: ")

        create = DjangoFuncionApp(project_root=project_root, project_name=project_name)

        asyncio.run(create.create_apps())

        #asyncio.run(create.installed_apps())

        #create.installed_url_in_project()

        #create.install_url_and_views_perfil()

        #create.install_templates_and_static_files()        

        #create.create_carpet_services_and_files()

        #create.carpet_utils_and_files()

        #create.create_carpet_test_and_files()

