from flask import Blueprint, render_template
from .models import Categoria

# Crear el Blueprint
main_routes = Blueprint('main_routes', __name__)

# Ruta para la página de inicio (Landing page)
@main_routes.route('/')
def index():
    # Obtener todos los registros de Categoria
    categorias = Categoria.query.all()

    return render_template('index.html', categorias=categorias)
    #return "Hello work ktm"