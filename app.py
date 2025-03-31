from flask import Flask, request, make_response, render_template, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# Duración de las cookies (30 días)
DURACION_COOKIE = 30

def actualizar_enlaces_visitados(nuevo_enlace):
    """Recupera la cookie 'visited' y añade nuevo_enlace si aún no está registrada."""
    visitados = request.cookies.get('visited', '').split(',')
    if visitados == ['']:
        visitados = []
    if nuevo_enlace not in visitados:
        visitados.append(nuevo_enlace)
    return visitados

@app.route('/', methods=['GET', 'POST'])
def inicio():
    # Inicialmente, las preferencias quedan en None si no existen
    tipo_fuente = None
    color = None
    # Recuperar enlaces visitados; si no hay, la lista queda vacía
    enlaces_visitados = request.cookies.get('visited', '')
    enlaces_visitados = [] if not enlaces_visitados else enlaces_visitados.split(',')

    if request.method == 'POST':
        # Obtener las preferencias del formulario
        tipo_fuente = request.form.get('tipo_texto')
        color = request.form.get('color')
        respuesta = make_response(redirect(url_for('inicio')))
        fecha_expiracion = datetime.now() + timedelta(days=DURACION_COOKIE)
        # Se establecen las cookies de forma individual desde el servidor
        respuesta.set_cookie('tipo_texto', tipo_fuente, expires=fecha_expiracion)
        respuesta.set_cookie('color', color, expires=fecha_expiracion)
        # Se reenvía la cookie 'visited' para conservar los enlaces previos
        respuesta.set_cookie('visited', ','.join(enlaces_visitados))
        return respuesta
    else:
        # En GET, se recuperan las preferencias individuales si existen
        tipo_fuente = request.cookies.get('tipo_texto')
        color = request.cookies.get('color')

    return render_template('index.html',
                           font_family=tipo_fuente,
                           color=color,
                           visited_links=enlaces_visitados)

# Esta ruta representa la solución con cookies gestionadas por el servidor.
# Puedes compararla con la solución JavaScript.
@app.route('/visit/<path:enlace>')
def visitar(enlace):
    # Actualizar la cookie 'visited' añadiendo el enlace visitado
    visitados = actualizar_enlaces_visitados(enlace)
    fecha_expiracion = datetime.now() + timedelta(days=DURACION_COOKIE)
    
    # Si el enlace no comienza con "http://" o "https://", se antepone "http://"
    if not (enlace.startswith("http://") or enlace.startswith("https://")):
        url_destino = "http://" + enlace
    else:
        url_destino = enlace

    respuesta = make_response(redirect(url_destino))
    respuesta.set_cookie('visited', ','.join(visitados))
    return respuesta

if __name__ == '__main__':
    app.run(debug=True)


