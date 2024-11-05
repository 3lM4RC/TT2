import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread('TT2/Lagos1.jpg')
overlay = img.copy()
output = img.copy()
mask = np.zeros(img.shape[:2], dtype=np.uint8)

# Tamaños y colores
brush_size = 10
current_color = (0, 0, 255, 100)  # Color inicial rojo transparente
painting = False
erasing = False
last_point = None

# Colores para la paleta, ahora como diccionario
color_buttons = {
    "rojo": ((0, 0, 255, 100), (480, 100)),
    "verde": ((0, 255, 0, 100), (520, 100)),
    "azul": ((255, 0, 0, 100), (560, 100)),
    "amarillo": ((0, 255, 255, 100), (480, 140)),
    "cafe": ((42, 42, 165, 100), (520, 140)),
    "negro": ((0, 0, 0, 100), (560, 140)),
    "blanco": ((255, 255, 255, 100), (480, 180)),
    "naranja": ((0, 165, 255, 100), (520, 180))
}

# Función para manejar la pintura y el borrado
def paint(event, x, y, flags, param):
    global painting, erasing, overlay, output, mask, current_color, last_point

    if x < img.shape[1]:  # Pintura solo en el área de la imagen
        if event == cv2.EVENT_LBUTTONDOWN:
            painting = True
            last_point = (x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            painting = False
            last_point = None

        elif event == cv2.EVENT_MOUSEMOVE and painting:
            if last_point:
                if erasing:
                    cv2.line(overlay, last_point, (x, y), img[y, x].tolist(), brush_size * 2)
                    cv2.line(mask, last_point, (x, y), 0, brush_size * 2)
                else:
                    cv2.line(overlay, last_point, (x, y), current_color[:3], brush_size * 2)
                    cv2.line(mask, last_point, (x, y), 255, brush_size * 2)
                last_point = (x, y)
                output = cv2.addWeighted(overlay, 0.3, img, 0.7, 0)

    # Selección de colores y manejo de botones
    elif event == cv2.EVENT_LBUTTONDOWN:
        if 450 <= y <= 480:
            if 20 <= x <= 90:  # Botón de regreso
                overlay[:] = img
                mask[:] = 0
                output = img.copy()
            elif 100 <= x <= 170:  # Botón de borrar
                erasing = not erasing

        # Selección de color en la paleta
        for color_name, (color_value, (cx, cy)) in color_buttons.items():
            if cx <= x <= cx + 30 and cy <= y <= cy + 30:
                current_color = color_value
                erasing = False

# Crear la ventana y dibujar los elementos de la interfaz
cv2.namedWindow('Image Editor')
cv2.setMouseCallback('Image Editor', paint)

while True:
    # Dibujar botones y paleta de colores
    ui = output.copy()
    cv2.rectangle(ui, (20, 450), (90, 480), (200, 200, 200), -1)  # Botón "Regresar"
    cv2.putText(ui, "Regresar", (25, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    erase_color = (255, 255, 255) if not erasing else (100, 100, 100)
    cv2.rectangle(ui, (100, 450), (170, 480), erase_color, -1)  # Botón "Borrar"
    cv2.putText(ui, "Borrar", (105, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Dibujar la paleta de colores en un cuadrado 3x3
    for color_name, (color_value, (cx, cy)) in color_buttons.items():
        cv2.rectangle(ui, (cx, cy), (cx + 30, cy + 30), color_value[:3], -1)
        cv2.rectangle(ui, (cx, cy), (cx + 30, cy + 30), (0, 0, 0), 1)

    # Mostrar la ventana de edición
    cv2.imshow('Image Editor', ui)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):  # Guardar la imagen binarizada al presionar 's'
        binary_img = cv2.bitwise_and(np.full_like(img, 255), np.full_like(img, 255), mask=mask)
        cv2.imwrite("image_masked.png", binary_img)
        print("Imagen binarizada guardada como 'image_masked.png'.")
    elif key == 27:  # Salir con 'Esc'
        break

cv2.destroyAllWindows()
