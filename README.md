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
