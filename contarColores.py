import cv2
import numpy as np

# Cargar la imagen
image = cv2.imread('bolasDiferentesMedidas.png')

# Convertir la imagen a formato HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Definir el rango de color amarillo en HSV
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# Crear una máscara con el rango de color amarillo
mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

# Encontrar los contornos en la máscara amarilla
contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filtrar y contar los contornos amarillos con un área significativa
min_area = 500  # Ajusta este valor según el tamaño de los objetos
yellow_objects = [cnt for cnt in contours_yellow if cv2.contourArea(cnt) > min_area]

# Definir el rango de color naranja en HSV
lower_orange = np.array([10, 100, 100])
upper_orange = np.array([20, 255, 255])

# Crear una máscara con el rango de color naranja
mask_orange = cv2.inRange(hsv_image, lower_orange, upper_orange)

# Encontrar los contornos en la máscara naranja
contours_orange, _ = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filtrar y contar los contornos naranjas con un área significativa
orange_objects = [cnt for cnt in contours_orange if cv2.contourArea(cnt) > min_area]

# Dibujar los contornos detectados en la imagen original
cv2.drawContours(image, yellow_objects, -1, (255, 255, 255), 3)  # Amarillo para amarillo
cv2.drawContours(image, orange_objects, -1, (0, 165, 255), 3)  # Naranja para naranja

# Mostrar el número de objetos detectados
print(f"Número de objetos amarillos detectados: {len(yellow_objects)}")
print(f"Número de objetos naranjas detectados: {len(orange_objects)}")

# Comparar el número de objetos
if len(yellow_objects) > len(orange_objects):
    print("Hay más objetos amarillos que naranjas.")
elif len(yellow_objects) < len(orange_objects):
    print("Hay más objetos naranjas que amarillos.")
else:
    print("El número de objetos amarillos y naranjas es igual.")

# Mostrar la imagen con los contornos dibujados
cv2.imshow('Objetos Amarillos y Naranjas Detectados', image)
cv2.waitKey(0)
cv2.destroyAllWindows()