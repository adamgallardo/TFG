import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
from deep_translator import GoogleTranslator

cam_port = 0

cam = cv2.VideoCapture(cam_port)

sucess, frame = cam.read()

cv2.imwrite("Webcam.png", frame)

cv2.waitKey(0)

img = cv2.imread("Webcam.png")

reader = easyocr.Reader(['en'], gpu=False)

text_ = reader.readtext(img)

threshold = 0.25
for t_, t in enumerate(text_):
    print(t)

    bbox, text, score = t

    if score > threshold:
        cv2.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5)
        cv2.putText(img, text, bbox[0], cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()

translated = GoogleTranslator(source='auto', target='en').translate(text)

print (translated)