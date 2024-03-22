import threading
from app import app, usuarios
from flask import Flask, render_template,redirect,request 
import  yagmail
import pymongo

@app.route('/')
def vistaIniciarSesion():
    return render_template('login.html')

@app.route('/iniciarSesion', methods=['POST'])
def iniciarSesion():
    mensaje = None
    estado = False
    try:
        usuario = request.form['usuario']
        password = request.form['password']
        datosConsulta = {'usuario':usuario, 'password':password}
        print (datosConsulta)
        user = usuarios.find_one(datosConsulta)
        if user:
            email = yagmail.SMTP("mosqueraperalta12@gmail.com", open(".password").read(), encoding='UTF-8')
            asunto = 'Reporte de ingreso al sistema de usuario'
            mensaje = f"Se informa que el usuario <b>'{user['nombres']} {user['apellidos']}'</b> ha ingresado al sistema"
            thread = threading.Thread(target=enviarCorreo, args=(email, ["enithperalta24@gmail.com" , user [ 'correo' ]], asunto, mensaje ))
            thread. start()
            estado = True
            return redirect("/home")  
        else:
            mensaje = 'Credenciales no válidas'            
    except pymongo.errors.PyMongoError as error: 
        mensaje = error
    return render_template('login.html', estado=estado, mensaje=mensaje)

def enviarCorreo(email=None, destinatario=None, asunto=None, mensaje=None):
    email. send (to=destinatario, subject=asunto, contents=mensaje)
            