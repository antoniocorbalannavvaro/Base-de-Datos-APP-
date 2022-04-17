from tkinter import *
from tkinter import messagebox
import sqlite3

#RAIZ:
root=Tk()
root.title("Sistema de BBDD")
root.geometry("260x400")

#-----------------------FUNCIONES----------------------#
def crearBase():

	try:
		miConexion=sqlite3.connect("Base de datos")
		miCursor=miConexion.cursor()

		miCursor.execute('''
			CREATE TABLE USUARIOS (
			ID INTEGER PRIMARY KEY AUTOINCREMENT, 
			NOMBRE VARCHAR(50), 
			APELLIDO VARCHAR(50), 
			CORREO VARCHAR(50) UNIQUE, 
			CONTRASEÑA VARCHAR(50), 
			COMENTARIO VARCHAR(100))
			''')

		messagebox.showinfo("BBDD","La base de datos se ha creado correctamente")

	except sqlite3.OperationalError:
		messagebox.showwarning("Error","La base de datos ya ha sido creada")

def salir():
	valor=messagebox.askquestion("Cerrar programa","¿Deseas salir de la aplicación?")
	if valor=="yes":
		root.destroy()

def borrarCampos():
	idEntry.delete(0, "end")
	nombreEntry.delete(0, "end")
	apellidoEntry.delete(0, "end")
	correoEntry.delete(0, "end")
	contraseñaEntry.delete(0, "end")
	comentarioEntry.delete("1.0","end")

def licencia():
	messagebox.showinfo("Licencia","Versión 1.0.1. La licencia es válida")

def acercaDe():
	messagebox.showinfo("Acerca del programa","Este programa es una mierda ¿Verdad?")

def crear():

	try:
		miConexion=sqlite3.connect("Base de datos")
		miCursor=miConexion.cursor()

		datosIntroducidos = (miNombre.get(), miApellido.get(), miCorreo.get(), miContraseña.get(), comentarioEntry.get('1.0', END))

		miCursor.execute('INSERT INTO USUARIOS VALUES(NULL,?,?,?,?,?)', datosIntroducidos)
		miConexion.commit()

		messagebox.showinfo('Información', '¡Registro creado con éxito!')

	except sqlite3.IntegrityError:
		messagebox.showwarning("Error","El correo ya se encuentra en la base de datos. Recuerda que no se pueden repetir direcciones de email.")

def leer():
	miConexion=sqlite3.connect("Base de datos")
	miCursor=miConexion.cursor()
	
	miCursor.execute("SELECT * FROM USUARIOS WHERE ID=" + miId.get())
	elUsuario=miCursor.fetchall()

	for i in elUsuario:

		miId.set(i[0])
		miNombre.set(i[1])
		miApellido.set(i[2])
		miCorreo.set(i[3])
		miContraseña.set(i[4])
		comentarioEntry.insert(1.0, i[5])

	miConexion.commit()

def actualizar():
	miConexion=sqlite3.connect("Base de datos")
	miCursor=miConexion.cursor()

	"""miCursor.execute("UPDATE USUARIOS SET NOMBRE='" + miNombre.get() +
		"', APELLIDO'" + miApellido.get() +
		"', CORREO'" + miCorreo.get() +
		"', CONTRASEÑA'" + miContraseña.get() +
		"', COMENTARIO'" + comentarioEntry.get("1.0", END) +
		"' WHERE ID'" + miId.get())"""

	datosIntroducidos = (miNombre.get(), miApellido.get(), miCorreo.get(), miContraseña.get(), comentarioEntry.get('1.0', END))

	miCursor.execute("UPDATE USUARIOS SET NOMBRE=?,APELLIDO=?,CORREO=?,CONTRASEÑA=?,COMENTARIO=?" +
		"WHERE ID=" + miId.get(), datosIntroducidos)

	miConexion.commit()
	messagebox.showinfo("BBDD", "Los datos se han actualizado correctamente")

def borrar():	
	miConexion=sqlite3.connect("Base de datos")
	miCursor=miConexion.cursor()
	#miCursor.execute("DELETE FROM USUARIOS WHERE NOMBRE_ARTICULO='Pantalones'")
	
	miCursor.execute("DELETE FROM USUARIOS WHERE ID=" + miId.get())

	miConexion.commit()

	messagebox.showinfo("BBDD", "Registro borrado correctamente")
#---------------------------------FIN_FUNCIONES----------------------------------


#---------------------INICIO_MENU------------------------------------------------
#BARRA DE MENU:
barraMenu=Menu(root) #Crea barra de menú.
root.config(menu=barraMenu, width=300,height=370)
archivoMenu=Menu(barraMenu, tearoff=0) #Crea las subcategorías dentro de cada barra de menú.

#VARIABLES DEL MENU: (No visibles)
archivoBBDD=Menu(barraMenu,tearoff=0)
archivoBorrar=Menu(barraMenu,tearoff=0)
archivoCRUD=Menu(barraMenu,tearoff=0)
archivoAyuda=Menu(barraMenu,tearoff=0)
archivoCSV=Menu(barraMenu,tearoff=0)

#LABELS DEL MENU: (Menús principales)
barraMenu.add_cascade(label="BBSS", menu=archivoBBDD)
barraMenu.add_cascade(label="Borrar", menu=archivoBorrar)
barraMenu.add_cascade(label="CRUD", menu=archivoCRUD)
barraMenu.add_cascade(label="Ayuda", menu=archivoAyuda)
barraMenu.add_cascade(label="CSV", menu=archivoCSV)

#LABELS DEL SUBMENU: (Menús secundarios)
archivoBBDD.add_command(label="Conectar",command=crearBase)
archivoBBDD.add_command(label="Salir", command=salir)

archivoBorrar.add_command(label="Borrar campos", command=borrarCampos)

archivoCRUD.add_command(label="Crear",command=crear)
archivoCRUD.add_command(label="Leer",command=leer)
archivoCRUD.add_command(label="Actualizar",command=actualizar)
archivoCRUD.add_command(label="Borrar",command=borrar)

archivoAyuda.add_command(label="Lincencia",command=licencia)
archivoAyuda.add_command(label="Acerca de... ",command=acercaDe)

#---------------------------------FIN_MENU-----------------------------------

#----------------------INICIO_BOTONES INFERIORES-----------------------------

botonCreate=Button(root,text="Create",command=crear)
#botonCreate.grid(row=6,column=0,padx=5, pady=10,columnspan=1)
botonCreate.place(x=10,y=360)

botonRead=Button(root,text="Read",command=leer) #command=
#botonRead.grid(row=6,column=1,padx=5, pady=10,columnspan=2)
botonRead.place(x=70,y=360)

botonUpdate=Button(root,text="Update",command=actualizar) #command=
#botonUpdate.grid(row=6,column=2,padx=5, pady=10,columnspan=3)
botonUpdate.place(x=125,y=360)

botonDelete=Button(root,text="Delete", command=borrar)
#botonDelete.grid(row=6,column=3,padx=5, pady=10,columnspan=4)
botonDelete.place(x=190,y=360)

#----------------------FIN_BOTONES_INFERIORES--------------------------------

#----------------------INICIO_CAMPOS_DE_LA_BBSS------------------------------
#LABELS:
idLabel=Label(root, text="ID:")
idLabel.grid(row=0,column=0,sticky="e", padx=20, pady=10)
idLabel.config(justify="right")

nombreLabel=Label(root, text="Nombre:")
nombreLabel.grid(row=1,column=0,sticky="e", padx=20, pady=10)
nombreLabel.config(justify="right")

apellidoLabel=Label(root, text="Apellido:")
apellidoLabel.grid(row=2,column=0,sticky="e",padx=20, pady=10)
apellidoLabel.config(justify="right")

correoLabel=Label(root, text="Correo:")
correoLabel.grid(row=3,column=0,sticky="e",padx=20, pady=10)
correoLabel.config(justify="right")

contraseñaLabel=Label(root, text="Contraseña:")
contraseñaLabel.grid(row=4,column=0,sticky="e",padx=20, pady=10)
contraseñaLabel.config(justify="right")

comentarioLabel=Label(root, text="Comentario:")
comentarioLabel.grid(row=5,column=0,sticky="e",padx=20, pady=10)
comentarioLabel.config(justify="right")

#ENTRYS:
#----------------------#
#Para poder utilizar el valor que le asignemos al entry en el interfaz.
#En Entry usaremos textvariable = miId, para vincularlos.
miId=StringVar()
miNombre=StringVar()
miApellido=StringVar()
miCorreo=StringVar()
miContraseña=StringVar()
#----------------------#

idEntry=Entry(root,textvariable=miId)
idEntry.grid(row=0,column=1)

nombreEntry=Entry(root,textvariable=miNombre)
nombreEntry.grid(row=1,column=1)

apellidoEntry=Entry(root,textvariable=miApellido)
apellidoEntry.grid(row=2,column=1)

correoEntry=Entry(root,textvariable=miCorreo)
correoEntry.grid(row=3,column=1)

contraseñaEntry=Entry(root,textvariable=miContraseña)
contraseñaEntry.grid(row=4,column=1)
contraseñaEntry.config(show="*")

comentarioEntry=Text(root, width=15,height=8)
comentarioEntry.grid(row=5,column=1)
scrollVert=Scrollbar(root, command=comentarioEntry.yview)
scrollVert.grid(row=5,column=2, sticky="nsw")
comentarioEntry.config(yscrollcommand=scrollVert.set)

#----------------------FIN_CAMPOS_DE_LA_BBSS------------------------------

root.mainloop()