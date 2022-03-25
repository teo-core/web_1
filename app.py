import os
from bottle import route, run,TEMPLATE_PATH,jinja2_view,static_file, request, redirect
import sqlite3

TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'templates'))
BASE_DATOS = os.path.join(os.path.dirname(__file__),'personas.db' )



@route('/static/<filename>')
def server_static(filename):
    return static_file(filename,root='./static')

@route('/')
@jinja2_view('home.html')
def hola():
    cnx = sqlite3.connect(BASE_DATOS)
    consulta = "select id,nombre, apelllidos,dni from persona"
    cursor = cnx.execute(consulta)
    filas = cursor.fetchall()
    cnx.close()
    return {"datos": filas}

@route('/formulario')
@jinja2_view('formulario.html')
def mi_form():
    return {}

@route('/guardar', method='POST')
def guardar():
    nombre = request.POST.nombre
    apellidos = request.POST.apellidos
    dni = request.POST.dni
    
    cnx = sqlite3.connect(BASE_DATOS)
    consulta = "insert into persona(nombre, apelllidos,dni) values (?,?,?)"
    cnx.execute(consulta,(nombre,apellidos,dni))
    cnx.commit()
    cnx.close()
    redirect('/')




run(host= 'localhost',port=8080, debug=True)