from tkinter import *
from tkinter import messagebox
import sqlite3
class Registro_clase:
    def __init__(self):
        pass

    def conexionDB (self):
        try:
            conexion = sqlite3.connect("C:/Users/Pablo/Documents/GitHub/PI/Proyecto Integrador/DBPI.db")
            print("Conectado a la DB")
            return conexion
        except sqlite3.OperationalError:
            print("No se pudo conectar")
    def registro(self,Nombre,Apellidos,Correo,Telefono,Contraseña,vacio):
        conx = self.conexionDB()
        if Nombre==vacio or Apellidos==vacio or Correo==vacio or Telefono==vacio or Contraseña==vacio:
            messagebox.showerror("Error","Se deben llenar todos los datos")
            conx.close()
        else:
            cursor = conx.cursor()
            datos = (Nombre,Apellidos,Correo,Telefono,Contraseña)
            sqlInsert = "insert into Usuarios(Nombre,Apellidos,Correo,Telefono,Contraseña) values (?,?,?,?,?)"
            cursor.execute(sqlInsert,datos)
            conx.commit()
            conx.close
            messagebox.showinfo("Correcto","Sus datos se han registrado correctamente")
    def Metod(self,Numero,Fecha,CVV,vacio):
        conx = self.conexionDB()
        if Numero==vacio or Fecha==vacio or CVV==vacio:
            messagebox.showerror("Error","Se deben llenar todos los datos")
            conx.close()
        else:
            cursor = conx.cursor()
            datos = (Numero,Fecha,CVV)
            sqlInsert = "insert into Tarjeta(Numero_tarjeta,Fecha_vencimiento,CVV) values (?,?,?)"
            cursor.execute(sqlInsert,datos)
            conx.commit()
            conx.close
            messagebox.showinfo("Correcto","Sus datos se han registrado correctamente")
    def Pago(self,MET,Total):
        conx = self.conexionDB()
        if Total==0:
            messagebox.showerror("Error","Se debe Elegir un producto")
            conx.close()
        else:
            cursor = conx.cursor()
            datos = (MET,Total)
            sqlInsert = "insert into Compras(Metodo_pago,Total) values (?,?)"
            cursor.execute(sqlInsert,datos)
            conx.commit()
            conx.close
            messagebox.showinfo("Correcto","Se pagó un total de " + str(Total))
            
    def consultarUsuario(self,id):
        #1. realizar conexion DB
        conx = self.conexionDB()
        #2. verificar que el id vacio
        if(id==""):
            messagebox.showwarning("Cuidado","Escribe un identificador")
        else:
            #3. Ejecutar la consulta
            try:
                #4. Preparamos lo necesario
                cursor=conx.cursor()
                sqlselect= "select * from Usuarios where id ="+id
                #5. Ejecutamos y cerramos conexion
                cursor.execute(sqlselect)
                RSUsuario = cursor.fetchall()
                conx.close()
                return RSUsuario
                
            except sqlite3.OperationalError:
                print("Error de consulta")
                
    def consulta(self):
        #1. realizar conexion DB
        conx = self.conexionDB()
        try:
            #4. Preparamos lo necesario
            cursor=conx.cursor()
            sqlselect= "select * from Usuarios"
            #5. Ejecutamos y cerramos conexion
            cursor.execute(sqlselect)
            RSUsuarios = cursor.fetchall()
            conx.close()
            return RSUsuarios
                
        except sqlite3.OperationalError:
            print("Error de consulta")
            
    def actualizar(self, id,nom,ap,corr,tel,con):
        conx = self.conexionDB()
        # 2. Validar vacios
        if(id==""):
            messagebox.showwarning("Error","Ingresa un ID")
        else:
            if nom == "" or corr == "" or con == ""or ap == "" or tel == "":
                messagebox.showwarning("Aguas!!", "Formulario incompleto")
                conx.close()
            else:
                try:
                    cursor = conx.cursor()
                    cursor.execute("SELECT * FROM Usuarios WHERE id=" + id)
                    if cursor.fetchone() is None:
                        messagebox.showerror("Error", "El ID no existe")
                    else:
                        datos = (nom, ap, corr, tel, con, id)
                        sqlUpdate = "UPDATE Usuarios SET Nombre=?, Apellidos=?, Correo=?, Telefono=?, Contraseña=? WHERE id=?"
                        cursor.execute(sqlUpdate, datos)
                        conx.commit()
                        conx.close()
                        messagebox.showinfo("Exito", "Usuario actualizado exitosamente")
                except sqlite3.OperationalError:
                    print("Error de actualización")
    
    def eliminar(self, id):
        conx = self.conexionDB()
        # 2. Validar vacios
        if(id==""):
            messagebox.showwarning("Error","Ingresa un ID")
        else:
            try:
                cursor = conx.cursor()
                cursor.execute("SELECT * FROM Usuarios WHERE id=" + id)
                if cursor.fetchone() is None:
                    messagebox.showerror("Error", "El ID no existe")
                else:
                    sqldelete = "DELETE FROM Usuarios WHERE id=?"
                    cursor.execute(sqldelete, id)
                    sqlupdate = "UPDATE Usuarios SET id=id-1 WHERE id > ?"
                    cursor.execute(sqlupdate, id)
                    conx.commit()
                    conx.close()
                    messagebox.showinfo("Exito", "Usuario eliminado exitosamente")
            except sqlite3.OperationalError:
                    print("Error al eliminar")
    
    def pedido(self,Pedido,Total):
        conx = self.conexionDB()
        cursor = conx.cursor()
        datos = (Pedido,Total)
        sqlInsert = "insert into Ventas(C1,Total) values (?,?)"
        cursor.execute(sqlInsert,datos)
        conx.commit()
        conx.close
        messagebox.showinfo("Correcto","Sus datos se han registrado correctamente")
            
    def con_compra(self,id):
        #1. realizar conexion DB
        conx = self.conexionDB()
        #2. verificar que el id vacio
        if(id==""):
            messagebox.showwarning("Cuidado","Escribe un identificador")
        else:
            #3. Ejecutar la consulta
            try:
                #4. Preparamos lo necesario
                cursor=conx.cursor()
                sqlselect= "select * from Ventas where id ="+id
                #5. Ejecutamos y cerramos conexion
                cursor.execute(sqlselect)
                RSUsuario = cursor.fetchall()
                conx.close()
                return RSUsuario
                
            except sqlite3.OperationalError:
                print("Error de consulta")
    
    def consultaP(self):
        #1. realizar conexion DB
        conx = self.conexionDB()
        try:
            #4. Preparamos lo necesario
            cursor=conx.cursor()
            sqlselect= "select * from Ventas"
            #5. Ejecutamos y cerramos conexion
            cursor.execute(sqlselect)
            RSUsuarios = cursor.fetchall()
            conx.close()
            return RSUsuarios
                
        except sqlite3.OperationalError:
            print("Error de consulta")