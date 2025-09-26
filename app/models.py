from app import db  # Importa la instancia de db desde el archivo __init__.py

# Modelo de Categorías
class Categoria(db.Model):
    __tablename__ = 'Categorias'  # Nombre de la tabla en la base de datos
    ID_Categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre_Categoria = db.Column(db.String(255), nullable=False)
    Descripcion = db.Column(db.Text)

    # Relación con Productos
    productos = db.relationship('Producto', backref='categoria', lazy=True)

# Modelo de Tiendas
class Tienda(db.Model):
    __tablename__ = 'Tiendas'
    ID_Tienda = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre_Tienda = db.Column(db.String(255), nullable=False)
    Ubicacion = db.Column(db.String(255))

    # Relación con Ventas y Stock_Tienda
    ventas = db.relationship('Venta', backref='tienda', lazy=True)
    stock_tienda = db.relationship('StockTienda', backref='tienda', lazy=True)

# Modelo de Productos
class Producto(db.Model):
    __tablename__ = 'Productos'
    ID_Producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(255), nullable=False)
    Descripcion = db.Column(db.Text)
    Precio = db.Column(db.Numeric(10, 2))
    Stock_Total = db.Column(db.Integer)
    Stock_Web = db.Column(db.Integer)
    Categoria_ID = db.Column(db.Integer, db.ForeignKey('Categorias.ID_Categoria'), nullable=False)

    # Relación con Ventas y Stock_Tienda
    ventas = db.relationship('Venta', backref='producto', lazy=True)
    stock_tienda = db.relationship('StockTienda', backref='producto', lazy=True)

# Modelo de Clientes
class Cliente(db.Model):
    __tablename__ = 'Clientes'
    ID_Cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre_Cliente = db.Column(db.String(255), nullable=False)
    Correo = db.Column(db.String(255), unique=True)
    Telefono = db.Column(db.String(20))
    Direccion = db.Column(db.String(255))
    Contraseña = db.Column(db.String(255), nullable=False)

    # Relación con Ventas
    ventas = db.relationship('Venta', backref='cliente', lazy=True)

# Modelo de Ventas
class Venta(db.Model):
    __tablename__ = 'Ventas'
    ID_Venta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Fecha = db.Column(db.DateTime, nullable=False)
    ID_Producto = db.Column(db.Integer, db.ForeignKey('Productos.ID_Producto'), nullable=False)
    Cantidad = db.Column(db.Integer, nullable=False)
    Precio_Total = db.Column(db.Numeric(10, 2), nullable=False)
    ID_Tienda = db.Column(db.Integer, db.ForeignKey('Tiendas.ID_Tienda'), nullable=False)
    ID_Cliente = db.Column(db.Integer, db.ForeignKey('Clientes.ID_Cliente'), nullable=False)

# Modelo de Stock_Tienda
class StockTienda(db.Model):
    __tablename__ = 'Stock_Tienda'
    ID_Stock = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Tienda = db.Column(db.Integer, db.ForeignKey('Tiendas.ID_Tienda'), nullable=False)
    ID_Producto = db.Column(db.Integer, db.ForeignKey('Productos.ID_Producto'), nullable=False)
    Cantidad = db.Column(db.Integer, nullable=False)
