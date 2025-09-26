from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Categoria, Tienda, Producto, Cliente, Venta, StockTienda
from app import db, bcrypt
from flask_login import login_user, login_required, logout_user, current_user

# Crear el Blueprint
main_routes = Blueprint('main_routes', __name__)

#Ruta para la página de inicio (Landing page)
@main_routes.route('/')
def index():
    return render_template('index.html')

#Ruta para la página de productos
@main_routes.route('/productos')
def productos():
    productos = Producto.query.all()
    cliente_id = current_user.get_id()
    return render_template('productos.html', productos=productos, cliente_id=cliente_id)

#Ruta para ver un producto específico
@main_routes.route('/producto/<int:id>')
def producto(id):
    producto = Producto.query.get_or_404(id)  # Obtener un producto por ID
    return render_template('producto.html', producto=producto)

#Ruta para el registro de usuarios
@main_routes.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        contraseña = request.form['contraseña']

        # Verificar si el correo ya está registrado
        if Cliente.query.filter_by(Correo=correo).first():
            flash('El correo ya está registrado.', 'danger')
            return redirect(url_for('main_routes.registro'))

        # Hashear la contraseña
        hashed_password = bcrypt.generate_password_hash(contraseña).decode('utf-8')

        # Crear un nuevo cliente
        nuevo_cliente = Cliente(
            Nombre_Cliente=nombre,
            Correo=correo,
            Telefono=telefono,
            Direccion=direccion,
            Contraseña=hashed_password
        )

        db.session.add(nuevo_cliente)
        db.session.commit()

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('main_routes.login'))

    return render_template('registro.html')

# Ruta para el login de usuarios
@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        cliente = Cliente.query.filter_by(Correo=correo).first()

        if cliente and bcrypt.check_password_hash(cliente.Contraseña, contraseña):
            login_user(cliente)
            flash('Inició sesión correctamente.', 'success')
            return redirect(url_for('main_routes.productos'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')
            return redirect(url_for('main_routes.login'))

    return render_template('login.html')

# Ruta para la compra de un producto
@main_routes.route('/comprar/<int:id>', methods=['POST'])
def comprar(id):
    producto = Producto.query.get_or_404(id)
    cliente_id = current_user.get_id()
    #flash('Compra realizada con éxito.', 'success')
    #return redirect(url_for('main_routes.productos'))
    return render_template('compra.html', producto=producto, cliente_id=cliente_id)

@main_routes.route('/logout')
def logout():
    logout_user()  # Cierra la sesión del usuario
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('main_routes.index'))