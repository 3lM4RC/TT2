import cv2
import numpy as np

# Cargar la imagen desde el archivo
file_path = "TT2/Lagos1.jpg"  # Cambia a la ruta de tu imagen
img = cv2.imread(file_path)
if img is None:
    print("Error: No se pudo cargar la imagen. Asegúrate de que el archivo exista.")
    exit()

# Ventanas
cv2.imshow("Original Image", img)

# Función para seleccionar el píxel con el mouse
def select_pixel(event, x, y, flags, param):
    global img, selected_color, highlighted_img, binary_img
    if event == cv2.EVENT_LBUTTONDOWN:
        # Obtener el color del píxel seleccionado
        selected_color = img[y, x]
        highlight_pixels(selected_color)

# Función para resaltar píxeles del mismo color en rojo transparente y binarizar
def highlight_pixels(color):
    global img, highlighted_img, binary_img

    # Crear una máscara para los píxeles con el mismo color
    mask = cv2.inRange(img, color, color)
    
    # Crear una copia en color de la imagen para superponer
    highlighted_img = img.copy()
    
    # Crear una superposición roja transparente solo en los píxeles coincidentes
    overlay = highlighted_img.copy()
    overlay[mask != 0] = [0, 0, 255]  # Rojo en los píxeles seleccionados
    
    # Combinar la imagen original y la superposición solo en los píxeles coincidentes
    highlighted_img = np.where(mask[:, :, None] != 0, cv2.addWeighted(img, 0.7, overlay, 0.3, 0), img)

    # Mostrar la imagen resaltada
    cv2.imshow("Highlighted Image", highlighted_img)

    # Crear imagen binarizada para mostrar y guardar
    binary_img = np.zeros_like(img)
    binary_img[mask != 0] = [255, 255, 255]  # Píxeles blancos en la binarizada
    binary_img[mask == 0] = [0, 0, 0]        # Fondo negro
    
    # Mostrar imagen binarizada
    cv2.imshow("Binary Image", binary_img)

    # Guardar imagen binarizada
    cv2.imwrite("binarized_image.png", binary_img)

# Configurar el callback del mouse en la imagen original
cv2.setMouseCallback("Original Image", select_pixel)

# Esperar hasta que el usuario cierre las ventanas
cv2.waitKey(0)
cv2.destroyAllWindows()
