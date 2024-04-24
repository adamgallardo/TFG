from tkinter import *
from djitellopy import Tello
import cv2 as cv
from PIL import Image
from PIL import ImageTk
import easyocr
import matplotlib.pyplot as plt
import numpy as np
from deep_translator import GoogleTranslator
import time
import threading

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
abajoButton.grid(row=1, column=7, padx=5, pady=5, sticky=N + S + E + W)

window.mainloop()