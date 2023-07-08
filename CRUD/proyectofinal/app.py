import mysql.connector
from conexion import DatabaseConnection

from flask import Flask
from flask import jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Delfines/2*@localhost/tienda_vicky_gurumis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Producto(db.Model):
    __tablename__ = 'producto'
    idproducto = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20))

    def __init__(self, tipo):
        self.tipo = tipo
        
class Amigurumi(db.Model):
    __tablename__ = 'amigurumi'
    idamigurumi = db.Column(db.Integer, primary_key=True)
    idproducto = db.Column(db.Integer, db.ForeignKey('producto.idproducto'))
    codigo = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.String(100))
    precio = db.Column(db.Float)
    stock = db.Column(db.Integer)  

    def __init__(self, idproducto, codigo, nombre, descripcion, precio, stock, imagen):
        self.idproducto = idproducto
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock

 
class Patron(db.Model):
    __tablename__ = 'patron'
    idpatron = db.Column(db.Integer, primary_key=True)
    idproducto = db.Column(db.Integer, db.ForeignKey('producto.idproducto'))
    codigo = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.String(100))
    precio = db.Column(db.Float)
    stock = db.Column(db.Integer)  # Corregido el tipo de dato

    def __init__(self, idproducto, codigo, nombre, descripcion, precio, stock, imagen):
        self.idproducto = idproducto
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        
        
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

class AmigurumiSchema(ma.Schema):
    class Meta:
        model = Amigurumi

class ClienteSchema(ma.Schema):
    class Meta:
        model = Cliente

class FacturaSchema(ma.Schema):
    class Meta:
        model = Factura

class PatronSchema(ma.Schema):
    class Meta:
        model = Patron

class PedidoSchema(ma.Schema):
    class Meta:
        model = Pedido

class ProductoSchema(ma.Schema):
    class Meta:
        model = Producto

amigurumi_schema = AmigurumiSchema()
cliente_schema = ClienteSchema()
factura_schema = FacturaSchema()
patron_schema = PatronSchema()
pedido_schema = PedidoSchema()
producto_schema = ProductoSchema()

amigurumis_schema = AmigurumiSchema(many=True)
clientes_schema = ClienteSchema(many=True)
facturas_schema = FacturaSchema(many=True)
patrones_schema = PatronSchema(many=True)
pedidos_schema = PedidoSchema(many=True)
productos_schema = ProductoSchema(many=True)

@app.route('/amigurumi', methods=['GET'])
def get_amigurumi():
    all_amigurumi = Amigurumi.query.all()
    result = amigurumis_schema.dump(all_amigurumi)
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

@app.route('/patron', methods=['GET'])
def get_patron():
    all_patrones = Patron.query.all()
    result = patrones_schema.dump(all_patrones)
    return jsonify(result)

@app.route('/pedido', methods=['GET'])
def get_pedido():
    all_pedidos = Pedido.query.all()
    result = pedidos_schema.dump(all_pedidos)
    return jsonify(result)

@app.route('/producto', methods=['GET'])
def get_producto():
    all_productos = Producto.query.all()
    result = productos_schema.dump(all_productos)
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
