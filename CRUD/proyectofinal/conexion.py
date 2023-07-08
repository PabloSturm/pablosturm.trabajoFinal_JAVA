from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# instancia de la aplicación Flask
app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Delfines/2'
app.config['MYSQL_DATABASE_DB'] = 'tienda_vicky_gurumis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Delfines/2@localhost/tienda_vicky_gurumis'

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



# Crear una instancia de DatabaseConnection
db_connection = DatabaseConnection()

# Llamar al método connect() para establecer la conexión
db_connection.connect()

# Cerrar la conexión a la base de datos
#db_connection.close()
