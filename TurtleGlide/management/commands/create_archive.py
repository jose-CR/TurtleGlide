import os
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

class Command(BaseCommand):
    help = 'Crea archivos dentro de la carpeta templates o static de una app'
    
    FILE_TEMPLATES = {
        '.html': '<div>Este es el contenido del componente.</div>',
        '.js': 'console.log("Este es el contenido del componente.");',
        '.css': '/* Este es el contenido del componente */'
    }
    
    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='Nombre de la app')
        parser.add_argument('file_path', type=str, help='Ruta del componente (con extensión)')
        parser.add_argument(
            '--type', 
            type=str, 
            choices=['template', 'static'], 
            default='template', 
            help='Tipo de archivo a crear: "template" para archivos en templates, "static" para archivos en static'
        )
        
    def handle(self, *args, **kwargs):
        app_name = kwargs['app_name']
        file_path = kwargs['file_path']
        file_type = kwargs['type']
        
        try:
            app_config = apps.get_app_config(app_name)
        except LookupError:
            raise CommandError(f'App "{app_name}" no encontrada.')
        
        base_dir = os.path.join(app_config.path, 'templates' if file_type == 'template' else 'static')
        file_full_path = os.path.normpath(os.path.join(base_dir, file_path))
        
        try:
            os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
            self.stdout.write(self.style.SUCCESS(f'Directorio {os.path.dirname(file_full_path)} verificado/creado.'))
        except PermissionError:
            raise CommandError(f'No se pudo crear el directorio {os.path.dirname(file_full_path)}. Verifica permisos.')
        
        if os.path.exists(file_full_path):
            self.stdout.write(self.style.WARNING(f'El archivo "{file_path}" ya existe en {app_name}/{file_type}/.'))
        else:
            content = self.FILE_TEMPLATES.get(os.path.splitext(file_path)[1], '')
        
        try:
            with open(file_full_path, 'w') as f:
                f.write(content)
            self.stdout.write(self.style.SUCCESS(f'Archivo "{file_path}" creado en {app_name}/{file_type}/.'))
        except PermissionError:
            raise CommandError(f'No se pudo escribir en "{file_full_path}". Verifica permisos.')
