from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import make_response # Agrega esto si no está
from weasyprint import HTML     # Esto es lo nuevo

# Inicializa la aplicación Flask
app = Flask(__name__)

# --------------------------
# CONFIGURACIÓN (CRÍTICA)
# --------------------------
# 1. Base de Datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///supervisor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. Clave Secreta para Sesiones (Indispensable para que funcione el login)
app.config['SECRET_KEY'] = 'super_clave_secreta_2025' 

# Inicializa SQLAlchemy
db = SQLAlchemy(app) 

# --------------------------
# MODELOS DE BASE DE DATOS (TABLAS)
# --------------------------

class User(db.Model):
    """
    Modelo para la tabla de Usuarios (Supervisor).
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False) # Nombre completo
    username = db.Column(db.String(80), unique=True, nullable=False) # Usuario login
    password = db.Column(db.String(120), nullable=False) # Contraseña
    email = db.Column(db.String(120), unique=True, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Nuevos campos del Supervisor
    cct_supervisor = db.Column(db.String(50))
    nombre_cct = db.Column(db.String(150))
    
    def __repr__(self):
        return f'<Supervisor {self.username}>'

class Escuela(db.Model):
    """
    Modelo para la tabla de Escuelas.
    Incluye datos generales, estadística y personal.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cct = db.Column(db.String(50), unique=True, nullable=False)
    director = db.Column(db.String(100))
    sostenimiento = db.Column(db.String(20)) # Público/Privado
    zona_escolar = db.Column(db.String(50))

    # Estadística de Grupos
    num_grupos = db.Column(db.Integer, default=0)
    g_primero = db.Column(db.Integer, default=0)
    g_segundo = db.Column(db.Integer, default=0)
    g_tercero = db.Column(db.Integer, default=0)
    g_cuarto = db.Column(db.Integer, default=0)
    g_quinto = db.Column(db.Integer, default=0)
    g_sexto = db.Column(db.Integer, default=0)
    asp = db.Column(db.Integer, default=0) # Alumnos con Servicios de Prioridad?

    # Personal de Apoyo
    subdirector_academico = db.Column(db.String(100))
    subdirector_administrativo = db.Column(db.String(100))
    promotor_tics = db.Column(db.String(100))
    promotor_lectura = db.Column(db.String(100))
    otros_personal = db.Column(db.String(100))

    # Clave Foránea (Relación con User)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    registrador = db.relationship('User', backref=db.backref('escuelas', lazy=True))
    
    def __repr__(self):
        return f'<Escuela {self.nombre}>'

    # app.py (Agregar debajo de class Escuela)



class PMC(db.Model):
    """
    Tabla para guardar el Registro de Programa de Mejora Continua (PMC).
    """
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False) # Guardaremos la fecha como texto YYYY-MM-DD
    
    # Relaciones
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # Indicadores (Guardaremos SI/NO y Observaciones para cada uno)
    # 1.1 Disponibilidad
    ind_1_1 = db.Column(db.String(5))
    obs_1_1 = db.Column(db.String(200))
    # 1.2 Diagnóstico
    ind_1_2 = db.Column(db.String(5))
    obs_1_2 = db.Column(db.String(200))
    # 1.3 Objetivos
    ind_1_3 = db.Column(db.String(5))
    obs_1_3 = db.Column(db.String(200))
    # 1.4 Metas
    ind_1_4 = db.Column(db.String(5))
    obs_1_4 = db.Column(db.String(200))
    # 1.5 Plan de Acciones
    ind_1_5 = db.Column(db.String(5))
    obs_1_5 = db.Column(db.String(200))
    # 1.6 Seguimiento
    ind_1_6 = db.Column(db.String(5))
    obs_1_6 = db.Column(db.String(200))
    # 1.7 Consenso
    ind_1_7 = db.Column(db.String(5))
    obs_1_7 = db.Column(db.String(200))
    # 1.8 Corresponsabilidad
    ind_1_8 = db.Column(db.String(5))
    obs_1_8 = db.Column(db.String(200))

    def __repr__(self):
        return f'<PMC ID: {self.id}>'
    
# app.py - Agregar debajo de la clase PMC

class APF(db.Model):
    """
    Tabla para el registro de Asociación de Madres y Padres de Familia (APF).
    """
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    
    # Relaciones
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # Indicadores (2.1 a 2.12) - Guardamos SI/NO y Observaciones
    ind_2_1 = db.Column(db.String(5)); obs_2_1 = db.Column(db.String(200))
    ind_2_2 = db.Column(db.String(5)); obs_2_2 = db.Column(db.String(200))
    ind_2_3 = db.Column(db.String(5)); obs_2_3 = db.Column(db.String(200))
    ind_2_4 = db.Column(db.String(5)); obs_2_4 = db.Column(db.String(200))
    ind_2_5 = db.Column(db.String(5)); obs_2_5 = db.Column(db.String(200))
    ind_2_6 = db.Column(db.String(5)); obs_2_6 = db.Column(db.String(200))
    ind_2_7 = db.Column(db.String(5)); obs_2_7 = db.Column(db.String(200))
    ind_2_8 = db.Column(db.String(5)); obs_2_8 = db.Column(db.String(200))
    ind_2_9 = db.Column(db.String(5)); obs_2_9 = db.Column(db.String(200))
    ind_2_10 = db.Column(db.String(5)); obs_2_10 = db.Column(db.String(200))
    ind_2_11 = db.Column(db.String(5)); obs_2_11 = db.Column(db.String(200))
    ind_2_12 = db.Column(db.String(5)); obs_2_12 = db.Column(db.String(200))

    # Campos de Texto Abierto (Fortalezas, Debilidades, Áreas de Oportunidad)
    fortalezas = db.Column(db.Text)
    debilidades = db.Column(db.Text)
    areas_oportunidad = db.Column(db.Text)


    def __repr__(self):
        return f'<APF ID: {self.id}>'    


# --------------------------
# RUTAS GET (VISUALIZACIÓN)
# --------------------------

@app.route('/')
def login():
    # Si ya hay sesión, mandarlo directo al menú
    if session.get('user_id'):
        return redirect(url_for('menu'))
    return render_template('index.html')

@app.route('/menu')
def menu():
    # 1. Recuperar nombre de la sesión
    user_name = session.get('user_name')
    
    # 2. Proteger la ruta: Si no hay usuario, mandar al login
    if not user_name:
        return redirect(url_for('login'))

    # 3. Mostrar menú con el nombre
    return render_template('menu.html', user_name=user_name)


# app.py

@app.route('/submenu_registro')
def submenu_registro():
    # 1. Verificar seguridad (que esté logueado)
    if not session.get('user_id'):
        return redirect(url_for('login'))
        
    # 2. Obtener el nombre para el saludo
    user_name = session.get('user_name', 'Usuario')
    
    # 3. Mostrar la nueva página
    return render_template('submenu_registro.html', user_name=user_name)


@app.route('/registro_usuario')
def registro_usuario():
    return render_template('registro.html')

# app.py

# 1. ACTUALIZA ESTA RUTA (GET)
@app.route('/registro_escuelas')
def registro_escuelas():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    user_name = session.get('user_name')
    
    # CONSULTA: Busca todas las escuelas registradas por ESTE usuario
    mis_escuelas = Escuela.query.filter_by(user_id=session['user_id']).all()
    
    # Pasamos la lista 'mis_escuelas' a la plantilla
    return render_template('escuelas.html', user_name=user_name, escuelas=mis_escuelas)


# 2. AGREGA ESTA NUEVA RUTA (POST)
@app.route('/registrar_escuela', methods=['POST'])
def registrar_escuela_post():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    # Recibir datos del formulario
    nombre = request.form.get('nombre_escuela')
    cct = request.form.get('cct')
    director = request.form.get('nombre_director')
    num_grupos = request.form.get('num_grupos')
    
    # Grados (convertimos a int, si está vacío ponemos 0)
    g1 = int(request.form.get('primero') or 0)
    g2 = int(request.form.get('segundo') or 0)
    g3 = int(request.form.get('tercero') or 0)
    g4 = int(request.form.get('cuarto') or 0)
    g5 = int(request.form.get('quinto') or 0)
    g6 = int(request.form.get('sexto') or 0)
    
    sub_acad = request.form.get('subdirector_academico')
    sub_admin = request.form.get('subdirector_administrativo')
    prom_tics = request.form.get('promotor_tics')
    prom_lec = request.form.get('promotor_lectura')
    otros = request.form.get('otros')
    asp = int(request.form.get('asp') or 0)
    sostenimiento = request.form.get('sostenimiento')

    # Crear el objeto Escuela
    nueva_escuela = Escuela(
        nombre=nombre,
        cct=cct,
        director=director,
        num_grupos=int(num_grupos or 0),
        g_primero=g1, g_segundo=g2, g_tercero=g3, 
        g_cuarto=g4, g_quinto=g5, g_sexto=g6,
        subdirector_academico=sub_acad,
        subdirector_administrativo=sub_admin,
        promotor_tics=prom_tics,
        promotor_lectura=prom_lec,
        otros_personal=otros,
        asp=asp,
        sostenimiento=sostenimiento,
        user_id=session['user_id'] # Importante: Asignar al usuario actual
    )

    # Guardar en Base de Datos
    try:
        db.session.add(nueva_escuela)
        db.session.commit()
    except Exception as e:
        # Si hay error (ej. CCT repetido), por ahora solo imprimimos en consola
        print(f"Error al guardar escuela: {e}")
        db.session.rollback()

    # Recargar la página para ver la tabla actualizada
    return redirect(url_for('registro_escuelas'))


# --------------------------
# RUTAS POST (PROCESAMIENTO)
# --------------------------

@app.route('/verificar_acceso', methods=['POST'])
def verificar_acceso():
    usuario_ingresado = request.form.get('username')
    contrasena_ingresada = request.form.get('password')

    # Buscar usuario en DB
    user = User.query.filter_by(username=usuario_ingresado).first()

    if user and user.password == contrasena_ingresada:
        # ¡ÉXITO! Guardamos datos en la sesión
        session['user_id'] = user.id
        session['user_name'] = user.nombre  # Guardamos el NOMBRE real
        print(f"Login exitoso: {user.nombre}")
        return redirect(url_for('menu'))
    else:
        return render_template('index.html', error="Usuario o contraseña incorrectos.")


@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario_post():
    # Recibir datos del formulario HTML
    nombre_completo = request.form.get('nombre_apellido')
    usuario = request.form.get('nombre_usuario')
    password = request.form.get('reg_password')
    email = request.form.get('correo_electronico')
    cct = request.form.get('cct_supervisor')
    nombre_cct = request.form.get('nombre_cct')
    
    # Verificar si existe
    if User.query.filter_by(username=usuario).first():
        return render_template('registro.html', error="El usuario ya existe")

    # Crear nuevo usuario
    new_user = User(
        nombre=nombre_completo,
        username=usuario,
        password=password,
        email=email,
        cct_supervisor=cct,
        nombre_cct=nombre_cct
    )
    
    # Guardar en DB
    db.session.add(new_user)
    db.session.commit()
    
    print(f"Usuario registrado: {nombre_completo}")
    return redirect(url_for('login'))

# app.py (Rutas nuevas)



# app.py - Pegar antes del bloque if __name__ == '__main__':

# 1. RUTA PARA MOSTRAR LA PÁGINA (Esta es la que el error dice que falta)
@app.route('/registro_pmc')
def registro_pmc():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    user_name = session.get('user_name')
    # Consultamos las escuelas para el select
    mis_escuelas = Escuela.query.filter_by(user_id=session['user_id']).all()
    
    return render_template('registro_pmc.html', user_name=user_name, escuelas=mis_escuelas)

# 2. RUTA PARA GUARDAR LOS DATOS
@app.route('/guardar_pmc', methods=['POST'])
def guardar_pmc():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    # Recogemos datos
    escuela_id = request.form.get('escuela_id')
    fecha = request.form.get('fecha_revision')
    
    # Guardamos en la nueva tabla
    nuevo_pmc = PMC(
        user_id=session['user_id'],
        escuela_id=escuela_id,
        fecha=fecha,
        ind_1_1 = request.form.get('ind_1_1'), obs_1_1 = request.form.get('obs_1_1'),
        ind_1_2 = request.form.get('ind_1_2'), obs_1_2 = request.form.get('obs_1_2'),
        ind_1_3 = request.form.get('ind_1_3'), obs_1_3 = request.form.get('obs_1_3'),
        ind_1_4 = request.form.get('ind_1_4'), obs_1_4 = request.form.get('obs_1_4'),
        ind_1_5 = request.form.get('ind_1_5'), obs_1_5 = request.form.get('obs_1_5'),
        ind_1_6 = request.form.get('ind_1_6'), obs_1_6 = request.form.get('obs_1_6'),
        ind_1_7 = request.form.get('ind_1_7'), obs_1_7 = request.form.get('obs_1_7'),
        ind_1_8 = request.form.get('ind_1_8'), obs_1_8 = request.form.get('obs_1_8')
    )
    
    db.session.add(nuevo_pmc)
    db.session.commit()
    
    return redirect(url_for('submenu_registro'))

# app.py - Rutas para APF

# app.py

@app.route('/registro_apf')
def registro_apf():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    user_name = session.get('user_name')
    mis_escuelas = Escuela.query.filter_by(user_id=session['user_id']).all()
    
    return render_template('registro_apf.html', user_name=user_name, escuelas=mis_escuelas)

@app.route('/guardar_apf', methods=['POST'])
def guardar_apf():
    if not session.get('user_id'): return redirect(url_for('login'))

    nuevo_apf = APF(
        user_id=session['user_id'],
        escuela_id=request.form.get('escuela_id'),
        fecha=request.form.get('fecha_revision'),
        
        ind_2_1=request.form.get('ind_2_1'), obs_2_1=request.form.get('obs_2_1'),
        ind_2_2=request.form.get('ind_2_2'), obs_2_2=request.form.get('obs_2_2'),
        ind_2_3=request.form.get('ind_2_3'), obs_2_3=request.form.get('obs_2_3'),
        ind_2_4=request.form.get('ind_2_4'), obs_2_4=request.form.get('obs_2_4'),
        ind_2_5=request.form.get('ind_2_5'), obs_2_5=request.form.get('obs_2_5'),
        ind_2_6=request.form.get('ind_2_6'), obs_2_6=request.form.get('obs_2_6'),
        ind_2_7=request.form.get('ind_2_7'), obs_2_7=request.form.get('obs_2_7'),
        ind_2_8=request.form.get('ind_2_8'), obs_2_8=request.form.get('obs_2_8'),
        ind_2_9=request.form.get('ind_2_9'), obs_2_9=request.form.get('obs_2_9'),
        ind_2_10=request.form.get('ind_2_10'), obs_2_10=request.form.get('obs_2_10'),
        ind_2_11=request.form.get('ind_2_11'), obs_2_11=request.form.get('obs_2_11'),
        ind_2_12=request.form.get('ind_2_12'), obs_2_12=request.form.get('obs_2_12'),

        fortalezas=request.form.get('fortalezas'),
        debilidades=request.form.get('debilidades'),
        areas_oportunidad=request.form.get('areas_oportunidad')
    )
    
    db.session.add(nuevo_apf)
    db.session.commit()
    return redirect(url_for('submenu_registro'))





# --- MODELO PARA LA BASE DE DATOS ---
class Asistencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # Indicadores 3.1 al 3.10
    ind_3_1 = db.Column(db.String(5)); obs_3_1 = db.Column(db.String(200))
    ind_3_2 = db.Column(db.String(5)); obs_3_2 = db.Column(db.String(200))
    ind_3_3 = db.Column(db.String(5)); obs_3_3 = db.Column(db.String(200))
    ind_3_4 = db.Column(db.String(5)); obs_3_4 = db.Column(db.String(200))
    ind_3_5 = db.Column(db.String(5)); obs_3_5 = db.Column(db.String(200))
    ind_3_6 = db.Column(db.String(5)); obs_3_6 = db.Column(db.String(200))
    ind_3_7 = db.Column(db.String(5)); obs_3_7 = db.Column(db.String(200))
    ind_3_8 = db.Column(db.String(5)); obs_3_8 = db.Column(db.String(200))
    ind_3_9 = db.Column(db.String(5)); obs_3_9 = db.Column(db.String(200))
    ind_3_10 = db.Column(db.String(5)); obs_3_10 = db.Column(db.String(200))

    # Campos de texto
    personal_incidencias = db.Column(db.Text)
    irregularidades = db.Column(db.Text)
    recomendaciones = db.Column(db.Text)

# --- RUTAS ---
@app.route('/registro_asistencia')
def registro_asistencia():
    if not session.get('user_id'): return redirect(url_for('login'))
    user_name = session.get('user_name')
    mis_escuelas = Escuela.query.filter_by(user_id=session['user_id']).all()
    return render_template('registro_asistencia.html', user_name=user_name, escuelas=mis_escuelas)

@app.route('/guardar_asistencia', methods=['POST'])
def guardar_asistencia():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    nuevo = Asistencia(
        user_id=session['user_id'],
        escuela_id=request.form.get('escuela_id'),
        fecha=request.form.get('fecha_revision'),
        
        ind_3_1=request.form.get('ind_3_1'), obs_3_1=request.form.get('obs_3_1'),
        ind_3_2=request.form.get('ind_3_2'), obs_3_2=request.form.get('obs_3_2'),
        ind_3_3=request.form.get('ind_3_3'), obs_3_3=request.form.get('obs_3_3'),
        ind_3_4=request.form.get('ind_3_4'), obs_3_4=request.form.get('obs_3_4'),
        ind_3_5=request.form.get('ind_3_5'), obs_3_5=request.form.get('obs_3_5'),
        ind_3_6=request.form.get('ind_3_6'), obs_3_6=request.form.get('obs_3_6'),
        ind_3_7=request.form.get('ind_3_7'), obs_3_7=request.form.get('obs_3_7'),
        ind_3_8=request.form.get('ind_3_8'), obs_3_8=request.form.get('obs_3_8'),
        ind_3_9=request.form.get('ind_3_9'), obs_3_9=request.form.get('obs_3_9'),
        ind_3_10=request.form.get('ind_3_10'), obs_3_10=request.form.get('obs_3_10'),

        personal_incidencias=request.form.get('personal_incidencias'),
        irregularidades=request.form.get('irregularidades'),
        recomendaciones=request.form.get('recomendaciones')
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('submenu_registro'))

# app.py - Modelo para CTE

class CTE(db.Model):
    """
    Tabla para el registro de Consejo Técnico Escolar (Grupo 4).
    """
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # Indicadores 4.1 al 4.10
    ind_4_1 = db.Column(db.String(5)); obs_4_1 = db.Column(db.String(200))
    ind_4_2 = db.Column(db.String(5)); obs_4_2 = db.Column(db.String(200))
    ind_4_3 = db.Column(db.String(5)); obs_4_3 = db.Column(db.String(200))
    ind_4_4 = db.Column(db.String(5)); obs_4_4 = db.Column(db.String(200))
    ind_4_5 = db.Column(db.String(5)); obs_4_5 = db.Column(db.String(200))
    ind_4_6 = db.Column(db.String(5)); obs_4_6 = db.Column(db.String(200))
    ind_4_7 = db.Column(db.String(5)); obs_4_7 = db.Column(db.String(200))
    ind_4_8 = db.Column(db.String(5)); obs_4_8 = db.Column(db.String(200))
    ind_4_9 = db.Column(db.String(5)); obs_4_9 = db.Column(db.String(200))
    ind_4_10 = db.Column(db.String(5)); obs_4_10 = db.Column(db.String(200))

    # Campos de texto abiertos
    practicas_exitosas = db.Column(db.Text)
    areas_mejora = db.Column(db.Text)
    acuerdos_relevantes = db.Column(db.Text)



# --- RUTAS PARA CTE ---
@app.route('/registro_cte')
def registro_cte():
    if not session.get('user_id'): return redirect(url_for('login'))
    user_name = session.get('user_name')
    mis_escuelas = Escuela.query.filter_by(user_id=session['user_id']).all()
    return render_template('registro_cte.html', user_name=user_name, escuelas=mis_escuelas)

@app.route('/guardar_cte', methods=['POST'])
def guardar_cte():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    nuevo = CTE(
        user_id=session['user_id'],
        escuela_id=request.form.get('escuela_id'),
        fecha=request.form.get('fecha_revision'),
        
        ind_4_1=request.form.get('ind_4_1'), obs_4_1=request.form.get('obs_4_1'),
        ind_4_2=request.form.get('ind_4_2'), obs_4_2=request.form.get('obs_4_2'),
        ind_4_3=request.form.get('ind_4_3'), obs_4_3=request.form.get('obs_4_3'),
        ind_4_4=request.form.get('ind_4_4'), obs_4_4=request.form.get('obs_4_4'),
        ind_4_5=request.form.get('ind_4_5'), obs_4_5=request.form.get('obs_4_5'),
        ind_4_6=request.form.get('ind_4_6'), obs_4_6=request.form.get('obs_4_6'),
        ind_4_7=request.form.get('ind_4_7'), obs_4_7=request.form.get('obs_4_7'),
        ind_4_8=request.form.get('ind_4_8'), obs_4_8=request.form.get('obs_4_8'),
        ind_4_9=request.form.get('ind_4_9'), obs_4_9=request.form.get('obs_4_9'),
        ind_4_10=request.form.get('ind_4_10'), obs_4_10=request.form.get('obs_4_10'),

        practicas_exitosas=request.form.get('practicas_exitosas'),
        areas_mejora=request.form.get('areas_mejora'),
        acuerdos_relevantes=request.form.get('acuerdos_relevantes')
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('submenu_registro'))


# app.py - Modelo Cooperativa (Grupo 5)

# --- RUTAS COOPERATIVA ---
# --- MODELO COOPERATIVA (Grupo 5) ---
class Cooperativa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # Indicadores 5.1 al 5.11
    ind_5_1 = db.Column(db.String(5)); obs_5_1 = db.Column(db.String(200))
    ind_5_2 = db.Column(db.String(5)); obs_5_2 = db.Column(db.String(200))
    ind_5_3 = db.Column(db.String(5)); obs_5_3 = db.Column(db.String(200))
    ind_5_4 = db.Column(db.String(5)); obs_5_4 = db.Column(db.String(200))
    ind_5_5 = db.Column(db.String(5)); obs_5_5 = db.Column(db.String(200))
    ind_5_6 = db.Column(db.String(5)); obs_5_6 = db.Column(db.String(200))
    ind_5_7 = db.Column(db.String(5)); obs_5_7 = db.Column(db.String(200))
    ind_5_8 = db.Column(db.String(5)); obs_5_8 = db.Column(db.String(200))
    ind_5_9 = db.Column(db.String(5)); obs_5_9 = db.Column(db.String(200))
    ind_5_10 = db.Column(db.String(5)); obs_5_10 = db.Column(db.String(200))
    ind_5_11 = db.Column(db.String(5)); obs_5_11 = db.Column(db.String(200))

    # Campos de texto abiertos
    obs_higiene = db.Column(db.Text)
    sit_admin = db.Column(db.Text)
    acuerdos = db.Column(db.Text)

# --- RUTAS COOPERATIVA ---
@app.route('/registro_cooperativa')
def registro_cooperativa():
    if not session.get('user_id'): return redirect(url_for('login'))
    user_name = session.get('user_name')
    mis_escuelas = Escuela.query.filter_by(user_id=session['user_id']).all()
    return render_template('registro_cooperativa.html', user_name=user_name, escuelas=mis_escuelas)

@app.route('/guardar_cooperativa', methods=['POST'])
def guardar_cooperativa():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    nuevo = Cooperativa(
        user_id=session['user_id'],
        escuela_id=request.form.get('escuela_id'),
        fecha=request.form.get('fecha_revision'),
        
        ind_5_1=request.form.get('ind_5_1'), obs_5_1=request.form.get('obs_5_1'),
        ind_5_2=request.form.get('ind_5_2'), obs_5_2=request.form.get('obs_5_2'),
        ind_5_3=request.form.get('ind_5_3'), obs_5_3=request.form.get('obs_5_3'),
        ind_5_4=request.form.get('ind_5_4'), obs_5_4=request.form.get('obs_5_4'),
        ind_5_5=request.form.get('ind_5_5'), obs_5_5=request.form.get('obs_5_5'),
        ind_5_6=request.form.get('ind_5_6'), obs_5_6=request.form.get('obs_5_6'),
        ind_5_7=request.form.get('ind_5_7'), obs_5_7=request.form.get('obs_5_7'),
        ind_5_8=request.form.get('ind_5_8'), obs_5_8=request.form.get('obs_5_8'),
        ind_5_9=request.form.get('ind_5_9'), obs_5_9=request.form.get('obs_5_9'),
        ind_5_10=request.form.get('ind_5_10'), obs_5_10=request.form.get('obs_5_10'),
        ind_5_11=request.form.get('ind_5_11'), obs_5_11=request.form.get('obs_5_11'),

        obs_higiene=request.form.get('obs_higiene'),
        sit_admin=request.form.get('sit_admin'),
        acuerdos=request.form.get('acuerdos')
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('submenu_registro'))

# --- MODELO INVENTARIO (Grupo 6) ---
# --- MODELO INVENTARIO (Grupo 6) ---
class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # Indicadores 6.1 al 6.10
    ind_6_1 = db.Column(db.String(5)); obs_6_1 = db.Column(db.String(200))
    ind_6_2 = db.Column(db.String(5)); obs_6_2 = db.Column(db.String(200))
    ind_6_3 = db.Column(db.String(5)); obs_6_3 = db.Column(db.String(200))
    ind_6_4 = db.Column(db.String(5)); obs_6_4 = db.Column(db.String(200))
    ind_6_5 = db.Column(db.String(5)); obs_6_5 = db.Column(db.String(200))
    ind_6_6 = db.Column(db.String(5)); obs_6_6 = db.Column(db.String(200))
    ind_6_7 = db.Column(db.String(5)); obs_6_7 = db.Column(db.String(200))
    ind_6_8 = db.Column(db.String(5)); obs_6_8 = db.Column(db.String(200))
    ind_6_9 = db.Column(db.String(5)); obs_6_9 = db.Column(db.String(200))
    ind_6_10 = db.Column(db.String(5)); obs_6_10 = db.Column(db.String(200))

    # Campos de texto abiertos
    discrepancias = db.Column(db.Text)
    estado_mobiliario = db.Column(db.Text)
    necesidades = db.Column(db.Text)

# --- RUTAS INVENTARIO ---
@app.route('/registro_inventario')
def registro_inventario():
    if not session.get('user_id'): return redirect(url_for('login'))
    user_name = session.get('user_name')
    mis_escuelas = Escuela.query.filter_by(user_id=session['user_id']).all()
    return render_template('registro_inventario.html', user_name=user_name, escuelas=mis_escuelas)

@app.route('/guardar_inventario', methods=['POST'])
def guardar_inventario():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    nuevo = Inventario(
        user_id=session['user_id'],
        escuela_id=request.form.get('escuela_id'),
        fecha=request.form.get('fecha_revision'),
        
        ind_6_1=request.form.get('ind_6_1'), obs_6_1=request.form.get('obs_6_1'),
        ind_6_2=request.form.get('ind_6_2'), obs_6_2=request.form.get('obs_6_2'),
        ind_6_3=request.form.get('ind_6_3'), obs_6_3=request.form.get('obs_6_3'),
        ind_6_4=request.form.get('ind_6_4'), obs_6_4=request.form.get('obs_6_4'),
        ind_6_5=request.form.get('ind_6_5'), obs_6_5=request.form.get('obs_6_5'),
        ind_6_6=request.form.get('ind_6_6'), obs_6_6=request.form.get('obs_6_6'),
        ind_6_7=request.form.get('ind_6_7'), obs_6_7=request.form.get('obs_6_7'),
        ind_6_8=request.form.get('ind_6_8'), obs_6_8=request.form.get('obs_6_8'),
        ind_6_9=request.form.get('ind_6_9'), obs_6_9=request.form.get('obs_6_9'),
        ind_6_10=request.form.get('ind_6_10'), obs_6_10=request.form.get('obs_6_10'),

        discrepancias=request.form.get('discrepancias'),
        estado_mobiliario=request.form.get('estado_mobiliario'),
        necesidades=request.form.get('necesidades')
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('submenu_registro'))


# --- MODELO INFRAESTRUCTURA (Grupo 7 - Actualizado a 18 items) ---
class Infraestructura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # Indicadores 7.1 al 7.18
    ind_7_1 = db.Column(db.String(5)); obs_7_1 = db.Column(db.String(200))
    ind_7_2 = db.Column(db.String(5)); obs_7_2 = db.Column(db.String(200))
    ind_7_3 = db.Column(db.String(5)); obs_7_3 = db.Column(db.String(200))
    ind_7_4 = db.Column(db.String(5)); obs_7_4 = db.Column(db.String(200))
    ind_7_5 = db.Column(db.String(5)); obs_7_5 = db.Column(db.String(200))
    ind_7_6 = db.Column(db.String(5)); obs_7_6 = db.Column(db.String(200))
    ind_7_7 = db.Column(db.String(5)); obs_7_7 = db.Column(db.String(200))
    ind_7_8 = db.Column(db.String(5)); obs_7_8 = db.Column(db.String(200))
    ind_7_9 = db.Column(db.String(5)); obs_7_9 = db.Column(db.String(200))
    ind_7_10 = db.Column(db.String(5)); obs_7_10 = db.Column(db.String(200))
    ind_7_11 = db.Column(db.String(5)); obs_7_11 = db.Column(db.String(200))
    ind_7_12 = db.Column(db.String(5)); obs_7_12 = db.Column(db.String(200))
    ind_7_13 = db.Column(db.String(5)); obs_7_13 = db.Column(db.String(200))
    ind_7_14 = db.Column(db.String(5)); obs_7_14 = db.Column(db.String(200))
    ind_7_15 = db.Column(db.String(5)); obs_7_15 = db.Column(db.String(200))
    ind_7_16 = db.Column(db.String(5)); obs_7_16 = db.Column(db.String(200))
    ind_7_17 = db.Column(db.String(5)); obs_7_17 = db.Column(db.String(200))
    ind_7_18 = db.Column(db.String(5)); obs_7_18 = db.Column(db.String(200))

    # Campos de texto abiertos
    riesgos_detectados = db.Column(db.Text)
    necesidades_mantenimiento = db.Column(db.Text)
    acuerdos = db.Column(db.Text)

# --- RUTAS INFRAESTRUCTURA ---
# --- RUTAS INFRAESTRUCTURA ---
@app.route('/registro_infraestructura')
def registro_infraestructura():
    if not session.get('user_id'): return redirect(url_for('login'))
    user_name = session.get('user_name')
    mis_escuelas = Escuela.query.filter_by(user_id=session['user_id']).all()
    return render_template('registro_infraestructura.html', user_name=user_name, escuelas=mis_escuelas)

@app.route('/guardar_infraestructura', methods=['POST'])
def guardar_infraestructura():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    nuevo = Infraestructura(
        user_id=session['user_id'],
        escuela_id=request.form.get('escuela_id'),
        fecha=request.form.get('fecha_revision'),
        
        # Indicadores del 1 al 18
        ind_7_1=request.form.get('ind_7_1'), obs_7_1=request.form.get('obs_7_1'),
        ind_7_2=request.form.get('ind_7_2'), obs_7_2=request.form.get('obs_7_2'),
        ind_7_3=request.form.get('ind_7_3'), obs_7_3=request.form.get('obs_7_3'),
        ind_7_4=request.form.get('ind_7_4'), obs_7_4=request.form.get('obs_7_4'),
        ind_7_5=request.form.get('ind_7_5'), obs_7_5=request.form.get('obs_7_5'),
        ind_7_6=request.form.get('ind_7_6'), obs_7_6=request.form.get('obs_7_6'),
        ind_7_7=request.form.get('ind_7_7'), obs_7_7=request.form.get('obs_7_7'),
        ind_7_8=request.form.get('ind_7_8'), obs_7_8=request.form.get('obs_7_8'),
        ind_7_9=request.form.get('ind_7_9'), obs_7_9=request.form.get('obs_7_9'),
        ind_7_10=request.form.get('ind_7_10'), obs_7_10=request.form.get('obs_7_10'),
        ind_7_11=request.form.get('ind_7_11'), obs_7_11=request.form.get('obs_7_11'),
        ind_7_12=request.form.get('ind_7_12'), obs_7_12=request.form.get('obs_7_12'),
        ind_7_13=request.form.get('ind_7_13'), obs_7_13=request.form.get('obs_7_13'),
        ind_7_14=request.form.get('ind_7_14'), obs_7_14=request.form.get('obs_7_14'),
        ind_7_15=request.form.get('ind_7_15'), obs_7_15=request.form.get('obs_7_15'),
        ind_7_16=request.form.get('ind_7_16'), obs_7_16=request.form.get('obs_7_16'),
        ind_7_17=request.form.get('ind_7_17'), obs_7_17=request.form.get('obs_7_17'),
        ind_7_18=request.form.get('ind_7_18'), obs_7_18=request.form.get('obs_7_18'),

        riesgos_detectados=request.form.get('riesgos_detectados'),
        necesidades_mantenimiento=request.form.get('necesidades_mantenimiento'),
        acuerdos=request.form.get('acuerdos')
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('submenu_registro'))

# --- MODELO CONTROL ESCOLAR (Grupo 8) ---
class ControlEscolar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # Indicadores 8.1 al 8.11
    ind_8_1 = db.Column(db.String(5)); obs_8_1 = db.Column(db.String(200))
    ind_8_2 = db.Column(db.String(5)); obs_8_2 = db.Column(db.String(200))
    ind_8_3 = db.Column(db.String(5)); obs_8_3 = db.Column(db.String(200))
    ind_8_4 = db.Column(db.String(5)); obs_8_4 = db.Column(db.String(200))
    ind_8_5 = db.Column(db.String(5)); obs_8_5 = db.Column(db.String(200))
    ind_8_6 = db.Column(db.String(5)); obs_8_6 = db.Column(db.String(200))
    ind_8_7 = db.Column(db.String(5)); obs_8_7 = db.Column(db.String(200))
    ind_8_8 = db.Column(db.String(5)); obs_8_8 = db.Column(db.String(200))
    ind_8_9 = db.Column(db.String(5)); obs_8_9 = db.Column(db.String(200))
    ind_8_10 = db.Column(db.String(5)); obs_8_10 = db.Column(db.String(200))
    ind_8_11 = db.Column(db.String(5)); obs_8_11 = db.Column(db.String(200))

    # Campos de texto abiertos
    inconsistencias = db.Column(db.Text)
    situacion_bap = db.Column(db.Text)
    observaciones_generales = db.Column(db.Text)


# --- MODELO PIPCE (Grupo 10 - Actualizado 11 items) ---
class PIPCE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # Indicadores 10.1 al 10.11
    ind_10_1 = db.Column(db.String(5)); obs_10_1 = db.Column(db.String(200))
    ind_10_2 = db.Column(db.String(5)); obs_10_2 = db.Column(db.String(200))
    ind_10_3 = db.Column(db.String(5)); obs_10_3 = db.Column(db.String(200))
    ind_10_4 = db.Column(db.String(5)); obs_10_4 = db.Column(db.String(200))
    ind_10_5 = db.Column(db.String(5)); obs_10_5 = db.Column(db.String(200))
    ind_10_6 = db.Column(db.String(5)); obs_10_6 = db.Column(db.String(200))
    ind_10_7 = db.Column(db.String(5)); obs_10_7 = db.Column(db.String(200))
    ind_10_8 = db.Column(db.String(5)); obs_10_8 = db.Column(db.String(200))
    ind_10_9 = db.Column(db.String(5)); obs_10_9 = db.Column(db.String(200))
    ind_10_10 = db.Column(db.String(5)); obs_10_10 = db.Column(db.String(200))
    ind_10_11 = db.Column(db.String(5)); obs_10_11 = db.Column(db.String(200))

    # Campos de texto abiertos
    riesgos_detectados = db.Column(db.Text)
    estado_equipamiento = db.Column(db.Text)
    acuerdos_seguridad = db.Column(db.Text)

# --- RUTAS CONTROL ESCOLAR ---
@app.route('/registro_control_escolar')
def registro_control_escolar():
    if not session.get('user_id'): return redirect(url_for('login'))
    user_name = session.get('user_name')
    mis_escuelas = Escuela.query.filter_by(user_id=session['user_id']).all()
    return render_template('registro_control_escolar.html', user_name=user_name, escuelas=mis_escuelas)

@app.route('/guardar_control_escolar', methods=['POST'])
def guardar_control_escolar():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    nuevo = ControlEscolar(
        user_id=session['user_id'],
        escuela_id=request.form.get('escuela_id'),
        fecha=request.form.get('fecha_revision'),
        
        ind_8_1=request.form.get('ind_8_1'), obs_8_1=request.form.get('obs_8_1'),
        ind_8_2=request.form.get('ind_8_2'), obs_8_2=request.form.get('obs_8_2'),
        ind_8_3=request.form.get('ind_8_3'), obs_8_3=request.form.get('obs_8_3'),
        ind_8_4=request.form.get('ind_8_4'), obs_8_4=request.form.get('obs_8_4'),
        ind_8_5=request.form.get('ind_8_5'), obs_8_5=request.form.get('obs_8_5'),
        ind_8_6=request.form.get('ind_8_6'), obs_8_6=request.form.get('obs_8_6'),
        ind_8_7=request.form.get('ind_8_7'), obs_8_7=request.form.get('obs_8_7'),
        ind_8_8=request.form.get('ind_8_8'), obs_8_8=request.form.get('obs_8_8'),
        ind_8_9=request.form.get('ind_8_9'), obs_8_9=request.form.get('obs_8_9'),
        ind_8_10=request.form.get('ind_8_10'), obs_8_10=request.form.get('obs_8_10'),
        ind_8_11=request.form.get('ind_8_11'), obs_8_11=request.form.get('obs_8_11'),

        inconsistencias=request.form.get('inconsistencias'),
        situacion_bap=request.form.get('situacion_bap'),
        observaciones_generales=request.form.get('observaciones_generales')
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('submenu_registro'))

# --- RUTAS PIPCE (Protección Civil) ---
@app.route('/registro_pipce')
def registro_pipce():
    if not session.get('user_id'): return redirect(url_for('login'))
    user_name = session.get('user_name')
    mis_escuelas = Escuela.query.filter_by(user_id=session['user_id']).all()
    return render_template('registro_pipce.html', user_name=user_name, escuelas=mis_escuelas)

@app.route('/guardar_pipce', methods=['POST'])
def guardar_pipce():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    # 1. CREAMOS LA VARIABLE 'nuevo' CON TODOS LOS DATOS
    # (Esta es la parte que probablemente faltaba o estaba incompleta)
    nuevo = PIPCE(
        user_id=session['user_id'],
        escuela_id=request.form.get('escuela_id'),
        fecha=request.form.get('fecha_revision'),
        
        # Indicadores 10.1 al 10.11
        ind_10_1=request.form.get('ind_10_1'), obs_10_1=request.form.get('obs_10_1'),
        ind_10_2=request.form.get('ind_10_2'), obs_10_2=request.form.get('obs_10_2'),
        ind_10_3=request.form.get('ind_10_3'), obs_10_3=request.form.get('obs_10_3'),
        ind_10_4=request.form.get('ind_10_4'), obs_10_4=request.form.get('obs_10_4'),
        ind_10_5=request.form.get('ind_10_5'), obs_10_5=request.form.get('obs_10_5'),
        ind_10_6=request.form.get('ind_10_6'), obs_10_6=request.form.get('obs_10_6'),
        ind_10_7=request.form.get('ind_10_7'), obs_10_7=request.form.get('obs_10_7'),
        ind_10_8=request.form.get('ind_10_8'), obs_10_8=request.form.get('obs_10_8'),
        ind_10_9=request.form.get('ind_10_9'), obs_10_9=request.form.get('obs_10_9'),
        ind_10_10=request.form.get('ind_10_10'), obs_10_10=request.form.get('obs_10_10'),
        ind_10_11=request.form.get('ind_10_11'), obs_10_11=request.form.get('obs_10_11'),

        riesgos_detectados=request.form.get('riesgos_detectados'),
        estado_equipamiento=request.form.get('estado_equipamiento'),
        acuerdos_seguridad=request.form.get('acuerdos_seguridad')
    )

    # 2. GUARDAMOS EN LA BASE DE DATOS
    db.session.add(nuevo)
    db.session.commit()
    
    # 3. AHORA SÍ, REDIRIGIMOS AL PDF (Porque 'nuevo' ya existe y tiene ID)
    return redirect(url_for('descargar_pdf_pipce', id_reporte=nuevo.id))

# --- RUTA PARA DESCARGAR PDF (WEASYPRINT) ---
@app.route('/descargar_pdf_pipce/<int:id_reporte>')
def descargar_pdf_pipce(id_reporte):
    if not session.get('user_id'): return redirect(url_for('login'))
    
    # 1. Buscamos el reporte en la Base de Datos
    reporte = PIPCE.query.get_or_404(id_reporte)
    escuela = Escuela.query.get(reporte.escuela_id)
    
    # CORRECCIÓN: AHORA USAMOS LAS FRASES COMPLETAS TAL CUAL ESTÁN EN EL FORMULARIO
    lista_indicadores = [
        {
            "texto": "Documento Vigente: ¿El PIPCE está actualizado y validado por la autoridad correspondiente?",
            "valor": reporte.ind_10_1, "obs": reporte.obs_10_1
        },
        {
            "texto": "Unidad Interna (UIPC): ¿Está formalmente constituida el Acta de Instalación de la UIPC con firmas?",
            "valor": reporte.ind_10_2, "obs": reporte.obs_10_2
        },
        {
            "texto": "Análisis de Riesgos: ¿Incluye diagnóstico de riesgos internos (instalaciones) y externos?",
            "valor": reporte.ind_10_3, "obs": reporte.obs_10_3
        },
        {
            "texto": "Brigadas Constituidas: ¿Existen las 4 brigadas básicas (Evacuación, Primeros Auxilios, Incendios, Búsqueda)?",
            "valor": reporte.ind_10_4, "obs": reporte.obs_10_4
        },
        {
            "texto": "Directorios de Emergencia: ¿Los números de emergencia están actualizados y visibles?",
            "valor": reporte.ind_10_5, "obs": reporte.obs_10_5
        },
        {
            "texto": "Equipamiento (Extintores): ¿Cuentan con extintores suficientes, vigentes y bien colocados?",
            "valor": reporte.ind_10_6, "obs": reporte.obs_10_6
        },
        {
            "texto": "Sistema de Alertamiento: ¿Disponen de alarma audible en todo el plantel conocida por la comunidad?",
            "valor": reporte.ind_10_7, "obs": reporte.obs_10_7
        },
        {
            "texto": "Señalización Normativa: ¿Cuentan con señales oficiales (Ruta de Evacuación, Punto de Reunión)?",
            "valor": reporte.ind_10_8, "obs": reporte.obs_10_8
        },
        {
            "texto": "Cronograma de Riesgos: ¿La programación de simulacros contempla distintos escenarios de riesgo?",
            "valor": reporte.ind_10_9, "obs": reporte.obs_10_9
        },
        {
            "texto": "Capacitación: ¿El personal y brigadas han recibido capacitación reciente en protección civil?",
            "valor": reporte.ind_10_10, "obs": reporte.obs_10_10
        },
        {
            "texto": "Evaluación y Bitácora: ¿Se realiza una evaluación posterior a cada simulacro y se registran los resultados en la bitácora?",
            "valor": reporte.ind_10_11, "obs": reporte.obs_10_11
        },
    ]

    # 3. Renderizamos el HTML limpio (sin estilo web, solo estilo papel)
    html_string = render_template('pdf_pipce.html',
                                  escuela=escuela.nombre,
                                  fecha=reporte.fecha,
                                  supervisor=session.get('user_name'),
                                  indicadores=lista_indicadores,
                                  riesgos=reporte.riesgos_detectados,
                                  equipamiento=reporte.estado_equipamiento,
                                  acuerdos=reporte.acuerdos_seguridad)

    # --- AGREGA ESTA LÍNEA DE DIAGNÓSTICO ---
    print("--- INICIO HTML ---")
    print(html_string) 
    print("--- FIN HTML ---")
    # ----------------------------------------
    
    
    # 4. Magia de WeasyPrint: Convertir a PDF
    pdf = HTML(string=html_string).write_pdf()

    # 5. Entregar el archivo al navegador
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    # 'inline' para ver en navegador, 'attachment' para bajar directo
    response.headers['Content-Disposition'] = f'attachment; filename=PIPCE_{escuela.nombre}.pdf'
    return response
# --------------------------
# EJECUCIÓN
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)