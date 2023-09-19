import serial.tools.list_ports

# Mostrar los puertos COM disponibles
print("Puertos COM disponibles:")
com_ports = serial.tools.list_ports.comports()
for port in com_ports:
    print(f"Nombre: {port.name}, Descripción: {port.description}")
