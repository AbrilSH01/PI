from tkinter import *
from tkinter import ttk
from tkinter import messagebox


ventana = Tk()
ventana.title("Registro")
ventana.geometry("600x400")

def registro():
        if Nombre.get()==vacio or Apellidos.get()==vacio or Correo.get()==vacio or Telefono.get()==vacio or Contraseña.get()==vacio:
            messagebox.showerror("Error","Se deben llenar todos los datos")
        else:
            messagebox.showinfo("Correcto","Sus datos se han registrado correctamente")

seccion1=Frame(ventana,bg="green")
seccion1.pack(expand=True,fill='both')

Nom = Label(ventana, text="Ingrese su Nombre:", bg="green")
Nom.place(x=50,y=50)

Nombre = ttk.Entry(width= 30)
Nombre.place(x=200,y=50)
    

AP = Label(ventana, text="Ingrese sus Apellidos:", bg="green")
AP.place(x=50,y=80)

Apellidos = ttk.Entry(width= 30)
Apellidos.place(x=200,y=80)


Corr = Label(ventana, text="Ingrese su Correo: ", bg="green")
Corr.place(x=50,y=110)

Correo = ttk.Entry(width=30)
Correo.place(x=200,y=110)
    

Tel = Label(ventana, text="Ingrese su Telefono: ", bg="green")
Tel.place(x=50,y=140)

Telefono = ttk.Entry(width=30)
Telefono.place(x=200,y=140)


Passw = Label(ventana, text="Ingrese su Contraseña: ", bg="green")
Passw.place(x=50,y=170)

Contraseña = ttk.Entry(width=30,show="*")
Contraseña.place(x=200,y=170)
vacio=""

BotonRegistrar = Button(seccion1,text="Registrar",bg="#255748",fg="white",command=registro)
BotonRegistrar.pack()

ventana.mainloop()