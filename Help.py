from prompt_toolkit.shortcuts import message_dialog

def menu():
    message_dialog(
        title='Help Menu',
        text='To get more information about a command, type the command name followed by -h\nFor example: vm -h'
             '\nAvailable commands:network_scan, vm, node, force_scan_all, ros2_scan\nPress ENTER to quit.').run()

def network_scan():
    message_dialog(
        title='Network Scan',
        text='It is a command that is used to know the active hosts that are in a network\nTo use it:\nnetwork_scan <network_target>  For exaple: network_scan 192.168.10.0/24'
             '\nIf the flag -e <dir_dest> is put at the end of the command, a .txt will be saved with the output. For example: network_scan 192.168.10.0/24 -e /home/example.txt'
             '\nPress ENTER to quit.').run()

def vm():
    message_dialog(
        title='Virtual Machine Scanner',
        text='It is a command that is used to check if a host is running in a virtual machine\nvm <ip_target> For example: vm 192.168.10.25\n'
             'If the flag -e <dir_dest> is put at the end of the command, a .txt will be saved with the output. For example: vm 192.168.10.25 -e /home/example.txt'
             '\nPress ENTER to quit.').run()

def node():
    message_dialog(
        title='Node ROS2 Scanner',
        text='It is a command that is used to check if a host is executing at least one ros2 node\nnode <ip_target> For example: node 192.168.6.9\n'
             'If the flag -e <dir_dest> is put at the end of the command, a .txt will be saved with the output. For example: node 192.168.6.9 -e /home/example.txt'
             '\nPress ENTER to quit.').run()

def force_scan_all():
    message_dialog(
        title='Full Scanner',
        text='This command combines the previous ones and also checks what ros2 nodes are in each host and what topics they are subscribed to or published in, who is the vendor and if security is enabled\n'
             'force_scan_all <network_target> For example: force_scan_all 192.168.100.0/24\n'
             'On the command line, you can pass the -oG argument to make the output grepeable or the -c argument to indicate how many packets to capture (default 100)\n'
             'For example: python3 app.py force_scan_all 192.168.100.0/24 -c 200 -oG'
             '\nPress ENTER to quit.').run()

def ros2_scan():
    message_dialog(
        title='ROS2 Full Scanner',
        text='This command is like force_scan_all but only gives information about hosts that are ros2 nodes\n'
             'ros2_scan <network_target> For example: ros2_scan 192.168.100.0/24\n'
             'On the command line, you can pass the -oG argument to make the output grepeable or the -c argument to indicate how many packets to capture (default 100)\n'
             'For example: python3 app.py ros2_scan 192.168.100.0/24 -c 200 -oG'
             '\nPress ENTER to quit.').run()

