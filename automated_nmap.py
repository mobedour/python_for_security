"""
This Python script uses the nmap and netifaces libraries to perform a network scan. It is designed for use on Kali Linux
or any other system with Python and the required libraries installed. The script automatically detects the local IP 
address and subnet of the network you are connected to and scans the specified range of ports (1-1024) for open ports 
and services running on them.

Usage:
1. Ensure you have Python installed on your system.

2. Install the required libraries if they are not already installed:
   - nmap: `pip install python-nmap`
   - netifaces: `sudo apt-get install python3-netifaces`

3. Run the script using Python:
   - in the terminal, type:
   python3 automated_nmap.py
   
The script will automatically detect your local IP address and subnet, perform a scan on the network, and display
the results, including the host IP addresses, states, and services detected.
Note: This script requires administrative privileges to run correctly. Make sure to run it with appropriate permissions.

Author: mobedour
"""

import nmap
import socket
import netifaces

def get_ip_address():
    """
    Retrieves the local IP address and netmask of the active network interface.
    Uses netifaces to get the addresses of all network interfaces and returns the first
    non-localhost IPv4 address and its corresponding netmask.
    
    Returns:
        tuple: (ip_address, netmask) if successful, (None, None) otherwise.
    """
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs:
            ip_info = addrs[netifaces.AF_INET][0]
            ip_address = ip_info['addr']
            netmask = ip_info['netmask']
            if ip_address != '127.0.0.1':
                return ip_address, netmask
    return None, None

def get_network_range(ip_address, netmask):
    """
    Calculates the network range (subnet) from the given IP address and netmask.
    
    Args:
        ip_address (str): The local IP address.
        netmask (str): The netmask corresponding to the local IP address.
    
    Returns:
        str: The network range in CIDR notation (e.g., '192.168.1.0/24').
    """
    ip_parts = ip_address.split('.')
    mask_parts = netmask.split('.')
    network_parts = [str(int(ip_parts[i]) & int(mask_parts[i])) for i in range(4)]
    network_range = '.'.join(network_parts) + '/24'
    return network_range

def scan_network(ip_range):
    """
    Scans the specified IP range for open ports and services using nmap.
    
    Args:
        ip_range (str): The network range to scan in CIDR notation (e.g., '192.168.1.0/24').
    """
    nm = nmap.PortScanner()
    nm.scan(ip_range, '1-1024', '-sV')
    for host in nm.all_hosts():
        print(f'Host: {host} ({nm[host].hostname()})')
        print(f'State: {nm[host].state()}')
        for proto in nm[host].all_protocols():
            print(f'Protocol: {proto}')
            lport = nm[host][proto].keys()
            for port in lport:
                print(f'port: {port}\tstate: {nm[host][proto][port]["state"]}\tservice: {nm[host][proto][port]["name"]}')

# Retrieve the local IP address and netmask
ip_address, netmask = get_ip_address()

# If IP address and netmask are found, calculate the network range and scan the network
if ip_address and netmask:
    network_range = get_network_range(ip_address, netmask)
    print(f'Scanning network: {network_range}')
    scan_network(network_range)
else:
    print('Could not determine local IP address and netmask.')
