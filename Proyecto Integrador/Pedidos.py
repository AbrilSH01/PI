from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
ventana = Tk()
ventana.title("Pedidos")
ventana.geometry("600x400")
seccion1=Frame(ventana,bg="green")
seccion1.pack(expand=True,fill='both')
        
menu = Label(ventana, text="Menu", bg="green")
menu.place(x=50,y=0)
Bebidas = Label(ventana, text="Bebidas:", bg="green")
Bebidas.place(x=50,y=20)
Bebidas1 = Label(ventana, text="1.Late $25 2.Espresso $30 3.Matcha $30 4.Frappe $50 ", bg="green")
Bebidas1.place(x=50,y=40)
Comida = Label(ventana, text="Comida:", bg="green")
Comida.place(x=50,y=60)
Comida1 = Label(ventana, text="5.Pizza $120 6.Sandwich $50 7.Hamburguesa $50  8.Hot Dog $30", bg="green")
Comida1.place(x=50,y=80)
Postres = Label(ventana, text="Postres:", bg="green")
Postres.place(x=50,y=100)
Postres1 = Label(ventana, text="9.cheesecake $25 10.Cupcake $30 11.Croisant $30 12.Pay $25", bg="green")
Postres1.place(x=50,y=120)
seleccionar = ["Late","Espresso","Matcha","Frappe", "Pizza","Sandwich","Hamburguesa","Hot Dog","cheesecake","Cupcake","Croisant","Pay"]
opcion_seleccionada = tk.StringVar()
Seleccionar = ttk.Combobox(textvariable=opcion_seleccionada, values=seleccionar)
Seleccionar.place(x=200,y=150)
Total=0
def Añadir():
    global Total
    if Seleccionar.get() == "Late" or Seleccionar.get() == "cheesecake" or Seleccionar.get() == "Pay":
        Total = Total + 25
    elif Seleccionar.get() == "Espresso" or Seleccionar.get() == "Matcha" or Seleccionar.get() == "Hot Dog" or Seleccionar.get() == "Cupcake" or Seleccionar.get() == "Croisant":
        Total = Total + 30
    elif Seleccionar.get() == "Frappe" or Seleccionar.get() == "Hamburguesa" or Seleccionar.get() == "Sandwich":
        Total = Total + 50
    elif Seleccionar.get() == "Pizza":
        Total = Total + 120
    else:
        messagebox.showerror("Error", "Seleccione un producto")

def Tot():
    messagebox.showinfo("Total", "El total de su compra es: " + str(Total))


Agregar = Button(seccion1, text="Agregar", bg="#255",command=Añadir)
Agregar.place(x=200,y=200)
total=Button(seccion1, text="Cobrar", bg="#255",command=Tot)
total.place(x=150,y=200)
ventana.mainloop()