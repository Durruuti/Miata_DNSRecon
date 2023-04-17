import pyfiglet
import socket
import sys
import dns.resolver
from datetime import datetime

#Creacion variable splash
splash = pyfiglet.figlet_format("MIATA DNSRECON")
print(splash)

#Conseguir la IP de nuestro dominio objetivo
tdomain = input("Introduce el dominio: ")

#Printear un banner sobre la busqueda del dominio

print("_"* 60)
print("Por favor espera, buscando la IP del dominio introducido")
print("_"* 60)

#Comprobar la fecha y el tiempo del scan
t1 = datetime.now()
print("La dirección IP del host es: ", socket.gethostbyname(tdomain))

#Comprobar el tiempo de nuevo
t2 = datetime.now()

#Calcular cuanto ha tardado el scan [t2 -t1]
total = t2 -t1

print("Escaneo completado en:", total)

#Creacion del escáner de puertos

tserver = input("Introduce la IP de un host remoto para escanear: ")
targetIP = socket.gethostbyname(tdomain)

#Comprobar el tiempo tardado 
t3 = datetime.now()
print("_" * 60)
print("Por favor espera, se está escaneando la IP por puertos abiertos ", targetIP)
print("_" * 60)

# Scaneo de la ip por puertos abiertos
try:
    for port in range (1, 65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Establecer el timeout para que no este de por vida
        socket.setdefaulttimeout(0.5)
# Respuesta con la lista de puertos
        result =s.connect_ex((targetIP, port))
        if result == 0:
            print("Port {}[+]: Open",format(port))
        s.close()

# Crear mensaje de error en caso de ctrl+c
except KeyboardInterrupt:
    print("Saliendo...")

#Crear mensaje de error si no responde el host
except socket.error:
    print("No se pudo conectar con el server")
    sys.exit()

#Comprobar el tiempo de nuevo
t4 = datetime.now()

#Calcular cuando ha tardado el scan en realizarse
total = t4 - t3
print("El escaneo se ha realizado en: ", total)

#Enumeración DNS


#Printear el banner
print("#" * 60)
print("AHORA ENUMEREMOS")
print("#" * 60)

record_types = ["A", "AAAA", "NS", "CNAME", "MX"]
try:
    domain = tdomain
except IndexError:
    print("Error de sintaxis! ")

for records in record_types:
    try:
        answer = dns.resolver.resolve(domain, records)
        print(f"{records} Records")
        print("_" * 60)
        for server in answer:
            print(server.to_text() + "\n")
    except dns.resolver.NoAnswer:
        pass
    except dns.resolver.NXDOMAIN:
        print(f"{domain} no existe")
    except KeyboardInterrupt:
        print("Saliendo... , Nos vemos !")
        quit()