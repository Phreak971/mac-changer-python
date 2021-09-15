import subprocess
import optparse
import re
from typing import cast

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='Interface to change its MAC Address')
    parser.add_option('-m', '--mac', dest='new_mac', help='New MAC Address')
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify an interface, use --help for more info.")
    return options

def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(['ifconfig', interface])
    except:
        print(f'[-] interface {interface} not found')
        return None
    mac_addr = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode())
    if mac_addr:
        return mac_addr.group(0)
    else:
        print(f"[-] Couldnot read MAC Address of {interface}")
    return None
    

options = get_arguments()
if re.fullmatch(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", options.new_mac): 
    if get_current_mac(options.interface):
        print(f'Current MAC for {options.interface}: {get_current_mac(options.interface)}')
        change_mac(options.interface, options.new_mac)
        if get_current_mac(options.interface) == options.new_mac:
            print(f'[+] MAC Address was Successfully changed to: {get_current_mac(options.interface)}')
        else:
            print('[-] Could not Change MAC')
else:
    print('[-] Invalid MAC Address')



