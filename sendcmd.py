#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import os
import time
from utils import clear, print_banner, gradient_print, gradient_input

def sendcmd_interactive():
    clear()
    print_banner()
    gradient_print(" === Send commands to server via bot ===", 0.03)
    ip = gradient_input(" Server IP: ").strip()
    port_str = gradient_input(" Port (default 25565): ").strip()
    port = int(port_str) if port_str.isdigit() else 25565
    version = gradient_input(" Minecraft version: ").strip() or "1.16.5"
    username = gradient_input(" Bot username: ").strip()
    if not username:
        gradient_print(" Username is required.", 0.03)
        time.sleep(1.5)
        return
    commands_file = gradient_input(" Path to commands file (one per line): ").strip()
    if not os.path.exists(commands_file):
        gradient_print(" File not found. No commands will be sent.", 0.03)
        time.sleep(1.5)
        return
    gradient_print(f" Launching bot and sending commands from {commands_file}...", 0.03)
    proc = subprocess.Popen(["node", "bot.js", ip, str(port), version, username, commands_file],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    gradient_print(" Bot started and will execute commands.", 0.02)
    gradient_input(" Press Enter to return to menu (bot continues).")