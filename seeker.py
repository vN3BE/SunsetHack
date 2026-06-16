#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import discord
from discord.ext import commands
import asyncio
from utils import clear, print_banner, gradient_print, gradient_input

def get_servers_by_token(token):
    bot = commands.Bot(command_prefix="!", self_bot=False, help_command=None)
    async def get_guilds():
        try:
            await bot.login(token)
            await bot.wait_until_ready()
            guilds = []
            for guild in bot.guilds:
                guilds.append({
                    'name': guild.name,
                    'id': guild.id,
                    'member_count': guild.member_count,
                    'owner': str(guild.owner) if guild.owner else "Unknown"
                })
            await bot.close()
            return guilds
        except discord.LoginFailure:
            return None
        except Exception as e:
            return {'error': str(e)}
        finally:
            try:
                await bot.close()
            except:
                pass
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_guilds())
        loop.close()
        return result
    except Exception as e:
        return {'error': str(e)}

def seeker_interactive():
    clear()
    print_banner()
    gradient_print(" === Seeker (Discord bot token) ===", 0.03)
    token = gradient_input(" Enter Discord bot token: ").strip()
    if not token:
        gradient_print(" Token not entered.", 0.03)
        time.sleep(1)
        return
    gradient_print(f"\n Connecting and fetching server list...", 0.04)
    time.sleep(0.5)
    result = get_servers_by_token(token)
    if result is None:
        gradient_print(" [Error] Invalid token or not a bot token.", 0.03)
    elif isinstance(result, dict) and 'error' in result:
        gradient_print(f" [Error] {result['error']}", 0.03)
    elif not result:
        gradient_print(" [Info] Bot is not a member of any server.", 0.03)
    else:
        gradient_print(f" [Servers found] {len(result)}", 0.025)
        for i, guild in enumerate(result, 1):
            gradient_print(f" [{i}] {guild['name']}", 0.025)
            gradient_print(f"     ID: {guild['id']}", 0.02)
            gradient_print(f"     Members: {guild['member_count']}", 0.02)
            gradient_print(f"     Owner: {guild['owner']}", 0.02)
            time.sleep(0.1)
    print()
    gradient_input(" Press Enter to return to menu...")