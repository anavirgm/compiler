import tkinter as tk

from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import ttk
import re



#Funcionamiento de los botones

def bold_action(event=None):
    sel_ranges = textoarea.tag_ranges("sel")
    if sel_ranges:
        start, end = sel_ranges
        current_tags = textoarea.tag_names(start)
        if "bold" in current_tags:
            textoarea.tag_remove('bold', start, end)
        else:
            textoarea.tag_add("bold", start, end)
            textoarea.tag_configure("bold", font=("Arial", 12, "bold"))


def italic_action(event=None):
    current_tags = textoarea.tag_names("sel.first")
    if "italic" in current_tags:
        textoarea.tag_remove('italic', 'sel.first','sel.last')
    else:
        textoarea.tag_add("italic", "sel.first", "sel.last")
        textoarea.tag_configure("italic", font=("Arial", 12, "italic"))

def underline_action(event=None):
    current_tags = textoarea.tag_names("sel.first")
    if "underline" in current_tags:
        textoarea.tag_remove('underline', 'sel.first','sel.last')
    else:
        textoarea.tag_add("underline", "sel.first", "sel.last")
        textoarea.tag_configure("underline", font=("Arial", 12, "underline"))

def cambiar_color_fuente():
    color = colorchooser.askcolor(title="Seleccionar color")
    if color[1]:
        textoarea.tag_add("color_fuente", "sel.first", "sel.last")
        textoarea.tag_configure("color_fuente", foreground=color[1])

def align_left_action():
    textoarea.tag_remove("center", 1.0, "end")
    textoarea.tag_remove("right", 1.0, "end")
    textoarea.tag_add("left", "sel.first", "sel.last")
    textoarea.tag_configure("left", justify=LEFT)

def align_center_action():
    textoarea.tag_remove("left", 1.0, "end")
    textoarea.tag_remove("right", 1.0, "end")
    textoarea.tag_add("center", "sel.first", "sel.last")
    textoarea.tag_configure("center", justify=CENTER)

def align_right_action():
    textoarea.tag_remove("left", 1.0, "end")
    textoarea.tag_remove("center", 1.0, "end")
    textoarea.tag_add("right", "sel.first", "sel.last")
    textoarea.tag_configure("right", justify=RIGHT)



#análisis léxico
def ejecutar_analisis_lexico():
    lines = textoarea.get(0.0, tk.END).splitlines()

    tokens = []

    for line in lines:
        words = line.split()

        for word in words:
            if word in [
                "si",
                "entonces",
                "sino",
                "fin",
                "mientras",
                "hacer",
                "finmientras",
                "para",
                "finpara",
                "repetir",
                "hasta",
                "leer",
                "escribir",
            ]:

                tokens.append((word, "palabra reservada"))
   
            elif word.isalpha():

                tokens.append((word, "variable"))

            elif word.isdigit():

                tokens.append((word, "numero"))
           
            elif word in ["+", "-", "*", "/", "=", "<", ">", "<=", ">=", "==", "!="]:
           
                tokens.append((word, "operador"))
          
            elif word in ["(", ")", ";"]:
               
                tokens.append((word, "separador"))
          
            elif word.startswith("#"):
              
                tokens.append((word, "inicio de comentario"))
            else:
                
                tokens.append((word, "no reconocida"))

    # Crear una nueva ventana
    newWindow = tk.Toplevel()
    newWindow.title("Resultado del Análisis Léxico")
    
    # Crear un Treeview para mostrar los resultados
    tree = ttk.Treeview(newWindow, columns=("Token", "Clasificación"), style="Custom.Treeview")
    tree.heading("#0", text="Índice")
    tree.heading("Token", text="Token")
    tree.heading("Clasificación", text="Clasificación")
    
    # Insertar los resultados en el Treeview
    for idx, token in enumerate(tokens, start=1):
        tree.insert("", idx, text=str(idx), values=(token[0], token[1]))

    # Configurar el Treeview
    tree.pack(expand=True, fill="both")

    letterCount = len([x for x in textoarea.get(0.0, tk.END) if x.isalpha()])
    numberCount = len([x for x in textoarea.get(0.0, tk.END) if x.isdigit()])
    unrecognizedCount = len([x for x in tokens if x[1] == "no reconocida"])
    whitespaceCount = len([x for x in textoarea.get(0.0, tk.END) if x.isspace()])
    newlineCount = len([x for x in textoarea.get(0.0, tk.END) if x == "\n"])
    comentariosCount = len([x for x in tokens if x[1] == "inicio de comentario"])

    # Mostrar estadísticas en etiquetas con colores
    tk.Label(newWindow, text=f"Letras: {letterCount}", foreground="blue").pack()
    tk.Label(newWindow, text=f"Números: {numberCount}", foreground="blue").pack()
    tk.Label(newWindow, text=f"No reconocidas: {unrecognizedCount}", foreground="red").pack()
    tk.Label(newWindow, text=f"Espacios en blanco: {whitespaceCount}", foreground="green").pack()
    tk.Label(newWindow, text=f"Saltos de línea: {newlineCount}", foreground="green").pack()
    tk.Label(newWindow, text=f"Comentarios: {comentariosCount}", foreground="purple").pack()
    
    # Contenido sin espacios con fondo azul
    content_label = tk.Label(
        newWindow,
        text="Contenido sin espacios: " + textoarea.get(0.0, tk.END).replace(" ", "").replace("\n", ""),
        background="lightblue",
    )
    content_label.pack()

    # Aplicar estilos
    style = ttk.Style()
    style.configure("Custom.Treeview", background="#e1f0ff", foreground="black", fieldbackground="#e1f0ff")





#Funciones de archivo

archivo_guardado = None


def nuevo(event=None):
    # Eliminar el contenido actual del área de texto
    textoarea.delete("1.0", "end")

def abrir(event=None):
    # Abrir el cuadro de diálogo de selección de archivo
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    if archivo:
        # Leer el contenido del archivo seleccionado
        with open(archivo, "r") as f:
            contenido = f.read()
        # Insertar el contenido en el área de texto
        textoarea.delete("1.0", "end")
        textoarea.insert("1.0", contenido)

def guardar(event=None):
    global archivo_guardado

    if archivo_guardado:
        # Si hay un archivo guardado previamente, se guarda directamente en ese archivo
        contenido = textoarea.get("1.0", "end")
        with open(archivo_guardado, "w") as f:
            f.write(contenido)
    else:
        # Si no hay un archivo guardado previamente, se utiliza la lógica de "Guardar como..."
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if archivo:
            contenido = textoarea.get("1.0", "end")
            with open(archivo, "w") as f:
                f.write(contenido)
                archivo_guardado = archivo

def guardar_como(event=None):
    # Abrir el cuadro de diálogo de guardar archivo
    archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    if archivo:
        # Obtener el contenido del área de texto
        contenido = textoarea.get("1.0", "end")
        # Guardar el contenido en el archivo seleccionado
        with open(archivo, "w") as f:
            f.write(contenido)


#Funciones de Editar

def cortar(event=None):
    # Check if there is a selection (text tagged with "sel")
    if textoarea.tag_ranges("sel"):
        contenido = textoarea.get("sel.first", "sel.last")
        textoarea.delete("sel.first", "sel.last")
        root.clipboard_clear()
        root.clipboard_append(contenido)

def copiar(event=None):
    contenido = textoarea.get("sel.first", "sel.last")
    root.clipboard_clear()
    root.clipboard_append(contenido)

def pegar(event=None):
    contenido = root.clipboard_get()
    textoarea.insert("insert", contenido)

def eliminar(event=None):
    textoarea.delete("sel.first", "sel.last")

def salir(event=None):
    root.quit()

def maximizar_ventana(event=None):
    root.attributes('-zoomed', True)

def restaurar_ventana(event=None):
    root.attributes('-zoomed', False)

def minimizar_ventana(event=None):
    root.iconify()

root = Tk()
root.title('Editor de texto')
root.geometry('500x500+10+10')
root.resizable(True, True)  # Permitir redimensionar la ventana
menubar = Menu(root)
root.config(menu=menubar)

# Archivo

archivomenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='Archivo', menu=archivomenu)
archivomenu.add_command(label='Nuevo', accelerator='Ctrl+N', command=nuevo)
archivomenu.add_command(label='Abrir...', accelerator='Ctrl+A', command=abrir)
archivomenu.add_command(label='Guardar', accelerator='Ctrl+G', command=guardar)
archivomenu.add_command(label='Guardar como...', accelerator='Ctrl+Mayús+S', command=guardar_como)
archivomenu.add_separator()
archivomenu.add_command(label='Salir', accelerator='Ctrl+Q', command=salir)

# Editar

editarmenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='Edición', menu=editarmenu)
editarmenu.add_command(label='Cortar', accelerator='Ctrl+X', command=cortar)
editarmenu.add_command(label='Copiar', accelerator='Ctrl+C', command=copiar)
editarmenu.add_command(label='Pegar', accelerator='Ctrl+V', command=pegar)
editarmenu.add_command(label='Eliminar', accelerator='Ctrl+Alt+X', command=eliminar)


# Ver

vermenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='Ver', menu=vermenu)
show_herramientasbar = BooleanVar()
show_estadobar = BooleanVar()

def toggle_herramientasbar():
    if show_herramientasbar.get():
        herramientas_bar.pack(side=TOP, fill=X)
    else:
        herramientas_bar.pack_forget()

def toggle_estadobar():
    if show_estadobar.get():
        barraestado.pack(side=BOTTOM)
    else:
        barraestado.pack_forget()

vermenu.add_checkbutton(label='Barra de Herramientas', variable=show_herramientasbar, onvalue=True, offvalue=False, command=toggle_herramientasbar)
vermenu.add_checkbutton(label='Barra de estado', variable=show_estadobar, onvalue=True, offvalue=False, command=toggle_estadobar)

herramientas_bar = Label(background='lightblue')
herramientas_bar.pack(side=TOP, fill=X)


#Analisis lexico

editarmenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='Analisis léxico', menu=editarmenu)
editarmenu.add_command(label='Ejecutar', command=ejecutar_analisis_lexico)


# Botones

boldImage = PhotoImage(file='bold.png')
boldBoton = Button(herramientas_bar, image=boldImage, command=bold_action)
boldBoton.grid(row=0, column=2, padx=5)

italicImage = PhotoImage(file='italic.png')
italicBoton = Button(herramientas_bar, image=italicImage, command=italic_action)
italicBoton.grid(row=0, column=3, padx=5)

underlineImage = PhotoImage(file='underline.png')
underlineBoton = Button(herramientas_bar, image=underlineImage, command=underline_action)
underlineBoton.grid(row=0, column=4, padx=5)

colorfuenteImage = PhotoImage(file='font_color.png')
colorfuenteBoton = Button(herramientas_bar, image=colorfuenteImage, command=cambiar_color_fuente)
colorfuenteBoton.grid(row=0, column=5, padx=5)

izquierdaImage = PhotoImage(file='left.png')
izquierdaBoton = Button(herramientas_bar, image=izquierdaImage, command=align_left_action)
izquierdaBoton.grid(row=0, column=6, padx=5)

centroImage = PhotoImage(file='center.png')
centroBoton = Button(herramientas_bar, image=centroImage, command=align_center_action)
centroBoton.grid(row=0, column=7, padx=5)

derechaImage = PhotoImage(file='right.png')
derechaBoton = Button(herramientas_bar, image=derechaImage, command=align_right_action)
derechaBoton.grid(row=0, column=8, padx=5)

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
textoarea = Text(root, yscrollcommand=scrollbar.set, font=('arial', 12))
textoarea.pack(fill=BOTH, expand=True)
scrollbar.config(command=textoarea.yview)

barraestado = Label(root, text='Barra de Estado')
barraestado.pack(side=BOTTOM)

def mostrar_detalles_texto(event=None):
    linea, columna = textoarea.index(INSERT).split('.')
    barraestado.config(text=f'Línea: {linea}, Columna: {columna}')

textoarea.bind('<KeyRelease>', mostrar_detalles_texto)
mostrar_detalles_texto()

root.bind('<Control-b>', bold_action)
root.bind('<Control-k>', italic_action)
root.bind('<Control-s>', underline_action)
root.bind('<Control-n>', nuevo)
root.bind('<Control-a>', abrir)
root.bind('<Control-g>', guardar)
root.bind('<Control-Shift-s>', guardar_como)
root.bind('<Control-q>', salir)

root.mainloop()