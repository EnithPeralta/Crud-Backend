from flask import Flask, redirect, render_template, request, jsonify, send_file, url_for, session
import os
from bson.objectid import ObjectId
import pymongo
from PIL import Image
from io import BytesIO
import base64
from app import app, productos, categorias, usuarios
from flask import send_from_directory
 
# permite servir archivos almacenados en un directorio específico a través de una ruta personalizada

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#muestra la lista de los prodcuto tanto sus categorias 
@app.route('/home')
def home():
    listaProductos = productos.find()
    listaP = []
    for p in listaProductos:
        categoria = categorias.find_one({'_id': p['categoria']})
        p['nombreCategoria'] = categoria['nombre']
        listaP.append(p)
    return render_template('listaProductos.html', productos=listaP)

#funcion para mostrar el formulario de agregar 
@app.route('/vistaAgregarProducto')
def vistaAgregarProducto():
    listaCategorias = categorias.find()
    return render_template('Formulario.html',categorias = listaCategorias)
#funcion para guardar los datos de entrada del formulario
@app.route('/agregarProducto', methods=['POST'])
def agregarProducto():
    mensaje = None
    estado = False
    try:
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        precio = int(request.form['precio'])
        idCategoria = ObjectId(request.form['cdCategoria'])
        foto = request.files.get('fileFoto')
        
        producto = {
            'codigo': codigo,
            'nombre': nombre,
            'precio': precio,
            'categoria': idCategoria
        }
        resultado = productos.insert_one(producto)
        if resultado.acknowledged:
            idProducto = resultado.inserted_id
            nombreFotos = f'{idProducto}.jpg'
            if foto:  
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreFotos))
            mensaje = 'Producto Agregado Correctamente'
            estado = True
        else:
            mensaje = 'Problema Al Agregar El Producto'
    except pymongo.errors.PyMongoError as error:
        mensaje = str(error)
    return render_template('Formulario.html', estado=estado, mensaje=mensaje)

#fucion para verificar si ese codigo exite
def consultarProducto(codigo):
    try:
        consulta = {"codigo": codigo}
        producto = productos.find_one(consulta)
        if (producto is not None):
            return True
        else:
            return False
    except pymongo.error as error:
        print(error)
        return False
#funcion para guardar los datos de entrada del formulario
@app.route('/agregarProductoJson', methods=['POST'])
def agregarProductoJson():
    estado = False
    mensaje = None  
    try:
        datos = request.json
        producto = datos.get('producto')
        fotoBase64 = datos.get('foto')["foto"]
        producto = {
            'codigo': int(producto["codigo"]),
            'nombre': producto["nombre"],
            'precio': int(producto["precio"]),
            'categoria': ObjectId(producto["categoria"])
        }
        resultado = productos.insert_one(producto)
        if resultado.acknowledged:
            rutaImagen = f"{os.path.join(app.config['UPLOAD_FOLDER'])}/{producto['_id']}.jpg"
            with open(rutaImagen, "wb") as f:
                f.write(base64.b64decode(fotoBase64))
            estado = True
            mensaje = 'Producto Agregado Correctamente'
        else:
            mensaje = 'Problemas al Agregar'
    except pymongo.errors.PyMongoError as error:
        mensaje = str(error)
    retorno = {"estado": estado, "mensaje": mensaje}
    return jsonify(retorno)
#funcio para editar un producto ya existente
@app.route("/editarProducto", methods=['GET', 'POST'])
def editar():
    estado = False
    mensaje = None
    producto = None
    listaCategorias = categorias.find()
    listaP = []
    try:
        if request.method == 'GET':
            idProducto = request.args.get('idProducto')
            producto = productos.find_one({'_id': ObjectId(idProducto)})
            listaProductos = productos.find()
            listaP = []
            for p in listaProductos:
                categoria = categorias.find_one({'_id': p['categoria']})
                p['nombreCategoria'] = categoria['nombre']
                listaP.append(p)

        elif request.method == 'POST':
            codigo = int(request.form["codigo"])
            nombre = request.form["nombre"]
            precio = int(request.form["precio"])
            idCategoria = ObjectId(request.form["cdCategoria"])
            foto = request.files["fileFoto"]
            idProducto = request.form['idProducto']
            producto = {
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "categoria": idCategoria
            }
            resultado = productos.update_one({'_id': ObjectId(idProducto)}, {"$set": producto})
            if resultado.acknowledged:
                if foto.filename:
                    nombreFoto = f"{idProducto}.jpg"
                    foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))
                    mensaje = "Producto Actualizado Correctamente"
                    estado = True
                else:
                    mensaje = "Problemas al actualizar: No se proporcionó una foto válida"
            else:
                mensaje = "Problemas al actualizar: No se pudo actualizar el producto"

    except ValueError as error:
        mensaje = "Error en la entrada: {}".format(error)

    except Exception as error:
        mensaje = "Error inesperado: {}".format(error)
    return render_template("/actualizar.html", mensaje=mensaje, producto=producto, categorias=listaCategorias, listaP=listaP)

#funcion para devolver los datos de un producto especifico 
@app.route("/consultarProducto/<producto_id>", methods=["GET"])
def consultar(producto_id):
    try:
        resultado = productos.find_one({"_id": ObjectId(producto_id)})
        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({"error": "Producto no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)})

#funcion para eliminar un producto
@app.route("/eliminarProducto/<producto_id>", methods=["GET"])
def eliminar_producto(producto_id):
    try:
        resultado = productos.delete_one({"_id": ObjectId(producto_id)})
        if resultado.deleted_count == 1:
            return redirect(url_for("home"))
        else:
            return "Producto no encontrado."
    except pymongo.errors.PyMongoError as error:
        return f"Error al eliminar el producto: {error}"

#funcion para salir de la app
app.secret_key = 'your_secret_key_here'  # Reemplazar con una clave única y secreta
@app.route('/salir')
def salir():
  session.clear() # Elimina todas las variables de la sesión
  mensaje = 'Ha cerrado la sesión' # Mensaje para mostrar al usuario
  return render_template('/login.html', mensaje=mensaje) # Redirige a la página de login con un mensaje