#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
from utils import clear, print_banner, gradient_print, gradient_input

def search_minecraft_servers(query):
    results = []
    # Minecraft-Server-List.com
    try:
        url = f"https://minecraft-server-list.com/search/?search={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            for row in soup.select('div.server-listing'):
                name_tag = row.select_one('a.server-name')
                ip_tag = row.select_one('span.server-ip')
                if name_tag and ip_tag:
                    name = name_tag.text.strip()
                    ip = ip_tag.text.strip()
                    results.append({'source': 'Minecraft-Server-List.com', 'name': name, 'ip': ip})
        else:
            results.append({'source': 'Minecraft-Server-List.com', 'error': f'HTTP {resp.status_code}'})
    except Exception as e:
        results.append({'source': 'Minecraft-Server-List.com', 'error': str(e)})
    # MinecraftServer.org
    try:
        url = f"https://minecraft-server.org/search/{query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            for row in soup.select('div.server-item'):
                name_tag = row.select_one('h3 a')
                ip_tag = row.select_one('div.server-ip')
                if name_tag and ip_tag:
                    name = name_tag.text.strip()
                    ip = ip_tag.text.strip()
                    results.append({'source': 'MinecraftServer.org', 'name': name, 'ip': ip})
        else:
            results.append({'source': 'MinecraftServer.org', 'error': f'HTTP {resp.status_code}'})
    except Exception as e:
        results.append({'source': 'MinecraftServer.org', 'error': str(e)})
    return results

def websearch_interactive():
    clear()
    print_banner()
    gradient_print(" === WebSearch – parse servers from monitoring sites ===", 0.03)
    query = gradient_input(" Enter server IP or name: ").strip()
    if not query:
        gradient_print(" Query not entered.", 0.03)
        time.sleep(1)
        return
    gradient_print(f"\n Searching servers for '{query}'...", 0.04)
    results = search_minecraft_servers(query)
    found = 0
    for res in results:
        if 'error' in res:
            gradient_print(f" [{res['source']}] Error: {res['error']}", 0.02)
        else:
            found += 1
            gradient_print(f" [{res['source']}] {res['name']} → {res['ip']}", 0.025)
    if found == 0 and not any('error' in r for r in results):
        gradient_print(" No servers found.", 0.03)
    print()
    gradient_input(" Press Enter to return to menu...")