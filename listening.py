#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import time
from utils import clear, print_banner, gradient_print, gradient_input

def listening_interactive():
    clear()
    print_banner()
    gradient_print(" === Listening check (TCP) ===", 0.03)
    target = gradient_input(" IP:port (e.g. 192.168.1.1:25565): ").strip()
    if ':' not in target:
        gradient_print(" Invalid format. Use IP:port", 0.03)
        time.sleep(1.5)
        return
    ip, port_str = target.split(':', 1)
    try:
        port = int(port_str)
    except:
        gradient_print(" Invalid port number.", 0.03)
        time.sleep(1.5)
        return

    gradient_print(f" Checking {ip}:{port}...", 0.03)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect((ip, port))
        gradient_print(f" [Result] {ip}:{port} is LISTENING", 0.02)
        sock.close()
    except:
        gradient_print(f" [Result] {ip}:{port} is CLOSED or FILTERED", 0.02)
    print()
    gradient_input(" Press Enter to return to menu...")