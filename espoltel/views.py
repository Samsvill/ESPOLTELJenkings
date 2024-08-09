import os

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
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

#enlistar todas las rutas de la api en la vista home
def home(request):
    response = HttpResponse()
    response.write("<h1>API de Espoltel</h1>")
    response.write("<h2>Endpoints:</h2>")
    response.write("<ul>")
    response.write("<br><b>General:</b>")
    response.write("<li><a href='/admin/'>/admin/</a> - Administración de la base de datos</li>")
    response.write("<li><a href='/api/token/'>/api/token/</a> - Obtener token de autenticación</li>")
    response.write("<li><a href='/api/token/refresh/'>/api/token/refresh/</a> - Refrescar token de autenticación</li>")
    response.write("<br><b>Usuarios:</b>")
    response.write("<li><a href='/user/registro/'>/user/registro/</a> - Registro de usuario</li>")
    response.write("<li><a href='/user/rol/'>/user/rol/</a> - Asignar rol a usuario</li>")
    response.write("<li><a href='/user/perfil/'>/user/perfil/</a> - Perfil del usuario autenticado</li>")
    response.write("<li><a href='/user/perfil/1/'>/user/perfil/1/</a> - Perfil del usuario con ID 1</li>")
    response.write("<br><b>Proyectos:</b>")
    response.write("<li><a href='/api/proyectos/'>/api/proyectos/</a> - Listado de todos los proyectos</li>")
    response.write("<li><a href='/api/proyectos/1/'>/api/proyectos/1/</a> - Detalle del proyecto con ID 1</li>")
    response.write("<li><a href='/api/proyectos/1/items/'>/api/proyectos/1/items/</a> - Crear un item de presupuesto para el proyecto con ID 1</li>")
    response.write("<br><b>Solicitudes:</b>")
    response.write("<li><a href='/api/solicitudes/all/'>/api/solicitudes/all/</a> - Listado de todas las solicitudes</li>")
    response.write("<li><a href='/api/solicitudes/1/'>/api/solicitudes/1/</a> - Detalle de la solicitud con ID 1</li>")
    response.write("<li><a href='/api/solicitudes/'>/api/solicitudes/</a> - Listado de solicitudes del usuario autenticado</li>")
    response.write("<li><a href='/api/solicitudes/1/cotizaciones/'>/api/solicitudes/1/cotizaciones/</a> - Listado de cotizaciones de la solicitud con ID 1</li>")
    response.write("<br><b>Operaciones:</b>")
    response.write("<li><a href='/api/proyectos/1/solicitud/'>/api/proyectos/1/solicitud/</a> - Crear una solicitud para el proyecto con ID 1</li>")
    response.write("<li><a href='/api/proyecto/1/solicitud/1/estado/'>/api/proyecto/1/solicitud/1/estado/</a> - Listado de estados de la solicitud con ID 1 del proyecto con ID 1</li>")
    response.write("<li><a href='/api/proyecto/1/solicitud/1/estado/1/'>/api/proyecto/1/solicitud/1/estado/1/</a> - Actualizar el estado con ID 1 de la solicitud con ID 1 del proyecto con ID 1</li>")
    response.write("<li><a href='/api/formulario/1/'>/api/formulario/1/</a> - Crear un formulario para la solicitud con ID 1</li>")
    response.write("<li><a href='/api/solicitud/1/factura/'>/api/solicitud/1/factura/</a> - Crear un detalle de factura para la solicitud con ID 1</li>")
    response.write("<li><a href='/api/solicitudes/1/items/'>/api/solicitudes/1/items/</a> - Listado de items de la solicitud con ID 1</li>")
    response.write("</ul>")
    response.write('''
    response.write("<table>")
    response.write("<tr><th>Endpoint</th><th>Descripción</th></tr>")
    response.write("<tr><td>/admin/</td><td>Administración de la base de datos</td></tr>")
    response.write("<tr><td>/api/token/</td><td>Obtener token de autenticación</td></tr>")
    response.write("<tr><td>/api/token/refresh/</td><td>Refrescar token de autenticación</td></tr>")
    response.write("<tr><td>/user/registro/</td><td>Registro de usuario</td></tr>")
    response.write("<tr><td>/user/rol/</td><td>Asignar rol a usuario</td></tr>")
    response.write("<tr><td>/user/perfil/</td><td>Perfil del usuario autenticado</td></tr>")
    response.write("<tr><td>/user/perfil/1/</td><td>Perfil del usuario con ID 1</td></tr>")
    response.write("<tr><td>/api/proyectos/</td><td>Listado de todos los proyectos</td></tr>")
    response.write("<tr><td>/api/proyectos/1/</td><td>Detalle del proyecto con ID 1</td></tr>")
    response.write("<tr><td>/api/proyectos/1/items/</td><td>Crear un item de presupuesto para el proyecto con ID 1</td></tr>")
    response.write("<tr><td>/api/solicitudes/all/</td><td>Listado de todas las solicitudes</td></tr>")
    response.write("<tr><td>/api/solicitudes/1/</td><td>Detalle de la solicitud con ID 1</td></tr>")
    response.write("<tr><td>/api/solicitudes/</td><td>Listado de solicitudes del usuario autenticado</td></tr>")
    response.write("<tr><td>/api/solicitudes/1/cotizaciones/</td><td>Listado de cotizaciones de la solicitud con ID 1</td></tr>")
    response.write("<tr><td>/api/proyectos/1/solicitud/</td><td>Crear una solicitud para el proyecto con ID 1</td></tr>")
    response.write("<tr><td>/api/proyecto/1/solicitud/1/estado/</td><td>Listado de estados de la solicitud con ID 1 del proyecto con ID 1</td></tr>")
    response.write("<tr><td>/api/proyecto/1/solicitud/1/estado/1/</td><td>Actualizar el estado con ID 1 de la solicitud con ID 1 del proyecto con ID 1</td></tr>")
    response.write("<tr><td>/api/formulario/1/</td><td>Crear un formulario para la solicitud con ID 1</td></tr>")
    response.write("<tr><td>/api/solicitud/1/factura/</td><td>Crear un detalle de factura para la solicitud con ID 1</td></tr>")
    response.write("<tr><td>/api/solicitudes/1/items/</td><td>Listado de items de la solicitud con ID 1</td></tr>")
    response.write("</table>")
''')
    return response