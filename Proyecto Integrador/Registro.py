from tkinter import *
from tkinter import ttk
import tkinter as tk
from Registro_clase import *

controlador = Registro_clase()

def ejecutaInsert():
    controlador.registro(Nombre.get(),Apellidos.get(),Correo.get(),Telefono.get(),Contraseña.get(),vacio)
    
def ejecutaInsert2():
    controlador.Metod(Numero.get(),Fecha.get(),CVV.get(),vacio)
    
def ejecutaInsert3():
    controlador.Pago(MET,Total)
    controlador.pedido(Pedido,Total)

def ejecutaSelect():
    rsUsu= controlador.consultarUsuario(varBus.get())
    for usu in rsUsu:
        cadena= str(usu[0])+" "+usu[1]+" "+usu[2]+" "+str(usu[3])+" "+str(usu[4])+" "+(usu[5])
    if(rsUsu): 
        textBus.config(state='normal')  # Configuración del estado del widget Text
        textBus.delete(1.0, 'end')  # Limpia el contenido del widget Text
        textBus.insert('end', cadena)  # Inserta la cadena en el widget Text
        textBus.config(state='disabled')  # Restaura el estado del widget Text a 'disabled'
    else:
        messagebox.showerror("Error","El usuario no existe en la base de datos")
        
def ejecutaconsulta():
    # Obtiene los usuarios de la base de datos
    rUsu= controlador.consulta()
    # Borra los datos existentes en la tabla
    tabla.delete(*tabla.get_children())
    # Inserta los nuevos datos en la tabla
    for usu in rUsu:
        tabla.insert('', 'end', text=usu[0], values=(usu[1], usu[2], usu[3], usu[4], usu[5]))
        
def ejecutaACT(varNomAE, varAPAE, varCorrAE, varTelAE, varPassAE):
    controlador.actualizar(varAct.get(),varNomAE.get(), varAPAE.get(), varCorrAE.get(), varTelAE.get(), varPassAE.get())
    
def ejecutadelete():
    controlador.eliminar(varElim.get())        
    
def ejecutaSelectP():
    rsUsu= controlador.con_compra(varBus.get())
    for usu in rsUsu:
        cadena= str(usu[0])+" "+usu[1]+" "+str(usu[2])
    if(rsUsu): 
        textBus.config(state='normal')  # Configuración del estado del widget Text
        textBus.delete(1.0, 'end')  # Limpia el contenido del widget Text
        textBus.insert('end', cadena)  # Inserta la cadena en el widget Text
        textBus.config(state='disabled')  # Restaura el estado del widget Text a 'disabled'
    else:
        messagebox.showerror("Error","El Pedido no existe en la base de datos")

def ejecutaconsultaP():
    # Obtiene los usuarios de la base de datos
    rUsu= controlador.consultaP()
    # Borra los datos existentes en la tabla
    tabla.delete(*tabla.get_children())
    # Inserta los nuevos datos en la tabla
    for usu in rUsu:
        tabla.insert('', 'end', text=usu[0], values=(usu[1], usu[2]))
ventana = Tk()
ventana.title("Reinvent Cafe")
ventana.geometry("800x400")

panel = ttk.Notebook(ventana)
panel.pack(fill='both',expand='yes')

pestaña1 = ttk.Frame(panel)
pestaña2 = ttk.Frame(panel)
pestaña3 = ttk.Frame(panel)
pestaña4 = ttk.Frame(panel)
pestaña5 = ttk.Frame(panel)
pestaña8 = ttk.Frame(panel)
pestaña9 = ttk.Frame(panel)
pestaña6 = ttk.Frame(panel)
pestaña7 = ttk.Frame(panel)

#Registro de usuario
titulo = Label(pestaña1,text="Registro de usuarios",fg="blue",font=("Modern",18)).pack()

Nom = Label(pestaña1, text="Ingrese su Nombre:")
Nom.place(x=50,y=50)
Nombre = ttk.Entry(pestaña1,width= 30)
Nombre.place(x=200,y=50)
    

AP = Label(pestaña1, text="Ingrese sus Apellidos:")
AP.place(x=50,y=80)
Apellidos = ttk.Entry(pestaña1,width= 30)
Apellidos.place(x=200,y=80)


Corr = Label(pestaña1, text="Ingrese su Correo: ")
Corr.place(x=50,y=110)
Correo = ttk.Entry(pestaña1,width=30)
Correo.place(x=200,y=110)
    

Tel = Label(pestaña1, text="Ingrese su Telefono: ")
Tel.place(x=50,y=140)
Telefono = ttk.Entry(pestaña1,width=30)
Telefono.place(x=200,y=140)


Passw = Label(pestaña1, text="Ingrese su Contraseña: ")
Passw.place(x=50,y=170)
Contraseña = ttk.Entry(pestaña1,width=30,show="*")
Contraseña.place(x=200,y=170)
vacio=""

BotonRegistrar = Button(pestaña1,text="Registrar",bg="#255748",fg="white",command=ejecutaInsert)
BotonRegistrar.place(y=200, x= 220)

#Metodo de pago
metodos= Label(pestaña2,text="Metodos de pago",fg="blue",font=("Modern",18)).pack()
Met = Label(pestaña2, text="Metodo de pago:")
Met.place(x=50,y=50)
metodos = ["Efectivo", "Tarjeta"]
opcion_seleccionada = tk.StringVar()
Metodo = ttk.Combobox(pestaña2,textvariable=opcion_seleccionada, values=metodos)
Metodo.place(x=200,y=50)
Numero = ttk.Entry(pestaña2,width= 30)
Fecha = ttk.Entry(pestaña2,width= 30)
CVV = ttk.Entry(pestaña2,width= 30,show="*")
Continuar=Button(pestaña2,text="Continuar",bg="#255748",command=ejecutaInsert2)
def tarjeta():  
    global MET
    if Metodo.get()=="Tarjeta":
        Num = Label(pestaña2, text="Numero de la tarjeta:")
        Num.place(x=50,y=80)
        Numero.place(x=200,y=80)
        fecha = Label(pestaña2, text="Fecha de vencimiento:")
        fecha.place(x=50,y=110)
        Fecha.place(x=200,y=110)
        cvv = Label(pestaña2, text="CVV:")
        cvv.place(x=50,y=140)
        CVV.place(x=200,y=140)
        Continuar.place(x=300,y=200)
        MET= "Tarjeta"
    
    elif Metodo.get()=="Efectivo":
        Cont2=Button(pestaña2,text="Continuar",bg="#255748",command=ejecutaInsert2)
        Cont2
        MET = "Efectivo"
    else:
        messagebox.showerror("Error","Seleccione un metodo de pago")
Enviar=Button(pestaña2,text="Registrar",bg="#255748",command=tarjeta)
Enviar.place(x=210,y=200)

#Menú

Total = 0
Pedido = ""
def late():
    global Total
    global Pedido
    messagebox.showinfo('Pedido','Se ha agregado un Late +$25')
    Total = Total + 25
    Pedido = Pedido  + "Late" + ", "
def pay():
    global Pedido
    global Total
    messagebox.showinfo('Pedido','Se ha agregado un Pay + $25')
    Total = Total + 25
    Pedido = Pedido  + "Pay" + ", "
def ck():
    global Total
    global Pedido
    messagebox.showinfo('Pedido','Se ha agregado Cheesecake +$25')
    Total = Total + 25
    Pedido = Pedido  + "Cheesecake" + ", "
def mt():
    global Total
    global Pedido
    messagebox.showinfo('Pedido','Se ha agregado Matcha +$30')
    Total = Total + 30
    Pedido = Pedido + "Matcha" + ", "
def xp():
    global Total
    global Pedido
    messagebox.showinfo('Pedido','Se ha agregado Espresso +$30')
    Total = Total + 30
    Pedido = Pedido  + "Espresso" + ", "
def HD():
    global Total
    global Pedido
    messagebox.showinfo('Pedido','Se ha agregado Hot dog +$30')
    Total = Total + 30
    Pedido = Pedido  + "Hot Dog" + ", "
def F():
    global Total
    global Pedido
    messagebox.showinfo('Pedido','Se ha agregado Frappe +$50')
    Total = Total + 50  
    Pedido = Pedido  + "Frappe" + ", "
def H():
    global Total
    global Pedido
    messagebox.showinfo('Pedido','Se ha agregado Hamburguesa +$50')
    Total = Total + 50 
    Pedido = Pedido  + "Hamburguesa" + ", "
def chanwis():
    global Total
    global Pedido
    messagebox.showinfo('Pedido','Se ha agregado Sandwich +$50')
    Total = Total + 50 
    Pedido = Pedido + "Sandwich" + ", "
def c120():
    global Total
    global Pedido
    messagebox.showinfo('Pedido','Se ha agregado Pizza +$120')
    Total = Total + 120
    Pedido = Pedido + "Pizza" + ", "


Mnu = Label(pestaña3,text="Menu",fg="blue",font=("Modern",18)).pack()
Late=Button(pestaña3,text="Late",bg="#255748",command=late)
Late.place(x=50,y=50)
Espresso=Button(pestaña3,text="Espresso",bg="#255748",command=xp)
Espresso.place(x=100,y=50)
Frappe=Button(pestaña3,text="Frappe",bg="#255748",command=F)
Frappe.place(x=170,y=50)
Matcha=Button(pestaña3,text="Matcha",bg="#255748",command=mt)
Matcha.place(x=230,y=50)
Pizza=Button(pestaña3,text="Pizza",bg="#255748",command=c120)
Pizza.place(x=50,y=100)
Hamburguesa=Button(pestaña3,text="Hamburguesa",bg="#255748",command=H)
Hamburguesa.place(x=100,y=100)
HotDog=Button(pestaña3,text="HotDog",bg="#255748",command=HD)
HotDog.place(x=190,y=100)
Sandwich=Button(pestaña3,text="Sandwich",bg="#255748",command=chanwis)
Sandwich.place(x=250,y=100)
Cheesecake=Button(pestaña3,text="Cheesecake",bg="#255748",command=pay)
Cheesecake.place(x=50,y=150)
Pay=Button(pestaña3,text="Pay",bg="#255748",command=ck)
Pay.place(x=130,y=150)

pagar = Button(pestaña3,text="Pagar",bg="#255748",command=ejecutaInsert3)
pagar.place(x=220,y=180)

#Buscar usuario
tituloo = Label(pestaña4,text="Buscar usuario:",fg ="green",font=("Modern",18)).pack()

varBus=tk.StringVar()
lblid= Label(pestaña4,text="Identificador de usuario:")
txtid= Entry(pestaña4,textvariable=varBus).pack()
btnBusqueda= Button(pestaña4,text="Buscar",command=ejecutaSelect).pack()

subBus= Label(pestaña4,text= "Registrado:",fg="blue",font=("Modern",15)).pack()
textBus = tk.Text(pestaña4, height=5, width=70)
textBus.pack() 

#Consultar usuarios
subUS= Label(pestaña5,text= "Usuarios:",fg="green",font=("Modern",15)).pack()
tabla = ttk.Treeview(pestaña5)
tabla['columns'] = ('nombre','apellidos', 'correo','telefono', 'contraseña')
tabla.column('#0', width=50, minwidth=50)
tabla.column('nombre', width=120, minwidth=120)
tabla.column('apellidos', width=120, minwidth=120)
tabla.column('correo', width=150, minwidth=150)
tabla.column('telefono', width=150, minwidth=150)
tabla.column('contraseña', width=100, minwidth=100)
tabla.heading('#0', text='ID', anchor=tk.CENTER)
tabla.heading('nombre', text='Nombre', anchor=tk.CENTER)
tabla.heading('apellidos', text='Apellidos', anchor=tk.CENTER)
tabla.heading('correo', text='Correo', anchor=tk.CENTER)
tabla.heading('telefono', text='Telefono', anchor=tk.CENTER)
tabla.heading('contraseña', text='Contraseña', anchor=tk.CENTER)
tabla.pack() 

Consultar= Button(pestaña5,text="Consultar",command=ejecutaconsulta).pack()

#Actualizar
     
titulo3 = Label(pestaña6,text="Actualizar Usuario:",fg ="green",font=("Modern",18))
titulo3.pack()

varAct = tk.StringVar()
lblidA = Label(pestaña6,text="Identificador de usuario:")
lblidA.pack()
txtidA = Entry(pestaña6,textvariable=varAct)
txtidA.pack()

varNomAE = tk.StringVar()
lblNomAE = Label(pestaña6,text="Nuevo nombre: ")
lblNomAE.pack()
txtNomAE = Entry(pestaña6,textvariable=varNomAE)
txtNomAE.pack()

varAPAE = tk.StringVar()
lblAPAE = Label(pestaña6,text="Nuevos apellidos: ")
lblAPAE.pack()
txtAPAE = Entry(pestaña6,textvariable=varAPAE)
txtAPAE.pack()

varCorrAE = tk.StringVar()
lblCorrAE = Label(pestaña6,text="Nuevo correo: ")
lblCorrAE.pack()
txtCorrAE = Entry(pestaña6,textvariable=varCorrAE)
txtCorrAE.pack()

varTelAE = tk.StringVar()
lblTelAE = Label(pestaña6,text="Nuevo telefono: ")
lblTelAE.pack()
txtTelAE = Entry(pestaña6,textvariable=varTelAE)
txtTelAE.pack()

varPassAE = tk.StringVar()
lblPassAE = Label(pestaña6,text="Nueva contraseña: ")
lblPassAE.pack()
txtPassAE = Entry(pestaña6,textvariable=varPassAE,show="*")
txtPassAE.pack()

btnACT = Button(pestaña6,text="Actualizar usuario", command=lambda: ejecutaACT(varNomAE, varAPAE, varCorrAE, varTelAE, varPassAE))
btnACT.pack()

#Eliminar usuario
titulo3 = Label(pestaña7,text="Eliminar Usuario:",fg ="red",font=("Modern",18))
titulo3.pack()

varElim = tk.StringVar()
lblidE = Label(pestaña7,text="Identificador de usuario:")
lblidE.pack()
txtidE = Entry(pestaña7,textvariable=varElim)
txtidE.pack()

btnElimina = Button(pestaña7,text="Eliminar usuario", command=ejecutadelete)
btnElimina.pack()

mensajeAE = tk.StringVar()
lblMensajeAE = Label(pestaña7, textvariable=mensajeAE)
lblMensajeAE.pack()

#Buscar pedido
tituloo = Label(pestaña8,text="Buscar Pedido:",fg ="green",font=("Modern",18)).pack()

varBus=tk.StringVar()
lblid= Label(pestaña8,text="Identificador de pedido:")
txtid= Entry(pestaña8,textvariable=varBus).pack()
btnBusqueda= Button(pestaña8,text="Buscar",command=ejecutaSelectP).pack()

subBus= Label(pestaña8,text= "Registrado:",fg="blue",font=("Modern",15)).pack()
textBus = tk.Text(pestaña8, height=5, width=70)
textBus.pack() 

#Consultar pedidos
subUS= Label(pestaña9,text= "Ventas:",fg="green",font=("Modern",15)).pack()
tabla = ttk.Treeview(pestaña9)
tabla['columns'] = ('productos','total')
tabla.column('#0', width=50, minwidth=50)
tabla.column('productos', width=200, minwidth=120)
tabla.column('total', width=120, minwidth=120)
tabla.heading('#0', text='ID', anchor=tk.CENTER)
tabla.heading('productos', text='Productos', anchor=tk.CENTER)
tabla.heading('total', text='Total', anchor=tk.CENTER)

tabla.pack() 

Consultar= Button(pestaña9,text="Consultar",command=ejecutaconsultaP).pack()

panel.add(pestaña1,text="Formulario usuarios")
panel.add(pestaña2,text="Metodo de pago")
panel.add(pestaña3,text="Menú")
panel.add(pestaña4,text="Buscar")
panel.add(pestaña5,text="Consultar")
panel.add(pestaña8,text="Pedidos")
panel.add(pestaña9,text="Consultar_Pedidos")
panel.add(pestaña6,text="Actualizar")
panel.add(pestaña7,text="Eliminar")
ventana.mainloop()