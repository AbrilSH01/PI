from tkinter import *
from tkinter import ttk
import tkinter as tk

ventana = Tk()
ventana.title("Cobro")
ventana.geometry("600x400")
seccion1=Frame(ventana,bg="green")
seccion1.pack(expand=True,fill='both')
total = Label(ventana, text="Total:", bg="green")
total.place(x=50,y=50)
Total = ttk.Entry(width= 30)
Total.place(x=200,y=50)

Met = Label(ventana, text="Metodo de pago:", bg="green")
Met.place(x=50,y=80)
metodos = ["Efectivo", "Tarjeta"]
opcion_seleccionada = tk.StringVar()
Metodo = ttk.Combobox(textvariable=opcion_seleccionada, values=metodos)
Metodo.place(x=200,y=80)
def tarjeta():  
    if Metodo.get()=="Tarjeta":
        Num = Label(ventana, text="Numero de la tarjeta:", bg="green")
        Num.place(x=50,y=110)
        Numero = ttk.Entry(width= 30)
        Numero.place(x=200,y=110)
        fecha = Label(ventana, text="Fecha de vencimiento:", bg="green")
        fecha.place(x=50,y=140)
        Fecha = ttk.Entry(width= 30)
        Fecha.place(x=200,y=140)
        cvv = Label(ventana, text="CVV:", bg="green")
        cvv.place(x=50,y=170)
        CVV = ttk.Entry(width= 30)
        CVV.place(x=200,y=170)
        
Enviar=Button(seccion1,text="Registrar",bg="#255748",fg="white",command=tarjeta)
Enviar.pack()
ventana.mainloop()