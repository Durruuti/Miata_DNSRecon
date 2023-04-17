import pyfiglet
import socket
import sys
import dns.resolver
from datetime import datetime


# Creación de la variable splash
splash = pyfiglet.figlet_format("MIATA DNSRECON")
print(splash)


# Obtener la IP del dominio objetivo
tdomain = input("Introduce el dominio: ")

# Mostrar un banner sobre la búsqueda del dominio
print("_" * 60)
print("Por favor espera, buscando la IP del dominio introducido...")
print("_" * 60)

# Comprobar la fecha y el tiempo del escaneo
t1 = datetime.now()
ip_address = socket.gethostbyname(tdomain)
print("La dirección IP del host es:", ip_address)

# Comprobar el tiempo de nuevo
t2 = datetime.now()

# Calcular cuánto ha tardado el escaneo (t2 - t1)
total = t2 - t1
print("Escaneo completado en:", total)


# Creación del escáner de puertos
tserver = input("Introduce la IP de un host remoto para escanear: ")

# Comprobar el tiempo tardado
t3 = datetime.now()
print("_" * 60)
print("Por favor espera, se está escaneando la IP por puertos abiertos", ip_address)
print("_" * 60)

# Escaneo de la IP por puertos abiertos
try:
    for port in range(1, 65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Establecer el timeout para que no esté de por vida
        s.settimeout(0.5)
        # Respuesta con la lista de puertos
        result = s.connect_ex((ip_address, port))
        if result == 0:
            print("Port {}: Open".format(port))
        s.close()

# Crear mensaje de error en caso de Ctrl+C
except KeyboardInterrupt:
    print("\nSaliendo...")

# Crear mensaje de error si no se puede conectar con el servidor
except socket.error:
    print("No se pudo conectar con el server")
    sys.exit()

# Comprobar el tiempo de nuevo
t4 = datetime.now()

# Calcular cuánto ha tardado el escaneo en realizarse
total = t4 - t3
print("El escaneo se ha realizado en:", total)


# Enumeración DNS
print("#" * 60)
print("AHORA ENUMEREMOS")
print("#" * 60)

record_types = ["A", "AAAA", "NS", "CNAME", "MX"]

try:
    domain = tdomain
except IndexError:
    print("Error de sintaxis! ")

for record_type in record_types:
    try:
        answer = dns.resolver.resolve(domain, record_type)
        print(f"{record_type} Records")
        print("_" * 60)
        for server in answer:
            print(server.to_text() + "\n")
    except dns.resolver.NoAnswer:
        pass
    except dns.resolver.NXDOMAIN:
        print(f"{domain} no existe")
    except KeyboardInterrupt:
        print("Saliendo...")
        quit()
