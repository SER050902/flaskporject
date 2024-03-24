from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import dp


app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'CADENA DE CARACTERS RANDOM'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'idUs' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_rol' not in session or session['id_rol'] != 1:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'idUs' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'GET':
        nomusuario = request.args.get('username')
        usuario = dp.getusuario(nomusuario)
        return render_template('login.html', usuario=usuario, error_message=error_message)

    elif request.method == 'POST':
        nomusuario = request.form['username']
        password = request.form['password']

        user = dp.validar_login(nomusuario, password)

        if user:
            usuarios = dp.getusuario(nomusuario)
            if usuarios:
                session['idUs'] = usuarios['idUs']
                session['id_rol'] = usuarios['id_rol']
                session['token'] = 'logged_in'
                return redirect(url_for('index'))
        else:
            error_message = 'Invalid username or password'
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')




@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('login'))

@app.route('/videojuego/')
@login_required
def videojuego():
    videojuegos = dp.getvideojuego()
    desarrolladores = dp.getdesarrolladores()
    return render_template('videojuego.html', videojuegos=videojuegos, desarrolladores=desarrolladores)

@app.route('/videojuego/<idVi>')
@login_required
def vigdeojuego(idVi):
    videojuegos = dp.getvideojuego(idVi)
    desarrolladores = dp.getdesarrolladores()
    return render_template('videojuego.html', videojuegos=videojuegos, desarrolladores=desarrolladores)

@app.route('/insert_videojuego', methods=['GET','POST'])
@admin_required
def insert_videojuego():
    if request.method == 'GET':
        videojuegos = dp.getvideojuego()
        desarrolladores = dp.getdesarrolladores()
        return render_template('inser_videojuego.html',videojuegos=videojuegos,desarrolladores=desarrolladores)

    elif request.method == 'POST':
        nombre = request.form['nombre'] or None
        genero = request.form['genero'] or None
        modo = request.form['modo'] or None
        desarrollado = request.form['desarrollado'] or None
        descripcion = request.form['descripcion'] or None
        lanzamiento_PC = request.form['lanzamiento_PC'] or None
        lanzamiento_PS4 = request.form['lanzamiento_PS4'] or None
        lanzamiento_PS5 = request.form['lanzamiento_PS5'] or None
        lanzamiento_XBOX_S_X = request.form['lanzamiento_XBOX_S_X'] or None
        lanzamiento_NS = request.form['lanzamiento_NS'] or None
        imagen_url = request.form['imagen_url'] or None

        dp.insertar_videojuego(nombre,genero,modo, desarrollado,descripcion, lanzamiento_PC, lanzamiento_PS4,lanzamiento_PS5, lanzamiento_XBOX_S_X, lanzamiento_NS,imagen_url)
        return redirect(url_for('videojuego'))

@app.route('/videojuego/<idVi>/delete')
@admin_required
def delete_videojuego(idVi):
    dp.delete_videojuego(idVi)
    return redirect(url_for('videojuego'))


@app.route('/videojuego/<idVi>/modificar', methods=['GET', 'POST'])
@admin_required
def modificar_videojuego(idVi):
    if request.method == 'GET':
        desarrolladores = dp.getdesarrolladores()
        videojuegos = dp.getvideojuego(idVi)
        return render_template('modificar_videojuego.html', videojuego=videojuegos[0], desarrolladores=desarrolladores)

    nombre = request.form['nombre'] or None
    genero = request.form['genero'] or None
    modo = request.form['modo'] or None
    desarrollado = request.form['desarrollado'] or None
    descripcion = request.form['descripcion'] or None
    lanzamiento_PC = request.form['lanzamiento_PC'] or None
    lanzamiento_PS4 = request.form['lanzamiento_PS4'] or None
    lanzamiento_PS5 = request.form['lanzamiento_PS5'] or None
    lanzamiento_XBOX_S_X = request.form['lanzamiento_XBOX_S_X'] or None
    lanzamiento_NS = request.form['lanzamiento_NS'] or None
    imagen_url = request.form['imagen_url'] or None

    dp.modificar_videojuego(idVi, nombre, genero, modo, desarrollado, descripcion, lanzamiento_PC, lanzamiento_PS4,
                            lanzamiento_PS5, lanzamiento_XBOX_S_X, lanzamiento_NS, imagen_url)
    return redirect(url_for('videojuego'))

@app.route('/api/videojuegos', methods=['GET'])
def api_get_videojuegos():
    videojuegos = dp.getvideojuego()
    json_data = []

    for videojuego in videojuegos:
        json_data.append({
            'idVi': videojuego['idVi'],
            'genero': videojuego['genero'],
            'modo': videojuego['modo'],
            'nombre': videojuego['nombre'],
            'desarrolladores': videojuego['desarrolladores'][0]['nombre'],
            'descripcion': videojuego['descripcion'],
            'lanzamiento_PC': str(videojuego['lanzamiento_PC']),
            'lanzamiento_PS4': str(videojuego['lanzamiento_PS4']),
            'lanzamiento_PS5': str(videojuego['lanzamiento_PS5']),
            'lanzamiento_XBOX_S_X': str(videojuego['lanzamiento_XBOX_S_X']),
            'lanzamiento_NS': str(videojuego['lanzamiento_NS']),
            'imagen_url': videojuego['imagen_url'],
        })
    return jsonify(videojuegos=json_data)

@app.route('/desarrollador/')
@login_required
def desarrollador():
    desarrolladores = dp.getdesarrolladores()
    return render_template('desarrollador.html', desarrolladores=desarrolladores)

@app.route('/desarrollador/<idDe>')
@login_required
def dessarrollador(idDe):
    desarrolladores = dp.getdesarrolladores(idDe)
    return render_template('desarrollador.html', desarrolladores=desarrolladores)

@app.route('/Insert_desarrollador', methods=['GET', 'POST'])
@admin_required
def insert_desarrollador():
    if request.method == 'GET':
        desarrolladores = dp.getdesarrolladores()
        return render_template('Inser_desarrollador.html', desarrolladores=desarrolladores)

    if request.method == 'POST':
        nombre = request.form['nombre'] or None
        ubicacion = request.form['ubicacion'] or None
        fundacion = request.form['fundacion']
        CEO = request.form['CEO'] or None
        empleados = request.form['empleados'] or None
        descripcion = request.form['descripcion'] or None
        imagen_url = request.form['imagen_url'] or None
        dp.insertar_desarrollador(nombre, ubicacion, fundacion, CEO, empleados, descripcion, imagen_url)

        return redirect(url_for('desarrollador'))



@app.route('/desarrollador/<idDe>/delete')
@admin_required
def delete_desarrollador(idDe):
    dp.delete_desarrollador(idDe)
    return redirect(url_for('desarrollador'))

@app.route('/desarrollador/<idDe>/modificar', methods=['GET', 'POST'])
@admin_required
def modificar_desarrollador(idDe):
    if request.method == 'GET':
        desarrolladores = dp.getdesarrolladores(idDe)
        return render_template('modificar_desarrollador.html', desarrollador=desarrolladores[0])

    nombre = request.form['nombre'] or None
    ubicacion = request.form['ubicacion'] or None
    fundacion = request.form['fundacion'] or None
    CEO = request.form['CEO'] or None
    empleados = request.form['empleados'] or None
    descripcion = request.form['descripcion'] or None
    imagen_url = request.form['imagen_url'] or None

    dp.modificar_desarrollador(idDe,nombre,ubicacion,fundacion,CEO,empleados,descripcion,imagen_url)
    return redirect(url_for('desarrollador'))

@app.route('/api/desarrolladores', methods=['GET'])
def api_get_desarrollador():
    desarrollador = dp.getdesarrolladores()
    json_data = []

    for desarrollador in desarrollador:
        json_data.append({
            'idDe': desarrollador['idDe'],
            'nombre': desarrollador['nombre'],
            'ubicacion': desarrollador['ubicacion'],
            'fundacion': desarrollador['fundacion'],
            'CEO': desarrollador['CEO'],
            'empleados': desarrollador['empleados'],
            'descripcion': desarrollador['descripcion'],
            'imagen_url': desarrollador['imagen_url']
        })
    return jsonify(desarrolladores=json_data)

if __name__ == '__main__':
    app.run()

