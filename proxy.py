#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import time
import socks
from utils import clear, print_banner, gradient_print, gradient_input

def proxy_interactive():
    clear()
    print_banner()
    gradient_print(" === Proxy tester (SOCKS4/5, HTTP) ===", 0.03)
    proxy_ip = gradient_input(" Proxy IP: ").strip()
    proxy_port_str = gradient_input(" Proxy port: ").strip()
    try:
        proxy_port = int(proxy_port_str)
    except:
        gradient_print(" Invalid port.", 0.03)
        time.sleep(1.5)
        return
    proxy_type = gradient_input(" Proxy type (socks4/socks5/http): ").strip().lower()
    target = gradient_input(" Target IP:port to test through proxy: ").strip()
    if ':' not in target:
        gradient_print(" Invalid target format (use IP:port).", 0.03)
        time.sleep(1.5)
        return
    target_ip, target_port_str = target.split(':', 1)
    try:
        target_port = int(target_port_str)
    except:
        gradient_print(" Invalid target port.", 0.03)
        time.sleep(1.5)
        return

    try:
        if proxy_type == 'socks4':
            s = socks.socksocket()
            s.set_proxy(socks.SOCKS4, proxy_ip, proxy_port)
        elif proxy_type == 'socks5':
            s = socks.socksocket()
            s.set_proxy(socks.SOCKS5, proxy_ip, proxy_port)
        elif proxy_type == 'http':
            # HTTP CONNECT not implemented here; use simple socket connect
            s = socket.socket()
            s.settimeout(5)
            s.connect((proxy_ip, proxy_port))
            s.sendall(f"CONNECT {target_ip}:{target_port} HTTP/1.1\r\nHost: {target_ip}:{target_port}\r\n\r\n".encode())
            resp = s.recv(1024)
            if b"200" in resp:
                gradient_print(" HTTP proxy works (CONNECT)", 0.02)
            else:
                gradient_print(" HTTP proxy failed", 0.02)
            s.close()
            gradient_input(" Press Enter...")
            return
        else:
            gradient_print(" Unknown proxy type.", 0.03)
            time.sleep(1.5)
            return

        s.settimeout(5)
        s.connect((target_ip, target_port))
        gradient_print(" Proxy works! Connection established.", 0.02)
        s.close()
    except Exception as e:
        gradient_print(f" Proxy test failed: {e}", 0.02)
    print()
    gradient_input(" Press Enter to return to menu...")