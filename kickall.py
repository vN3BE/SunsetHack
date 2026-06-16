#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import time
import random
from utils import clear, print_banner, gradient_print, gradient_input

def kickall_interactive():
    clear()
    print_banner()
    gradient_print(" Kick all (random names, connect & disconnect)", 0.03)
    ip = gradient_input(" Server IP: ").strip()
    port_str = gradient_input(" Port (default 25565): ").strip()
    port = int(port_str) if port_str.isdigit() else 25565
    version = gradient_input(" Minecraft version: ").strip() or "1.16.5"
    loop_str = gradient_input(" Loop count (1 = single kick, 0 = infinite): ").strip()
    loop = int(loop_str) if loop_str.isdigit() else 1
    gradient_print(" Starting kick bots with random usernames...", 0.03)
    if loop == 0:
        while True:
            username = f"Kicker_{random.randint(1000,9999)}"
            proc = subprocess.Popen(["node", "bot.js", ip, str(port), version, username],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
            proc.terminate()
            time.sleep(0.5)
    else:
        for _ in range(loop):
            username = f"Kicker_{random.randint(1000,9999)}"
            proc = subprocess.Popen(["node", "bot.js", ip, str(port), version, username],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
            proc.terminate()
            time.sleep(0.5)
    gradient_print(" KickAll test completed.", 0.03)
    gradient_input(" Press Enter to return to menu...")