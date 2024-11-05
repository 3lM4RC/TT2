import cv2
import numpy as np

# Cargar la imagen desde la ubicación especificada
file_path = "TT2/Lagos1.jpg"
img = cv2.imread(file_path)
if img is None:
    print("Error: No se pudo cargar la imagen. Asegúrate de que el archivo exista en la ruta especificada.")
    exit()

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
button_reset = (20, 20, 120, 60)  # [x1, y1, x2, y2]
button_select_color = (140, 20, 280, 60)
button_close = (300, 20, 380, 60)

# Función para manejar los eventos de mouse
def paint(event, x, y, flags, param):
    global painting, erasing, selecting_color, overlay, output, mask, color_to_paint

    if event == cv2.EVENT_LBUTTONDOWN:
        if button_reset[0] <= x <= button_reset[2] and button_reset[1] <= y <= button_reset[3]:
            # Reiniciar la máscara y la capa de pintura
            overlay = img.copy()
            output = img.copy()
            mask.fill(0)
            print("Malla roja reiniciada.")
        
        elif button_select_color[0] <= x <= button_select_color[2] and button_select_color[1] <= y <= button_select_color[3]:
            # Activar el modo de selección de color
            selecting_color = True
            print("Selecciona un píxel en la imagen.")
        
        elif button_close[0] <= x <= button_close[2] and button_close[1] <= y <= button_close[3]:
            # Cerrar la aplicación
            print("Cerrando aplicación.")
            cv2.destroyAllWindows()
            exit()

        elif selecting_color:
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

# Dibujar los botones en la imagen
def draw_buttons(output_img):
    cv2.rectangle(output_img, (button_reset[0], button_reset[1]), (button_reset[2], button_reset[3]), (200, 200, 200), -1)
    cv2.putText(output_img, "Reiniciar", (button_reset[0] + 10, button_reset[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    cv2.rectangle(output_img, (button_select_color[0], button_select_color[1]), (button_select_color[2], button_select_color[3]), (200, 200, 200), -1)
    cv2.putText(output_img, "Seleccionar Color", (button_select_color[0] + 10, button_select_color[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    cv2.rectangle(output_img, (button_close[0], button_close[1]), (button_close[2], button_close[3]), (200, 200, 200), -1)
    cv2.putText(output_img, "Cerrar", (button_close[0] + 10, button_close[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

# Configurar el callback del mouse en la imagen
cv2.namedWindow("Paint Tool")
cv2.setMouseCallback("Paint Tool", paint)

while True:
    # Dibujar botones en la imagen de salida y mostrar la imagen
    output_with_buttons = output.copy()
    draw_buttons(output_with_buttons)
    cv2.imshow("Paint Tool", output_with_buttons)
    
    # Presionar "s" para guardar la imagen binarizada
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        # Crear la imagen binarizada a partir de la máscara
        binary_img = np.zeros_like(img)
        binary_img[mask != 0] = [255, 255, 255]
        binary_img[mask == 0] = [0, 0, 0]
        
        cv2.imwrite("binarized_painted_image.png", binary_img)
        print("Imagen binarizada guardada como 'binarized_painted_image.png'.")

# Cerrar las ventanas de OpenCV
cv2.destroyAllWindows()
