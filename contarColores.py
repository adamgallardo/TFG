import cv2
import numpy as np

# Cargar la imagen
image = cv2.imread('tu_imagen.jpg')

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

# Definir el rango de color rojo en HSV
# Nota: el color rojo puede estar en dos rangos diferentes debido a la forma en que se representa el HSV.
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([179, 255, 255])

# Crear dos máscaras para los diferentes rangos de rojo
mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)

# Combinar las dos máscaras para obtener la detección completa del color rojo
mask_red = cv2.bitwise_or(mask_red1, mask_red2)

# Encontrar los contornos en la máscara roja
contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filtrar y contar los contornos rojos con un área significativa
red_objects = [cnt for cnt in contours_red if cv2.contourArea(cnt) > min_area]

# Dibujar los contornos detectados en la imagen original
cv2.drawContours(image, yellow_objects, -1, (0, 255, 0), 3)  # Verde para amarillo
cv2.drawContours(image, red_objects, -1, (255, 0, 0), 3)     # Azul para rojo (para distinguir en la visualización)

# Mostrar el número de objetos detectados
print(f"Número de objetos amarillos detectados: {len(yellow_objects)}")
print(f"Número de objetos rojos detectados: {len(red_objects)}")

# Comparar el número de objetos
if len(yellow_objects) > len(red_objects):
    print("Hay más objetos amarillos que rojos.")
elif len(yellow_objects) < len(red_objects):
    print("Hay más objetos rojos que amarillos.")
else:
    print("El número de objetos amarillos y rojos es igual.")

# Mostrar la imagen con los contornos dibujados
cv2.imshow('Objetos Amarillos y Rojos Detectados', image)
cv2.waitKey(0)
cv2.destroyAllWindows()