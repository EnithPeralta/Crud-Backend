from flask import Flask, render_template, request, jsonify
import pymongo

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/img'

miConexion = pymongo.MongoClient("mongodb://localhost:27017")
baseDatos = miConexion['GestionProductos']

productos = baseDatos['Productos']
categorias = baseDatos['Categorias']
usuarios = baseDatos["Usuarios"]

from controlador.productosControler import *
from controlador.categoriasControler import *
from controlador.usuariosControler import *

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
