from flask import Blueprint, render_template

# Crear el Blueprint
main_routes = Blueprint('main_routes', __name__)

# Ruta para la página de inicio (Landing page)
@main_routes.route('/')
def index():
    return render_template('index.html')
    #return "Hello work ktm"