#-----------------------------------------------------paquetes-------------------------------------------------------------
import sqlite3
import sys
import cv2
import numpy as np
import imutils
import os
from PyQt5.QtSql import *
from PyQt5.QtWidgets import QApplication, QMainWindow,QDialog, QMessageBox, QTabWidget,QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
import re
from os import remove
#---------------------------------------------login-------------------------------------------
class loginn(QMainWindow):#creacion de clase 
    def __init__(self):#creacion de fincion __init___
        super(loginn,self).__init__()#invocacion de la clase
        loadUi("login.ui",self)#mandamos llamar a la interfaz login
        self.botonregistrar.clicked.connect(self.registrar)#mandamos llamar al boton registro
        self.botonprender.clicked.connect(self.prenderca)#mandamos llamar al boton prender    

    def prenderca(self):#creamos la funcion perderca
        ruta = "C:/Users/Brand/OneDrive/Documentos/Proyecto-modular/Rostro" #ruta donde estan las fotos
        imagen = os.listdir(ruta)#creamos una lista de las carpetas
        reconocimiento = cv2.face.EigenFaceRecognizer_create()#creamos el reconocimeinto
        # Leyendo el modelo
        reconocimiento.read('EigenFaceRecognizer.xml')#madamos llamar al reconocimieno
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)#prendemos camra
        detector = cv2.CascadeClassifier('cascade.xml')#mandamos llamar al detector
        while True:
            ret,frame = cap.read()#leer lo de camara
            if ret == False: break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#pnemos las imagenes en gris
            auxFrame = gray.copy()#copiamos lo de la camara
            faces = detector.detectMultiScale(gray,1.3,5)#nivelamos los parametro de imagen
            for (x,y,w,h) in faces:
                rostro = auxFrame[y:y+h,x:x+w]#pasamos los parametros a rostro
                rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)#cambiamos el tamañano de la imagen
                result = reconocimiento.predict(rostro)#comparams rostro
                cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)#ponemos el numero de rango
                
                # EigenFaces
                if result[1] < 4500 and result[1] > 2400:
                    cv2.putText(frame,'{}'.format(imagen[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)#ponemos nombre 
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)#creamos rentangulo
                   # QMessageBox.information(self, "registro", "nombre correcto", QMessageBox.Ok)#nos aparec un mensaje
                    #cap.release()#apagamos camara
                    #cv2.destroyAllWindows()#destruimos las ventanas que queden de opencv
                else:
                    cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)#ponemos desconocido
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)#creamos rentangulo
            cv2.imshow('frame',frame)#muestra la imagen
            k = cv2.waitKey(1)#camara encendida
            if k == 27:#si precionas esc se cierra la marara
                break
        cap.release()#apagamos camara
        cv2.destroyAllWindows()#destruimos las ventanas que queden de opencv
        
            
        
    def registrar(self):#creamos la funsion registarar
        widget.setCurrentIndex(widget.currentIndex()+1)#nos dirije a la segunda interfaz grafica la cual es loginregistro
        
class regislogin(QMainWindow):#creamos la clase  menu 
    def __init__(self):#creamos la funsion __init__
        super(regislogin,self).__init__()#invocacion de la clase
        loadUi("registrar.ui",self)#mandamos llamar a la interfaz loginregistro
        self.botonregresar.clicked.connect(self.regresarr)#mandamos llamar al boton registro
        self.botonprender.clicked.connect(self.prendercam)#mandamos llamar al boton prender
        self.botonregistrar.clicked.connect(self.registro)#mandamos llamar al boton registrar
        self.botoncu.clicked.connect(self.registroc)#mandamos llamar al boton cu
        self.botoncompro.clicked.connect(self.compro)#mandamos llamar al boton compro
        
    def prendercam(self):
        nombre =str(self.nombre.text())#copiamos lo que esta en lineedit
        ruta = "C:/Users/Brand/OneDrive/Documentos/Proyecto-modular/Rostro"#ruta donde estan las fotos
        carpet = ruta + '/' + nombre#concatenamos ruta y nombre
        if not os.path.exists(carpet):#verificamos si la carpeta existe
            os.makedirs(carpet)#creamos la carpeta
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)#prendemos la camara
        detector = cv2.CascadeClassifier('cascade.xml')#mandamos llamar al detector
        count = 0#creamos un contador
        while True:
            
            ret, frame = cap.read()#leer lo de camara
            if ret == False: break
            frame =  imutils.resize(frame, width=640)#le damos tamaño a la imagen
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#la imagen a grises
            auxFrame = frame.copy()#copiamos lo de frame 
            faces = detector.detectMultiScale(gray,1.3,5)#nivelamos los parametro de imagen
            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)#dibujamos un rectangulo
                rostro = auxFrame[y:y+h,x:x+w]#copiamos lo de auxiliar 
                rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)#cambiamos el tamañano de la imagen
                cv2.imwrite(carpet + '/rotro_{}.jpg'.format(count),rostro)#guaramos rostro
                count = count + 1#contador incrementando
            cv2.imshow('frame',frame)#muestra la imagen
            k =  cv2.waitKey(1)#dejamos camara prendida
            if k == 27 or count >= 50:
                break
        cap.release()#apagamos camara
        cv2.destroyAllWindows()#cerramos todas las ventanas

 
        
    def regresarr(self):#creamos la funcion regresarr
        widget.setCurrentIndex(widget.currentIndex()-1)#nos dirije a la segunda interfaz grafica la cual es loginregistro
        
    def registro(self):#creamos la funcion regstro
        self.miconeccion=sqlite3.connect("login.db")#mandamos llamar a la base de datos empleados
        self.micursor=self.miconeccion.cursor()#creamos un puntero
        self.nombr =str(self.nombre.text())#copiamos lo que este en lienedid
        self.val ="^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$"#Expresion regular por la cual se basa a validar
        self.resultado = re.search(self.val,self.nombr)#comparamos la validacion con el nombre
        self.query='select * from login where  nombre=?'#buscamos el nombre de la sabe de datos
        self.micursor.execute(self.query,(self.nombr,))#ingresamos a la base detos
        if self.micursor.fetchall():#si son iguales entra 
            QMessageBox.information(self, "registro", "nombre ya existente", QMessageBox.Ok)#nos aparec un mensaje
        elif not self.resultado:
            QMessageBox.information(self, "registro", "no numeros", QMessageBox.Ok)#nos aparec un mensaje
        else:#si no 
            self.queryy='insert into login (nombre)values(?)'#accedemos a la tabla logn
            self.micursor.execute(self.queryy,(self.nombr,))#ingresamos el nombre a la base de datos
            QMessageBox.information(self, "registro", "nombre correcto", QMessageBox.Ok)#nos aparec un mensaje
            remove("EigenFaceRecognizer.xml")#remover archivo
            ruta = "C:/Users/Brand/OneDrive/Documentos/Proyecto-modular/Rostro"# ruta de la carpeta
            nombrelis = os.listdir(ruta)#hacemos una lista de carpetas
            labels = []#creamos variabe labels
            fotos = []#creamos variable labels
            label = 0#creamos label 
            for nombredir in nombrelis:
                carut = ruta + '/' + nombredir#creamos la ruta
                for nombrearch in os.listdir(carut):
                    labels.append(label)#agregamos un nuevo elemento
                    fotos.append(cv2.imread(carut+'/'+nombrearch,0))
                label = label + 1#label incrementa
            face_recognizer = cv2.face.EigenFaceRecognizer_create()#creamos archivo
            face_recognizer.train(fotos, np.array(labels))#entrenamos al reconocimiento
            face_recognizer.write('EigenFaceRecognizer.xml')#guardamos archivo
        self.miconeccion.commit()#esto nos sirve para que este la coneccion hasta que queramos
        self.miconeccion.close()#serramos la coneccion 
        widget.setCurrentIndex(widget.currentIndex()-1)#nos dirije a la segunda interfaz grafica la cual es loginregistro
            
        
        
        
    def registroc(self):#creamos la funcion registroc
        nombre =str(self.nombre.text())#copiamos lo que esta en lineedit
        ruta = "C:/Users/Brand/OneDrive/Documentos/Proyecto-modular/Rostro"#ruta donde estan las fotos
        carpet = ruta + '/' + nombre#concatenamos ruta y nombre
        if not os.path.exists(carpet):#verificamos si la carpeta existe
            os.makedirs(carpet)#creamos la carpeta
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)#prendemos la camara
        detector = cv2.CascadeClassifier('cascade.xml')#mandamos llamar al detector
        count = 0#creamos un contador
        while True:
            
            ret, frame = cap.read()#leer lo de camara
            if ret == False: break
            frame =  imutils.resize(frame, width=640)#le damos tamaño a la imagen
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#la imagen a grises
            auxFrame = frame.copy()#copiamos lo de frame 
            faces = detector.detectMultiScale(gray,1.3,5)#nivelamos los parametro de imagen
            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)#dibujamos un rectangulo
                rostro = auxFrame[y:y+h,x:x+w]#copiamos lo de auxiliar 
                rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)#cambiamos el tamañano de la imagen
                cv2.imwrite(carpet + '/rotroc_{}.jpg'.format(count),rostro)#guaramos rostro
                count = count + 1#contador incrementando
            cv2.imshow('frame',frame)#muestra la imagen
            k =  cv2.waitKey(1)#dejamos camara prendida
            if k == 27 or count >= 50:
                break
        cap.release()#apagamos camara
        cv2.destroyAllWindows()#cerramos todas las ventanas



        
        
    def compro(self):#creamos la funcion compro
        miconeccion=sqlite3.connect("login.db")#mandamos llamar a la base de datos empleados
        micursor=miconeccion.cursor()#creamos un puntero
        self.nombr =str(self.nombre.text())#copiamos el texto de lineedis 
        self.val ="^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$"#Expresion regular por la cual se basa a validar
        self.resultado = re.search(self.val,self.nombr)
        
        self.query='select * from login where  nombre=?'#seleccionamos la base de datos
        micursor.execute(self.query,(self.nombr,))#agregamos el nobre a la  base de datos
        if micursor.fetchall():#si son iguales entra 
            QMessageBox.information(self, "registro", "nombre ya existente", QMessageBox.Ok)#nos aparec un mensaje
        elif not self.resultado:
            QMessageBox.information(self, "registro", "no numeros", QMessageBox.Ok) #nos aparec un mensaje
       
        else:#si no 
            QMessageBox.information(self, "registro", "nombre correcto", QMessageBox.Ok)#nos aparec un mensaje
        
        miconeccion.commit()#esto nos sirve para que este la coneccion hasta que queramos
        miconeccion.close()#serramos la coneccion 
        
        
                
            
        







app=QApplication(sys.argv)#mandamos llamar a QApplication para que funcione
widget=QtWidgets.QStackedWidget()#mandamos llamar a widges para que nso permita usar las interfaces 
_login=loginn()#pasamos lo de login a _login
_regislogin=regislogin()#pasmos lo de loginregistro a _loginregistro

widget.addWidget(_login)#estos nos sirve para decir que _login es un widget  
widget.addWidget(_regislogin)#estos nos sirve para decir que _loginregistro es un widget  
widget.show()#nos sirve para visualizar las intyerfaces 
sys.exit(app.exec_())#para que el programa se mantenga abierto hasta que nosotros queramos
