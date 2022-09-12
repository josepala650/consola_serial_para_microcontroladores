# importamos la libreria tkinter
from ast import AugStore
from cgitb import text
from itertools import filterfalse
from operator import truediv
import tkinter # importo tkinter para el icono
from tkinter import *
from tkinter import messagebox as MessageBox
from tkinter import Tk
from tkinter import filedialog as FileDialog #importar el módulo file dialog para pedirle al usuario que seleccione un fichero del disco duro

import serial, time
from playsound import playsound # libreria para reproducir sonido mp3
import threading  # creo la clase segundoplano
from io import open # para trabajar con threading

#variables globales
leer=False # inicializo la variable que determinara si voy a leer con el arduino
leyendo=False # inicializo la variable que me indica si el arduino efectivamente esta leyendo(True)o no(False)
bEncontrado = False # indica si se encontro puerto
conectado = False# indica si esta conectado 
Arduino = serial.Serial() # creo el objeto arduino
datos_enviados=""# variable global donde acumulamos los datos enviados
datos_RECIBIDOS=""#variable global donde acumulamos los datos RECIBIDOS
ruta="" #variable que se utilizara para guardar el texto exportado



# Creamos la raíz de nombre "pala"
pala = Tk()
# configuramos la raiz
pala.title("Consola de comunicación serial versión 0.01")
# creo el icon que se vera en la barra de tareas al ejecutar el prograna
img = tkinter.Image("photo", file="arduino_serial/monitor_serial.png")
pala.tk.call('wm','iconphoto',pala._w,img)

pala.resizable(0, 0)         # Desactivar redimensión de ventana 
pala.config(bg="blue")          # color de fondo, background
pala.config(cursor="pirate")    # tipo de cursor (arrow defecto)
pala.config(relief="sunken")    # relieve del root 
pala.config(bd=10)              # tamaño del borde en píxeles

# Hijo de la ventana pala, no ocurre nada
#creo en el marco pala la ventana de nombre ventanapala
ventanapala_1= Frame(pala)  

# Empaqueta el frame en la raíz
ventanapala_1.pack()      
#insertamos la imagen en el marco "ventanapala_1" para que la imagen este arriba
# la ubicamos en la fila 1 y columna 0
imagen =PhotoImage(file="arduino_serial/usb_serial_off.png")
imagen_fondo= Label(ventanapala_1, image=imagen, bd=0)
imagen_fondo.grid(row=1,column=0,sticky=W, padx=5, pady=5)
# creo una label donde indico el autor en fila 0 columna o
AUTOR = Label(ventanapala_1, text="Autoria=TUTORIALES JEP  .Canal de canal en YouTube= TUTORIALES JEP")
AUTOR.grid(row=0,column=0,sticky=W, padx=5, pady=5)
# Hijo de la ventana pala, no ocurre nada
#creo en el marco pala la ventana de nombre ventanapala
ventanapala = Frame(pala)  

# Empaqueta el frame en la raíz
ventanapala.pack()      

# configuramos la ventana
ventanapala.config(bg="lightblue")    # Color de fondo, background
ventanapala.config(cursor="arrow")         # Tipo de cursor
ventanapala.config(relief="sunken")   # relieve del frame hundido
ventanapala.config(bd=10)             # tamaño del borde en píxeles 
 
# Podemos establecer un tamaño,
# la raíz se adapta al frame que contiene
ventanapala.config(width=400,height=400) 

# VARIABLES A USAR 
Dato_A_enviar = StringVar()# donde cargo el dato a enviar
enviado = StringVar()# donde cargo el dato enviado en la ventana
recibio = StringVar()# donde cargo el dato recibido
variable_puerto = StringVar()# donde cargo el puerto detectado
VELOCIDAD = StringVar()## donde cargo la velocidad en baudios
VELOCIDAD.set(9600)# velocidad de inicial
PUERTO = "" # inicializo la variable de puerto vacia
estado = StringVar() # indica el estado conectado o desconectado
estado.set("Arduino desconectado")

#funciones
def detecto_arduino():
    # Importamos la libreria PySerial
   # import serial
    global variable_puerto
    global VELOCIDAD
    global PUERTO
    global bEncontrado
    bEncontrado=False
    global estado
    estado.set("Arduino desconectado")
    boton_2.configure(text="Conectar")
    global conectado
    conectado=False
    global leer
    leer=False
    global leyendo 
    boton_4.configure(text="Habilitar Lectura")
    if leyendo==False:

        for iPuerto in range(0, 20):
            try:
                PUERTO = '/dev/ttyUSB' + str(iPuerto)   #'/dev/ttyUSB' para linux
                Arduino = serial.Serial(PUERTO, VELOCIDAD.get())
                Arduino.close()
                bEncontrado = True
                break
            except:
                pass
        
        if bEncontrado:

             #print('el puerto del arduino es: ' + '/dev/ttyUSB' + str(iPuerto)+str(VELOCIDAD.get()))# PAARA LINUX
            variable_puerto.set(str(PUERTO))
            cambioimagen_on()
            

        else:
            for iPuerto in range(0, 20):
                try:
                     PUERTO = '/dev/ttyACM' + str(iPuerto)   #'/dev/ttyACM' para linux original
                     Arduino = serial.Serial(PUERTO, VELOCIDAD.get())
                     Arduino.close()
                     bEncontrado = True
                     break
                except:
                    pass

            if bEncontrado:
                #print('el puerto del arduino es: ' + '/dev/ttyACM' + str(iPuerto)+str(VELOCIDAD.get()))# PAARA LINUX
                variable_puerto.set(str(PUERTO))
                cambioimagen_on()
        
            else:
                for iPuerto in range(2, 20):#para windows arranco en COM 2
                    try:
                        PUERTO ='COM'+ str(iPuerto)   #'/dev/ttyACM' para linux original
                        Arduino = serial.Serial(PUERTO, VELOCIDAD.get())
                        Arduino.close()
                        bEncontrado = True
                        break
                    except:
                        pass

                if bEncontrado:
                    #print('el puerto del arduino es: ' + '/dev/ttyACM' + str(iPuerto)+str(VELOCIDAD.get()))# PAARA LINUX
                    variable_puerto.set(str(PUERTO))
                    cambioimagen_on()
                else:
                    #print('No se ha encontrado Ardunio'+PUERTO)
                    variable_puerto.set('No se ha encontrado Ardunio')
                    cambioimagen_off()
    else:
        alerta_leyendo()



  



                 

def cambioimagen_off():
    global imagen # indico que uso la variable imagen que es de tipo global
    global imagen_fondo
    imagen =PhotoImage(file="arduino_serial/usb_serial_off.png")
    imagen_fondo= Label(ventanapala_1, image=imagen, bd=0)
    imagen_fondo.grid(row=1,column=0,sticky=W, padx=5, pady=5)

def cambioimagen_on():
    global imagen # indico que uso la variable imagen que es de tipo global
    global imagen_fondo
    imagen =PhotoImage(file="arduino_serial/usb_serial_on.png")
    imagen_fondo= Label(ventanapala_1, image=imagen, bd=0)
    imagen_fondo.grid(row=1,column=0,sticky=W, padx=5, pady=5)

def conecto_arduino():
    global variable_puerto
    global VELOCIDAD
    global conectado
    global bEncontrado
    global Arduino
    global estado
    global leer
    leer=False
    global leyendo
    boton_4.configure(text="Habilitar Lectura")
    if bEncontrado:
        if leyendo==False:
             if conectado:
                    Arduino.close() 
                    conectado=False
                    #print("arduino desconectado")
                    estado.set("Arduino desconectado")
                    boton_2.configure(text="Conectar")
            
            

             else:
                    Arduino = serial.Serial(PUERTO, VELOCIDAD.get())
                    conectado=True
                    #print("arduino conectado")
                    estado.set("Arduino conectado")
                    boton_2.configure(text="Desconectar")  
        else:
            alerta_leyendo()
    else:
        alerta_detectar()


    
        
def enviar_dato():
    global Arduino
    global Dato_A_enviar
    global conectado
    global datos_enviados
    dato_1=Dato_A_enviar.get()
    if conectado:
        Arduino.flushInput() #borro el bufer de entrada
        Arduino.flushOutput() # borro el bufer de salida
        Arduino.write(dato_1.encode())# envio valor de la variable al arduino variable dat_1.encode()
        #datos_enviados=datos_enviados +dato_1+"\n" # cargo el valor dato_1 y lo acomulo a la variable golbal datos_enviados descendente (último dato abajo)
        datos_enviados=dato_1+"\n"+datos_enviados# ascendente (último dato arriba)
        enviado.set(datos_enviados)# paso el valor de la variable datos_enviados en la variable enviado que la muestra en pantalla
           
    else:
        alerta_conectar()
        
def borro_dato_enviado():
    global datos_enviados
    datos_enviados=""
    enviado.set(datos_enviados)

def leoarduino(estado_2):

    global recibio 
    global Arduino
    global conectado
    global leer
    global leyendo
    global datos_RECIBIDOS
    entrada_1=""
    if estado_2:
        entrada_1=Arduino.readline() # leo la entrada recibida
        if(entrada_1.decode() != ''):
            #print(entrada_1.decode()) # decodifico la entrada y la imprimo
            paso=entrada_1.decode() # variable de paso
            #datos_RECIBIDOS=datos_RECIBIDOS+paso+"\n" # cargo el valor recibido y lo acomulo a la variable golbal datos_RECIBIDOS descendente (último dato abajo)
            datos_RECIBIDOS=paso+"\n"+datos_RECIBIDOS# ascendente (último dato arriba)
            recibio.set(datos_RECIBIDOS) # paso el valor de la variable datos_RECIBIDOS en la variable recibido que la muestra en pantalla
            label2.configure(text="Leyendo")
            leyendo=True
            
    else:
        label2.configure(text="Sin leer")
        leyendo=False

def borro_dato_leido():
    global datos_RECIBIDOS
    datos_RECIBIDOS=""
    recibio.set(datos_RECIBIDOS)

def segundoplano_1():
    global leer
    global conectado
    
    segundoplano = threading.Thread(target=segundoplano_leer)
    if conectado:
        if leer :
            leer=False
            boton_4.configure(text="Habilitar Lectura")
            
        
        else:
            #funcion en segundo plano
            segundoplano.start()   # Iniciamos la ejecución del thread,
            leer=True
            boton_4.configure(text="Deshabilitar Lectura")
            
    
    else:
        alerta_conectar()

def segundoplano_leer():
    global leer
    while True:
        if leer:
            leoarduino(True)
        else:
            leoarduino(False)
        
    


    

def alerta_detectar():
     audio = threading.Thread(target=reproducir_audio)
     audio.start()# Iniciamos la ejecución del thread,
     #creo_ventana()
     mostrar_ventana()
     MessageBox.showwarning("ALERTA", "Falto detectar conexión") # título, mensaje
     oculto_ventana()

def alerta_conectar():
     audio = threading.Thread(target=reproducir_audio)
     audio.start()# Iniciamos la ejecución del thread,
     #creo_ventana()
     mostrar_ventana()
     MessageBox.showwarning("ALERTA", "Falto Conectar") # título, mensaje
     oculto_ventana()

def alerta_leyendo():
     audio = threading.Thread(target=reproducir_audio)
     audio.start()# Iniciamos la ejecución del thread,
     creo_ventana()
     MessageBox.showwarning("ALERTA", "Aún sigues leyendo Oprime el boton para Deshabilitar Lectura . Y enviar un dato a") # título, mensaje
     oculto_ventana()

def reproducir_audio():
     playsound('arduino_serial/audio_3.wav') 
     

     
# Open New Window
def creo_ventana():
    global second
    global imagen_2
    global imagen_fondo_2
    second = Toplevel()
    second.title("no has dicho la palabra magica")   
    second.geometry("498x423+600+0")  
    imagen_2 =PhotoImage(file="arduino_serial/palabra_magica.gif")
    imagen_fondo_2= Label(second, image=imagen_2, bd=0)
    imagen_fondo_2.grid(row=0,column=0,sticky=W, padx=5, pady=5)
 
# Show the window
def mostrar_ventana():
    second.deiconify()
 
# Hide the window
def oculto_ventana():
    second.withdraw()

def exportar_enviados():
    global ruta
    global datos_enviados
    mensaje= StringVar()
    fichero = FileDialog.asksaveasfile(title="Guardar fichero", mode='w',defaultextension=".txt")
    ruta = fichero.name  # El atributo name es la ruta, si está abierto
    if fichero is not None:
        contenido = datos_enviados  # recuperamos el texto que tenemos en la variable texto y lo pasamos a la variable contenido
        fichero = open(ruta, 'w+') # creamos el fichero o abrimos
        fichero.write(contenido)  # escribimos en el txt el texto contenido en la variable contenido
        fichero.close()
        mensaje.set('Fichero guardado correctamente')
    else:
        mensaje.set('Guardado cancelado')

def exportar_recibidos():
    global ruta
    global datos_RECIBIDOS
    mensaje= StringVar()
    fichero = FileDialog.asksaveasfile(title="Guardar fichero", mode='w',defaultextension=".txt")
    ruta = fichero.name  # El atributo name es la ruta, si está abierto
    if fichero is not None:
        contenido = datos_RECIBIDOS  # recuperamos el texto que tenemos en la variable texto y lo pasamos a la variable contenido
        fichero = open(ruta, 'w+') # creamos el fichero o abrimos
        fichero.write(contenido)  # escribimos en el txt el texto contenido en la variable contenido
        fichero.close()
        mensaje.set('Fichero guardado correctamente')
    else:
        mensaje.set('Guardado cancelado')

#etiqueta de texto
label7 = Label(ventanapala, text="Baudios")
label7.grid(row=1,column=0,sticky=W, padx=5, pady=5)

entrada_5 = Entry(ventanapala,justify=CENTER, textvariable=VELOCIDAD)
entrada_5.grid(row=1,column=1,sticky=W, padx=5, pady=5)

label2 = Label(ventanapala, text="Sin leer",width=10)
label2.grid(row=2,column=3,sticky=W, padx=5, pady=5)


entrada_2 = Entry(ventanapala,justify=CENTER, textvariable=Dato_A_enviar)
entrada_2.grid(row=2,column=1,sticky=W, padx=5, pady=5)

label3 = Label(ventanapala, text="Enviado")
label3.grid(row=3,column=0,sticky=W, padx=5, pady=5)

label6 = Label(ventanapala, textvariable=enviado,width=20, height=10,anchor=NW, justify=LEFT)
label6.grid(row=3,column=1,sticky=W, padx=5, pady=5)

label8 = Label(ventanapala, text="Recibido")
label8.grid(row=3,column=2,sticky=W, padx=5, pady=5)

label9 = Label(ventanapala, textvariable=recibio,width=20, height=10,anchor=NW, justify=LEFT)
label9.grid(row=3,column=3,sticky=W, padx=5, pady=5)

label4=Label(ventanapala, text="Puerto de conexión")
label4.grid(row=0,column=1,sticky=W, padx=5, pady=5)

label5=Label(ventanapala, textvariable=variable_puerto,width=27)
label5.grid(row=0,column=2,sticky=W, padx=5, pady=5)

label7=Label(ventanapala, textvariable=estado,width=27)
label7.grid(row=1,column=2,sticky=W, padx=5, pady=5)
#agregamos un boton

boton_1=Button(ventanapala, text="Detectar",command=detecto_arduino,width=10)
boton_1.grid(row=0,column=0,sticky=W, padx=5, pady=5)

boton_2=Button(ventanapala, text="Conectar",command=conecto_arduino,width=10)
boton_2.grid(row=1,column=3,sticky=W, padx=5, pady=5)

boton_3=Button(ventanapala, text="Enviar",command=enviar_dato,width=10)
boton_3.grid(row=2,column=0,sticky=W, padx=5, pady=5)

boton_4=Button(ventanapala, text="Habilitar Lectura",command=segundoplano_1,width=20)
boton_4.grid(row=2,column=2,sticky=W, padx=5, pady=5)

boton_5=Button(ventanapala, text="Borrar datos enviados",command=borro_dato_enviado,width=20)
boton_5.grid(row=4,column=1,sticky=W, padx=5, pady=5)

boton_6=Button(ventanapala, text="Borrar datos Recibidos",command=borro_dato_leido,width=20)
boton_6.grid(row=4,column=3,sticky=W, padx=5, pady=5)

boton_7=Button(ventanapala, text="Guardar datos enviados",command=exportar_enviados,width=20)
boton_7.grid(row=4,column=0,sticky=W, padx=5, pady=5)

boton_8=Button(ventanapala, text="Guardar datos Recibidos",command=exportar_recibidos,width=20)
boton_8.grid(row=4,column=2,sticky=W, padx=5, pady=5)

creo_ventana()
     
oculto_ventana()

# Comenzamos el bucle de aplicación, es como un while True
pala.mainloop()  
