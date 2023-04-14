import os
import re
import sys
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.styles import Style
import Help
import Recon

stylePrompt = Style.from_dict(
    {
        # Default style.
        "": "#ff0066",
        # Prompt.
        "username": "#884444 italic",
        "at": "#00aa00",
        "colon": "#00aa00",
        "pound": "#00aa00",
        "host": "#000088 bg:#aaaaff",
        "path": "#884444 underline",
        # Make a selection reverse/underlined.
        # (Use Control-Space to select.)
        "selected-text": "reverse underline",
    }
)

banner= """
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

def main():
    print(banner)
    print('         __')
    print(' _(\    |@@|')
    print('(__/\__ \--/ __')
    print('   \___|----|  |   __')
    print('       \ }{ /\ )_ / _\\')
    print('       /\__/\ \__O (__')
    print('      (--/\--)    \__/')
    print('      _)(  )(_')
    print('     `---\'\'---`')

    session = PromptSession()

    while True:
        text = session.prompt(HTML("<b>console>></b> "), style=stylePrompt, rprompt=os.getcwd(), enable_history_search=True)
        string = re.split(" +", text)
        print("Scanning... please wait")

        if re.match(r'^network_scan*', text.lower()):  #Pongo lower() para que no sea case sensitive
            if text.lower() == 'network_scan -h':
                Help.network_scan()

            elif re.match(r'^network_scan ((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}/\d{1,2}$', text.lower()):
                direction = string[1]
                Recon.print_hosts(direction)

            elif re.match(r'^network_scan ((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}/\d{1,2} -e .*$', text.lower()):
                direction = string[1]
                file_name = string[3].split("/").pop()
                path = string[3].replace(file_name, '')
                Recon.print_hosts_export(direction, path, file_name)

            else:
                print("Enter a valid command, write network_scan -h for more info")

        elif re.match(r'^vm*', text.lower()):
            if text.lower() == 'vm -h':
                Help.vm()

            elif re.match(r'^vm ((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$', text.lower()):
                direction = string[1]
                Recon.vm_scan(direction)

            elif re.match(r'^vm ((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4} -e .*$', text.lower()):
                direction = string[1]
                file_name = string[3].split("/").pop()
                path = string[3].replace(file_name, '')
                Recon.vm_scan_export(direction, path, file_name)

            else:
                print("Enter a valid command, write vm -h for more info")

        elif re.match(r'^node*', text.lower()):
            if text.lower() == 'node -h':
                Help.node()

            elif re.match(r'^node ((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$', text.lower()):
                direction = string[1]
                Recon.node_scan(direction)

            elif re.match(r'^node ((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4} -e .*$', text.lower()):
                direction = string[1]
                file_name = string[3].split("/").pop()
                path = string[3].replace(file_name, '')
                Recon.node_scan_export(direction, path, file_name)

            else:
                print("Enter a valid command, write node -h for more info")

        elif re.match(r'^force_scan_all*', text.lower()):
            if text.lower() == 'force_scan_all -h':
                Help.force_scan_all()

            elif re.match(r'^force_scan_all ((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}/\d{1,2}$', text.lower()):
                direction = string[1]
                Recon.force_scan_all(direction)

            else:
                print("Enter a valid command, write force_scan_all -h for more info")

        elif re.match(r'^ros2_scan*', text.lower()):
            if text.lower() == 'ros2_scan -h':
                Help.ros2_scan()

            elif re.match(r'^ros2_scan ((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}/\d{1,2}$', text.lower()):
                direction = string[1]
                Recon.ros2_scan(direction)

            else:
                print("Enter a valid command, write ros2_scan -h for more info")

        elif text.lower() == 'help':
            Help.menu()
        elif text == '':
            continue
        else:
            print('Invalid command, write "help" for more info')

def args():
    list_valid_comands = ["network_scan", "vm", "node", "force_scan_all", "ros2_scan"]

    if sys.argv[1].lower() == '-help':
        print("Valid commands are: network_scan, vm, node, force_scan_all, ros2_scan")
    elif sys.argv[1].lower() in list_valid_comands:
        if sys.argv[1].lower() == list_valid_comands[0]:
            try:
                if sys.argv[2].lower() == '-h':
                    Help.network_scan()

                elif re.match(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}/\d{1,2}$', sys.argv[2].lower()):
                    direction = sys.argv[2]
                    Recon.print_hosts(direction)

                else:
                    print("Enter a valid command, write network_scan -h for more info")
            except:
                print("Enter a valid command, write network_scan -h for more info")

        elif sys.argv[1].lower() == list_valid_comands[1]:
            try:
                if sys.argv[2].lower() == '-h':
                    Help.vm()

                elif re.match(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$', sys.argv[2].lower()):
                    direction = sys.argv[2]
                    Recon.vm_scan(direction)

                else:
                    print("Enter a valid command, write vm -h for more info")
            except:
                print("Enter a valid command, write vm -h for more info")

        elif sys.argv[1].lower() == list_valid_comands[2]:
            try:
                if sys.argv[2].lower() == '-h':
                    Help.node()

                elif re.match(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$', sys.argv[2].lower()):
                    direction = sys.argv[2]
                    Recon.node_scan(direction)

                else:
                    print("Enter a valid command, write node -h for more info")
            except:
                print("Enter a valid command, write node -h for more info")

        elif sys.argv[1].lower() == list_valid_comands[3]:
            try:
                if sys.argv[2].lower() == '-h':
                    Help.force_scan_all()

                elif re.match(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}/\d{1,2}$', sys.argv[2].lower()):
                    if len(sys.argv) == 6:
                        if sys.argv[5] == "-oG" and sys.argv[3] == "-c" and re.match(r'^\d{2,3}$', sys.argv[4].lower()):
                            direction = sys.argv[2]
                            paquetes = sys.argv[4]
                            Recon.force_scan_all_grepeable(direction, paquetes)
                        else:
                            print("Enter a valid command, write force_scan_all -h for more info", file=sys.stderr)

                    elif len(sys.argv) == 5:
                        if sys.argv[3] == "-c" and re.match(r'^\d{2,3}$', sys.argv[4].lower()):
                            direction = sys.argv[2]
                            paquetes = sys.argv[4]
                            Recon.force_scan_all(direction, paquetes)
                        else:
                            print("Enter a valid command, write force_scan_all -h for more info", file=sys.stderr)

                    elif len(sys.argv) == 4:
                        if sys.argv[3] == "-oG":
                            direction = sys.argv[2]
                            paquetes = "100"
                            Recon.force_scan_all_grepeable(direction, paquetes)
                        else:
                            print("Enter a valid command, write force_scan_all -h for more info", file=sys.stderr)

                    elif len(sys.argv) == 3:
                        direction = sys.argv[2]
                        paquetes = "100"
                        Recon.force_scan_all(direction, paquetes)

                    else:
                        print("Enter a valid command, write force_scan_all -h for more info", file=sys.stderr)
                else:
                    print("Enter a valid command, write force_scan_all -h for more info", file=sys.stderr)
            except:
                print("Enter a valid command, write force_scan_all -h for more info", file=sys.stderr)

        elif sys.argv[1].lower() == list_valid_comands[4]:
            try:
                if sys.argv[2].lower() == '-h':
                    Help.ros2_scan()

                elif re.match(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}/\d{1,2}$', sys.argv[2].lower()):
                    if len(sys.argv) == 6:
                        if sys.argv[5] == "-oG" and sys.argv[3] == "-c" and re.match(r'^\d{2,3}$', sys.argv[4].lower()):
                            direction = sys.argv[2]
                            paquetes = sys.argv[4]
                            Recon.ros2_scan_grepeable(direction, paquetes)
                        else:
                            print("Enter a valid command, write ros2_scan -h for more info", file=sys.stderr)

                    elif len(sys.argv) == 5:
                        if sys.argv[3] == "-c" and re.match(r'^\d{2,3}$', sys.argv[4].lower()):
                            direction = sys.argv[2]
                            paquetes = sys.argv[4]
                            Recon.ros2_scan(direction, paquetes)
                        else:
                            print("Enter a valid command, write ros2_scan -h for more info", file=sys.stderr)

                    elif len(sys.argv) == 4:
                        if sys.argv[3] == "-oG":
                            direction = sys.argv[2]
                            paquetes = "100"
                            Recon.ros2_scan_grepeable(direction, paquetes)
                        else:
                            print("Enter a valid command, write ros2_scan -h for more info", file=sys.stderr)

                    elif len(sys.argv) == 3:
                        direction = sys.argv[2]
                        paquetes = "100"
                        Recon.ros2_scan(direction, paquetes)

                    else:
                        print("Enter a valid command, write ros2_scan -h for more info", file=sys.stderr)
                else:
                    print("Enter a valid command, write ros2_scan -h for more info", file=sys.stderr)
            except:
                print("Enter a valid command, write ros2_scan -h for more info", file=sys.stderr)
    else:
        print('Invalid command, write "-help" for more info')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        args()