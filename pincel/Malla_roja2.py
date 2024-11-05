import cv2
import numpy as np

# Cargar la imagen desde el archivo
file_path = "TT2/Lagos1.jpg"
img = cv2.imread(file_path)
if img is None:
    print("Error: No se pudo cargar la imagen. Asegúrate de que el archivo exista.")
    exit()

# Variables para el punto inicial y final de la línea
start_point = None
end_point = None
selected_color = None

# Ventanas
cv2.imshow("Original Image", img)

# Función para manejar el evento del mouse y dibujar una línea
def select_line(event, x, y, flags, param):
    global start_point, end_point, selected_color
    if event == cv2.EVENT_LBUTTONDOWN:
        # Guardar el punto inicial al presionar el mouse
        start_point = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        # Guardar el punto final al soltar el mouse y obtener el color inicial
        end_point = (x, y)
        selected_color = img[start_point[1], start_point[0]]
        highlight_pixels(selected_color, start_point, end_point)

# Función para resaltar píxeles del mismo color en rojo transparente a lo largo de la línea
def highlight_pixels(color, start, end):
    global img, highlighted_img, binary_img

    # Crear una copia de la imagen para superponer
    highlighted_img = img.copy()

    # Crear una máscara en blanco para los píxeles en la línea
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.line(mask, start, end, 255, 1)  # Dibujar línea de 1 píxel de ancho en la máscara

    # Aplicar la máscara para resaltar solo los píxeles que coinciden con el color seleccionado
    color_mask = cv2.inRange(img, color, color)
    final_mask = cv2.bitwise_and(mask, color_mask)  # Combina la línea y la coincidencia de color
    
    # Crear una superposición roja transparente solo en los píxeles coincidentes en la línea
    overlay = highlighted_img.copy()
    overlay[final_mask != 0] = [0, 0, 255]  # Rojo en los píxeles seleccionados
    
    # Combinar la imagen original y la superposición solo en los píxeles coincidentes
    highlighted_img = np.where(final_mask[:, :, None] != 0, cv2.addWeighted(img, 0.7, overlay, 0.3, 0), img)

    # Mostrar la imagen resaltada
    cv2.imshow("Highlighted Image", highlighted_img)

    # Crear imagen binarizada para mostrar y guardar
    binary_img = np.zeros_like(img)
    binary_img[final_mask != 0] = [255, 255, 255]  # Píxeles blancos en la binarizada
    binary_img[final_mask == 0] = [0, 0, 0]        # Fondo negro
    
    # Mostrar imagen binarizada
    cv2.imshow("Binary Image", binary_img)

    # Guardar imagen binarizada
    cv2.imwrite("TT2/binarized_image.png", binary_img)

# Configurar el callback del mouse en la imagen original
cv2.setMouseCallback("Original Image", select_line)

# Esperar hasta que el usuario cierre las ventanas
cv2.waitKey(0)
cv2.destroyAllWindows()
