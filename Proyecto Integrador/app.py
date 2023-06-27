from flask import Flask, render_template, request, redirect, url_for, flash
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
        CS.execute('INSERT INTO usuario (Matricula,Nombre, Apellidos, Correo, Contraseña) VALUES (%s,%s, %s, %s, %s)', (VMat, VNom, VAp, VCorr, VPass))
        mysql.connection.commit()
        flash('Usuario agregado correctamente')
        return redirect(url_for('main'))

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
        
        # Verificar si las credenciales son válidas
        if resultado is not None:
            # Las credenciales son válidas, redirigir al menú principal
                return render_template('main_menu.html')
        else:
            # Las credenciales son inválidas, redirigir a la página de inicio de sesión con un mensaje de error
            flash('Correo o contraseña incorrectos. Intente nuevamente.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/main', methods=['GET'])
def main():
    return render_template('main_menu.html')

@app.route('/menu', methods=['GET'])
def menu():
    return render_template('menu.html')

@app.route('/buscar', methods=['GET'])
def buscar():
    return render_template('buscar_pedido.html')

@app.route('/actualizar', methods=['GET'])
def actualizar():
    return render_template('actualizar_usuario.html')


@app.route('/consultar', methods=['GET'])
def consultar():
    return render_template('buscar_usuario.html')

@app.route('/met', methods=['GET'])
def met():
    return render_template('metodo_pago.html')

#Ejecucion de servidor
if __name__ =='__main__':
    app.run(port=3000,debug=True)