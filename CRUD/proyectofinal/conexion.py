from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# instancia de la aplicación Flask
app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '**'
app.config['MYSQL_DATABASE_DB'] = 'tienda_vicky_gurumis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:***@localhost/tienda_vicky_gurumis'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = db.engine.connect()
            print("Conexión exitosa a la base de datos.")
        except Exception as error:
            print("No se pudo establecer la conexión: {}".format(str(error)))

    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")

class Amigurumi(db.Model):
    __tablename__ = 'amigurumi'
    idamigurumi = db.Column(db.Integer, primary_key=True)
    idproducto = db.Column(db.Integer, db.ForeignKey('producto.idproducto'))
    codigo = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.String(100))
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


class Patron(db.Model):
    __tablename__ = 'patron'
    idpatron = db.Column(db.Integer, primary_key=True)
    idproducto = db.Column(db.Integer, db.ForeignKey('producto.idproducto'))
    codigo = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.String(100))
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



# Crear una instancia de DatabaseConnection
db_connection = DatabaseConnection()

# Llamar al método connect() para establecer la conexión
db_connection.connect()

# Cerrar la conexión a la base de datos
#db_connection.close()
