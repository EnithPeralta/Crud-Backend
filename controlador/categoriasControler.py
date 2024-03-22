from app import app, productos, categorias
from flask import render_template, request, jsonify
import pymongo
from bson.json_util import dumps

@app.route('/obtenerCategorias')
def obtenerCategorias():
    cat = categorias.find()
    listaCategorias = list(cat)
    json_data = dumps(listaCategorias)
    print(json_data)
    retorno = {'categorias': json_data}
    return jsonify(retorno)