import cv2
import numpy as np
import imutils
import os
ruta = 'C:/Users/luis_/Documents/proyecto/rostro' #ruta donde estan las fotos
        imagePaths = os.listdir(ruta)#creamos una lista de las carpetas
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
                if result[1] < 4500 and result[1] > 2800:
                    cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)#ponemos nombre 
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)#creamos rentangul
                else:
                    cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)#ponemos desconocido
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)#creamos rentangulo
            cv2.imshow('frame',frame)#muestra la imagen
            k = cv2.waitKey(1)#camara encendida
            if k == 27:#si precionas esc se cierra la marara
                break
        cap.release()#apagamos camara
        cv2.destroyAllWindows()#destruimos las ventanas que queden de opencv