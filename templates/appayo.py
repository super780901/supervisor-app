
# app.py (PRIMERA LÍNEA)
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime # Esta también es necesaria


from flask import Flask, render_template

# Inicializa la aplicación Flask
# __name__ ayuda a Flask a localizar recursos como los archivos 'templates'
app = Flask(__name__)

# --------------------------
# CONFIGURACIÓN DE BASE DE DATOS
# --------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///supervisor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --------------------------
# CONFIGURACIÓN DE SESIÓN (CRÍTICO)
# --------------------------
# ⚠️ ¡IMPORTANTE! Cambia esta clave por una cadena larga y aleatoria en producción
app.config['SECRET_KEY'] = 'colosio' 
# --------------------------

db = SQLAlchemy(app)

# --------------------------
# RUTAS DE VISUALIZACIÓN (GET)
# --------------------------

# 1. Ruta principal / (Página de Login)
@app.route('/')
def login():
    # render_template busca el archivo en la carpeta 'templates'
    return render_template('index.html')

# 2. Ruta para el Menú Principal
# app.py

# app.py

# 🚨 CRÍTICO: Asegúrate de que 'session' esté importado aquí
from flask import Flask, render_template, request, redirect, url_for, session 

# ...

# app.py

# app.py

# app.py

@app.route('/menu')
def menu():
    # 1. IGNORAMOS la sesión por un momento para probar
    # user_name = session.get('user_name', "") 
    
    # 2. FORZAMOS un nombre manual. 
    # Si esto aparece en pantalla, tu HTML está perfecto y el problema es la base de datos.
    nombre_forzado = "SUPERVISOR PRUEBA"
    
    print(f"Enviando al template: {nombre_forzado}")

    # 3. Enviamos el nombre forzado
    return render_template('menu.html', user_name=nombre_forzado)

# 3. Ruta para el Registro de Usuario
@app.route('/registro_usuario')
def registro_usuario():
    # Sirve el archivo registro.html
    return render_template('registro.html')

# 4. Ruta para el Registro de Escuelas
@app.route('/registro_escuelas')
def registro_escuelas():
    # Sirve el archivo escuelas.html
    return render_template('escuelas.html')

    # app.py

# app.py

@app.route('/verificar_acceso', methods=['POST'])
def verificar_acceso():
    usuario_ingresado = request.form.get('username')
    contrasena_ingresada = request.form.get('password')

    user = User.query.filter_by(username=usuario_ingresado).first()

    if user and user.password == contrasena_ingresada:
        
        # 🚨 NUEVA LÍNEA DE DIAGNÓSTICO: Muestra el nombre completo y el ID
        print(f"DEBUG: USUARIO AUTENTICADO. Nombre a guardar: {user.nombre}, ID: {user.id}") 
        
        session['user_id'] = user.id
        session['user_name'] = user.nombre
        
        return redirect(url_for('menu'))
    else:
        return render_template('index.html', error="Usuario o contraseña incorrectos.")

# --------------------------
# EJECUTAR APLICACIÓN
# --------------------------
if __name__ == '__main__':
    # Ejecuta el servidor en modo de depuración para que los cambios se vean automáticamente
    app.run(debug=True)