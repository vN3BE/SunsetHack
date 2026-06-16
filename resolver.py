#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import time
from utils import clear, print_banner, gradient_print, gradient_input

def resolver_interactive():
    clear()
    print_banner()
    domain = gradient_input(" Enter server domain (e.g. mc.hypixel.net): ").strip()
    if not domain:
        gradient_print(" Domain not entered.", 0.03)
        time.sleep(1)
        return
    gradient_print(f"\n Resolving {domain}...", 0.04)
    time.sleep(0.5)
    try:
        ipv4 = socket.gethostbyname(domain)
        gradient_print(f" [IPv4] {ipv4}", 0.025)
    except:
        gradient_print(" [IPv4] resolution failed", 0.025)
    try:
        addrinfo = socket.getaddrinfo(domain, None, socket.AF_INET6)
        ipv6 = addrinfo[0][4][0] if addrinfo else None
        if ipv6:
            gradient_print(f" [IPv6] {ipv6}", 0.025)
        else:
            gradient_print(" [IPv6] not available", 0.025)
    except:
        gradient_print(" [IPv6] resolution failed", 0.025)
    print()
    gradient_input(" Press Enter to return to menu...")