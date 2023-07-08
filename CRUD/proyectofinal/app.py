import mysql.connector
from conexion import DatabaseConnection, app, db, ma, Amigurumi, Patron
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
#En este bloque se importa la clase Flask del módulo flask y las clases Amigurumi y Patron, junto con los esquemas amigurumis_schema y patrones_schema del módulo conexion. Además, se importa la instancia de la aplicación Flask y la base de datos db.
CORS(app)


class Producto(db.Model):
    __tablename__ = 'producto'
    idproducto = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20))

    def __init__(self, tipo):
        self.tipo = tipo
 
# class Amigurumi(db.Model):
#     __tablename__ = 'amigurumi'
#     idamigurumi = db.Column(db.Integer, primary_key=True)
#     idproducto = db.Column(db.Integer, db.ForeignKey('producto.idproducto'))
#     codigo = db.Column(db.Integer, nullable=False)
#     nombre = db.Column(db.String(20), nullable=False)
#     descripcion = db.Column(db.String(100))
#     precio = db.Column(db.Float)
#     stock = db.Column(db.Integer)

#     def __init__(self, idproducto, codigo, nombre, descripcion, precio, stock, imagen):
#         self.idproducto = idproducto
#         self.codigo = codigo
#         self.nombre = nombre
#         self.descripcion = descripcion
#         self.precio = precio
#         self.stock = stock

# class Patron(db.Model):
#     __tablename__ = 'patron'
#     idpatron = db.Column(db.Integer, primary_key=True)
#     idproducto = db.Column(db.Integer, db.ForeignKey('producto.idproducto'))
#     codigo = db.Column(db.Integer, nullable=False)
#     nombre = db.Column(db.String(20), nullable=False)
#     descripcion = db.Column(db.String(100))
#     precio = db.Column(db.Float)
#     stock = db.Column(db.Integer)  # Corregido el tipo de dato

#     def __init__(self, idproducto, codigo, nombre, descripcion, precio, stock, imagen):
#         self.idproducto = idproducto
#         self.codigo = codigo
#         self.nombre = nombre
#         self.descripcion = descripcion
#         self.precio = precio
#         self.stock = stock

class Pedido(db.Model):
    __tablename__ = 'pedido'
    idpedido = db.Column(db.Integer, primary_key=True)
    idcliente = db.Column(db.Integer, db.ForeignKey('cliente.idcliente'))
    fecha = db.Column(db.Date)
    idproducto = db.Column(db.Integer, db.ForeignKey('producto.idproducto'))
    cantidad_solicitada = db.Column(db.Integer)
    precio = db.Column(db.Float)
    fecha_pedido = db.Column(db.Date)
    estado_pedido = db.Column(db.String(20))

    def __init__(self, idcliente, fecha, idproducto, cantidad_solicitada, precio, fecha_pedido, estado_pedido):
        self.idcliente = idcliente
        self.fecha = fecha
        self.idproducto = idproducto
        self.cantidad_solicitada = cantidad_solicitada
        self.precio = precio
        self.fecha_pedido = fecha_pedido
        self.estado_pedido = estado_pedido

class Cliente(db.Model):
    __tablename__ = 'cliente'
    idcliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    apellido = db.Column(db.String(20), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    cel = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __init__(self, nombre, apellido, edad, cel, direccion, email, password):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.cel = cel
        self.direccion = direccion
        self.email = email
        self.password = password

class Factura(db.Model):
    __tablename__ = 'factura'
    idfactura = db.Column(db.Integer, primary_key=True)
    idcliente = db.Column(db.Integer, db.ForeignKey('cliente.idcliente'))
    fecha_emision = db.Column(db.Date)

    def __init__(self, idcliente, fecha_emision):
        self.idcliente = idcliente
        self.fecha_emision = fecha_emision


class ProductoSchema(ma.Schema):
    class Meta:
        model = Producto


class AmigurumiSchema(ma.Schema):
    class Meta:
        model = Amigurumi
        fields = ('idamigurumi', 'idproducto', 'codigo', 'nombre', 'descripcion', 'precio', 'stock', 'imagen')

class PatronSchema(ma.Schema):
    class Meta:
        model = Patron
        fields = ('idpatron', 'idproducto', 'codigo', 'nombre', 'descripcion', 'precio', 'stock', 'imagen')

class PedidoSchema(ma.Schema):
    class Meta:
        model = Pedido

class ClienteSchema(ma.Schema):
    class Meta:
        model = Cliente

class FacturaSchema(ma.Schema):
    class Meta:
        model = Factura

producto_schema = ProductoSchema()
amigurumi_schema = AmigurumiSchema()
patron_schema = PatronSchema()
pedido_schema = PedidoSchema()
cliente_schema = ClienteSchema()
factura_schema = FacturaSchema()

productos_schema = ProductoSchema(many=True)
amigurumis_schema = AmigurumiSchema(many=True)
patrones_schema = PatronSchema(many=True)
pedidos_schema = PedidoSchema(many=True)
clientes_schema = ClienteSchema(many=True)
facturas_schema = FacturaSchema(many=True)


@app.route('/producto', methods=['GET'])
def get_producto():
    all_productos = Producto.query.all()
    result = productos_schema.dump(all_productos)
    return jsonify(result)

@app.route('/amigurumi', methods=['GET'])
def get_amigurumi():
    all_amigurumi = Amigurumi.query.all()
    result = amigurumis_schema.dump(all_amigurumi)
    return jsonify(result)
# Esta función decorada con @app.route('/amigurumi', methods=['GET']) define una ruta '/amigurumi' con el método GET. Cuando se accede a esta ruta, se ejecuta la función get_amigurumi(). Dentro de esta función, se realiza una consulta a la base de datos para obtener todos los objetos Amigurumi y luego se utiliza el esquema amigurumis_schema para serializar los resultados en formato JSON.

@app.route('/patron', methods=['GET'])
def get_patron():
    all_patrones = Patron.query.all()
    result = patrones_schema.dump(all_patrones)
    return jsonify(result)
# Esta función decorada con @app.route('/patron', methods=['GET']) define una ruta '/patron' con el método GET. Cuando se accede a esta ruta, se ejecuta la función get_patron(). Dentro de esta función, se realiza una consulta a la base de datos para obtener todos los objetos Patron y luego se utiliza el esquema patrones_schema para serializar los resultados en formato JSON.

@app.route('/pedido', methods=['GET'])
def get_pedido():
    all_pedidos = Pedido.query.all()
    result = pedidos_schema.dump(all_pedidos)
    return jsonify(result)

@app.route('/cliente', methods=['GET'])
def get_cliente():
    all_clientes = Cliente.query.all()
    result = clientes_schema.dump(all_clientes)
    return jsonify(result)

@app.route('/factura', methods=['GET'])
def get_factura():
    all_facturas = Factura.query.all()
    result = facturas_schema.dump(all_facturas)
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        #  colocar código que interactúa con la base de datos u otras funcionalidades de Flask

        # Ejemplo 1: Consulta a la base de datos
        all_productos = Producto.query.all()
        # Realiza operaciones con los datos obtenidos de la base de datos

        # Ejemplo 2: Iniciar el servidor Flask
        app.run(debug=True)


    
#Esta parte del código asegura que el servidor Flask se ejecute solo cuando el script se ejecuta directamente (no cuando se importa como un módulo). Dentro de if __name__ == '__main__':, se crea la estructura de la base de datos utilizando db.create_all() y luego se inicia la aplicación Flask utilizando app.run(debug=True).