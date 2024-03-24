import sqlite3

def validar_login(nomusuario, password):
    conn = sqlite3.connect('VI-DE.sqlite')
    cursor = conn.execute('SELECT idUs FROM usuarios WHERE username=? AND password=?', (nomusuario, password))
    usuario = cursor.fetchone()
    conn.close()
    return usuario is not None

def getusuario(nomusuario):
    conn = sqlite3.connect('VI-DE.sqlite')
    cursor = conn.execute('SELECT idUs, id_rol FROM usuarios WHERE username=?', (nomusuario,))
    usuario = cursor.fetchone()
    conn.close()
    return {'idUs': usuario[0], 'id_rol': usuario[1]} if usuario else None


def getvideojuego(idVi=None):
    conn = sqlite3.connect('VI-DE.sqlite')
    sql = 'select v.idVi,v.nombre,v.genero,v.modo,d.nombre,v.descripcion,v.lanzamiento_PC,v.lanzamiento_PS4,v.lanzamiento_PS5,v.lanzamiento_XBOX_S_X,v.lanzamiento_NS,v.imagen_url from videojuegos v join desarrolladores d on (v.desarrollado = d.idDe)'

    if idVi is not None:
        sql += ' WHERE v.idVi=' + str(idVi)

    cursor = conn.execute(sql)
    videojuegos = []
    for row in cursor:
        videojuego = {}
        desarrolladores = []

        videojuego['idVi'] = row[0]
        videojuego['nombre'] = row[1]
        videojuego['genero'] = row[2]
        videojuego['modo'] = row[3]

        desarrollador = {}
        desarrollador['nombre'] = row[4]
        desarrolladores.append(desarrollador)

        videojuego['descripcion'] = row[5]
        videojuego['lanzamiento_PC'] = row[6]
        videojuego['lanzamiento_PS4'] = row[7]
        videojuego['lanzamiento_PS5'] = row[8]
        videojuego['lanzamiento_XBOX_S_X'] = row[9]
        videojuego['lanzamiento_NS'] = row[10]
        videojuego['imagen_url'] = row[11]

        videojuego['desarrolladores'] = desarrolladores
        videojuegos.append(videojuego)

    conn.close()
    return videojuegos


def insertar_videojuego(nombre, genero, modo, desarrollado, descripcion, lanzamiento_PC, lanzamiento_PS4, lanzamiento_PS5,
                        lanzamiento_XBOX_S_X, lanzamiento_NS, imagen_url):
    conn = sqlite3.connect('VI-DE.sqlite')
    sql = "INSERT INTO videojuegos (nombre, genero, modo, desarrollado, descripcion, lanzamiento_PC, lanzamiento_PS4, lanzamiento_PS5, lanzamiento_XBOX_S_X, lanzamiento_NS, imagen_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    values = (
    nombre, genero, modo, desarrollado, descripcion, lanzamiento_PC, lanzamiento_PS4, lanzamiento_PS5, lanzamiento_XBOX_S_X,
    lanzamiento_NS, imagen_url)

    conn.execute(sql, values)
    conn.commit()
    conn.close()

def delete_videojuego(idVi):
    conn = sqlite3.connect('VI-DE.sqlite')
    sql = 'DELETE FROM videojuegos WHERE idVi = ?'
    values = [idVi]
    conn.execute(sql,values)
    conn.commit()
    conn.close()

def modificar_videojuego(idVi, nombre, genero, modo, desarrollado, descripcion, lanzamiento_PC, lanzamiento_PS4, lanzamiento_PS5,
                        lanzamiento_XBOX_S_X, lanzamiento_NS, imagen_url):
    conn = sqlite3.connect('VI-DE.sqlite')
    sql = 'UPDATE Videojuegos SET nombre=?, genero=?, modo=?, desarrollado=?, descripcion=?, lanzamiento_PC=?, lanzamiento_PS4=?, lanzamiento_PS5=?, lanzamiento_XBOX_S_X=?, lanzamiento_NS=?, imagen_url=? WHERE idVi=?'
    values = [nombre,genero, modo, desarrollado, descripcion, lanzamiento_PC, lanzamiento_PS4, lanzamiento_PS5,
              lanzamiento_XBOX_S_X, lanzamiento_NS, imagen_url,idVi]

    conn.execute(sql, values)
    conn.commit()
    conn.close()

def getdesarrolladores(idDe=None):
    conn = sqlite3.connect('VI-DE.sqlite')
    sql = 'select idDe,nombre,ubicacion,fundacion,CEO,empleados,descripcion,imagen_url from desarrolladores'

    if idDe is not None:
        sql += ' WHERE idDe=' + str(idDe)

    cursor = conn.execute(sql)
    desarrolladores = []
    for row in cursor:
        desarrollador={}
        desarrollador['idDe'] = row[0]
        desarrollador['nombre'] = row[1]
        desarrollador['ubicacion'] = row[2]
        desarrollador['fundacion'] = row[3]
        desarrollador['CEO'] = row[4]
        desarrollador['empleados'] = row[5]
        desarrollador['descripcion'] = row[6]
        desarrollador['imagen_url'] = row[7]

        desarrolladores.append(desarrollador)

    conn.close()
    return desarrolladores

def insertar_desarrollador(nombre,ubicacion,fundacion,CEO,empleados,descripcion,imagen_url):
    conn = sqlite3.connect('VI-DE.sqlite')
    sql = "INSERT INTO Desarrolladores (nombre, ubicacion, fundacion, CEO, empleados, descripcion, imagen_url) VALUES (?, ?, ?, ?, ?, ?, ?)"

    values = (nombre, ubicacion, fundacion, CEO, empleados, descripcion, imagen_url)

    conn.execute(sql, values)
    conn.commit()
    conn.close()
def delete_desarrollador(idDe):
    conn = sqlite3.connect('VI-DE.sqlite')
    sql = 'DELETE FROM Desarrolladores WHERE idDe = ?'
    values = [idDe]
    conn.execute(sql, values)
    conn.commit()
    conn.close()

def modificar_desarrollador(idDe,nombre, ubicacion, fundacion, CEO, empleados,descripcion, imagen_url):
    conn = sqlite3.connect('VI-DE.sqlite')
    sql = 'UPDATE Desarrolladores SET nombre=?, ubicacion=?, fundacion=?, CEO=?, empleados=?, descripcion=?, imagen_url=? WHERE idDe=?'

    values = [nombre, ubicacion,fundacion, CEO, empleados,descripcion, imagen_url,idDe]

    conn.execute(sql, values)
    conn.commit()
    conn.close()