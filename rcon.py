#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from utils import clear, print_banner, gradient_print, gradient_input
try:
    from mcrcon import MCRcon
    RCON_AVAILABLE = True
except ImportError:
    RCON_AVAILABLE = False

def rcon_interactive():
    clear()
    print_banner()
    if not RCON_AVAILABLE:
        gradient_print(" [Error] mcrcon library not installed. Run: pip install mcrcon", 0.03)
        gradient_input(" Press Enter...")
        return
    gradient_print(" === RCON interactive console ===", 0.03)
    ip = gradient_input(" Server IP: ").strip()
    port_str = gradient_input(" RCON port (default 25575): ").strip()
    port = int(port_str) if port_str.isdigit() else 25575
    password = gradient_input(" RCON password: ").strip()
    try:
        with MCRcon(ip, password, port=port) as mcr:
            gradient_print(" Connected. Type 'exit' to close.", 0.02)
            while True:
                cmd = gradient_input("> ")
                if cmd.lower() == 'exit':
                    break
                resp = mcr.command(cmd)
                print(resp)
    except Exception as e:
        gradient_print(f" RCON error: {e}", 0.03)
    gradient_input("\n Press Enter to return to menu...")