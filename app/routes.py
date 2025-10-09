from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Categoria, Tienda, Producto, Cliente, Venta, StockTienda
from app import db, bcrypt
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

# Crear el Blueprint
main_routes = Blueprint('main_routes', __name__)

#Ruta para la página de inicio (Landing page)
@main_routes.route('/')
def index():
    productos = Producto.query.all()
    categorias = Categoria.query.all()   
    cliente_id = current_user.get_id()
    return render_template(
        "index.html",
        productos=productos,
        categorias=categorias, 
        cliente_id=cliente_id
    )

#Ruta para la página de productos
@main_routes.route('/productos')
def productos():
    productos = Producto.query.all()
    cliente_id = current_user.get_id()
    return render_template('productos.html', productos=productos, cliente_id=cliente_id)

#Ruta para ver un producto específico
@main_routes.route('/producto/<int:id>')
def producto(id):
    producto = Producto.query.get_or_404(id)  

    return render_template(
        'producto.html', 
        producto=producto, 
        logged_in=current_user.is_authenticated,
        current_user=current_user 
    )

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
    next_page = request.args.get('next')

    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        cliente = Cliente.query.filter_by(Correo=correo).first()

        if cliente and bcrypt.check_password_hash(cliente.Contraseña, contraseña):
            login_user(cliente)
            flash('Inició sesión correctamente.', 'success')
            
            return redirect(next_page or url_for('main_routes.index'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')
            return redirect(url_for('main_routes.login', next=next_page))
            

    return render_template('login.html')


@main_routes.route('/comprar/<int:id>', methods=['POST'])
def comprar(id):
    producto = Producto.query.get_or_404(id)
    
    cantidad_str = request.form.get('quantity') 
    try:
        cantidad = int(cantidad_str)
    except (ValueError, TypeError):
        cantidad = 1

    return render_template('compra.html', producto=producto, cantidad=cantidad)

@main_routes.route('/comprar_redirect/<int:id>', methods=['GET'])
def comprar_redirect(id):
    if not current_user.is_authenticated:
        return redirect(url_for('main_routes.login')) 
    
    producto = Producto.query.get_or_404(id)
    cantidad_str = request.args.get('quantity', '1') 
    
    try:
        cantidad = int(cantidad_str)
    except (ValueError, TypeError):
        cantidad = 1
        
    return render_template('compra.html', producto=producto, cantidad=cantidad)

@main_routes.route('/checkout', methods=['POST'])
@login_required 
def checkout():

    producto_id_str = request.form.get('producto_id')
    cantidad_str = request.form.get('cantidad')

    try:
        producto_id = int(producto_id_str)
        cantidad = int(cantidad_str)
    except (ValueError, TypeError):
        flash('Error al procesar la compra. Producto o cantidad inválida.', 'danger')
        return redirect(url_for('main_routes.index')) 
    
    
    producto = Producto.query.get_or_404(producto_id)

    cliente_id = current_user.ID_Cliente 

    if cantidad > producto.Stock_Web:
        flash(f'Error: Solo hay {producto.Stock_Web} unidades de {producto.Nombre} disponibles en stock web.', 'danger')

        return redirect(url_for('main_routes.comprar_redirect_carrito', id=producto_id, quantity=cantidad))

    try:
        precio_total = producto.Precio * cantidad
        
        nueva_venta = Venta(
            Fecha=datetime.now(),
            ID_Producto=producto_id,
            Cantidad=cantidad,
            Precio_Total=precio_total,
            ID_Tienda=4, 
            ID_Cliente=cliente_id
        )
        
        try:
            db.session.add(nueva_venta)
            db.session.commit()
            flash('¡Compra realizada con éxito!', 'success')
            return render_template('pago.html', 
                                producto_id=producto_id, 
                                cantidad=cantidad, 
                                venta_id=nueva_venta.ID_Venta, 
                                total=precio_total)
        except Exception as e:
            db.session.rollback()
            print("Error al finalizar la compra:", e) 
            flash('Ocurrió un error al procesar tu compra. Intenta nuevamente.', 'danger')
            return redirect(url_for('main_routes.comprar_redirect_carrito', id=producto_id, quantity=cantidad))


    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error al finalizar la compra: {str(e)}', 'danger')
        return redirect(url_for('main_routes.comprar_redirect_carrito', id=producto_id, quantity=cantidad))



@main_routes.route('/comprar_redirect_carrito/<int:id>', methods=['GET'])
def comprar_redirect_carrito(id):

    if not current_user.is_authenticated:
        return redirect(url_for('main_routes.login')) 
    
    producto = Producto.query.get_or_404(id)
    cantidad_str = request.args.get('quantity', '1') 
    
    try:
        cantidad = int(cantidad_str)
    except (ValueError, TypeError):
        cantidad = 1
        

    flash('Ahora puedes completar tu compra.', 'success')
    return render_template('compra.html', producto=producto, cantidad=cantidad)

@main_routes.route('/logout')
def logout():
    logout_user() 
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('main_routes.index'))

