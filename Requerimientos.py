import os, time
from sys import stdout

def red():
    RED = "\033[1;31m"
    stdout.write(RED)

def green():
    GREEN = "\033[0;32m"
    stdout.write(GREEN)

def blue():
    BLUE = "\033[1;34m"
    stdout.write(BLUE)

def yellow():
    YELLOW = "\033[1;33m"
    stdout.write(YELLOW)

def purple():
    PURPLE = "\033[1;35m"
    stdout.write(PURPLE)

def white():
    WHITE = "\033[1;37m"
    stdout.write(WHITE)

banner = """
 ███████████            █████              ███████████            
░░███░░░░░███          ░░███              ░░███░░░░░███           
 ░███    ░███   ██████  ░███████   ██████  ░███    ░███ █████ ████
 ░██████████   ███░░███ ░███░░███ ███░░███ ░██████████ ░░███ ░███ 
 ░███░░░░░███ ░███ ░███ ░███ ░███░███ ░███ ░███░░░░░░   ░███ ░███ 
 ░███    ░███ ░███ ░███ ░███ ░███░███ ░███ ░███         ░███ ░███ 
 █████   █████░░██████  ████████ ░░██████  █████        ░░███████ 
░░░░░   ░░░░░  ░░░░░░  ░░░░░░░░   ░░░░░░  ░░░░░          ░░░░░███ 
                                                         ███ ░███ 
                                                        ░░██████  
                                                         ░░░░░░                                                                                                                                                                                                                                                          
"""

def menu():
    green()
    print(banner)
    blue()
    time.sleep(1)
    print("1 -> Instalar Requerimientos necesarios")
    time.sleep(1)
    print("\n2 -> Salir")
    time.sleep(1)

    while True:
        option = input("\n-->> ")

        if option == "1":
            req()
            break
        elif option == "2":
            exit()


def req():
    green()
    print("[+] Instalando requerimientos...\n")

    # Instalando Requerimientos
    os.system("sudo apt-get update -y")
    os.system("sudo apt install python3-pip")
    os.system("python3 -m pip install prompt-toolkit")
    os.system("python3 -m pip install nmap")
    os.system("sudo python3 -m pip install --pre scapy[basic]")
    os.system("sudo add-apt-repository -y ppa:wireshark-dev/stable")
    os.system("sudo apt install -y tshark")
    os.system("sudo python3 -m pip install texttable")
    os.system("sudo pip install python-nmap")

    time.sleep(2)
    print("[+] Requetimientos instalados correctamente")


if __name__ == '__main__':
    id = os.getuid()

    if id == 0:
        red()
        print()
        print("[!] No hay que ser root para ejecutar la herramienta")
        print()
    else:
        menu()
