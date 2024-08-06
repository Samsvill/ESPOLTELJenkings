import os
from flask import Flask, render_template, request
from django.conf import settings
from django.http import FileResponse, Http404
from urllib.parse import unquote
from django.views.decorators.csrf import csrf_exempt


def download_file(request, path):
    # Descodificar cualquier carácter URL-encoded
    file_path = os.path.join(settings.MEDIA_ROOT, unquote(path))
    
    # Verificar si el archivo existe
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    else:
        raise Http404("File does not exist")