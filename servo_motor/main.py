#------------------LLAMADO DE BIBLIOTECAS------------------------------------

import cv2
import serial
import mediapipe as mp
#----------------------------- Puerto Serial Configuracion ----------------------------
com = serial.Serial("COM3", 9600, write_timeout= 10)

i = 'i'  #izquierda
d = 'd'  #derecha
p = 'p'  #parado
ar = 'a'    #arriba
ab = 'b'    #abajo

marca = 0
#--------------------DECLARAMOS EL DETECTOR DE ROSTRO---------------------



detector = mp.solutions.face_detection
dibujo = mp.solutions.drawing_utils

#------------------CAPTURA DE VIDEO-------------------------

camara = cv2.VideoCapture(0,cv2.CAP_DSHOW)

def mouse(evento, xm, ym, bandera, param):
    global xmo, ymo, marca
    # Evento doble click
    if evento == cv2.EVENT_LBUTTONDOWN:
        xmo = xm
        ymo = ym
        marca = 1
        #print(xmo, ymo)


#----------FUCION WHILE PARA OBTENCION DE FOTOGRAMAS--------------------

with detector.FaceDetection(min_detection_confidence=0.75) as rostros:
    while True:
        ret, frame = camara.read()

        frame=cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        resultado = rostros.process(rgb)


        listacentro = []
        click = []
        listarostro = []

        if resultado.detections is not None:
            for rostro in resultado.detections:
                dibujo.draw_detection(frame, rostro, dibujo.DrawingSpec(color=(0,255,0),))

                for id, puntos in enumerate(resultado.detections):



                    #Extraemos el ancho y el alto del pantalla
                    al, an, c = frame.shape

                    #Extraemos el medio de la pantalla
                    centro_ancho = int(an / 2)
                    centro_alto = int(al / 2)

                    #Extraemos las coordenadas X e Y min
                    x = puntos.location_data.relative_bounding_box.xmin
                    y = puntos.location_data.relative_bounding_box.ymin

                    #Extraemos el ancho y el alto
                    ancho = puntos.location_data.relative_bounding_box.width
                    alto = puntos.location_data.relative_bounding_box.height

                    #Pasamos X e Y a coordenadas en pixeles
                    x, y = int(x * an), int(y * al)
                    print("X, Y: ", x, y)

                    #Pasamos el ancho y el alto a pixeles
                    x1, y1 = int(ancho * an), int(alto * al)
                    xf, yf = x + x1, y + y1

                    #Extraemos el punto central
                    cx = (x + (x + x1)) // 2
                    cy = (y + (y + y1)) // 2
                    #print("Centro: ", cx, cy)

                    listacentro.append([id, cx, cy])
                    listarostro.append([x, y, x1, y1])

                    #Mostrar un punto en el centro
                    cv2.circle(frame, (cx, cy), 3, (0, 0, 255), cv2.FILLED)
                    cv2.line(frame, (cx, 0), (cx, 480), (0, 0, 255), 2)

                    cv2.namedWindow('Camara')
                    cv2.setMouseCallback('Camara', mouse)

                    if marca == 1:
                        # SI estamos dentro de las coordenadas
                        if x < xmo < xf and y < ymo < yf:
                            # Dibujamos el click
                            cv2.circle(frame, (xmo, ymo), 20, (0, 255, 0), 2)
                            cv2.rectangle(frame, (x, y), (xf, yf), (255, 255, 0), 3)  # Dibujamos el rectangulo
                            cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
                            xmo = cx
                            ymo = cy

                            print("coordenada X del rostro",xmo)
                            print("coordenada Y del rostro",ymo)
                            print("centro_ancho", centro_ancho)
                            print("centro_alto", centro_alto)

                            # Condiciones para mover el servo en eje "X"

                            if xmo < centro_ancho - 50:
                                # Movemos hacia la izquierda
                                print("izquierda")
                                com.write(i.encode("ascii"))
                                print(i)

                            if xmo > centro_ancho + 50:
                                # Movemos hacia la derecha
                                print("derecha")
                                com.write(d.encode("ascii"))
                                print(d)

                            #if xmo>=270 and xmo<=370:
                            #    # Paramos el servo
                            #    print("centro x")
                            #    com.write(p.encode("ascii"))
                            #    print(p)

                            #Condiciones de eje Y

                            if ymo < centro_alto - 50:
                                # Movemos hacia arriva
                                print("arriba")
                                com.write(ar.encode("ascii"))
                                print(ar)

                            if ymo > centro_alto + 50:
                                # movemos hacia abajo
                                print("abajo")
                                com.write(ab.encode("ascii"))
                                print(ab)

                            if ymo>=190 and ymo<=290 and xmo>=270 and xmo<=390:
                                #paramos el servo
                                print("centro y")
                                com.write(p.encode("ascii"))
                                print(p)


        cv2.imshow("Camara", frame)
        t = cv2.waitKey(1)
        if t == 27:
            com.close()
            break
camara.release()
cv2.destroyAllWindows()

