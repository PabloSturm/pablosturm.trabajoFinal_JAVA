from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '***',
    'database': 'tienda_vicky_gurumis'
}
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '***'
app.config['MYSQL_DATABASE_DB'] = 'tienda_vicky_gurumis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:***@localhost/tienda_vicky_gurumis'

db = SQLAlchemy(app)
db.init_app(app)
ma = Marshmallow(app)
#**********************************************************************

# Modelos

class Amigurumi(db.Model):
    __tablename__ = 'amigurumi'
    idamigurumi = db.Column(db.Integer, primary_key=True)
    idproducto = db.Column(db.Integer, nullable=False)
    codigo = db.Column(db.String(10), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(500))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.String(20))
    imagen = db.Column(db.String(255))

    def __init__(self, idproducto, codigo, nombre, descripcion, precio, stock, imagen):
        self.idproducto = idproducto
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen

class Cliente(db.Model):
    __tablename__ = 'cliente'
    idcliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    apellido = db.Column(db.String(20), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    cel = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), nullable=False)

    def __init__(self, nombre, apellido, edad, cel, direccion, email):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.cel = cel
        self.direccion = direccion
        self.email = email


class Factura(db.Model):
    __tablename__ = 'factura'
    idfactura = db.Column(db.Integer, primary_key=True)
    idcliente = db.Column(db.Integer, nullable=False)
    fecha_emision = db.Column(db.Date)

    def __init__(self, idcliente, fecha_emision):
        self.idcliente = idcliente
        self.fecha_emision = fecha_emision


class Pedido(db.Model):
    __tablename__ = 'pedido'
    idpedido = db.Column(db.Integer, primary_key=True)
    idcliente = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date)
    idproducto = db.Column(db.Integer)
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

with app.app_context():
    db.create_all()

#  ************************************************************

class AmigurumiSchema(ma.Schema):
    class Meta:
        model = Amigurumi
        fields = ('idamigurumi', 'idproducto', 'codigo', 'nombre', 'descripcion', 'precio', 'stock', 'imagen')

class ClienteSchema(ma.Schema):
    class Meta:
        model = Cliente


class FacturaSchema(ma.Schema):
    class Meta:
        model = Factura


class PedidoSchema(ma.Schema):
    class Meta:
        model = Pedido
        fields = ('idpedido', 'idcliente', 'fecha', 'idproducto', 'cantidad_solicitada', 'precio', 'fecha_pedido', 'estado_pedido')



# Inicializar esquemas
amigurumi_schema = AmigurumiSchema()
amigurumis_schema = AmigurumiSchema(many=True)
pedido_schema = PedidoSchema()
pedidos_schema = PedidoSchema(many=True)


# Rutas

@app.route("/amigurumi", methods=["POST"])
def create_amigurumi():
    idproducto = request.json.get("idproducto")
    codigo = request.json.get("codigo")
    nombre = request.json.get("nombre")
    descripcion = request.json.get("descripcion")
    precio = request.json.get("precio")
    stock = request.json.get("stock")
    imagen = request.json.get("imagen")

    new_amigurumi = Amigurumi(idproducto=idproducto, codigo=codigo, nombre=nombre, descripcion=descripcion, precio=precio, stock=stock, imagen=imagen)
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


# Rutas para "pedido"
@app.route("/pedido", methods=["POST"])
def create_pedido():
    idcliente = request.json.get("idcliente")
    fecha = request.json.get("fecha")
    idproducto = request.json.get("idproducto")
    cantidad_solicitada = request.json.get("cantidad_solicitada")
    precio = request.json.get("precio")
    fecha_pedido = request.json.get("fecha_pedido")
    estado_pedido = request.json.get("estado_pedido")

    new_pedido = Pedido(idcliente=idcliente, fecha=fecha, idproducto=idproducto, cantidad_solicitada=cantidad_solicitada, precio=precio, fecha_pedido=fecha_pedido, estado_pedido=estado_pedido)
    db.session.add(new_pedido)
    db.session.commit()

    return pedido_schema.jsonify(new_pedido)

@app.route("/pedido", methods=["GET"])
def get_pedidos():
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

#programa principal *******************************

'''
@app.route('/')
def hello():
    return 'Hello YOU'

@app.route('/')
def index():
    return render_template('Ingresar.html')
    '''

if __name__ == '__main__':
    app.run(debug=True)

