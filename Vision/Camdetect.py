import cv2

# Obtiene una lista de todos los dispositivos de captura disponibles
def get_connected_cameras():
    connected_cameras = []
    for i in range(10):  # Verificar hasta 10 posibles cámaras (puedes ajustar este valor según tus necesidades)
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            connected_cameras.append(f"Cámara {i}")
            cap.release()
    return connected_cameras

# Obtén la lista de cámaras conectadas
cameras = get_connected_cameras()

# Imprime la lista de cámaras
if cameras:
    print("Cámaras conectadas:")
    for camera in cameras:
        print(camera)
else:
    print("No se encontraron cámaras conectadas.")