import cv2
import numpy as np

# Cargar la imagen desde la ubicación especificada
file_path = "pincel2/Lagos1.jpg"
img = cv2.imread(file_path)
if img is None:
    print("Error: No se pudo cargar la imagen. Asegúrate de que el archivo exista en la ruta especificada.")
    exit()

# Configurar dimensiones de la ventana y el área de botones
button_panel_width = 150  # Ancho del área de botones
button_panel = np.ones((img.shape[0], button_panel_width, 3), dtype=np.uint8) * 200  # Fondo gris claro

# Variables iniciales
overlay = img.copy()
output = img.copy()
mask = np.zeros(img.shape[:2], dtype=np.uint8)  # Máscara para binarización
brush_size = 10  # Tamaño de la brocha
painting = False
erasing = False
selecting_color = False
current_color = (0, 0, 255, 127)  # Color inicial (Rojo transparente)

# Paleta de colores y botones
colors = {
    'Rojo': (0, 0, 255),
    'Verde': (0, 255, 0),
    'Azul': (255, 0, 0),
    'Amarillo': (0, 255, 255),
    'Cafe': (42, 42, 165),
    'Negro': (0, 0, 0),
    'Blanco': (255, 255, 255),
    'Naranja': (0, 128, 255),
}

button_reset = (10, 20, 140, 60)  # Coordenadas del botón de reinicio
button_select_color = (10, 80, 140, 120)
button_close = (10, 140, 140, 180)
button_erase = (10, 200, 140, 240)  # Botón de borrado
color_buttons = {color: (10, 260 + i * 30, 40, 290 + i * 30) for i, color in enumerate(colors)}  # Coordenadas de la paleta

# Variable global para almacenar la última posición del mouse
last_point = None

# Actualización de la función 'paint' con interpolación de líneas
def paint(event, x, y, flags, param):
    global painting, erasing, selecting_color, overlay, output, mask, current_color, last_point

    if x < img.shape[1]:  # Solo activar si se hace clic en la imagen
        if event == cv2.EVENT_LBUTTONDOWN:
            painting = True
            last_point = (x, y)  # Almacenar la posición inicial del trazo

        elif event == cv2.EVENT_LBUTTONUP:
            painting = False
            last_point = None  # Restablecer la posición al soltar el botón

        elif event == cv2.EVENT_MOUSEMOVE and painting:
            # Dibuja una línea entre el último punto y el actual
            if erasing:
                # Borrar la pintura y actualizar la máscara
                cv2.line(overlay, last_point, (x, y), img[y, x].tolist(), brush_size * 2)
                cv2.line(mask, last_point, (x, y), 0, brush_size * 2)
            else:
                # Pintar en la capa overlay con transparencia y actualizar la máscara
                cv2.line(overlay, last_point, (x, y), current_color[:3], brush_size * 2)
                cv2.line(mask, last_point, (x, y), 255, brush_size * 2)

            last_point = (x, y)  # Actualizar la última posición del mouse
            output = cv2.addWeighted(overlay, 0.3, img, 0.7, 0)

    elif event == cv2.EVENT_LBUTTONDOWN:
        # Comprobar si se ha hecho clic en algún botón
        if button_reset[0] <= x - img.shape[1] <= button_reset[2] and button_reset[1] <= y <= button_reset[3]:
            # Reiniciar la máscara y la capa de pintura
            overlay = img.copy()
            output = img.copy()
            mask.fill(0)
            print("Malla roja reiniciada.")

        elif button_select_color[0] <= x - img.shape[1] <= button_select_color[2] and button_select_color[1] <= y <= button_select_color[3]:
            # Activar el modo de selección de color
            selecting_color = True
            print("Selecciona un color de la paleta para pintar.")

        elif button_close[0] <= x - img.shape[1] <= button_close[2] and button_close[1] <= y <= button_close[3]:
            # Cerrar la aplicación
            print("Cerrando aplicación.")
            cv2.destroyAllWindows()
            exit()

        elif button_erase[0] <= x - img.shape[1] <= button_erase[2] and button_erase[1] <= y <= button_erase[3]:
            # Cambiar estado de borrado
            erasing = not erasing
            print("Modo borrar activado." if erasing else "Modo borrar desactivado.")

        # Comprobar si se ha seleccionado algún color
        for color_name, (cx1, cy1, cx2, cy2) in color_buttons.items():
            if cx1 <= x - img.shape[1] <= cx2 and cy1 <= y <= cy2:
                current_color = (*colors[color_name], 127)  # Cambiar el color actual con transparencia
                print(f"Color de pintura seleccionado: {color_name}")
                erasing = False  # Desactivar el modo borrador si se selecciona un color

# Dibujar los botones y la paleta en el área de botones
def draw_buttons(panel):
    # Botón de reinicio
    cv2.rectangle(panel, (button_reset[0], button_reset[1]), (button_reset[2], button_reset[3]), (180, 180, 180), -1)
    cv2.putText(panel, "Reiniciar", (button_reset[0] + 10, button_reset[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Botón de seleccionar color
    cv2.rectangle(panel, (button_select_color[0], button_select_color[1]), (button_select_color[2], button_select_color[3]), (180, 180, 180), -1)
    cv2.putText(panel, "Sel. Color", (button_select_color[0] + 10, button_select_color[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Botón de cerrar
    cv2.rectangle(panel, (button_close[0], button_close[1]), (button_close[2], button_close[3]), (180, 180, 180), -1)
    cv2.putText(panel, "Cerrar", (button_close[0] + 10, button_close[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Botón de borrar (cambia de color si está activado)
    erase_button_color = (255, 255, 255) if erasing else (180, 180, 180)
    cv2.rectangle(panel, (button_erase[0], button_erase[1]), (button_erase[2], button_erase[3]), erase_button_color, -1)
    cv2.putText(panel, "Borrar", (button_erase[0] + 30, button_erase[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Paleta de colores
    for i, (color_name, color_rgb) in enumerate(colors.items()):
        color_coords = color_buttons[color_name]
        cv2.rectangle(panel, (color_coords[0], color_coords[1]), (color_coords[2], color_coords[3]), color_rgb, -1)
        #cv2.putText(panel, color_name, (color_coords[0] + 10, color_coords[1] + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255) if np.mean(color_rgb) < 128 else (0, 0, 0), 1)

# Configurar el callback del mouse en la imagen
cv2.namedWindow("Paint Tool")
cv2.setMouseCallback("Paint Tool", paint)

while True:
    # Crear una imagen combinada de la imagen y el panel de botones
    combined_output = np.hstack((output, button_panel))
    draw_buttons(button_panel)

    # Mostrar la imagen combinada
    cv2.imshow("Paint Tool", combined_output)
    
    # Presionar "s" para guardar la imagen binarizada
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        # Crear la imagen binarizada a partir de la máscara
        binary_img = np.zeros_like(img)
        binary_img[mask != 0] = (255, 255, 255)
        cv2.imwrite("pincel2/image_masked.png", binary_img)
        print("Imagen binarizada guardada como 'image_masked.png'.")
    elif key == 27:  # Esc para salir
        break

cv2.destroyAllWindows()
