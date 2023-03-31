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