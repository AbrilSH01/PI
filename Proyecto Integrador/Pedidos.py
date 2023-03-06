from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
ventana = Tk()
ventana.title("Pedidos")
ventana.geometry("600x400")
seccion1=Frame(ventana,bg="green")
seccion1.pack(expand=True,fill='both')
        

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


def Tot():
    if Total==0:
        messagebox.showerror("Error","Seleccione minimo una opcion")
    else:
        messagebox.showinfo("Total", "El total de su compra es: " + str(Total))



total=Button(seccion1, text="Cobrar", bg="#255",command=Tot)
total.place(x=150,y=200)

Met = Label(ventana, text="Metodo de pago:", bg="green")
Met.place(x=50,y=250)
metodos = ["Efectivo", "Tarjeta"]
opcion_seleccionada = tk.StringVar()
Metodo = ttk.Combobox(textvariable=opcion_seleccionada, values=metodos)
Metodo.place(x=200,y=250)
def tarjeta():  
    if Metodo.get()=="Tarjeta":
        Num = Label(ventana, text="Numero de la tarjeta:", bg="green")
        Num.place(x=50,y=280)
        Numero = ttk.Entry(width= 30)
        Numero.place(x=200,y=280)
        fecha = Label(ventana, text="Fecha de vencimiento:", bg="green")
        fecha.place(x=50,y=310)
        Fecha = ttk.Entry(width= 30)
        Fecha.place(x=200,y=310)
        cvv = Label(ventana, text="CVV:", bg="green")
        cvv.place(x=50,y=340)
        CVV = ttk.Entry(width= 30,show="*")
        CVV.place(x=200,y=340)
        
Enviar=Button(seccion1,text="Registrar",bg="#255748",command=tarjeta)
Enviar.place(x=255,y=200)
Mnu = Label(ventana, text="MENU:", bg="green")
Mnu.place(x=20,y=10)
Late=Button(seccion1,text="Late",bg="#255748",command=late)
Late.place(x=50,y=50)
Espresso=Button(seccion1,text="Espresso",bg="#255748",command=xp)
Espresso.place(x=100,y=50)
Frappe=Button(seccion1,text="Frappe",bg="#255748",command=F)
Frappe.place(x=170,y=50)
Matcha=Button(seccion1,text="Matcha",bg="#255748",command=mt)
Matcha.place(x=230,y=50)
Pizza=Button(seccion1,text="Pizza",bg="#255748",command=c120)
Pizza.place(x=50,y=100)
Hamburguesa=Button(seccion1,text="Hamburguesa",bg="#255748",command=H)
Hamburguesa.place(x=100,y=100)
HotDog=Button(seccion1,text="HotDog",bg="#255748",command=HD)
HotDog.place(x=190,y=100)
Sandwich=Button(seccion1,text="Sandwich",bg="#255748",command=chanwis)
Sandwich.place(x=250,y=100)
Cheesecake=Button(seccion1,text="Cheesecake",bg="#255748",command=pay)
Cheesecake.place(x=50,y=150)
Pay=Button(seccion1,text="Pay",bg="#255748",command=ck)
Pay.place(x=130,y=150)

ventana.mainloop()