import os

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
from urllib.parse import unquote
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


def download_file(request, path):
    # Descodificar cualquier carácter URL-encoded
    file_path = os.path.join(settings.MEDIA_ROOT, unquote(path))
    
    # Verificar si el archivo existe
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    else:
        raise Http404("File does not exist")

#enlistar todas las rutas de la api en la vista home
def home(request):
    response = HttpResponse(content_type="text/plain")
    
    urls = [
        ('registro', reverse('registro')),
        ('get_token', reverse('get_token')),
        ('roles', reverse('roles')),
        ('roles-delete', reverse('roles-delete', kwargs={'pk': 1})),  # Example pk
        ('proyecto-list-create', reverse('proyecto-list-create')),
        ('proyecto-detail', reverse('proyecto-detail', kwargs={'pk': 1})),  # Example pk
        ('crear-budget-items', reverse('crear-budget-items', kwargs={'proyecto_id': 1})),  # Example proyecto_id
        ('crear-solicitud', reverse('crear-solicitud', kwargs={'pk': 1})),  # Example pk
        ('detalle-solicitud', reverse('detalle-solicitud', kwargs={'pk': 1})),  # Example pk
        ('cotizaciones-solicitud', reverse('cotizaciones-solicitud', kwargs={'pk': 1})),  # Example pk
        ('crear-formulario', reverse('crear-formulario', kwargs={'pk_s': 1})),  # Example pk_s
        ('crear-detalle-factura', reverse('crear-detalle-factura', kwargs={'pk_s': 1})),  # Example pk_s
        ('crear-items-solicitud', reverse('crear-items-solicitud', kwargs={'pk_s': 1})),  # Example pk_s
        ('estado-solicitud', reverse('estado-solicitud', kwargs={'pk_p': 1, 'pk_s': 1, 'pk_e': 1}))  # Example pk_p, pk_s, pk_e
    ]
    
    for name, url in urls:
        response.write(f"Name: {name} -> URL: {url}\n")

    return response