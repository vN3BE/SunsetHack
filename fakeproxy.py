#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import time
from utils import clear, print_banner, gradient_print, gradient_input

def fakeproxy_interactive():
    clear()
    print_banner()
    gradient_print(" === FakeProxy (Velocity/BungeeCord forwarding simulation) ===", 0.03)
    ip = gradient_input(" Server IP: ").strip()
    port_str = gradient_input(" Port: ").strip()
    try:
        port = int(port_str)
    except:
        gradient_print(" Invalid port.", 0.03)
        time.sleep(1.5)
        return
    mode = gradient_input(" Forwarding mode (legacy/modern): ").strip().lower()
    gradient_print(f" Connecting to {ip}:{port} with {mode} fake proxy header...", 0.03)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    try:
        sock.connect((ip, port))
        if mode == "legacy":
            # Simple BungeeCord forwarding (not full implementation)
            sock.send(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        else:
            # Modern forwarding – just a test
            sock.send(b"\x00\x01\x00\x00")
        time.sleep(0.5)
        data = sock.recv(1024)
        gradient_print(" Fake proxy test completed. Server responded.", 0.02)
        sock.close()
    except Exception as e:
        gradient_print(f" Error: {e}", 0.02)
    print()
    gradient_input(" Press Enter to return to menu...")