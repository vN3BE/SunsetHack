#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import ipaddress
import threading
import time
from utils import clear, print_banner, gradient_print, gradient_input

def parse_ip_range(ip_str):
    ips = []
    ip_str = ip_str.strip()
    if '-' not in ip_str and '/' not in ip_str:
        try:
            ipaddress.ip_address(ip_str)
            return [ip_str]
        except:
            return []
    if '-' in ip_str and '/' not in ip_str:
        parts = ip_str.split('-')
        if len(parts) == 2:
            start = parts[0].strip()
            end = parts[1].strip()
            try:
                start_ip = ipaddress.ip_address(start)
                end_ip = ipaddress.ip_address(end)
                if start_ip.version != end_ip.version:
                    return []
                if start_ip > end_ip:
                    start_ip, end_ip = end_ip, start_ip
                current = int(start_ip)
                last = int(end_ip)
                while current <= last:
                    ips.append(str(ipaddress.ip_address(current)))
                    current += 1
                return ips
            except:
                return []
    if '/' in ip_str:
        try:
            net = ipaddress.ip_network(ip_str, strict=False)
            return [str(ip) for ip in net.hosts()]
        except:
            return []
    return []

def parse_port_range(port_str):
    ports = []
    port_str = port_str.strip()
    if ',' in port_str:
        for part in port_str.split(','):
            ports.extend(parse_port_range(part.strip()))
        return sorted(set(ports))
    if '-' in port_str:
        try:
            a, b = map(int, port_str.split('-'))
            if a > b:
                a, b = b, a
            return list(range(a, b+1))
        except:
            return []
    try:
        return [int(port_str)]
    except:
        return []

def scan_port(ip, port, timeout=0.5):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_ip_port(ip, port, timeout, results_dict, lock):
    open = scan_port(ip, port, timeout)
    with lock:
        if open:
            results_dict[(ip, port)] = open

def port_scanner_interactive():
    clear()
    print_banner()
    gradient_print(" === Port scanner (IP/port ranges, TCP connect) ===", 0.03)
    ip_input = gradient_input(" IP or range (e.g. 192.168.1.1, 192.168.1.1-192.168.1.10, 192.168.1.0/24): ").strip()
    if not ip_input:
        gradient_print(" IP not entered.", 0.03)
        time.sleep(1)
        return
    ip_list = parse_ip_range(ip_input)
    if not ip_list:
        gradient_print(" Invalid IP or range format.", 0.03)
        time.sleep(1.5)
        return
    port_input = gradient_input(" Port or range (e.g. 80, 1-1000, 80,443,25565): ").strip()
    if not port_input:
        gradient_print(" Port not entered.", 0.03)
        time.sleep(1)
        return
    port_list = parse_port_range(port_input)
    if not port_list:
        gradient_print(" Invalid port or range format.", 0.03)
        time.sleep(1.5)
        return
    method = gradient_input(" Scanning method (connect only): ").strip().lower()
    if method not in ['connect']:
        method = 'connect'
    timeout_str = gradient_input(" Timeout in seconds (default 0.5): ").strip()
    timeout = float(timeout_str) if timeout_str.replace('.','',1).isdigit() else 0.5
    total_checks = len(ip_list) * len(port_list)
    gradient_print(f"\n Scanning {len(ip_list)} IP × {len(port_list)} ports = {total_checks} combinations", 0.03)
    gradient_print(" This may take some time. Press Enter to start...")
    input()
    results = {}
    lock = threading.Lock()
    threads = []
    max_threads = 200
    scanned = 0
    start_time = time.time()
    for ip in ip_list:
        for port in port_list:
            t = threading.Thread(target=scan_ip_port, args=(ip, port, timeout, results, lock))
            t.start()
            threads.append(t)
            scanned += 1
            if len(threads) >= max_threads:
                for t in threads:
                    t.join()
                threads = []
            if scanned % 100 == 0:
                elapsed = time.time() - start_time
                rate = scanned / elapsed if elapsed > 0 else 0
                gradient_print(f" Progress: {scanned}/{total_checks} (≈{rate:.0f} ports/sec)", 0.01)
    for t in threads:
        t.join()
    elapsed = time.time() - start_time
    gradient_print(f"\n Scan completed in {elapsed:.2f} sec", 0.03)
    open_ports = sorted([(ip, port) for (ip, port), open in results.items() if open])
    if not open_ports:
        gradient_print(" No open ports found.", 0.03)
    else:
        gradient_print(f" Found open ports: {len(open_ports)}", 0.025)
        for ip, port in open_ports:
            gradient_print(f"   {ip}:{port} — open", 0.02)
            time.sleep(0.01)
    print()
    gradient_input(" Press Enter to return to menu...")