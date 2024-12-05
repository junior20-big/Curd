from flask import Flask #Se utiliza para importar la libreria de Flask
from flask_cors import CORS #Permite configurar políticas de CORS en aplicaciones Flask
from flask import jsonify, request #El método JSONIFY simplifica la creación de respuestas JSON
                                #El REQUEST permite el acceso a toda la información que pasa desde el navegador del cliente al servidor

import pymysql # permite la interacción con bases de datos MySQL escrito completamente en Python

app = Flask(__name__) # Sirve para que Flask sepa dónde buscar recursos como plantillas y archivos estáticos

CORS(app) # es un mecanismo de seguridad que permite a las aplicaciones web interactuar con recursos de otros dominios

# Funcion para conectarnos a la base de datos de mysql
def conectar(vhost, vuser, vpass, vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn
# Ruta para consulta general del baul de contraseñas
@app.route("/")
def consulta_general():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM baul """)
        datos = cur.fetchall()
        data = []
        
        for row in datos:
            dato = {'id_baul': row[0], 'Plataforma': row[1], 'usuario': row[2], 'clave': row[3]}
            data.append(dato)
            
        cur.close()
        conn.close()
        return jsonify({'baul': data, 'mensaje': 'Baul de contraseñas'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

# Ruta para consulta individual de un registro en el baúl
@app.route("/consulta_individual/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM baul where id_baul='{0}' """.format(codigo))
        datos = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if datos != None:
           dato = {'id_baul': datos[0], 'Plataforma': datos[1], 'usuario': datos[2], 'clave': datos[3]}
           return jsonify({'baul': dato, 'mensaje': 'Registro encontrado'})
        else:
           return jsonify({'mensaje': 'Registro no encontrado'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

# Ruta para agragar nuevos datos a la base de datos
@app.route('/registro/', methods=['POST'])
def registro():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute(""" insert into baul (plataforma, usuario, clave) values
        ('{0}', '{1}', '{2}')""".format(request.json['plataforma'],request.json['usuario'], request.json['clave']))
        conn.commit()  # Para confirmar la inserción de la información
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

# Ruta para eliminar datos de la base de datos
@app.route('/eliminar/<codigo>', methods=['DELETE'])
def eliminar(codigo):
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        x = cur.execute(""" delete from baul where id_baul='{0}'""".format(codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@app.route('/actualizar/<codigo>', methods=['PUT'])
def actualizar(codigo):
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        
        x = cur.execute(""" update baul set plataforma='{0}', usuario='{1}', clave='{2}' where 
        id_baul='{3}'""".format(request.json['plataforma'], request.json['usuario'], 
                               request.json['clave'], codigo))
        
        conn.commit() # Guarda de forma permanente los cambios realizados en una transacción de base de datos o tabla
        cur.close() # Cierra un cursor, es decir, finaliza el uso de un cursor en una aplicación
        conn.close() # Cierra la conexión con la base de datos
        
         # Retornar un mensaje de éxito
        return jsonify({'mensaje': 'Registro Actualizado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

# el COMMIT es el proceso de convertir un conjunto de cambios provisionales en permanentes
if __name__ == '__main__':
    app.run(debug=True)