#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import time
from utils import clear, print_banner, gradient_print, gradient_input

def connect_interactive():
    clear()
    print_banner()
    gradient_print(" === Connect one bot (no commands) ===", 0.03)
    ip = gradient_input(" Server IP: ").strip()
    port_str = gradient_input(" Port (default 25565): ").strip()
    port = int(port_str) if port_str.isdigit() else 25565
    version = gradient_input(" Minecraft version (e.g. 1.16.5): ").strip() or "1.16.5"
    username = gradient_input(" Bot username: ").strip()
    if not username:
        gradient_print(" Username is required.", 0.03)
        time.sleep(1.5)
        return
    gradient_print(f" Starting bot {username}...", 0.03)
    proc = subprocess.Popen(["node", "bot.js", ip, str(port), version, username],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    gradient_print(" Bot launched. It will stay online until you close this window.", 0.02)
    gradient_input(" Press Enter to return to menu (bot will continue in background).")
    # We don't kill the bot here – it keeps running.