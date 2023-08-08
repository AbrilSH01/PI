from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import UserMixin
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename
from functools import wraps
#inicialización del servidor Flask
app = Flask(__name__)

#Configuracion de la conexion
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="cafeteriaapp"
app.config['UPLOAD_FOLDER'] = 'Proyecto integrador/static/img'

app.secret_key='mysecretkey'


mysql= MySQL(app)

#Declaramos una ruta
#ruta Index http://localhost:5000
#ruta se compone de nombre y funcion
@app.route('/')
def index():
     return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        VMat = request.form['txtMat']
        VNom = request.form['txtNom']
        VAp = request.form['txtAp']
        VCorr = request.form['txtCorr']
        VPass = request.form['txtPass']
        
        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO usuario (Matricula,Nombre, Apellidos, Correo, Contraseña, Rol) VALUES (%s,%s, %s, %s, %s,2)', (VMat, VNom, VAp, VCorr, VPass))
        mysql.connection.commit()
        flash('Usuario agregado correctamente')
        return redirect(url_for('index'))

    return render_template('registro_usuarios.html')
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si el correo electrónico está almacenado en la sesión
        if 'Matricula' not in session:
            # Redirigir al inicio de sesión si no ha iniciado sesión
            flash('Debe iniciar sesión para acceder a esta página.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        VCorr = request.form['txtCorr']
        VPass = request.form['txtPass']
        
        # Conectamos a la base de datos
        CS = mysql.connection.cursor()
        
        # Verificar las credenciales en la base de datos
        consulta = "SELECT Correo FROM usuario WHERE Correo = %s AND Contraseña = %s"
        CS.execute(consulta, (VCorr, VPass))
        resultado = CS.fetchone()
        Rol = "Select Rol, Matricula from usuario where correo = %s and contraseña = %s"
        
        # Verificar si las credenciales son válidas
        if resultado is not None:
            CS.execute(Rol,(VCorr, VPass))
            rol_resultado = CS.fetchone()
            if rol_resultado is not None and rol_resultado[0] == 1:
                 # Almacenar el ID del usuario en la sesión para marcarlo como autenticado
                session['Matricula'] = rol_resultado[1]
            # Las credenciales son válidas, redirigir al menú principal
                return redirect(url_for('main'))
            else:
                session['Matricula'] = rol_resultado[1]
                return redirect(url_for('cliente'))
        else:
            # Las credenciales son inválidas, redirigir a la página de inicio de sesión con un mensaje de error
            flash('Correo o contraseña incorrectos. Intente nuevamente.')
            return redirect(url_for('login'))
    return render_template('login.html')



@app.route('/main', methods=['GET'])
@login_required
def main():
    return render_template('main_menu.html')


@app.route('/cliente', methods=['GET'])
@login_required
def cliente():
    return render_template('mm_cl.html')


@app.route('/menu', methods=['GET', 'POST'])
@login_required
def menu():

    # Obtener todos los productos de la base de datos
    productos = obtener_productos()

    # Renderizar la plantilla HTML y pasar la lista de productos
    ultimo_folio = obtener_ultimo_folio()
    user_id = session.get('Matricula')
    cursorBU = mysql.connection.cursor()
    cursorBU.execute('SELECT t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad, t.total FROM ticket t INNER JOIN Menu m ON t.id_producto = m.ID where t.id_cliente = %s and t.folio_ticket = %s',(user_id, ultimo_folio))
    consBU = cursorBU.fetchall()
    flash("Su orden es la numero " + str(ultimo_folio) + ", Favor de pagar en caja") 
    return render_template('menu.html', productos=productos, listaPedido=consBU)




    

def obtener_productos():
    # Conexión a la base de datos MySQL
   
    cursor = mysql.connection.cursor()

    # Obtener todos los productos de la tabla "productos"
    cursor.execute('SELECT * FROM Menu')
    productos = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()

    return productos

def agregar_producto(nombre, precio):
    # Conexión a la base de datos MySQL
    cursor = mysql.connection.cursor()

    # Insertar el producto en la tabla "productos"
    cursor.execute('INSERT INTO Menu (producto, precio) VALUES (%s, %s)', (nombre, precio))

    # Guardar los cambios en la base de datos
    cursor.commit()

    # Cerrar la conexión a la base de datos
    cursor.close()

@app.route('/orden', methods=['GET', 'POST'])
@login_required
def orden():
    
    

    # Obtener todos los productos de la base de datos
    productos = obtener_productos()

    # Obtener el último folio incrementado
    nuevo_folio = obtener_ultimo_folio()

    # Renderizar la plantilla HTML y pasar la lista de productos y el nuevo folio
    user_id = session.get('Matricula')
    cursorBU = mysql.connection.cursor()
    cursorBU.execute('SELECT t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad, sum(t.cantidad *  m.precio) FROM ticket t INNER JOIN Menu m ON t.id_producto = m.ID where t.id_cliente = %s and t.folio_ticket = %s group by t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad',(user_id, nuevo_folio))
    consBU = cursorBU.fetchall()
    if not consBU:
        flash('No se realizó ninguna orden, por favor ordene algun producto.')
        return redirect(url_for('menu'))
    else:
        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO orden (x) VALUES (1)')
        mysql.connection.commit()
        
    
        return render_template('orden.html', productos=productos, listaPedido=consBU, nuevo_folio=nuevo_folio)
    

def obtener_ultimo_folio():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT MAX(ID) FROM orden')
    ultimo_folio = cursor.fetchone()[0]
    cursor.close()

    return ultimo_folio or 1



@app.route('/buscar', methods=['POST', 'GET'])
@login_required
def buscar():
    if request.method == 'POST':
        VBusc = request.form['busc']
        
        cursorBU = mysql.connection.cursor()
        if not VBusc:
            cursorBU.execute('SELECT t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad, sum(t.cantidad *  m.precio) FROM ticket t INNER JOIN Menu m ON t.id_producto = m.ID group by t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad')

        else:
            cursorBU.execute('SELECT t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad, sum(t.cantidad *  m.precio) FROM ticket t INNER JOIN Menu m ON t.id_producto = m.ID WHERE folio_ticket = %s group by t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad', (VBusc,))
        consBP = cursorBU.fetchall()
        
        if consBP is not None:
            return render_template('buscar_pedido.html', listaPedido=consBP)
        else:
            mensaje = 'No se encontraron resultados.'
            return render_template('buscar_pedido.html', mensaje=mensaje)
    cursorBU = mysql.connection.cursor()
    cursorBU.execute('SELECT t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad, sum(t.cantidad *  m.precio) FROM ticket t INNER JOIN Menu m ON t.id_producto = m.ID group by t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad')
    consBU = cursorBU.fetchall()
    return render_template('buscar_pedido.html', listaPedido=consBU)


@app.route('/visualizarAct/<string:id>')
@login_required
def visualizar(id):
    cursorVis = mysql.connection.cursor()
    cursorVis.execute('select * from usuario where Matricula = %s', (id,))
    visualisarDatos = cursorVis.fetchone()
    return render_template('actualizar_usuario.html', UpdUsuario = visualisarDatos)


@app.route('/actualizar/<id>', methods=['POST'])
@login_required
def actualizar(id):
    if request.method == 'POST':
 
        varNombre = request.form['txtNombre']
        varApellidos = request.form['txtApellidos']
        varCorreo = request.form['txtCorreo']
        varContraseña = request.form['txtContraseña']
        cursorUpd = mysql.connection.cursor()
        cursorUpd.execute('update usuario set Nombre = %s, Apellidos = %s, Correo = %s, Contraseña = %s where Matricula = %s', ( varNombre, varApellidos, varCorreo, varContraseña, id))
        mysql.connection.commit()
    flash ('El usuario con Matricula' + id +  'se actualizo correctamente.')
    return redirect(url_for('buscaru'))

@app.route("/confirmacion/<id>")
@login_required
def eliminar(id):
    cursorConfi = mysql.connection.cursor()
    cursorConfi.execute('select * from usuario where Matricula = %s', (id,))
    consuUsuario = cursorConfi.fetchone()
    return render_template('borrar_usuarios.html', usuario=consuUsuario)

@app.route("/eliminar/<id>", methods=['POST'])
@login_required
def eliminarBD(id):
    cursorDlt = mysql.connection.cursor()
    cursorDlt.execute('delete from tarjetas where cliente = %s', (id,))
    mysql.connection.commit()
    cursorDlt = mysql.connection.cursor()
    cursorDlt.execute('delete from ticket where id_cliente = %s', (id,))
    mysql.connection.commit()
    cursorDlt = mysql.connection.cursor()
    cursorDlt.execute('delete from usuario where Matricula = %s', (id,))
    mysql.connection.commit()
    flash('Se elimino el usuario con Matricula'+ id)
    return redirect(url_for('buscaru'))

@app.route('/buscaru', methods=['GET', 'POST'])
@login_required
def buscaru():
    if request.method == 'POST':
        VBusc = request.form['busc']
        
        cursorBU = mysql.connection.cursor()
        if not VBusc:
            cursorBU.execute('SELECT * FROM usuario')
        else:
            cursorBU.execute('SELECT * FROM usuario WHERE Matricula = %s', (VBusc,))
        consBU = cursorBU.fetchall()
        
        if consBU is not None:
            return render_template('buscar_Usuario.html', listaUsuario=consBU)
        else:
            mensaje = 'No se encontraron resultados.'
            return render_template('buscar_Usuario.html', mensaje=mensaje)
    
    cursorBU = mysql.connection.cursor()
    cursorBU.execute('SELECT * FROM usuario')
    consBU = cursorBU.fetchall()
    return render_template('buscar_Usuario.html', listaUsuario=consBU)




@app.route('/metodo/<string:id>')
@login_required
def metodo(id):
    cursorVis = mysql.connection.cursor()
    cursorVis.execute('select * from usuario where Matricula = %s', (id,))
    visualisarDatos = cursorVis.fetchone()
    return render_template('metodo_pago.html', UpdUsuario = visualisarDatos)


@app.route('/met/<id>', methods=['GET', 'POST'])
@login_required
def met(id):
    if request.method == 'POST':
        if request.form['txtMet'] == 'efectivo':
            flash('Eligio efectivo')
            return redirect(url_for('main'))
        
        elif request.form['txtMet'] == 'tarjeta':
            VMat = request.form['txtNum']
            VEnom = request.form['txtNom']
            VNom = request.form['txtVen']
            VAp = request.form['txtCVV']
    
            
            CS = mysql.connection.cursor()
            CS.execute('INSERT INTO tarjetas (cliente, numero, nombre, vencimiento, CVV) VALUES (%s, %s, %s, %s, %s)', (id,VMat, VEnom, VNom, VAp))
            mysql.connection.commit()
            flash('Tarjeta agregada correctamente')
            return redirect(url_for('consultar'))
            

@app.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        # Obtener el nombre y precio del producto desde el formulario
        nombre_producto = request.form['txtProd']
        precio_producto = request.form['txtPrec']

        # Obtener el archivo de imagen del formulario
        imagen_producto = request.files['imagen_producto']

        # Verificar si se proporcionó una imagen
        if imagen_producto and allowed_file(imagen_producto.filename):
            # Generar un nombre único para el archivo de imagen
            nombre_archivo = nombre_producto + '.jpg'
            

            # Guardar el archivo en la carpeta "img" dentro de "static"
            imagen_producto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo))

            # Guardar el nombre y precio del producto en la base de datos
            CS = mysql.connection.cursor()
            CS.execute('INSERT INTO menu (Producto, precio) VALUES (%s,%s)', (nombre_producto, precio_producto))
            mysql.connection.commit()

            # Mostrar un mensaje flash para indicar que el producto se registró correctamente
            flash(f'El producto {nombre_producto} se ha registrado correctamente', 'success')

            # Redireccionar al menú principal o a donde desees después de guardar el producto
            return redirect(url_for('vista_prev'))

    return render_template('Nuevo.html')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/buscarm', methods=['GET', 'POST'])
@login_required
def buscarm():
    if request.method == 'POST':
        VBusc = request.form['busc']
        
        cursorBU = mysql.connection.cursor()
        if not VBusc:
            cursorBU.execute('SELECT * FROM menu')
        else:
            cursorBU.execute('SELECT * FROM menu WHERE producto = %s', (VBusc,))
        consBU = cursorBU.fetchall()

        if consBU is not None:
            return render_template('cons_Menu.html', listaUsuario=consBU)
        else:
            mensaje = 'No se encontraron resultados.'
            return render_template('cons_Menu.html', mensaje=mensaje)
    
    cursorBU = mysql.connection.cursor()
    cursorBU.execute('SELECT * FROM menu')
    consBU = cursorBU.fetchall()
    return render_template('cons_Menu.html', listaUsuario=consBU)

@app.route('/vista_prev', methods=['GET', 'POST'])
@login_required
def vista_prev():
    if request.method == 'POST':
        # Obtener el nombre y precio del producto agregado desde el formulario
        nombre_producto = request.form['nombre_producto']
        precio_producto = request.form['precio_producto']

        # Agregar el producto a la base de datos
        agregar_producto(nombre_producto, precio_producto)

    # Obtener todos los productos de la base de datos
    productos = obtener_productos()

    # Renderizar la plantilla HTML y pasar la lista de productos
    return render_template('vp.html', productos=productos)

def obtener_productos():
    # Conexión a la base de datos MySQL
   
    cursor = mysql.connection.cursor()

    # Obtener todos los productos de la tabla "productos"
    cursor.execute('SELECT producto, precio FROM Menu')
    productos = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()

    return productos

def agregar_producto(nombre, precio):
    # Conexión a la base de datos MySQL
    cursor = mysql.connection.cursor()

    # Insertar el producto en la tabla "productos"
    cursor.execute('INSERT INTO Menu (producto, precio) VALUES (%s, %s)', (nombre, precio))

    # Guardar los cambios en la base de datos
    cursor.commit()

    # Cerrar la conexión a la base de datos
    cursor.close()


#VER ACTUALIZACIONES MENU
@app.route('/visualizarMen/<string:id>')
@login_required
def visualizarMen(id):
    cursorVis = mysql.connection.cursor()
    cursorVis.execute('SELECT * FROM menu WHERE id = %s', (id, ))
    visualisarDatos = cursorVis.fetchone()
    return render_template('actualizar_menu.html', UpdMenu = visualisarDatos)

#ACTUALIZAR PRODUCTOS
@app.route('/actualizarm/<id>', methods=['POST'])
@login_required
def actualizarP(id):
    if request.method == 'POST':
        varPlatillo = request.form['txtPlatillo']
        varPrecio = request.form['txtPrecio']
        cursorUpd = mysql.connection.cursor()
        cursorUpd.execute('update menu set producto = %s, precio = %s where id = %s', ( varPlatillo, varPrecio, id))
        mysql.connection.commit()
    flash ('El platillo  ' + varPlatillo +  ' se actualizo correctamente.')
    return redirect(url_for('buscarm'))

@app.route("/confirmacionm/<id>")
@login_required
def eliminarm(id):
    cursorConfi = mysql.connection.cursor()
    cursorConfi.execute('select * from menu where ID = %s', (id,))
    consuUsuario = cursorConfi.fetchone()
    return render_template('borrar_menu.html', menu=consuUsuario)

@app.route("/eliminarm/<id>", methods=['POST'])
@login_required
def eliminarBDm(id):
    cursorDlt = mysql.connection.cursor()
    cursorDlt.execute('delete from ticket where id_producto = %s', (id,))
    mysql.connection.commit()
    cursorDlt = mysql.connection.cursor()
    cursorDlt.execute('delete from menu where ID = %s', (id,))
    mysql.connection.commit()
    flash('Se elimino el producto')
    return redirect(url_for('buscarm'))


@app.route('/registroa', methods=['GET', 'POST'])
@login_required
def registroa():
    if request.method == 'POST':
        VMat = request.form['txtMat']
        VNom = request.form['txtNom']
        VAp = request.form['txtAp']
        VCorr = request.form['txtCorr']
        VPass = request.form['txtPass']
        
        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO usuario (Matricula,Nombre, Apellidos, Correo, Contraseña, Rol) VALUES (%s,%s, %s, %s, %s,1)', (VMat, VNom, VAp, VCorr, VPass))
        mysql.connection.commit()
        flash('Administrador agregado correctamente')
        return redirect(url_for('main'))

    return render_template('registro_Admin.html')


@app.route('/visualizarActc/<string:id>')
@login_required
def visualizarc(id):
    cursorVis = mysql.connection.cursor()
    cursorVis.execute('select * from usuario where Matricula = %s', (id,))
    visualisarDatos = cursorVis.fetchone()
    return render_template('act_mi_usu.html', UpdUsuario = visualisarDatos)


@app.route('/actualizarc/<id>', methods=['POST'])
@login_required
def actualizarc(id):
    if request.method == 'POST':
 
        varNombre = request.form['txtNombre']
        varApellidos = request.form['txtApellidos']
        varCorreo = request.form['txtCorreo']
        varContraseña = request.form['txtContraseña']
        cursorUpd = mysql.connection.cursor()
        cursorUpd.execute('update usuario set Nombre = %s, Apellidos = %s, Correo = %s, Contraseña = %s where Matricula = %s', ( varNombre, varApellidos, varCorreo, varContraseña, id))
        mysql.connection.commit()
    flash ('El usuario se actualizo correctamente.')
    return redirect(url_for('mc'))

@app.route("/confirmacionc/<id>")
@login_required
def eliminarc(id):
    cursorConfi = mysql.connection.cursor()
    cursorConfi.execute('select * from usuario where Matricula = %s', (id,))
    consuUsuario = cursorConfi.fetchone()
    return render_template('elim_mi_usu.html', usuario=consuUsuario)

@app.route("/eliminarc/<id>", methods=['POST'])
@login_required
def eliminarBDc(id):
    cursorDlt = mysql.connection.cursor()
    cursorDlt.execute('delete from tarjetas where cliente = %s', (id,))
    mysql.connection.commit()
    cursorDlt = mysql.connection.cursor()
    cursorDlt.execute('delete from ticket where id_cliente = %s', (id,))
    mysql.connection.commit()
    cursorDlt = mysql.connection.cursor()
    cursorDlt.execute('delete from usuario where Matricula = %s', (id,))
    mysql.connection.commit()
    session.pop('Matricula', None)
    flash('Se elimino su cuenta')
    return redirect(url_for('login'))

@app.route('/mc', methods=['GET', 'POST'])
@login_required
def mc():
    user_id = session.get('Matricula')
    cursorBU = mysql.connection.cursor()
    cursorBU.execute('SELECT * FROM usuario where Matricula = %s',(user_id,))
    consBU = cursorBU.fetchall()
    return render_template('mc.html', listaUsuario=consBU)


@app.route('/buscarp', methods=['POST', 'GET'])
@login_required
def buscarp():
    if request.method == 'POST':
        VBusc = request.form['busc']
        user_id = session.get('Matricula')
        cursorBU = mysql.connection.cursor()
        if not VBusc:
            cursorBU.execute('SELECT t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad, sum(t.cantidad *  m.precio) FROM ticket t INNER JOIN Menu m ON t.id_producto = m.ID where t.id_cliente = %s group by t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad',(user_id,))

        else:
            cursorBU.execute('SELECT t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad, sum(t.cantidad *  m.precio) FROM ticket t INNER JOIN Menu m ON t.id_producto = m.ID WHERE t.id_cliente = %s AND folio_ticket = %s group by t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad', (user_id,VBusc, ))
        consBP = cursorBU.fetchall()
        
        if consBP is not None:
            return render_template('mis_pedidos.html', listaPedido=consBP)
        else:
            mensaje = 'No se encontraron resultados.'
            return render_template('bmis_pedidos.html', mensaje=mensaje)
    user_id = session.get('Matricula')
    cursorBU = mysql.connection.cursor()
    cursorBU.execute('SELECT t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad, sum(t.cantidad *  m.precio) FROM ticket t INNER JOIN Menu m ON t.id_producto = m.ID where t.id_cliente = %s group by t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad',(user_id,))
    consBU = cursorBU.fetchall()
    return render_template('mis_pedidos.html', listaPedido=consBU)

@app.route('/conf/<id>', methods=['GET', 'POST'])
@login_required
def conf(id):
    curEditar = mysql.connection.cursor()
    curEditar.execute('SELECT * FROM Menu WHERE producto = %s', (id,))
    producto_principal = curEditar.fetchone()

    if request.method == 'POST':
        Vcant = request.form['cantidad']
        Vtot = request.form['total']
        user_id = session.get('Matricula')
        cursorBU = mysql.connection.cursor()
        ultimo_folio=obtener_ultimo_folio()
        
        cursorBU.execute('INSERT INTO ticket(folio_ticket, id_cliente, id_producto, cantidad, total) VALUES (%s, %s, %s, %s, %s)', (ultimo_folio, user_id, id, Vcant, Vtot))
        mysql.connection.commit()  # Commit the changes to the database
        cursorBU.close()
        return redirect(url_for('menu'))
    
    return render_template('compra.html', producto_principal=producto_principal)

@app.route('/cerrar')
def cerrar():
    # Eliminar el correo electrónico del usuario de la sesión
    session.pop('Matricula', None)
    # Redirigir al usuario a la página de inicio de sesión
    return redirect(url_for('index'))


@app.route("/confirmacionp/<id>")
@login_required
def eliminarp(id):
    cursorConfi = mysql.connection.cursor()
    cursorConfi.execute('select * from ticket where ID = %s', (id,))
    consuUsuario = cursorConfi.fetchone()
    return render_template('borrar_prod.html', menu=consuUsuario)

@app.route("/eliminarp/<id>", methods=['POST'])
@login_required
def eliminarBDp(id):
    cursorDlt = mysql.connection.cursor()
    cursorDlt.execute('delete from ticket where ID = %s', (id,))
    mysql.connection.commit()
    flash('Se elimino el producto')
    return redirect(url_for('menu'))




#Ejecucion de servidor
if __name__ =='__main__':
    app.run(port=3000,debug=True)
    
    

