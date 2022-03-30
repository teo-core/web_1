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
    consulta = """SELECT p.id, p.nombre,p.apelllidos ,p.dni ,to2.descripcion 
                from persona p left join T_ocupacion to2 
                on p.id_ocupacion =to2 .id"""
    cursor = cnx.execute(consulta)
    filas = cursor.fetchall()
    cnx.close()
    return {"datos": filas}

@route('/editar')
@route('/editar/<id:int>')
@jinja2_view('formulario.html')
def mi_form(id=None):
    cnx = sqlite3.connect(BASE_DATOS)
    consulta = "select * from T_ocupacion"
    cursor = cnx.execute(consulta)
    ocupaciones = cursor.fetchall()

    if id is None:
        return {'ocupaciones':ocupaciones}
    else:
        consulta = "select id,nombre, apelllidos,dni, id_ocupacion from persona where id =?"
        cursor = cnx.execute(consulta,(id,))
        filas = cursor.fetchone()

    cnx.close()
    return {'datos': filas,'ocupaciones':ocupaciones}

@route('/guardar', method='POST')
def guardar():
    nombre = request.POST.nombre
    apellidos = request.POST.apellidos
    dni = request.POST.dni
    id = request.POST.id
    ocupacion = request.POST.ocupacion
    
    cnx = sqlite3.connect(BASE_DATOS)
    
    if id =='': #Alta
        consulta = "insert into persona(nombre, apelllidos,dni, id_ocupacion) values (?,?,?,?)"
        cnx.execute(consulta,(nombre,apellidos,dni,ocupacion))
    else: #Actualización
        consulta = "update persona set nombre = ?, apelllidos = ?, dni =?, id_ocupacion=? where id =?"
        cnx.execute(consulta,(nombre,apellidos,dni,ocupacion,id))

    cnx.commit()
    cnx.close()
    redirect('/')

@route('/borrar/<id:int>')
def borrar(id):
    cnx = sqlite3.connect(BASE_DATOS)
    consulta = f'delete from persona where id="{id}"'
    cnx.execute(consulta) 
    cnx.commit()
    cnx.close()
    redirect('/')


run(host= 'localhost',port=8080, debug=True)