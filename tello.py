from tkinter import *
from djitellopy import Tello
import cv2 as cv
from PIL import Image
from PIL import ImageTk
import easyocr
import matplotlib.pyplot as plt
import numpy as np
from deep_translator import GoogleTranslator
import threading
import enchant
from spellchecker import SpellChecker
import pygame
import threading
import time
from pynput import keyboard

tello = None
takingVideo = False
velocity = [0, 0, 0, 0]

def volar ():
    global tello
    tello.takeoff()
    #tello.takeoff()
    #tello.move_left(50)
    #tello.move_up(50)
    #tello.rotate_clockwise(90)
    #tello.move_forward(50)
    #tello.land()

def aterrizar ():
    global tello
    tello.land()

def abajo ():
    global tello
    tello.move_down(20)
    #tello.send_rc_control(left_right_velocity=0,forward_backward_velocity=0,up_down_velocity=0,yaw_velocity=0)

def arriba ():
    global tello
    tello.move_up(20)
    #tello.send_rc_control(left_right_velocity=20,forward_backward_velocity=0,up_down_velocity=0,yaw_velocity=0)

def takeVideoStream ():
    global tello
    global takingVideo
    while takingVideo:
        telloFrame = tello.get_frame_read().frame
        telloFrame = cv.resize(telloFrame, (360, 240))
        cv.imshow("tello", telloFrame)
        cv.waitKey(1)
    cv.destroyWindow ('tello')

def takeVideoButtonClick ():
    global takingVideo
    takingVideo = True
    x = threading.Thread(target=takeVideoStream)
    x.start()

def stopVideoButtonClick ():
    global takingVideo
    takingVideo = False

def takePictureDroneButtonClick ():
    global tello
    frame = tello.get_frame_read().frame
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    image = Image.fromarray(frame_rgb)
    max_size = (400, 300)
    image.thumbnail(max_size)
    dronePicturePanel.image = ImageTk.PhotoImage(image)
    dronePicturePanel.create_image(0, 0, anchor=NW, image=dronePicturePanel.image)

def connectButtonClick ():
    global tello
    global cap
    tello = Tello()
    tello.connect()
    batteryLabel['text'] = str (tello.get_battery())
    tello.streamon()

    cap = cv.VideoCapture(0)

def maths ():
    global tello
    frame = tello.get_frame_read().frame
    cv.imwrite("Webcam.png", frame)
    reader = easyocr.Reader(['en'], gpu=False)
    img = cv.imread("Webcam.png")
    text_ = reader.readtext(img)
    threshold = 0.25
    for t_, t in enumerate(text_):
         print(t)
         bbox, text, score = t
         if score > threshold:
             cv.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5)
             cv.putText(img, text, bbox[0], cv.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
    resultado = eval(text)
    print(resultado)
    mensaje = f"EXT mled l r 2.5 {resultado}"
    tello.rotate_clockwise(180)
    tello.send_control_command(mensaje)

def traduction ():
    global tello
    frame = tello.get_frame_read().frame
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    cv.imwrite("Webcam.png", frame)
    reader = easyocr.Reader(['en'], gpu=False)
    img = cv.imread("Webcam.png")
    text_ = reader.readtext(img)
    threshold = 0.25
    for t_, t in enumerate(text_):
        print(t)
        bbox, text, score = t
    translated = GoogleTranslator(source='auto', target='en').translate(text)
    print (translated)
    mensaje = f"EXT mled l r 2.5 {translated}"
    tello.rotate_clockwise(180)
    tello.send_control_command(mensaje)

def correccion ():
    global tello
    i = 0
    correcto=0
    while (i<4):
        frame = tello.get_frame_read().frame
        cv.imwrite("Webcam.png", frame)
        reader = easyocr.Reader(['en'], gpu=False)
        img = cv.imread("Webcam.png")
        text_ = reader.readtext(img)
        threshold = 0.25
        for t_, t in enumerate(text_):
            print(t)
            bbox, text, score = t
            if score > threshold:
                cv.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5)
                cv.putText(img, text, bbox[0], cv.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
        try:
            partes = text.split("w")
            resultado = eval(partes[0])
            if(resultado == int(partes[1])):
                print("Correcto")
                correcto= correcto+1
            else:
                print("Incorrecto")
        except Exception as e:
            print("Error en la lectura")
        print("Mover a la derecha")
        tello.move_right(20)
        i=i+1
    msg=f"{correcto}/{i}--"
    mensaje = f"EXT mled l r 2.5 {msg}"
    tello.rotate_clockwise(180)
    tello.send_control_command(mensaje)

def altura ():
    global tello
    i = 0
    j=0
    count = 0
    derecha= True
    correcto=0
    while (j<4):
        while (i<4):
            frame = tello.get_frame_read().frame
            cv.imwrite("Webcam.png", frame)
            reader = easyocr.Reader(['en'], gpu=False)
            img = cv.imread("Webcam.png")
            text_ = reader.readtext(img)
            threshold = 0.25
            for t_, t in enumerate(text_):
                print(t)
                bbox, text, score = t
                if score > threshold:
                    cv.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5)
                    cv.putText(img, text, bbox[0], cv.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
            try:
                partes = text.split("=")
                resultado = eval(partes[0])
                if(resultado == int(partes[1])):
                    print("Correcto")
                    correcto= correcto+1
                    i=i+1
                else:
                    print("Incorrecto")
                    i=i+1
            except Exception as e:
                print("Error en la lectura")
            if(derecha==True):
                print("Mover a la derecha")
                tello.move_right(20)
            else:
                print("Mover a la izquierda")
                tello.move_left(20)
            count=count+1
        derecha= not derecha
        j=j+1
        tello.move_down(20)
        i=0
    msg=f"{correcto}/{count}--"
    mensaje = f"EXT mled l r 2.5 {msg}"
    tello.rotate_clockwise(180)
    tello.send_control_command(mensaje)

def faltas ():
    global tello
    frame = tello.get_frame_read().frame
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    cv.imwrite("Webcam.png", frame)
    reader = easyocr.Reader(['en'], gpu=False)
    img = cv.imread("Webcam.png")
    text_ = reader.readtext(img)
    threshold = 0.25
    for t_, t in enumerate(text_):
        print(t)
        bbox, text, score = t
    spell = SpellChecker(language="es")
    #palabras = text.split()
    #palabras_erroneas = []
    #for palabra in palabras:
    #    if not d.check(palabra):
    #        palabras_erroneas.append(palabra)
    print(text)
    if spell.known (text):
        msg=f"La palabra es correcta"
    else:
        msg="La palabra es erronea"
    mensaje = f"EXT mled l r 2.5 {msg}"
    #tello.rotate_clockwise(180)
    tello.send_control_command(mensaje)

def auto():
    global tello
    amarillo=0
    global takingVideo
    while takingVideo:
        frame = tello.get_frame_read().frame
        frame = cv.resize(frame, (360, 240))
        cv.waitKey(1)
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2
        region = hsv_frame[center_y-10:center_y+10, center_x-10:center_x+10]
        avg_color = np.mean(region, axis=(0, 1))
        if is_yellow(avg_color):
            #tello.send_rc_control(0,0,0,0)
            amarillo=amarillo+1
            print(f"Amarillo detectado {amarillo}")
            #tello.send_rc_control(10,0,0,0)
            time.sleep(1)

def is_yellow(color):
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    return cv.inRange(np.array([[color]], dtype=np.uint8), lower_yellow, upper_yellow)[0][0] == 255

def start_monitoring():
    print("Iniciando")
    global tello
    #tello.send_rc_control(10,0,0,0)
    monitor_thread = threading.Thread(target=auto)
    monitor_thread.start()

def derecha():
    tello.move_right(20)

def on_press(key):
    print("Tecla pulsada")
    global velocity
    try:
        if key.char == '8':  # Flecha hacia arriba
            velocity[1] = 10
        elif key.char == '2':  # Flecha hacia abajo
            velocity[1] = -10
        elif key.char == '4':  # Flecha hacia izquierda
            velocity[0] = -10
        elif key.char == '6':  # Flecha hacia derecha
            velocity[0] = 10
            print("Derecha")
        elif key.char == '7':  # Subir
            velocity[2] = 30
        elif key.char == '1':  # Bajar
            velocity[2] = -10
        send_rc_control()
    except AttributeError:
        pass

def send_rc_control():
    global tello, velocity
    print("Movimiento")
    tello.send_rc_control(velocity[0], velocity[1], velocity[2], velocity[3])

def stop():
    global tello, velocity
    velocity = [0, 0, 0, 0]
    send_rc_control()

def on_release(key):
    global velocity
    if key.char in ['8', '2', '4', '6', '7', '1']:
        stop()

def start_key_listener():
    print("Inicio de movimiento con botones")
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

window = Tk()
window.geometry("800x400")
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=5)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)


connectButton = Button(window, text="Conecta", bg='red', fg="white",command=connectButtonClick)
connectButton.grid(row=0, column=0, padx=5, pady=5, sticky=N + S + E + W)
batteryLabel = Label(window, text = "", font=("Courier", 20, "italic"))
batteryLabel.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky=N + S + E + W)

takePictureDroneButton = Button(window, text="Toma foto con dron", bg='red', fg="white",command=takePictureDroneButtonClick)
takePictureDroneButton.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)
dronePicturePanel = Canvas(window)
dronePicturePanel.grid(row=2, column =0, sticky=N + S + E + W)

takeVideoButton = Button(window, text="Toma video con dron", bg='red', fg="white",command=takeVideoButtonClick)
takeVideoButton.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)

stopVideoButton = Button(window, text="Stop video con dron", bg='red', fg="white",command=stopVideoButtonClick)
stopVideoButton.grid(row=1, column=2, padx=5, pady=5, sticky=N + S + E + W)

mathsComputerButton = Button(window, text='Calculo', bg='red', fg='white',command=maths)
mathsComputerButton.grid(row=1, column=3, padx=5, pady=5, sticky=N + S + E + W)

traductionComputerButton = Button(window, text='Traducir', bg='red', fg='white', command=traduction)
traductionComputerButton.grid(row=1, column=4, padx=5, pady=5, sticky=N + S + E + W)

flyButton = Button(window, text='Volar', bg='red', fg='white', command=volar)
flyButton.grid(row=1, column=5, padx=5, pady=5, sticky=N + S + E + W)

aterrizarButton = Button(window, text='Aterrizar', bg='red', fg='white', command=aterrizar)
aterrizarButton.grid(row=1, column=6, padx=5, pady=5, sticky=N + S + E + W)

abajoButton = Button(window, text='Abajo', bg='red', fg='white', command=abajo)
abajoButton.grid(row=2, column=1, padx=5, pady=5, sticky=N + S + E + W)

arribaButton = Button(window, text='Arriba', bg='red', fg='white', command=arriba)
arribaButton.grid(row=2, column=2, padx=5, pady=5, sticky=N + S + E + W)

#faltasButton = Button(window, text='Faltas', bg='red', fg='white', command=faltas)
#faltasButton.grid(row=1, column=8, padx=5, pady=5, sticky=N + S + E + W)

autoButton = Button(window, text='Post-it', bg='red', fg='white', command=start_monitoring)
autoButton.grid(row=2, column=3, padx=5, pady=5, sticky=N + S + E + W)

correccionButton = Button(window, text='Correccion', bg='red', fg='white', command=correccion)
correccionButton.grid(row=2, column=4, padx=5, pady=5, sticky=N + S + E + W)

alturaButton = Button(window, text='Varias Alturas', bg='red', fg='white', command=altura)
alturaButton.grid(row=2, column=5, padx=5, pady=5, sticky=N + S + E + W)

derechaButton = Button(window, text='Derecha', bg='red', fg='white', command=derecha)
derechaButton.grid(row=2, column=6, padx=5, pady=5, sticky=N + S + E + W)

start_key_listener()

window.mainloop()


