import mysql.connector
from flask import Flask, request, render_template
from flaskext.mysql import MySQL

# instancia de la aplicación Flask
app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '****'
app.config['MYSQL_DATABASE_DB'] = 'tienda_vicky_gurumis'
mysql = MySQL(app)


class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connect()
            print("Conexión exitosa a la base de datos.")
        except mysql.connector.Error as error:
            print("No se pudo establecer la conexión: {}".format(error))

    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")