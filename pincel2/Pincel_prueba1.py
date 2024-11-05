import cv2
import numpy as np

# Cargar la imagen desde la ubicación especificada
file_path = "TT2/Lagos1.jpg"
img = cv2.imread(file_path)
if img is None:
    print("Error: No se pudo cargar la imagen. Asegúrate de que el archivo exista en la ruta especificada.")
    exit()

# Crear una copia de la imagen para pintar y una máscara para binarización
overlay = img.copy()  # Capa para pintar con transparencia
output = img.copy()  # Imagen final con la pintura
mask = np.zeros(img.shape[:2], dtype=np.uint8)  # Máscara para binarización
brush_size = 10  # Tamaño de la brocha
painting = False
erasing = False

# Función para manejar el evento del mouse y dibujar
def paint(event, x, y, flags, param):
    global painting, erasing, overlay, output, mask

    if event == cv2.EVENT_LBUTTONDOWN:
        painting = True  # Iniciar pintura al presionar el botón izquierdo del mouse
    elif event == cv2.EVENT_RBUTTONDOWN:
        erasing = True  # Iniciar borrado al presionar el botón derecho del mouse
    elif event == cv2.EVENT_LBUTTONUP:
        painting = False  # Dejar de pintar al soltar el botón izquierdo
    elif event == cv2.EVENT_RBUTTONUP:
        erasing = False  # Dejar de borrar al soltar el botón derecho
    elif event == cv2.EVENT_MOUSEMOVE:
        if painting:
            # Pintar en la capa overlay con transparencia
            cv2.circle(overlay, (x, y), brush_size, (0, 0, 255), -1)
            cv2.circle(mask, (x, y), brush_size, 255, -1)  # Actualizar máscara

            # Combinar la imagen original con la capa de pintura roja transparente
            output = cv2.addWeighted(overlay, 0.3, img, 0.7, 0)
        
        elif erasing:
            # Borrar la pintura de la capa overlay restaurando la parte de la imagen original
            cv2.circle(overlay, (x, y), brush_size, img[y, x].tolist(), -1)
            cv2.circle(mask, (x, y), brush_size, 0, -1)  # Actualizar máscara

            # Combinar la imagen original con la capa overlay para reflejar el borrado
            output = cv2.addWeighted(overlay, 0.3, img, 0.7, 0)

# Configurar el callback del mouse en la imagen para pintar
cv2.namedWindow("Paint Tool")
cv2.setMouseCallback("Paint Tool", paint)

while True:
    # Mostrar la imagen en la ventana
    cv2.imshow("Paint Tool", output)
    
    # Presiona "q" para salir o "s" para guardar
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        # Crear imagen binarizada a partir de la máscara y guardar
        binary_img = np.zeros_like(img)
        binary_img[mask != 0] = [255, 255, 255]  # Píxeles blancos en el área pintada
        binary_img[mask == 0] = [0, 0, 0]        # Fondo negro
        
        cv2.imwrite("TT2/Imagen_binarizada.png", binary_img)
        print("Imagen binarizada guardada como 'binarized_painted_image.png'.")

# Cerrar las ventanas de OpenCV
cv2.destroyAllWindows()
