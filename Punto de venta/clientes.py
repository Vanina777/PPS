import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime
import sys
import os

class Clientes(tk.Frame):
    db_name = "database.db"
    
    def __init__(self, padre):
        super().__init__(padre)
        self.contador = 1  
        self.widgets()
        self.cargar_registros()
        
    def rutas(self,ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)
        
    def widgets(self):
        
#Frame superior
        frame1 = tk.Frame(self, bg="#BEBEBE",highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)
        
        titulo = tk.Label(self, text="CLIENTES", font="sans 30 bold", bg="#BEBEBE", anchor="center")
        titulo.pack()  
        titulo.place(x=5, y=0, width=1090, height=90)
        
#Frame inferior       
        frame2 = tk.Frame(self, bg="#545454",highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)
        
        # Crear etiqueta para mostrar la fecha actual
        ruta=self.rutas(r"icono/calendario.png")
        imagen_pil = Image.open(ruta)
        imagen_resize11 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize11)
        
        self.label_fecha = tk.Label(frame2, text="", font="sans 14 bold", bg="#545454", fg="#FFFFFF")
        self.label_fecha.config(image=imagen_tk, compound="left", padx=10)
        self.label_fecha.image = imagen_tk
        self.label_fecha.place(x=780, y=3)

        # Crear etiqueta para mostrar la hora actualizada
        ruta=self.rutas(r"icono/hora.png")
        imagen_pil = Image.open(ruta)
        imagen_resize12 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize12)
        
        self.label_hora = tk.Label(frame2, text="", font="sans 14 bold", bg="#545454", fg="#FFFFFF")
        self.label_hora.config(image=imagen_tk, compound="left", padx=10)
        self.label_hora.image = imagen_tk
        self.label_hora.place(x=930, y=3)

        # Actualizar la fecha y la hora cada segundo
        self.actualizar_fecha_y_hora()
        
#LabelFrame con entrys para ingresar datos
        self.labelframe = tk.LabelFrame(frame2, text="Clientes", font="sans 22 bold", bg="#BEBEBE")
        self.labelframe.place(x=20,y=30,width=400,height=500)
        
        lblnombre = tk.Label(self.labelframe, text="Nombre: ", font="sans 14 bold", bg="#BEBEBE")
        lblnombre.place(x=10, y=20)
        self.nombre = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.nombre.place(x=140,y=20,width=240,height=40)
        
        lblcedula = tk.Label(self.labelframe, text="Cédula: ", font="sans 14 bold", bg="#BEBEBE")
        lblcedula.place(x=10, y=80)
        self.cedula = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.cedula.place(x=140,y=80,width=240,height=40)

        lblcelular = Label(self.labelframe, text="Celular: ", font="sans 14 bold", bg="#BEBEBE")
        lblcelular.place(x=10, y=140)
        self.celular = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.celular.place(x=140,y=140,width=240,height=40)
        
        lbldireccion = tk.Label(self.labelframe, text="Dirección: ", font="sans 14 bold", bg="#BEBEBE")
        lbldireccion.place(x=10, y=200)
        self.direccion = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.direccion.place(x=140,y=200,width=240,height=40)
        
        lblcorreo = tk.Label(self.labelframe, text="Correo: ", font="sans 14 bold", bg="#BEBEBE")
        lblcorreo.place(x=10, y=260)
        self.correo = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.correo.place(x=140,y=260,width=240,height=40)
        
        ruta=self.rutas(r"icono/ingresarc.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        btn1 = Button(self.labelframe, bg="#FFFFFF", fg="black", text="Ingresar", font="roboto 16 bold", command=self.registrar)
        btn1.config(image=imagen_tk, compound=LEFT, padx=10)
        btn1.image = imagen_tk
        btn1.place(x=140, y=340,width=150, height=40)

        ruta=self.rutas(r"icono/eliminar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize1 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize1)
        
        btn_eliminar = Button(self.labelframe, bg="#FFFFFF", fg="black", text="Eliminar", font="roboto 16 bold", command=self.eliminar)
        btn_eliminar.config(image=imagen_tk, compound=LEFT, padx=10)
        btn_eliminar.image = imagen_tk
        btn_eliminar.place(x=20, y=400,width=150,height=40)

        ruta=self.rutas(r"icono/modificar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize2 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize2)

        btn_modificar = Button(self.labelframe, bg="#FFFFFF", fg="black", text="Modificar", font="roboto 16 bold", command=self.modificar)
        btn_modificar.config(image=imagen_tk, compound=LEFT, padx=10)
        btn_modificar.image = imagen_tk
        btn_modificar.place(x=220, y=400,width=150, height=40)

    #Treeview Tabla
        treFrame=Frame(frame2,bg="#FFFFFF") 
        treFrame.place(x=440,y=50,width=620,height=450)
        
        # Barra de desplazamiento vertical
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        # Barra de desplazamiento horizontal
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        # Widget Treeview
        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, 
                                columns=("ID", "Nombre", "Cédula", "Celular", "Dirección", "Correo"),show="headings")
        self.tre.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        #Columnas
        self.tre.heading("ID", text="ID")
        self.tre.heading("Nombre", text="Nombre")
        self.tre.heading("Cédula", text="Cédula")
        self.tre.heading("Celular", text="Celular")
        self.tre.heading("Dirección", text="Dirección")
        self.tre.heading("Correo", text="Correo")

        # Formato 
        self.tre.column("ID", width=50, anchor="center")
        self.tre.column("Nombre", width=150, anchor="center")
        self.tre.column("Cédula", width=120, anchor="center")
        self.tre.column("Celular", width=120, anchor="center")
        self.tre.column("Dirección", width=200, anchor="center")
        self.tre.column("Correo", width=200, anchor="center")

        # Asignar función para seleccionar cliente
        self.tre.bind("<ButtonRelease-1>", self.seleccionar_cliente)

#Funciones
    def cargar_registros(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            rows = cursor.fetchall()
            for row in rows:
                self.tre.insert("", "end", values=row)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo cargar los registros: {e}")

    def validar_campos(self):
        if not self.nombre.get() or not self.cedula.get() or not self.celular.get() or not self.direccion.get() or not self.correo.get():
            messagebox.showerror("Error", "Todos los campos son requeridos.")
            return False
        return True

    def registrar(self):
        if not self.validar_campos():
            return

        nombre = self.nombre.get()
        cedula = self.cedula.get()
        celular = self.celular.get()
        direccion = self.direccion.get()
        correo = self.correo.get()

        # Guardar en la base de datos
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clientes (nombre, cedula, celular, direccion, correo) VALUES (?, ?, ?, ?, ?)",
                           (nombre, cedula, celular, direccion, correo))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            self.limpiar_campos()
            self.cargar_registros()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")

    def eliminar(self):
        if not self.tre.selection():
            messagebox.showerror("Error", "Por favor seleccione un cliente para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este cliente?"):
            item = self.tre.selection()[0]
            id_cliente = self.tre.item(item, "values")[0]

            # Eliminar registro de la base de datos
            try:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE ID=?", (id_cliente,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                self.tre.delete(item)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")

    def modificar(self):
        if not self.tre.selection():
            messagebox.showerror("Error", "Por favor seleccione un cliente para modificar.")
            return

        item = self.tre.selection()[0]
        id_cliente = self.tre.item(item, "values")[0]

        # Obtener los datos del cliente seleccionado
        nombre_actual = self.tre.item(item, "values")[1]
        cedula_actual = self.tre.item(item, "values")[2]
        celular_actual = self.tre.item(item, "values")[3]
        direccion_actual = self.tre.item(item, "values")[4]
        correo_actual = self.tre.item(item, "values")[5]

        #Toplevel para la modificación
        top_modificar = Toplevel(self)
        top_modificar.title("Modificar Cliente")
        top_modificar.geometry("400x400") 
        top_modificar.config(bg="#BEBEBE")

        # Crear etiquetas y campos de entrada para los nuevos datos
        tk.Label(top_modificar, text="Nombre:",font="sans 14 bold",bg="#BEBEBE").grid(row=0, column=0, padx=10, pady=5)
        nombre_nuevo = tk.Entry(top_modificar,font="sans 14 bold")
        nombre_nuevo.insert(0, nombre_actual)
        nombre_nuevo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Cedula:",font="sans 14 bold",bg="#BEBEBE").grid(row=1, column=0, padx=10, pady=5)
        cedula_nueva = tk.Entry(top_modificar,font="sans 14 bold")
        cedula_nueva.insert(0, cedula_actual)
        cedula_nueva.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Celular:",font="sans 14 bold",bg="#BEBEBE").grid(row=2, column=0, padx=10, pady=5)
        celular_nuevo = tk.Entry(top_modificar,font="sans 14 bold")
        celular_nuevo.insert(0, celular_actual)
        celular_nuevo.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Dirección:",font="sans 14 bold",bg="#BEBEBE").grid(row=3, column=0, padx=10, pady=5)
        direccion_nueva = tk.Entry(top_modificar,font="sans 14 bold")
        direccion_nueva.insert(0, direccion_actual)
        direccion_nueva.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Correo:",font="sans 14 bold",bg="#BEBEBE").grid(row=4, column=0, padx=10, pady=5)
        correo_nuevo = tk.Entry(top_modificar,font="sans 14 bold")
        correo_nuevo.insert(0, correo_actual)
        correo_nuevo.grid(row=4, column=1, padx=10, pady=5)

        # Función para actualizar el cliente en la base de datos
        def actualizar_cliente():
            # Obtener los nuevos datos
            nuevo_nombre = nombre_nuevo.get()
            nueva_cedula = cedula_nueva.get()
            nuevo_celular = celular_nuevo.get()
            nueva_direccion = direccion_nueva.get()
            nuevo_correo = correo_nuevo.get()

            # Modificar el registro en la base de datos
            try:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute("UPDATE clientes SET nombre=?, cedula=?, celular=?, direccion=?, correo=? WHERE ID=?",
                            (nuevo_nombre, nueva_cedula, nuevo_celular, nueva_direccion, nuevo_correo, id_cliente))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
                # Actualizar los datos en el Treeview
                self.tre.item(item, values=(id_cliente, nuevo_nombre, nueva_cedula, nuevo_celular, nueva_direccion, nuevo_correo))
                top_modificar.destroy()  # Cerrar la ventana emergente después de la modificación
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo modificar el cliente: {e}")

        ruta=self.rutas(r"icono/guardar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize4 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize4)
        
        # Botón para confirmar la modificación
        btn_guardar = Button(top_modificar, text="Guardar cambios", bg="#FFFFFF", fg="black", font="sans 14 bold", command=actualizar_cliente)
        btn_guardar.config(image=imagen_tk, compound=LEFT, padx=10)
        btn_guardar.image = imagen_tk
        btn_guardar.place(x=80, y=200,width=240, height=40)

    def limpiar_campos(self):
        self.nombre.delete(0, END)
        self.cedula.delete(0, END)
        self.celular.delete(0, END)
        self.direccion.delete(0, END)
        self.correo.delete(0, END)

    def seleccionar_cliente(self, event):
        item = self.tre.selection()[0]
        valores = self.tre.item(item, "values")

        # Llenar campos de entry con los valores seleccionados
        self.nombre.delete(0, END)
        self.nombre.insert(END, valores[1])
        self.cedula.delete(0, END)
        self.cedula.insert(END, valores[2])
        self.celular.delete(0, END)
        self.celular.insert(END, valores[3])
        self.direccion.delete(0, END)
        self.direccion.insert(END, valores[4])
        self.correo.delete(0, END)
        self.correo.insert(END, valores[5])
        item = self.tre.selection()[0]
        valores = self.tre.item(item, "values")

        self.nombre.delete(0, END)
        self.nombre.insert(END, valores[1])
        self.cedula.delete(0, END)
        self.cedula.insert(END, valores[2])
        self.celular.delete(0, END)
        self.celular.insert(END, valores[3])
        self.direccion.delete(0, END)
        self.direccion.insert(END, valores[4])
        self.correo.delete(0, END)
        self.correo.insert(END, valores[5])
        
    def actualizar_fecha_y_hora(self):
        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

        # Actualizar las etiquetas de fecha y hora
        self.label_fecha.config(text=fecha_actual)
        self.label_hora.config(text=hora_actual)

        # Llamar a este método nuevamente cada
        self.after(1000, self.actualizar_fecha_y_hora)