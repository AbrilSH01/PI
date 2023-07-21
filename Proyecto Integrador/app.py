from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
#inicialización del servidor Flask
app = Flask(__name__)

#Configuracion de la conexion
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="cafeteriaapp"

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
        Rol = "Select Rol from usuario where correo = %s and contraseña = %s"
        
        # Verificar si las credenciales son válidas
        if resultado is not None:
            CS.execute(Rol,(VCorr, VPass))
            rol_resultado = CS.fetchone()
            if rol_resultado is not None and rol_resultado[0] == 1:
            # Las credenciales son válidas, redirigir al menú principal
                return redirect(url_for('main'))
            else:
                return redirect(url_for('cliente'))
        else:
            # Las credenciales son inválidas, redirigir a la página de inicio de sesión con un mensaje de error
            flash('Correo o contraseña incorrectos. Intente nuevamente.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/main', methods=['GET'])
def main():
    return render_template('main_menu.html')

@app.route('/cliente', methods=['GET'])
def cliente():
    return render_template('mm_cl.html')

@app.route('/menu', methods=['GET'])
def menu():
    return render_template('menu.html')

@app.route('/buscar', methods=['POST', 'GET'])
def buscar():
    if request.method == 'POST':
        VBusc = request.form['busc']
        
        cursorBU = mysql.connection.cursor()
        if not VBusc:
            cursorBU.execute('SELECT t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad, t.total FROM ticket t INNER JOIN Menu m ON t.id_producto = m.ID')

        else:
            cursorBU.execute('SELECT t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad, t.total FROM ticket t INNER JOIN Menu m ON t.id_producto = m.ID WHERE folio_ticket = %s', (VBusc,))
        consBP = cursorBU.fetchall()
        
        if consBP is not None:
            return render_template('buscar_pedido.html', listaPedido=consBP)
        else:
            mensaje = 'No se encontraron resultados.'
            return render_template('buscar_pedido.html', mensaje=mensaje)
    cursorBU = mysql.connection.cursor()
    cursorBU.execute('SELECT t.ID, t.folio_ticket, t.id_cliente, m.Producto, t.cantidad, t.total FROM ticket t INNER JOIN Menu m ON t.id_producto = m.ID')
    consBU = cursorBU.fetchall()
    return render_template('buscar_pedido.html', listaPedido=consBU)


@app.route('/visualizarAct/<string:id>')
def visualizar(id):
    cursorVis = mysql.connection.cursor()
    cursorVis.execute('select * from usuario where Matricula = %s', (id,))
    visualisarDatos = cursorVis.fetchone()
    return render_template('actualizar_usuario.html', UpdUsuario = visualisarDatos)


@app.route('/actualizar/<id>', methods=['POST'])
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
def eliminar(id):
    cursorConfi = mysql.connection.cursor()
    cursorConfi.execute('select * from usuario where Matricula = %s', (id,))
    consuUsuario = cursorConfi.fetchone()
    return render_template('borrar_usuarios.html', usuario=consuUsuario)

@app.route("/eliminar/<id>", methods=['POST'])
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
def metodo(id):
    cursorVis = mysql.connection.cursor()
    cursorVis.execute('select * from usuario where Matricula = %s', (id,))
    visualisarDatos = cursorVis.fetchone()
    return render_template('metodo_pago.html', UpdUsuario = visualisarDatos)


@app.route('/met/<id>', methods=['GET', 'POST'])
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
def nuevo():
    if request.method == 'POST':
        VProd = request.form['txtProd']
        VPrec = request.form['txtPrec']
        
        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO menu (Producto, precio) VALUES (%s,%s)', (VProd, VPrec))
        mysql.connection.commit()
        flash('Producto agregado correctamente')
        return redirect(url_for('main'))

    return render_template('Nuevo.html')

@app.route('/buscarm', methods=['GET', 'POST'])
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

@app.route("/confirmacionm/<id>")
def eliminarm(id):
    cursorConfi = mysql.connection.cursor()
    cursorConfi.execute('select * from menu where ID = %s', (id,))
    consuUsuario = cursorConfi.fetchone()
    return render_template('borrar_menu.html', menu=consuUsuario)

@app.route("/eliminarm/<id>", methods=['POST'])
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



#Ejecucion de servidor
if __name__ =='__main__':
    app.run(port=3000,debug=True)
    
    

