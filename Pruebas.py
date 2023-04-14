import json
import os
from pprint import pprint
import nmap
from prompt_toolkit import print_formatted_text as print, PromptSession
from scapy.all import *
from texttable import Texttable

nm = nmap.PortScanner()


def network_scan(direction):
    output = nm.scan(hosts=direction, arguments='-sP', sudo=True)
    ips = output.get('scan').keys()

    hosts = []
    for ip in ips:
        hosts.append(ip)

    return hosts, output


def print_hosts(direction):
    [hosts, output] = network_scan(direction)
    for host in hosts:
        print(host)


def print_hosts_export(direction, path, file_name):
    if os.path.exists(path):
        [hosts, output] = network_scan(direction)
        file = open(path + file_name, "w")

        for host in hosts:
            file.write(host + os.linesep)
        file.close()
    else:
        print("The directory", path, "does not exist")


def vm_scan(direction):
    [host, output] = network_scan(direction)

    info_of_a_host = output.get('scan').get(host[0])
    string = str(info_of_a_host)

    if 'virtualbox' in string.lower():
        print('The host', host[0], 'is running in a virtual machine')
    else:
        print('The host', host[0], 'is not running in a virtual machine')


def vm_scan_export(direction, path, file_name):
    if os.path.exists(path):
        [host, output] = network_scan(direction)
        file = open(path + file_name, "w")

        info_of_a_host = output.get('scan').get(host[0])
        string = str(info_of_a_host)

        if 'virtualbox' in string.lower():
            file.write('The host ' + host[0] + ' is running in a virtual machine' + os.linesep)
        else:
            file.write('The host ' + host[0] + ' is not running in a virtual machine' + os.linesep)
        file.close()
    else:
        print("The directory", path, "does not exist")


def node_scan(direction):
    [host, none] = network_scan(direction)

    output = nm.scan(hosts=host[0], arguments='-p 7400 -sU --open -T3 --max-rate=10000', sudo=True)
    string = str(output.get('scan'))

    if '7400' in string:
        print('The host', host[0], 'is running a ROS2 node')
    else:
        print('The host', host[0], 'is not running a ROS2 node')


def node_scan_export(direction, path, file_name):
    if os.path.exists(path):
        [host, none] = network_scan(direction)
        file = open(path + file_name, "w")

        output = nm.scan(hosts=host[0], arguments='-p 7400 -sU --open -T3 --max-rate=10000', sudo=True)
        string = str(output.get('scan'))

        if '7400' in string:
            file.write('The host ' + host[0] + ' is running a ROS2 node' + os.linesep)
        else:
            file.write('The host ' + host[0] + ' is not running a ROS2 node' + os.linesep)
        file.close()
    else:
        print("The directory", path, "does not exist")


##########################################################################

def DDS_vendor(ports, fila=None):
    list_of_DDS_vendors = [
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

    os.system("/bin/bash -c \"tcpdump -r data.pcap -w filter.pcap udp portrange " + ports[0] + "-" + ports[1] + "\"")
    os.system("/bin/bash -c \"tshark -r filter.pcap -T json > data.json\"")

    with open("data.json", 'r') as json_file:
        vendorID = re.findall("vendorId\": \"(0x[\da-f]{4})", json_file.read(), re.I | re.DOTALL)

    os.system("/bin/bash -c \"rm data.json\"")

    for id in list_of_DDS_vendors:
        if vendorID[0] == id[0]:
            if fila is None:
                return id[1]
            else:
                fila.append(id[1])


def checkSeg(ports, fila=None):
    os.system("/bin/bash -c \"tcpdump -r data.pcap -w filter.pcap udp portrange " + ports[0] + "-" + ports[1] + "\"")
    os.system("/bin/bash -c \"tshark -r filter.pcap -T json > data.json\"")

    with open("data.json", 'r') as json_file:
        check = re.search("Secure Data Tag", json_file.read(), re.I | re.DOTALL)

    os.system("/bin/bash -c \"rm data.json\"")

    if fila is None:
        if check is not None:
            return "Security activated"
        else:
            return "Security not activated"
    else:
        if check is not None:
            fila.append("Security activated")
        else:
            fila.append("Security not activated")


def topicName(ports, fila=None):
    os.system("/bin/bash -c \"tcpdump -r data.pcap -w filter.pcap udp portrange " + ports[0] + "-" + ports[1] + "\"")
    os.system("/bin/bash -c \"tshark -r filter.pcap -T json > data.json\"")

    with open("data.json", 'r') as json_file:
        topic = re.findall("rt/(\w*)", json_file.read(),
                           re.I | re.DOTALL)  # Le indico que lo que viene después de un rt/ es el nombre del topic

    if len(topic) == 0:  # Esto significa que no se ha podido capturar los topics pues sólo se envian al principio de la comunicación (En paquetes Discovery)
        if fila is None:
            return "None"
        else:
            fila.append("None")
    else:
        topics_repetidos = []  # Esta lista auxiliar se usa para que no imprima topics repetidos
        for i in topic:
            if i not in topics_repetidos:
                topics_repetidos.append(i)

        if fila is None:
            return topics_repetidos
        else:
            fila.append(topics_repetidos)

    os.system("/bin/bash -c \"rm data.json\"")


def serviceName(ports, fila=None):
    os.system("/bin/bash -c \"tcpdump -r data.pcap -w filter.pcap udp portrange " + ports[0] + "-" + ports[1] + "\"")
    os.system("/bin/bash -c \"tshark -r filter.pcap -T json > data.json\"")

    with open("data.json", 'r') as json_file:
        service = re.findall("rq/\w*/(\w*)R", json_file.read(),
                             re.I | re.DOTALL)  # Le indico que lo que viene después de un rq/ es el nombre del servicio

    if len(service) == 0:  # Esto significa que no se ha podido capturar los servicios pues sólo se envian al principio de la comunicación (En paquetes Discovery)
        if fila is None:
            return "None"
        else:
            fila.append("None")
    else:
        services_repetidos = []  # Esta lista auxiliar se usa para que no imprima servicios repetidos
        for i in service:
            if i not in services_repetidos:
                services_repetidos.append(i)

        if fila is None:
            return services_repetidos
        else:
            fila.append(services_repetidos)

    os.system("/bin/bash -c \"rm data.json\"")



def ros2_scan_grepeable(direction, paquetes=None):
    if paquetes is None:
        session = PromptSession()

        print("¿Cuántos paquetes quieres capturar? (Para unos resultados óptimos es recomendable 100)")
        paquetes = session.prompt()

        while not re.match(r'^\d{2,3}$', paquetes):
            print("Dame un número del 10 al 999")
            paquetes = session.prompt()

    # Si nos obliga a ejecutar thsark con el usuario root, debemos añadir a nuestro usuario $USER al grupo de wireshark para evitar así ejecutar el fichero como root.
    tcpdump(prog=conf.prog.tshark, args=["-T", "json", "-f udp portrange 7400-7450", "-c", paquetes, "-w", 'data.pcap > /dev/null'],
            dump=True, quiet=True)  # -c quiere decir cuátos paquetes capturar.

    [hosts, output] = network_scan(direction)

    text = {}
    for host in hosts:
        # Nodo Ros2
        info_node = nm.scan(hosts=host, arguments='-p 7410-7440 -sU -n -T2 --open', sudo=True)
        string_node = str(info_node.get('scan'))

        if string_node != '{}':
            string_node = str(info_node.get('scan').get(host).get('udp'))

        matches = re.findall("(\d{4})", string_node)
        num_nodes = len(
            matches) // 2  # Por cada listener o talker se abren 2 puertos por lo que capturo todos los puiertos abiertos del 7400-7500 y lo divido entre 2
        list_nodes = []

        for i in range(num_nodes):
            list_nodes.append([matches[0], matches[1]])
            matches = matches[2:]

        if num_nodes != 0:  # A partir de aquí decimos que esta máquina ejecuta al menos un nodo ROS2
            text[host] = {"Instances ROS2": []}

            for i in range(num_nodes):
                # Topics
                topics = topicName(list_nodes[i])

                # Services
                services = serviceName(list_nodes[i])

                # DDS/RTPS vendor
                vendor = DDS_vendor(list_nodes[i])

                # Seguridad
                seg = checkSeg(list_nodes[i])

                text.get(host).get("Instances ROS2").append(
                    {"Node": list_nodes[i], "Topic Suscribed/Publishing": topics, "Services": services,
                     "DDS/RTPS vendor": vendor, "Security": seg})

    with open('data.json', 'w') as file:
        json.dump(text, file, indent=5)

    with open('data.json', 'r') as file:
        pprint(json.load(file))


ros2_scan_grepeable("192.168.100.0/24", "100")