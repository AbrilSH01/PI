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
    
ventana = Tk()
ventana.title("Reinvent Cafe")
ventana.geometry("500x300")

panel = ttk.Notebook(ventana)
panel.pack(fill='both',expand='yes')

pestaña1 = ttk.Frame(panel)
pestaña2 = ttk.Frame(panel)
pestaña3 = ttk.Frame(panel)

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
    elif Metodo.get()=="":
        messagebox.showerror("Error","eleccione un metodo de pago")
Enviar=Button(pestaña2,text="Registrar",bg="#255748",command=tarjeta)
Enviar.place(x=210,y=200)

#Menú

Total=0
def late():
    global Total
    messagebox.showinfo('Pedido','Se ha agregado un Late +$25')
    Total = Total + 25
def pay():
    global Total
    messagebox.showinfo('Pedido','Se ha agregado un Pay + $25')
    Total = Total + 25
def ck():
    global Total
    messagebox.showinfo('Pedido','Se ha agregado Cheesecake +$25')
    Total = Total + 25
def mt():
    global Total
    messagebox.showinfo('Pedido','Se ha agregado Matcha +$30')
    Total = Total + 30
def xp():
    global Total
    messagebox.showinfo('Pedido','Se ha agregado Espresso +$30')
    Total = Total + 30
def HD():
    global Total
    messagebox.showinfo('Pedido','Se ha agregado Hot dog +$30')
    Total = Total + 30
def F():
    global Total
    messagebox.showinfo('Pedido','Se ha agregado Frappe +$50')
    Total = Total + 50  
def H():
    global Total
    messagebox.showinfo('Pedido','Se ha agregado Hamburguesa +$50')
    Total = Total + 50 
def chanwis():
    global Total
    messagebox.showinfo('Pedido','Se ha agregado Sandwich +$50')
    Total = Total + 50 
def c120():
    global Total
    messagebox.showinfo('Pedido','Se ha agregado Pizza +$120')
    Total = Total + 120


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
panel.add(pestaña1,text="Formulario usuarios")
panel.add(pestaña2,text="Metodo de pago")
panel.add(pestaña3,text="Menú")
ventana.mainloop()