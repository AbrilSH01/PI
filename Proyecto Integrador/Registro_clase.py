from tkinter import *
from tkinter import messagebox
class Registrar:
    def __init__(self,Nombre,Apellidos,Correo,Telefono,Contraseña,vacio):
        self.Nombre=Nombre
        self.Apellidos=Apellidos
        self.Correo=Correo
        self.Telefono=Telefono
        self.Contraseña=Contraseña
        self.vacio=vacio
    def registro(self):
        if self.Nombre.get()==self.vacio or self.Apellidos.get()==self.vacio or self.Correo.get()==self.vacio or self.Telefono.get()==self.vacio or self.Contraseña.get()==self.vacio:
            messagebox.showerror("Error","Se deben llenar todos los datos")
        else:
            messagebox.showinfo("Correcto","Sus datos se han registrado correctamente")
