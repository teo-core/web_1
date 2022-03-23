import os
from bottle import route, run,TEMPLATE_PATH,jinja2_view,static_file

TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'templates'))

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename,root='./static')

@route('/')
@jinja2_view('home.html')
def hola():
    return {'datos':[
        ('Teo',1,'lunes'),
        ('Jose',2, 'martes'),
        ('Pau',3,'Jueves')
    ]
    }


run(host= 'localhost',port=8080, debug=True)