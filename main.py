################################
#imports
import os
import threading
import time, datetime
from flask import Flask,render_template, request,url_for,redirect, send_file
from flask_socketio import  SocketIO, emit
from LibLocal import config, getuso,notas as notaJson, encrip

################################
app= Flask(__name__)
Socket = SocketIO(app)
################################
#mantener un log de conección
def log_connection(ip, timestamp, methods,url):
    with open('log/log.txt', 'a') as log_file:
        log_file.write(f"IP: {ip} - Date/Time: {timestamp} - {methods} - URL: {url}\n")
################################
#secret key
app.secret_key = config.configDB['flask_key']
################################
#declarar folders
app.template_folder = config.configDB['template_folder']
app.static_folder = config.configDB['static_folder']
################################

#route index
@app.route('/')
def index():
	################################
    #sistema de log
    url = '/'
    methods = request.method
    ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_connection(ip, timestamp,methods,url)
	################################
    return render_template('home.html',
                           cssCustom = 'home.css',
                           title= 'Home')
#enviar datos por socket
def send_Data():
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cpu = getuso.getCpu()
        ram = getuso.getRam()
        disco = getuso.getDisco()
        Socket.emit('response_Data', {'hora': now,
                                      'cpu':cpu,
                                      'ram':ram,
                                      'disco':disco,
                                      })
        time.sleep(1)

################################
# sistema de log para consultar por la web 

@app.route('/logs')
def logViw():
    ################################
    #sistema de log
    url = '/logs'
    methods = request.method
    ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_connection(ip, timestamp,methods,url)
    ################################
    with open('log/log.txt', 'r') as log_file:
        log = log_file.read()
    
    return render_template('logs.html',
                           PageNamed='logs',
                           logs=log,
                           cssCustom='logs.css')

################################
#route /notas
@app.route('/notas',methods=['GET','POST'])
def notas():
    ################################
    #sistema de log
    url = '/notas'
    methods = request.method
    ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_connection(ip, timestamp,methods,url)
    ################################
    data = notaJson.getNotas()
    return render_template('notas.html',
                           notas = data,
                           PageNamed = 'notas',
                           cssCustom = 'notas.css'
                           )
################################
################################
#ruta crear nota
@app.route('/nota/create',methods=['GET','POST'])
def crearNota():
    if request.method == 'POST':
        ################################
        #sistema de log
        url = '/nota/create'
        methods = request.method
        ip = request.remote_addr
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_connection(ip, timestamp,methods,url)
        ################################
        Nombre = request.form['nombre']
        Fecha = request.form['fecha']
        Data = request.form['data']
        notaJson.createNota(nombre=Nombre,
                            fecha=Fecha,
                            data=Data)
        return redirect('/notas')
    ################################
    #sistema de log
    url = '/nota/create'
    methods = request.method
    ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_connection(ip, timestamp,methods,url)
	################################
    return render_template('createNote.html',
                           cssCustom= 'createNote.css',
                           PageName= 'Crear Nota')
################################
@app.route('/cifrado')
def cifradoList():
        ################################
        #sistema de log
        url = '/cifrado'
        methods = request.method
        ip = request.remote_addr
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_connection(ip, timestamp,methods,url)
        ################################
        return render_template('cifradoList.html',
                               cssCustom = 'cifradoList.css')
################################
@app.route('/cifrado/generateParKey',methods=['POST','GET'])
def generateKey():
    ################################
    #sistema de log
    url = '/cifrado/generateParKey'
    methods = request.method
    ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_connection(ip, timestamp,methods,url)
    ################################
    if request.method == 'POST':
        ################################
        # sistema de log
        url = '/cifrado/generateParKey'
        methods = request.method
        ip = request.remote_addr
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_connection(ip, timestamp, methods, url)
        ################################
        names = request.form['name']
        
        # Genera el archivo de clave
        ruta = encrip.generar_clave()
        
        # Envía el archivo al cliente
        response = send_file(ruta, as_attachment=True, download_name=f"{names}_clave.key")
        
        # Elimina el archivo después de enviarlo
        os.remove(ruta)
        
        return response
    return render_template('generateKey.html',
                           cssCustom='generateKey.css')

################################

@app.route('/cifrado/cifrar',methods=['GET','POST'])
def cifrar():
    try:
        os.remove("archivo_cifrado.bin")
    except:
        pass
# Registro de la conexión
    ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_connection(ip, timestamp, request.method, '/cifrado/cifrar')

    if request.method == 'POST':
        try:
            os.remove("archivo_cifrado.bin")
        except:
            pass

        # Registro de la conexión
        ip = request.remote_addr
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_connection(ip, timestamp, request.method, '/cifrado/cifrar')
        
        # Verificación de archivos recibidos
        if 'archivo' not in request.files or 'archivoKey' not in request.files:
            return 'Falta el archivo o la clave'

        archivo_original = request.files['archivo']
        archivo_key = request.files['archivoKey']
        
        if archivo_original.filename == '' or archivo_key.filename == '':
            return 'No se seleccionó ningún archivo o clave'

        # Cifrado del archivo
        encrip.cifrar_archivo(ruta_archivo_original= archivo_original.read(), clave=archivo_key.read())
        
        # Envío del archivo cifrado como respuesta al cliente
        return send_file(
        "archivo_cifrado.bin",
        as_attachment=True,
        download_name='cifrado.bin',
        mimetype='application/octet-stream'
    )
    
    # Si la solicitud es GET, simplemente renderiza el template cifrar.html
    return render_template('cifrado.html', cssCustom='cifrado.css')

################################
@app.route('/cifrado/descifrar',methods=['GET','POST'])
def decifrar():
    try:
        os.remove('fileCifrado.bin')
    except:
        pass
    ################################
    #sistema de log
    url = '/cifrado/descifrar'
    methods = request.method
    ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_connection(ip, timestamp,methods,url)
    ################################
    if request.method=='POST':
        try:
            os.remove('fileCifrado.bin')
        except:
            pass
        ################################
        #sistema de log
        url = '/cifrado/descifrar'
        methods = request.method
        ip = request.remote_addr
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_connection(ip, timestamp,methods,url)
        ################################

        fileCifrado = request.files['cifrado']
        claves = request.files['key']
        
        encrip.descifrar_archivo(clave=claves.read(),
                                 ruta_archivo_bin=fileCifrado.read()
                                 )
        
        return send_file(path_or_file='fileCifrado.bin',
                         as_attachment=True,
                         download_name='desifrado.bin')
    

    return render_template('decifrar.html',
                          cssCustom='cifrado.css')
################################


#routes SocketIO
@Socket.on('connect')
def handle_connect():
    emit('response_Data', {'hora': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
################################
#iniciar en local 
if '__main__'== __name__:
    thread = threading.Thread(target=send_Data)
    thread.daemon = True
    thread.start()
    Socket.run(
        app,
        host=config.configDB['host'],
        port=config.configDB['port'],  # Asegúrate de incluir el puerto
        debug=config.configDB['debug']
    )
################################