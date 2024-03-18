import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np

cam_port = 0

cam = cv2.VideoCapture(cam_port)

sucess, frame = cam.read()

#cv2.imshow("Webcam", frame)

cv2.imwrite("Webcam.png", frame)

cv2.waitKey(0)

# read image
#img = 'data/test5.png'

img = cv2.imread("Webcam.png")

# instance text detector
reader = easyocr.Reader(['en'], gpu=False)

# detect text on image
text_ = reader.readtext(img)

threshold = 0.25
# draw bbox and text
for t_, t in enumerate(text_):
    print(t)

    bbox, text, score = t

    if score > threshold:
        cv2.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5)
        cv2.putText(img, text, bbox[0], cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()

def dividir_por_operadores(cadena):
    partes = []
    operadores = ['+', '-', 'x', '/', '=']
    inicio = 0
    
    for i, caracter in enumerate(cadena):
        if caracter in operadores:
            partes.append(cadena[inicio:i])
            partes.append(caracter)
            inicio = i + 1
    
    partes.append(cadena[inicio:]) 
    return partes

resultado = dividir_por_operadores(text)
print(resultado)
final = 0
if (resultado[1]=="+"):
    final = int(resultado[0]) + int(resultado[2])
if (resultado[1]=="-"):
    final = int(resultado[0]) - int(resultado[2])
if (resultado[1]=="x"):
    final = int(resultado[0]) * int(resultado[2])
if (resultado[1]=="/"):
    final = int(resultado[0]) / int(resultado[2])

print(final)
if (final == int(resultado[4])):
    print("Correcto")
if (final != int(resultado[4])):
    print("Incorrecto")