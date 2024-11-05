import cv2
import numpy as np

# Cargar la imagen desde la ubicación especificada
file_path = "TT2/Lagos1.jpg"
img = cv2.imread(file_path)
if img is None:
    print("Error: No se pudo cargar la imagen. Asegúrate de que el archivo exista en la ruta especificada.")
    exit()

# Configurar dimensiones de la ventana y el área de botones
button_panel_width = 150  # Ancho del área de botones
button_panel = np.ones((img.shape[0], button_panel_width, 3), dtype=np.uint8) * 200  # Fondo gris claro

# Variables iniciales
overlay = img.copy()  # Capa para pintar
output = img.copy()  # Imagen de salida
mask = np.zeros(img.shape[:2], dtype=np.uint8)  # Máscara para binarización
brush_size = 10  # Tamaño de la brocha
painting = False
erasing = False
selecting_color = False
color_to_paint = None

# Posiciones de los botones
button_reset = (10, 20, 140, 60)  # Coordenadas dentro del área de botones
button_select_color = (10, 80, 140, 120)
button_close = (10, 140, 140, 180)

# Función para manejar los eventos de mouse
def paint(event, x, y, flags, param):
    global painting, erasing, selecting_color, overlay, output, mask, color_to_paint

    if x < img.shape[1]:  # Solo activar si se hace clic en la imagen, no en el área de botones
        if event == cv2.EVENT_LBUTTONDOWN:
            if selecting_color:
                # Guardar el color del píxel seleccionado
                color_to_paint = img[y, x]
                selecting_color = False
                print(f"Color seleccionado: {color_to_paint}. Pintando píxeles del mismo color.")
                
                # Crear la malla roja de los píxeles que coinciden con el color seleccionado
                overlay = img.copy()
                mask = np.zeros(img.shape[:2], dtype=np.uint8)
                color_distance = 30  # Tolerancia en el color
                lower_bound = np.maximum(color_to_paint - color_distance, 0)
                upper_bound = np.minimum(color_to_paint + color_distance, 255)
                mask = cv2.inRange(img, lower_bound, upper_bound)
                overlay[mask != 0] = [0, 0, 255]  # Color rojo
                output = cv2.addWeighted(overlay, 0.3, img, 0.7, 0)
            else:
                painting = True  # Iniciar pintura con brocha

        elif event == cv2.EVENT_RBUTTONDOWN:
            erasing = True  # Iniciar borrado

        elif event == cv2.EVENT_LBUTTONUP:
            painting = False

        elif event == cv2.EVENT_RBUTTONUP:
            erasing = False

        elif event == cv2.EVENT_MOUSEMOVE:
            if painting:
                # Pintar en la capa overlay con transparencia y actualizar la máscara
                cv2.circle(overlay, (x, y), brush_size, (0, 0, 255), -1)
                cv2.circle(mask, (x, y), brush_size, 255, -1)
                output = cv2.addWeighted(overlay, 0.3, img, 0.7, 0)

            elif erasing:
                # Borrar la pintura y actualizar la máscara
                cv2.circle(overlay, (x, y), brush_size, img[y, x].tolist(), -1)
                cv2.circle(mask, (x, y), brush_size, 0, -1)
                output = cv2.addWeighted(overlay, 0.3, img, 0.7, 0)

    elif event == cv2.EVENT_LBUTTONDOWN:
        # Comprobar si el clic es en algún botón
        if button_reset[0] <= x - img.shape[1] <= button_reset[2] and button_reset[1] <= y <= button_reset[3]:
            # Reiniciar la máscara y la capa de pintura
            overlay = img.copy()
            output = img.copy()
            mask.fill(0)
            print("Malla roja reiniciada.")
        
        elif button_select_color[0] <= x - img.shape[1] <= button_select_color[2] and button_select_color[1] <= y <= button_select_color[3]:
            # Activar el modo de selección de color
            selecting_color = True
            print("Selecciona un píxel en la imagen.")
        
        elif button_close[0] <= x - img.shape[1] <= button_close[2] and button_close[1] <= y <= button_close[3]:
            # Cerrar la aplicación
            print("Cerrando aplicación.")
            cv2.destroyAllWindows()
            exit()

# Dibujar los botones en el área de botones
def draw_buttons(panel):
    cv2.rectangle(panel, (button_reset[0], button_reset[1]), (button_reset[2], button_reset[3]), (180, 180, 180), -1)
    cv2.putText(panel, "Reiniciar", (button_reset[0] + 10, button_reset[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    cv2.rectangle(panel, (button_select_color[0], button_select_color[1]), (button_select_color[2], button_select_color[3]), (180, 180, 180), -1)
    cv2.putText(panel, "Sel. Color", (button_select_color[0] + 10, button_select_color[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    cv2.rectangle(panel, (button_close[0], button_close[1]), (button_close[2], button_close[3]), (180, 180, 180), -1)
    cv2.putText(panel, "Cerrar", (button_close[0] + 10, button_close[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

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
        binary_img[mask != 0] = [255, 255, 255]
        binary_img[mask == 0] = [0, 0, 0]
        
        cv2.imwrite("binarized_painted_image.png", binary_img)
        print("Imagen binarizada guardada como 'binarized_painted_image.png'.")
        
    elif key == ord('q'):
        break

# Cerrar las ventanas de OpenCV
cv2.destroyAllWindows()
