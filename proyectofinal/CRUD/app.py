import mysql.connector
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Delfines/2'
app.config['MYSQL_DATABASE_DB'] = 'tienda_vicky_gurumis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Delfines/2@localhost/tienda_vicky_gurumis'

db = SQLAlchemy(app)
ma = Marshmallow(app)

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
    codigo = db.Column(db.varchar(10), nullable=False)
    nombre = db.Column(db.varchar(200), nullable=False)
    descripcion = db.Column(db.varchar(500))
    precio = db.Column(db.double)
    stock = db.Column(db.varchar(20))
    imagen = db.Column(db.String(255))

    def __init__(self, idproducto, codigo, nombre, descripcion, precio, stock, imagen):
        self.idproducto = idproducto
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen


class Patron(db.Model):
    __tablename__ = 'patron'
    idpatron = db.Column(db.Integer, primary_key=True)
    idproducto = db.Column(db.Integer, db.ForeignKey('producto.idproducto'))
    codigo = db.Column(db.varchar(10), nullable=False)
    nombre = db.Column(db.varchar(20), nullable=False)
    descripcion = db.Column(db.varchar(200))
    precio = db.Column(db.Float)
    stock = db.Column(db.Integer)
    imagen = db.Column(db.String(255))

    def __init__(self, idproducto, codigo, nombre, descripcion, precio, stock, imagen):
        self.idproducto = idproducto
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen


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

# Rutas

#**************productos*********************

@app.route("/producto", methods=["POST"])
def create_producto():
    tipo = request.json["tipo"]

    new_producto = Producto(tipo)

    db.session.add(new_producto)
    db.session.commit()

    return producto_schema.jsonify(new_producto)


@app.route('/producto', methods=['GET'])
def get_producto():
    all_productos = Producto.query.all()
    result = productos_schema.dump(all_productos)
    return jsonify(result)

@app.route("/producto/<id>", methods=["PUT"])
def update_producto(id):
    producto = Producto.query.get(id)
    if producto:
        producto.tipo = request.json["tipo"]
        db.session.commit()
        return jsonify({"message": "Producto actualizado correctamente"})
    else:
        return jsonify({"message": "Producto no encontrado"}), 404


@app.route("/producto/<id>", methods=["DELETE"])
def delete_producto(id):
    producto = Producto.query.get(id)

    if producto:
        db.session.delete(producto)
        db.session.commit()
        return jsonify({"message": "Producto eliminado correctamente"})
    else:
        return jsonify({"message": "Producto no encontrado"}), 404


#**************Amigurumis********************

@app.route("/amigurumi", methods=["POST"])
def create_amigurumi():
    idproducto = request.json["idproducto"]
    codigo = request.json["codigo"]
    nombre = request.json["nombre"]
    descripcion = request.json["descripcion"]
    precio = request.json["precio"]
    stock = request.json["stock"]
    imagen = request.json["imagen"]
    new_amigurumi = Amigurumi(idproducto, codigo, nombre, descripcion, precio, stock, imagen)

    db.session.add(new_amigurumi)
    db.session.commit()

    return amigurumi_schema.jsonify(new_amigurumi)

@app.route('/amigurumi', methods=['GET'])
def get_amigurumi():
    all_amigurumi = Amigurumi.query.all()
    result = amigurumis_schema.dump(all_amigurumi)
    return jsonify(result)


@app.route("/amigurumi/<id>", methods=["PUT"])
def update_amigurumi(id):
    amigurumi = Amigurumi.query.get(id)
    if amigurumi:
        amigurumi.idproducto = request.json["idproducto"]
        amigurumi.codigo = request.json["codigo"]
        amigurumi.nombre = request.json["nombre"]
        amigurumi.descripcion = request.json["descripcion"]
        amigurumi.precio = request.json["precio"]
        amigurumi.stock = request.json["stock"]
        amigurumi.imagen = request.json["imagen"]

        db.session.commit()
        return jsonify({"message": "Amigurumi actualizado correctamente"})
    else:
        return jsonify({"message": "Amigurumi no encontrado"}), 404


@app.route("/amigurumi/<id>", methods=["DELETE"])
def delete_amigurumi(id):
    amigurumi = Amigurumi.query.get(id)

    if amigurumi:
        db.session.delete(amigurumi)
        db.session.commit()
        return jsonify({"message": "Amigurumi eliminado correctamente"})
    else:
        return jsonify({"message": "Amigurumi no encontrado"}), 404
#**************Patrones********************

@app.route("/patron", methods=["POST"])
def create_patron():
    tipo = request.json["tipo"]
    new_patron = Patron(tipo)

    db.session.add(new_patron)
    db.session.commit()

    return patron_schema.jsonify(new_patron)

@app.route('/patron', methods=['GET'])
def get_patron():
    all_patrones = Patron.query.all()
    result = patrones_schema.dump(all_patrones)
    return jsonify(result)

@app.route("/patron/<id>", methods=["PUT"])
def update_patron(id):
    patron = Patron.query.get(id)
    if patron:
        patron.tipo = request.json["tipo"]
        db.session.commit()
        return jsonify({"message": "Patrón actualizado correctamente"})
    else:
        return jsonify({"message": "Patrón no encontrado"}), 404

@app.route("/patron/<id>", methods=["DELETE"])
def delete_patron(id):
    patron = Patron.query.get(id)

    if patron:
        db.session.delete(patron)
        db.session.commit()
        return jsonify({"message": "Patrón eliminado correctamente"})
    else:
        return jsonify({"message": "Patrón no encontrado"}), 404

#**************Pedidos********************

@app.route("/pedido", methods=["POST"])
def create_pedido():
    tipo = request.json["tipo"]
    new_pedido = Pedido(tipo)

    db.session.add(new_pedido)
    db.session.commit()

@app.route('/pedido', methods=['GET'])
def get_pedido():
    all_pedidos = Pedido.query.all()
    result = pedidos_schema.dump(all_pedidos)
    return jsonify(result)

@app.route("/pedido/<id>", methods=["DELETE"])
def delete_pedido(id):
    pedido = Pedido.query.get(id)

    if pedido:
        db.session.delete(pedido)
        db.session.commit()
        return jsonify({"message": "Pedido eliminado correctamente"})
    else:
        return jsonify({"message": "Pedido no encontrado"}), 404

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
        db.create_all()

    app.run(debug=True)