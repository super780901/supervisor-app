from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import make_response # Agrega esto si no está
from weasyprint import HTML     # Esto es lo nuevo
##import pdfkit  # <--- ¡ESTA ES LA QUE FALTA Y CAUSA EL ERROR!
# --- 1.1 AGREGAR AL INICIO DE APP.PY (Junto a los otros imports) ---
from flask import make_response
import pdfkit
import platform  # <--- Para detectar si es Windows o Linux
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



# --- MODELO PMC (Módulo 1 - ACTUALIZADO A 10 PUNTOS) ---
class PMC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # Indicadores 1.1 al 1.10
    ind_1_1 = db.Column(db.String(5)); obs_1_1 = db.Column(db.String(200))
    ind_1_2 = db.Column(db.String(5)); obs_1_2 = db.Column(db.String(200))
    ind_1_3 = db.Column(db.String(5)); obs_1_3 = db.Column(db.String(200))
    ind_1_4 = db.Column(db.String(5)); obs_1_4 = db.Column(db.String(200))
    ind_1_5 = db.Column(db.String(5)); obs_1_5 = db.Column(db.String(200))
    ind_1_6 = db.Column(db.String(5)); obs_1_6 = db.Column(db.String(200))
    ind_1_7 = db.Column(db.String(5)); obs_1_7 = db.Column(db.String(200))
    ind_1_8 = db.Column(db.String(5)); obs_1_8 = db.Column(db.String(200))
    ind_1_9 = db.Column(db.String(5)); obs_1_9 = db.Column(db.String(200)) # Esto era lo que faltaba
    ind_1_10 = db.Column(db.String(5)); obs_1_10 = db.Column(db.String(200)) # Y esto

    # Campos de texto abiertos
    comentarios_generales = db.Column(db.Text)
    metas_prioritarias = db.Column(db.Text)
    acuerdos = db.Column(db.Text)

    def __repr__(self):
        return f'<PMC ID: {self.id}>'
    
# app.py - Agregar debajo de la clase PMC

# --- MODELO APF (Módulo 2 - ACTUALIZADO) ---
class APF(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # 10 Indicadores
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

    # Campos de Texto (Específicos para APF)
    manejo_recursos = db.Column(db.Text)      # Dinero, cuentas claras
    participacion_social = db.Column(db.Text) # Eventos, faenas
    acuerdos_apf = db.Column(db.Text)         # Compromisos de la mesa directiva

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

# --- REEMPLAZA TU FUNCIÓN MENU ANTIGUA POR ESTA ---

@app.route('/menu')
def menu():
    # 1. Verificamos si hay un ID de usuario en la sesión
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 2. Buscamos al usuario en la Base de Datos (IGUAL QUE EN LOS OTROS MÓDULOS)
    usuario = User.query.get(session['user_id'])
    
    # 3. Seguridad: Si el usuario no aparece en la BD, limpiamos y sacamos
    if not usuario:
        session.clear()
        return redirect(url_for('login'))

    # 4. Renderizamos el menú pasando el NOMBRE REAL de la base de datos
    return render_template('menu.html', user_name=usuario.nombre)

# app.py

# En app.py

@app.route('/submenu_registro')  # <-- Esta es la dirección URL
def submenu_registro():          # <-- Este es el NOMBRE DE LA FUNCIÓN (El Puente)
    
    # 1. Protección: Si no está logueado, va pa' fuera
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 2. Obtener datos del usuario (para que salga su nombre)
    usuario = User.query.get(session['user_id'])
    
    # 3. Cargar el archivo destino
    # OJO: Aquí debe decir exactamente el nombre de tu archivo
    return render_template('submenu_registro.html', user_name=usuario.nombre if usuario else "Usuario")

    # 4 . Seguridad anti-bucle: Si el usuario no existe en BD
    if not usuario:
        session.clear()
        return redirect(url_for('login'))

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
    if not session.get('user_id'): return redirect(url_for('login'))
    
    # Recogemos los datos (Asegúrate de que coincida con tu Modelo PMC existente)
    nuevo = PMC(
        user_id=session['user_id'],
        escuela_id=request.form.get('escuela_id'),
        fecha=request.form.get('fecha_revision'),
        
        # Indicadores 1.1 al 1.10 (ajusta si tienes más o menos)
        ind_1_1=request.form.get('ind_1_1'), obs_1_1=request.form.get('obs_1_1'),
        ind_1_2=request.form.get('ind_1_2'), obs_1_2=request.form.get('obs_1_2'),
        ind_1_3=request.form.get('ind_1_3'), obs_1_3=request.form.get('obs_1_3'),
        ind_1_4=request.form.get('ind_1_4'), obs_1_4=request.form.get('obs_1_4'),
        ind_1_5=request.form.get('ind_1_5'), obs_1_5=request.form.get('obs_1_5'),
        ind_1_6=request.form.get('ind_1_6'), obs_1_6=request.form.get('obs_1_6'),
        ind_1_7=request.form.get('ind_1_7'), obs_1_7=request.form.get('obs_1_7'),
        ind_1_8=request.form.get('ind_1_8'), obs_1_8=request.form.get('obs_1_8'),
        ind_1_9=request.form.get('ind_1_9'), obs_1_9=request.form.get('obs_1_9'),
        ind_1_10=request.form.get('ind_1_10'), obs_1_10=request.form.get('obs_1_10'),

        # Campos de texto (ajusta los nombres si usaste otros en tu modelo original)
        comentarios_generales=request.form.get('comentarios_generales'),
        metas_prioritarias=request.form.get('metas_prioritarias'),
        acuerdos=request.form.get('acuerdos')
    )
    db.session.add(nuevo)
    db.session.commit()
    
    # REDIRECCIÓN A DESCARGA PDF
    return redirect(url_for('descargar_pdf_pmc', id_reporte=nuevo.id))

# --- RUTA DE DESCARGA PMC (ACTUALIZADA) ---

# --- RUTAS APF (Módulo 2) ---


@app.route('/descargar_pdf_apf/<int:id_reporte>')
def descargar_pdf_apf(id_reporte):
    if not session.get('user_id'): return redirect(url_for('login'))
    
    reporte = APF.query.get_or_404(id_reporte)
    escuela = Escuela.query.get(reporte.escuela_id)
    
    # DATOS DE ZONA (Igual que en PMC)
    supervisor_user = User.query.get(session['user_id'])
    nombre_supervisor = supervisor_user.nombre
    nombre_zona = supervisor_user.nombre_cct
    texto_zona_formal = f"ZONA ESCOLAR: {nombre_zona}"

    # LISTA DE INDICADORES APF (Propuesta estándar)
    lista_indicadores = [
        {"texto": "¿Está constituida el Acta de la APF del ciclo escolar vigente?", "valor": reporte.ind_2_1, "obs": reporte.obs_2_1},
        {"texto": "¿La Mesa Directiva cuenta con registro ante la autoridad educativa?", "valor": reporte.ind_2_2, "obs": reporte.obs_2_2},
        {"texto": "¿Existe un Plan de Trabajo anual de la APF?", "valor": reporte.ind_2_3, "obs": reporte.obs_2_3},
        {"texto": "¿Se realizan asambleas ordinarias informativas con los padres?", "valor": reporte.ind_2_4, "obs": reporte.obs_2_4},
        {"texto": "¿Llevan libro de actas y acuerdos actualizado?", "valor": reporte.ind_2_5, "obs": reporte.obs_2_5},
        {"texto": "¿Existe transparencia y cortes de caja sobre las aportaciones voluntarias?", "valor": reporte.ind_2_6, "obs": reporte.obs_2_6},
        {"texto": "¿La APF apoya en el mantenimiento y limpieza del plantel?", "valor": reporte.ind_2_7, "obs": reporte.obs_2_7},
        {"texto": "¿Participan en los Consejos de Participación Escolar?", "valor": reporte.ind_2_8, "obs": reporte.obs_2_8},
        {"texto": "¿Existe un clima de colaboración entre APF y Dirección?", "valor": reporte.ind_2_9, "obs": reporte.obs_2_9},
        {"texto": "¿Se respetan los reglamentos respecto al no condicionamiento de servicios?", "valor": reporte.ind_2_10, "obs": reporte.obs_2_10},
    ]

    html_string = render_template('pdf_apf.html',
                                  escuela=escuela.nombre,
                                  zona_escolar=texto_zona_formal,
                                  fecha=reporte.fecha,
                                  supervisor=nombre_supervisor,
                                  indicadores=lista_indicadores,
                                  recursos=reporte.manejo_recursos,
                                  participacion=reporte.participacion_social,
                                  acuerdos=reporte.acuerdos_apf)

    pdf = HTML(string=html_string).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=APF_{escuela.nombre}.pdf'
    return response


@app.route('/registro_apf')
def registro_apf():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    user_name = session.get('user_name')
    mis_escuelas = Escuela.query.filter_by(user_id=session['user_id']).all()
    
    return render_template('registro_apf.html', user_name=user_name, escuelas=mis_escuelas)

@app.route('/guardar_apf', methods=['POST'])
def guardar_apf():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    nuevo = APF(
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

        manejo_recursos=request.form.get('manejo_recursos'),
        participacion_social=request.form.get('participacion_social'),
        acuerdos_apf=request.form.get('acuerdos_apf')
    )
    db.session.add(nuevo)
    db.session.commit()
    
    return redirect(url_for('descargar_pdf_apf', id_reporte=nuevo.id))





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



# app.py - Modelo para CTE
# --- MODELO CTE (Módulo 7) ---
class CTE(db.Model):
    __tablename__ = 'cte'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # 10 Indicadores (7.1 al 7.10)
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

    # Campos de Texto Específicos para CTE
    temas_tratados = db.Column(db.Text)   # Resumen de temas
    avances_pemc = db.Column(db.Text)     # Análisis del PEMC
    acuerdos_cte = db.Column(db.Text)     # Acuerdos finales


# --- RUTAS CTE (Módulo 7) ---

@app.route('/registro_cte')
def registro_cte():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    # Obtener usuario real y escuelas
    usuario = User.query.get(session['user_id'])
    escuelas = Escuela.query.all()
    
    return render_template('registro_cte.html', 
                           escuelas=escuelas, 
                           user_name=usuario.nombre)

@app.route('/guardar_cte', methods=['POST'])
def guardar_cte():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    nuevo = CTE(
        user_id=session['user_id'],
        escuela_id=request.form.get('escuela_id'),
        fecha=request.form.get('fecha_revision'),
        
        # Indicadores 7.1 al 7.10
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

        # Campos de texto
        temas_tratados=request.form.get('temas_tratados'),
        avances_pemc=request.form.get('avances_pemc'),
        acuerdos_cte=request.form.get('acuerdos_cte')
    )
    db.session.add(nuevo)
    db.session.commit()
    
    # --- ESTA ES LA LÍNEA CLAVE ---
    return redirect(url_for('descargar_pdf_cte', id_reporte=nuevo.id))


@app.route('/descargar_pdf_cte/<int:id_reporte>')
def descargar_pdf_cte(id_reporte):
    if not session.get('user_id'): return redirect(url_for('login'))
    
    reporte = CTE.query.get_or_404(id_reporte)
    escuela = Escuela.query.get(reporte.escuela_id)
    supervisor_user = User.query.get(session['user_id'])
    
    # LISTA DE INDICADORES (CTE)
    lista_indicadores = [
        {"texto": "Quórum y Organización: ¿Está presente la totalidad del personal docente y directivo convocados e iniciaron puntualmente?", "valor": reporte.ind_7_1, "obs": reporte.obs_7_1},
        {"texto": "Insumos y Datos: ¿Cuentan con la información necesaria (evaluaciones, listas, fichas) organizada para su análisis?", "valor": reporte.ind_7_2, "obs": reporte.obs_7_2},
        {"texto": "Liderazgo Directivo: ¿El director(a) conduce promoviendo el diálogo profesional (no solo lectura de la guía)?", "valor": reporte.ind_7_3, "obs": reporte.obs_7_3},
        {"texto": "Apego a los Propósitos: ¿Las actividades corresponden a los objetivos de la Guía de Trabajo oficial?", "valor": reporte.ind_7_4, "obs": reporte.obs_7_4},
        {"texto": "Análisis del PEMC: ¿Se revisan los avances, metas y acciones comprometidas en el Programa Escolar de Mejora Continua?", "valor": reporte.ind_7_5, "obs": reporte.obs_7_5},
        {"texto": "Alumnos en Riesgo: ¿Se identifican nominalmente a los alumnos que requieren apoyo y se diseñan estrategias?", "valor": reporte.ind_7_6, "obs": reporte.obs_7_6},
        {"texto": "Trabajo Colaborativo: ¿Existe participación activa y propositiva de los docentes (intercambio de estrategias)?", "valor": reporte.ind_7_7, "obs": reporte.obs_7_7},
        {"texto": "Uso del Tiempo: ¿Se utiliza el tiempo exclusivamente para asuntos técnico-pedagógicos (evitando temas sindicales/sociales)?", "valor": reporte.ind_7_8, "obs": reporte.obs_7_8},
        {"texto": "Acuerdos y Compromisos: ¿Se establecen acuerdos concretos, medibles y con responsables claros?", "valor": reporte.ind_7_9, "obs": reporte.obs_7_9},
        {"texto": "Registro en Bitácora: ¿Los acuerdos tomados quedan asentados formalmente en el Cuaderno de Bitácora del CTE?", "valor": reporte.ind_7_10, "obs": reporte.obs_7_10}
    ]

    html_string = render_template('pdf_cte.html',
                                  escuela=escuela.nombre,
                                  zona_escolar=f"ZONA ESCOLAR: {supervisor_user.nombre_cct}",
                                  fecha=reporte.fecha,
                                  supervisor=supervisor_user.username,
                                  indicadores=lista_indicadores,
                                  temas=reporte.temas_tratados,
                                  pemc=reporte.avances_pemc,
                                  acuerdos=reporte.acuerdos_cte)

    pdf = HTML(string=html_string).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=CTE_{escuela.nombre}.pdf'
    return response

# app.py - Modelo Cooperativa (Grupo 5)

# --- RUTAS COOPERATIVA ---
# --- MODELO COOPERATIVA (Módulo 8) ---
class Cooperativa(db.Model):
    __tablename__ = 'cooperativa'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # 11 Indicadores (8.1 al 8.11)
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

    # Campos de Texto Específicos
    obs_general = db.Column(db.Text)          # Observaciones generales
    estado_contabilidad = db.Column(db.Text)  # Sobre libros y cuentas
    acuerdos_cooperativa = db.Column(db.Text) # Compromisos

# --- RUTAS COOPERATIVA ---
# --- RUTAS COOPERATIVA (Módulo 8) ---

@app.route('/registro_cooperativa')
def registro_cooperativa():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    # Buscamos al usuario para obtener su NOMBRE REAL
    usuario = User.query.get(session['user_id'])
    escuelas = Escuela.query.all()
    
    return render_template('registro_cooperativa.html', 
                           escuelas=escuelas, 
                           user_name=usuario.nombre)

@app.route('/guardar_cooperativa', methods=['POST'])
def guardar_cooperativa():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    nuevo = Cooperativa(
        user_id=session['user_id'],
        escuela_id=request.form.get('escuela_id'),
        fecha=request.form.get('fecha_revision'),
        
        # 11 Indicadores
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

        # Campos de texto
        obs_general=request.form.get('obs_general'),
        estado_contabilidad=request.form.get('estado_contabilidad'),
        acuerdos_cooperativa=request.form.get('acuerdos_cooperativa')
    )
    db.session.add(nuevo)
    db.session.commit()
    
    return redirect(url_for('descargar_pdf_cooperativa', id_reporte=nuevo.id))

@app.route('/descargar_pdf_cooperativa/<int:id_reporte>')
def descargar_pdf_cooperativa(id_reporte):
    if not session.get('user_id'): return redirect(url_for('login'))
    
    reporte = Cooperativa.query.get_or_404(id_reporte)
    escuela = Escuela.query.get(reporte.escuela_id)
    supervisor_user = User.query.get(session['user_id'])
    
    # LISTA DE INDICADORES (COOPERATIVA)
    lista_indicadores = [
        {"texto": "Acta Constitutiva: ¿Cuenta con el Acta de Constitución del Comité de la Cooperativa Escolar vigente y debidamente firmada?", "valor": reporte.ind_8_1, "obs": reporte.obs_8_1},
        {"texto": "Documentos Físicos y Actualizados: (Libro contable, Libro de actas, Registro de venta semanal, Cuadernos de notas, Cuenta bancaria).", "valor": reporte.ind_8_2, "obs": reporte.obs_8_2},
        {"texto": "Certificados de Salud: ¿El personal cuenta con tarjeta de salud vigente y vestimenta adecuada (cofia, mandil, cubrebocas)?", "valor": reporte.ind_8_3, "obs": reporte.obs_8_3},
        {"texto": "Higiene del Local: ¿El espacio físico se encuentra limpio, iluminado, ventilado y libre de fauna nociva?", "valor": reporte.ind_8_4, "obs": reporte.obs_8_4},
        {"texto": "Alimentos Permitidos: ¿La oferta evita productos con 'Sellos de Advertencia' y comida chatarra?", "valor": reporte.ind_8_5, "obs": reporte.obs_8_5},
        {"texto": "Precios a la Vista: ¿La lista de precios está exhibida públicamente y corresponde a lo autorizado?", "valor": reporte.ind_8_6, "obs": reporte.obs_8_6},
        {"texto": "Comité de Vigilancia: ¿El Comité lleva un registro de la verificación de alimentos, calidad y precios?", "valor": reporte.ind_8_7, "obs": reporte.obs_8_7},
        {"texto": "Comisión de Educación Cooperativa: ¿La comisión lleva un registro de las actividades de difusión con enfoque educativo?", "valor": reporte.ind_8_8, "obs": reporte.obs_8_8},
        {"texto": "Libro Contable (Operación): ¿Se lleva un registro diario de ventas, egresos y utilidad neta en el Libro autorizado?", "valor": reporte.ind_8_9, "obs": reporte.obs_8_9},
        {"texto": "Cuenta Bancaria Mancomunada: ¿Los recursos se resguardan en cuenta mancomunada y no en efectivo o cuentas personales?", "valor": reporte.ind_8_10, "obs": reporte.obs_8_10},
        {"texto": "Rendición de Cuentas: ¿Se conserva evidencia de los informes financieros a la comunidad escolar?", "valor": reporte.ind_8_11, "obs": reporte.obs_8_11}
    ]

    html_string = render_template('pdf_cooperativa.html',
                                  escuela=escuela.nombre,
                                  zona_escolar=f"ZONA ESCOLAR: {supervisor_user.nombre_cct}",
                                  fecha=reporte.fecha,
                                  supervisor=supervisor_user.username,
                                  indicadores=lista_indicadores,
                                  obs_general=reporte.obs_general,
                                  contabilidad=reporte.estado_contabilidad,
                                  acuerdos=reporte.acuerdos_cooperativa)

    pdf = HTML(string=html_string).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=Cooperativa_{escuela.nombre}.pdf'
    return response


# --- MODELO INVENTARIO (Grupo 6) ---
# --- MODELO INVENTARIOS (Ajustado a Indicadores 6.x) ---
class Inventarios(db.Model):
    __tablename__ = 'inventarios'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # 10 Indicadores (6.1 al 6.10)
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

    # Campos de Texto Específicos
    discrepancias = db.Column(db.Text)
    estado_general = db.Column(db.Text)
    necesidades = db.Column(db.Text)


# --- RUTAS INVENTARIO ---
# --- RUTAS INVENTARIOS (Con indicadores 6.x) ---
@app.route('/registro_inventarios')
def registro_inventarios():
    # 1. Verificar si hay sesión
    if not session.get('user_id'): 
        return redirect(url_for('login'))
    
    # 2. Obtener el usuario REAL de la base de datos
    usuario = User.query.get(session['user_id'])
    
    # 3. Obtener escuelas
    escuelas = Escuela.query.all()
    
    # 4. Renderizar pasando el nombre correcto (usuario.username)
    return render_template('registro_inventarios.html', 
                           escuelas=escuelas, 
                           user_name=usuario.nombre)
    
    
@app.route('/guardar_inventarios', methods=['POST'])
def guardar_inventarios():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    nuevo = Inventarios(
        user_id=session['user_id'],
        escuela_id=request.form.get('escuela_id'),
        fecha=request.form.get('fecha_revision'),
        
        # Guardamos los indicadores 6.1 al 6.10
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
        estado_general=request.form.get('estado_general'),
        necesidades=request.form.get('necesidades')
    )
    db.session.add(nuevo)
    db.session.commit()
    
    return redirect(url_for('descargar_pdf_inventarios', id_reporte=nuevo.id))

@app.route('/descargar_pdf_inventarios/<int:id_reporte>')
def descargar_pdf_inventarios(id_reporte):
    if not session.get('user_id'): return redirect(url_for('login'))
    
    reporte = Inventarios.query.get_or_404(id_reporte)
    escuela = Escuela.query.get(reporte.escuela_id)
    supervisor_user = User.query.get(session['user_id'])
    
    # LISTA EXACTA PROPORCIONADA POR TI
    lista_indicadores = [
        {"texto": "Inventario Oficial: ¿Cuenta con el inventario general actualizado y validado por la autoridad competente?", "valor": reporte.ind_6_1, "obs": reporte.obs_6_1},
        {"texto": "Resguardos Individuales: ¿Existen resguardos firmados por cada docente/administrativo de los bienes bajo su custodia?", "valor": reporte.ind_6_2, "obs": reporte.obs_6_2},
        {"texto": "Etiquetado: ¿Los bienes cuentan con número de inventario o etiqueta visible y legible?", "valor": reporte.ind_6_3, "obs": reporte.obs_6_3},
        {"texto": "Verificación Física (Muestreo): ¿Existe correspondencia física al verificar aleatoriamente 5 artículos contra el listado?", "valor": reporte.ind_6_4, "obs": reporte.obs_6_4},
        {"texto": "Trámite de Bajas: ¿El mobiliario inservible cuenta con dictamen de baja o trámite en proceso (no solo arrumbado)?", "valor": reporte.ind_6_5, "obs": reporte.obs_6_5},
        {"texto": "Equipo Tecnológico: ¿El equipo de cómputo y audiovisual está completo, funcional y resguardado seguro?", "valor": reporte.ind_6_6, "obs": reporte.obs_6_6},
        {"texto": "Donaciones y Adquisiciones: ¿Se han incorporado al inventario los bienes adquiridos por APF, Cooperativa o donaciones?", "valor": reporte.ind_6_7, "obs": reporte.obs_6_7},
        {"texto": "Control de Llaves: ¿Existe un control/duplicado de llaves de las áreas con bienes de alto valor?", "valor": reporte.ind_6_8, "obs": reporte.obs_6_8},
        {"texto": "Reportes de Robo/Extravío: ¿En caso de faltantes, se cuenta con denuncia ante MP y notificación oficial?", "valor": reporte.ind_6_9, "obs": reporte.obs_6_9},
        {"texto": "Almacenamiento: ¿Las bodegas están ordenadas, limpias y libres de material de riesgo?", "valor": reporte.ind_6_10, "obs": reporte.obs_6_10},
    ]

    html_string = render_template('pdf_inventarios.html',
                                  escuela=escuela.nombre,
                                  zona_escolar=f"ZONA ESCOLAR: {supervisor_user.nombre_cct}",
                                  fecha=reporte.fecha,
                                  supervisor=supervisor_user.nombre,
                                  indicadores=lista_indicadores,
                                  discrepancias=reporte.discrepancias,
                                  estado=reporte.estado_general,
                                  necesidades=reporte.necesidades)

    pdf = HTML(string=html_string).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=Inventario_{escuela.nombre}.pdf'
    return response


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

# --- MODELO CONTROL ESCOLAR (Módulo 3 - 11 INDICADORES) ---
class ControlEscolar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # 11 Indicadores
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
    # EL NUEVO INDICADOR 11:
    ind_3_11 = db.Column(db.String(5)); obs_3_11 = db.Column(db.String(200))

    # Campos de Texto
    obs_expedientes = db.Column(db.Text)
    obs_plataforma = db.Column(db.Text)
    acuerdos_control = db.Column(db.Text)

# --- MODELO PIPCE (Grupo 10 - Actualizado 11 items) ---
# --- MODELO PIPCE (Módulo 5) ---
class PIPCE(db.Model):
    __tablename__ = 'pipce'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    escuela_id = db.Column(db.Integer, db.ForeignKey('escuela.id'), nullable=False)
    
    # 11 Indicadores (5.1 al 5.11)
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

    # Campos de Texto Específicos para Protección Civil
    obs_general = db.Column(db.Text)      # Observaciones generales
    obs_simulacros = db.Column(db.Text)   # Detalles sobre simulacros
    acuerdos_pipce = db.Column(db.Text)   # Compromisos

@app.route('/registro_control_escolar')
def registro_control_escolar():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    # Obtenemos las escuelas para el desplegable
    escuelas = Escuela.query.all()
    
    return render_template('registro_control_escolar.html', 
                           escuelas=escuelas, 
                           user_name=session.get('nombre')) # O session.get('user_name') según como lo guardes en login


# --- RUTAS CONTROL ESCOLAR (Módulo 3 - Actualizado a 11) ---

@app.route('/guardar_control_escolar', methods=['POST'])
def guardar_control_escolar():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    nuevo = ControlEscolar(
        user_id=session['user_id'],
        escuela_id=request.form.get('escuela_id'),
        fecha=request.form.get('fecha_revision'),
        
        # Guardamos los 11 Indicadores
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
        ind_3_11=request.form.get('ind_3_11'), obs_3_11=request.form.get('obs_3_11'), # <--- NUEVO

        obs_expedientes=request.form.get('obs_expedientes'),
        obs_plataforma=request.form.get('obs_plataforma'),
        acuerdos_control=request.form.get('acuerdos_control')
    )
    db.session.add(nuevo)
    db.session.commit()
    
    return redirect(url_for('descargar_pdf_control_escolar', id_reporte=nuevo.id))

@app.route('/descargar_pdf_control_escolar/<int:id_reporte>')
def descargar_pdf_control_escolar(id_reporte):
    if not session.get('user_id'): return redirect(url_for('login'))
    
    reporte = ControlEscolar.query.get_or_404(id_reporte)
    escuela = Escuela.query.get(reporte.escuela_id)
    supervisor_user = User.query.get(session['user_id'])
    
    # 11 ITEMS EN LA LISTA
    lista_indicadores = [
        {"texto": "Matrícula Escolar: ¿El número de alumnos inscritos físicamente coincide con la estadística oficial reportada?", "valor": reporte.ind_3_1, "obs": reporte.obs_3_1},
        {"texto": "Plataforma SIIE Web: ¿La información cargada en el sistema (alumnos, grupos, docentes) está actualizada y sin errores?", "valor": reporte.ind_3_2, "obs": reporte.obs_3_2},
        {"texto": "Expedientes de Alumnos: ¿Están organizados y cuentan con documentación normativa (Acta, CURP, Boletas)?", "valor": reporte.ind_3_3, "obs": reporte.obs_3_3},
        {"texto": "Altas y Bajas: ¿Los movimientos de ingreso y baja cuentan con el soporte documental correspondiente?", "valor": reporte.ind_3_4, "obs": reporte.obs_3_4},
        {"texto": "Registro de Asistencia: ¿Los docentes llevan control diario y reportan ausentismo a la dirección?", "valor": reporte.ind_3_5, "obs": reporte.obs_3_5},
        {"texto": "Alumnos con BAP: ¿Se tiene censo y seguimiento de alumnos con Barreras para el Aprendizaje y la Participación?", "valor": reporte.ind_3_6, "obs": reporte.obs_3_6},
        {"texto": "Registro de Incidencias: ¿Cuentan con Bitácora de Incidencias (conducta/salud) foliada y en uso?", "valor": reporte.ind_3_7, "obs": reporte.obs_3_7},
        {"texto": "Expediente de Becas: ¿Está completo con solicitudes, asignaciones y nóminas firmadas?", "valor": reporte.ind_3_8, "obs": reporte.obs_3_8},
        {"texto": "Evaluación (Boletas): ¿Existe evidencia de entrega de boletas firmadas por los padres?", "valor": reporte.ind_3_9, "obs": reporte.obs_3_9},
        {"texto": "Libros de Texto: ¿Se cuenta con acuses de recibo de la entrega total a los alumnos?", "valor": reporte.ind_3_10, "obs": reporte.obs_3_10},
        # AGREGAR AQUÍ EL TEXTO DE TU INDICADOR 11:
        {"texto": "Certificación: (En su caso) ¿La documentación para certificación de 6° grado está en orden?", "valor": reporte.ind_3_11, "obs": reporte.obs_3_11}, 
    ]

    html_string = render_template('pdf_control_escolar.html',
                                  escuela=escuela.nombre,
                                  zona_escolar=f"ZONA ESCOLAR: {supervisor_user.nombre_cct}",
                                  fecha=reporte.fecha,
                                  supervisor=supervisor_user.nombre,
                                  indicadores=lista_indicadores,
                                  expedientes=reporte.obs_expedientes,
                                  plataforma=reporte.obs_plataforma,
                                  acuerdos=reporte.acuerdos_control)

    pdf = HTML(string=html_string).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=ControlEscolar_{escuela.nombre}.pdf'
    return response

# --- RUTAS PIPCE (Protección Civil) ---
# --- RUTAS PIPCE (Módulo 5) ---

@app.route('/registro_pipce')
def registro_pipce():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    # Corrección de nombre aplicada:
    usuario = User.query.get(session['user_id'])
    escuelas = Escuela.query.all()
    
    return render_template('registro_pipce.html', 
                           escuelas=escuelas, 
                           user_name=usuario.username)

@app.route('/guardar_pipce', methods=['POST'])
def guardar_pipce():
    if not session.get('user_id'): return redirect(url_for('login'))
    
    nuevo = PIPCE(
        user_id=session['user_id'],
        escuela_id=request.form.get('escuela_id'),
        fecha=request.form.get('fecha_revision'),
        
        # 11 Indicadores
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

        # Campos de texto
        obs_general=request.form.get('obs_general'),
        obs_simulacros=request.form.get('obs_simulacros'),
        acuerdos_pipce=request.form.get('acuerdos_pipce')
    )
    db.session.add(nuevo)
    db.session.commit()
    
    return redirect(url_for('descargar_pdf_pipce', id_reporte=nuevo.id))

@app.route('/descargar_pdf_pipce/<int:id_reporte>')
def descargar_pdf_pipce(id_reporte):
    if not session.get('user_id'): return redirect(url_for('login'))
    
    reporte = PIPCE.query.get_or_404(id_reporte)
    escuela = Escuela.query.get(reporte.escuela_id)
    supervisor_user = User.query.get(session['user_id'])
    
    # TUS INDICADORES EXACTOS
    lista_indicadores = [
        {"texto": "Documento Vigente: ¿El PIPCE está actualizado y validado por la autoridad correspondiente?", "valor": reporte.ind_5_1, "obs": reporte.obs_5_1},
        {"texto": "Unidad Interna (UIPC): ¿Está formalmente constituida el Acta de Instalación de la UIPC con firmas?", "valor": reporte.ind_5_2, "obs": reporte.obs_5_2},
        {"texto": "Análisis de Riesgos: ¿Incluye diagnóstico de riesgos internos (instalaciones) y externos?", "valor": reporte.ind_5_3, "obs": reporte.obs_5_3},
        {"texto": "Brigadas Constituidas: ¿Existen las 4 brigadas básicas (Evacuación, Primeros Auxilios, Incendios, Búsqueda)?", "valor": reporte.ind_5_4, "obs": reporte.obs_5_4},
        {"texto": "Directorios de Emergencia: ¿Los números de emergencia están actualizados y visibles?", "valor": reporte.ind_5_5, "obs": reporte.obs_5_5},
        {"texto": "Equipamiento (Extintores): ¿Cuentan con extintores suficientes, vigentes y bien colocados?", "valor": reporte.ind_5_6, "obs": reporte.obs_5_6},
        {"texto": "Sistema de Alertamiento: ¿Disponen de alarma audible en todo el plantel conocida por la comunidad?", "valor": reporte.ind_5_7, "obs": reporte.obs_5_7},
        {"texto": "Señalización Normativa: ¿Cuentan con señales oficiales (Ruta de Evacuación, Punto de Reunión)?", "valor": reporte.ind_5_8, "obs": reporte.obs_5_8},
        {"texto": "Cronograma de Riesgos: ¿La programación de simulacros contempla distintos escenarios de riesgo?", "valor": reporte.ind_5_9, "obs": reporte.obs_5_9},
        {"texto": "Capacitación: ¿El personal y brigadas han recibido capacitación reciente en protección civil?", "valor": reporte.ind_5_10, "obs": reporte.obs_5_10},
        {"texto": "Evaluación y Bitácora: ¿Se realiza una evaluación posterior a cada simulacro y se registran los resultados?", "valor": reporte.ind_5_11, "obs": reporte.obs_5_11}
    ]

    html_string = render_template('pdf_pipce.html',
                                  escuela=escuela.nombre,
                                  zona_escolar=f"ZONA ESCOLAR: {supervisor_user.nombre_cct}",
                                  fecha=reporte.fecha,
                                  supervisor=supervisor_user.nombre, # Nombre real
                                  indicadores=lista_indicadores,
                                  obs_general=reporte.obs_general,
                                  obs_simulacros=reporte.obs_simulacros,
                                  acuerdos=reporte.acuerdos_pipce)

    pdf = HTML(string=html_string).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=PIPCE_{escuela.nombre}.pdf'
    return response

# --- AGREGAR EN APP.PY ---

@app.route('/registro_asistencia')
def registro_asistencia():
    # 1. Seguridad: Verificar login
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 2. Obtener datos necesarios
    usuario = User.query.get(session['user_id'])
    escuelas = Escuela.query.all()  # <--- IMPORTANTE: Necesario para llenar el select de escuelas
    
    # 3. Mostrar la página
    return render_template('registro_asistencia.html', 
                           user_name=usuario.nombre, 
                           escuelas=escuelas)


# --- 1.2 LA FUNCIÓN COMPLETA (Reemplaza cualquier versión anterior de guardar_asistencia) ---
@app.route('/guardar_asistencia', methods=['POST'])
def guardar_asistencia():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    usuario = User.query.get(session['user_id'])
    
    # 1. Recibir datos del formulario
    escuela_id = request.form.get('escuela_id')
    fecha_revision = request.form.get('fecha_revision')
    
    # Buscar nombre de la escuela
    obj_escuela = Escuela.query.get(escuela_id)
    nombre_escuela = obj_escuela.nombre if obj_escuela else "Desconocida"
    # Ajusta esto si tienes la zona en la BD
    zona_texto = "ZONA ESCOLAR 078" 

    # 2. Armar la lista de indicadores
# ... dentro de def guardar_asistencia(): ...

    # 2. Armar la lista de indicadores (VERSIÓN CON TEXTO COMPLETO)
    textos_indicadores = [
        "Disponibilidad y Ubicación: ¿El libro se encuentra en un lugar accesible y visible al momento de la visita?",
        "Apertura Oficial: ¿Cuenta con la autorización y sello de apertura por parte de la Supervisión Escolar al inicio del ciclo?",
        "Formato e Integridad: ¿El libro está libre de tachaduras, enmendaduras, uso de corrector o renglones en blanco injustificados?",
        "Registro Cronológico: ¿Los registros de asistencia corresponden estrictamente al día en curso (sin firmas adelantadas)?",
        "Horarios Contractuales: ¿La hora de entrada registrada por los docentes coincide con su horario laboral oficial?",
        "Registro de Salida: ¿El personal registra su hora de salida al término de la jornada laboral?",
        "Firmas Autógrafas: ¿Las firmas corresponden al puño y letra del personal (se descarta firma de terceros)?",
        "Registro de Incidencias: ¿Están señaladas claramente las inasistencias, retardos, permisos económicos o licencias médicas en el día correspondiente?",
        "Cierre Diario: ¿El director cancela los espacios vacíos y cierra el registro diariamente con su firma/visto bueno?",
        "Plantilla Completa: ¿Coincide el número de personas registradas (o justificadas) con la plantilla de personal real de la escuela?"
    ]
    
    # ... el resto de la función sigue igual ...
    
    lista_indicadores = []
    for i in range(1, 11):
        lista_indicadores.append({
            'numero': f"3.{i}",
            'texto': textos_indicadores[i-1],
            'valor': request.form.get(f'ind_3_{i}', ''), 
            'obs': request.form.get(f'obs_3_{i}', '')
        })

    # 3. Recibir textos largos
    personal = request.form.get('personal_incidencias', '')
    irregularidades = request.form.get('irregularidades', '')
    recomendaciones = request.form.get('recomendaciones', '')

    # 4. Generar el PDF
    html_content = render_template(
        'pdf_asistencia.html',
        zona_escolar=zona_texto,
        escuela=nombre_escuela,
        fecha=fecha_revision,
        supervisor=usuario.nombre,
        indicadores=lista_indicadores,
        personal_incidencias=personal,
        irregularidades=irregularidades,
        recomendaciones=recomendaciones
    )

    # Configuración de PDF (Directo al navegador)
   # ... (código anterior del render_template) ...

    # --- CONFIGURACIÓN INTELIGENTE (DETECTA WINDOWS O LINUX) ---
    if platform.system() == "Windows":
        # Ruta para TU computadora
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    else:
        # Ruta para el SERVIDOR (PythonAnywhere)
        # En PythonAnywhere suele estar en /usr/bin/wkhtmltopdf
        path_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # Generamos el PDF usando la configuración detectada
    pdf = pdfkit.from_string(html_content, False, configuration=config)
    
    response = make_response(pdf)
    # ... (resto de la función igual) ...


# --------------------------
# EJECUCIÓN
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)