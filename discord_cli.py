#!/home/chumby/.openclaw/mcp-servers/discord/.venv/bin/python
"""
Discord CLI - System-wide Discord bot interface for OpenClaw agents.

USAGE (from command line):
    discord-cli list_channels <guild_id>
    discord-cli create_channel <guild_id> <category_id> <name>
    discord-cli send_message <channel_id> <content>
    discord-cli get_channel_id <guild_id> <channel_name>

AGENT INTEGRATION:
    See ~/docs/discord-cli.md for comprehensive documentation on how agents
    should use this CLI, including error handling, rate limiting, and examples.

QUICK REFERENCE:
    - list_channels: Get all channels in a guild
    - create_channel: Create a text channel in a category
    - send_message: Send a message to a channel
    - get_channel_id: Find channel ID by name

COMMON IDs:
    - Guild: 1467329846265909446 (main server)
    - OPENCLAW category: 14673649053836288852
    - Heartbeats channel: 1482113021592735887

EXAMPLES:
    discord-cli list_channels 1467329846265909446
    discord-cli create_channel 1467329846265909446 14673649053836288852 test-channel
    discord-cli send_message 1482113021592735887 "Heartbeat report"
    discord-cli get_channel_id 1467329846265909446 general

ERRORS:
    All commands print "Error: <reason>" on failure and exit with code 1.
    Agents should check exit code and parse stderr/stdout.

RATE LIMITING:
    - Message sending: ~5/second limit (use delays between bulk ops)
    - Channel creation: ~5/guild/5-minute limit
    - Cache channel IDs; don't call list_channels per operation

PERMISSIONS REQUIRED:
    - View Channels (list_channels, get_channel_id)
    - Manage Channels (create_channel)
    - Send Messages (send_message)

FULL DOCUMENTATION: ~/docs/discord-cli.md
"""

import asyncio
import discord
from discord.ext import commands
import os
import sys
from typing import Optional

# Bot token from environment variable
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    print("Error: DISCORD_BOT_TOKEN environment variable not set")
    print("Set it before running: export DISCORD_BOT_TOKEN=\"your_token_here\"")
    sys.exit(1)

# Minimal intents
intents = discord.Intents.default()
intents.message_content = False
intents.guilds = True

async def list_channels(guild_id: str):
    """List all channels in a guild."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            guild = bot.get_guild(int(guild_id))
            if guild is None:
                guild = await bot.fetch_guild(int(guild_id))
            
            print(f"Channels in guild {guild_id}:")
            for ch in guild.channels:
                channel_type = {0: "text", 1: "voice", 4: "category"}.get(ch.type, "unknown")
                print(f"  - {ch.name} (ID: {ch.id}, type: {channel_type})")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def create_channel(guild_id: str, category_id: str, name: str):
    """Create a new text channel."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            guild = bot.get_guild(int(guild_id))
            if guild is None:
                guild = await bot.fetch_guild(int(guild_id))
            
            channel = await guild.create_text_channel(name, category=discord.Object(int(category_id)))
            print(f"Created channel '{name}' (ID: {channel.id})")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def send_message(channel_id: str, content: str):
    """Send a message to a channel."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            channel = bot.get_channel(int(channel_id))
            if channel is None:
                print(f"Error: Channel {channel_id} not found")
                await bot.close()
                return
            
            await channel.send(content)
            print(f"Message sent to channel {channel_id}: {content}")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def get_channel_id(guild_id: str, channel_name: str):
    """Get channel ID by name."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            guild = bot.get_guild(int(guild_id))
            if guild is None:
                guild = await bot.fetch_guild(int(guild_id))
            
            channel = discord.utils.get(guild.channels, name=channel_name)
            if channel is None:
                print(f"Error: Channel '{channel_name}' not found in guild {guild_id}")
            else:
                print(f"Channel '{channel_name}' ID: {channel.id}")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

def main():
    import sys
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nExamples:")
        print("  python discord_cli_simple.py list_channels 1467329846265909446")
        print("  python discord_cli_simple.py create_channel 1467329846265909446 1467364905383628852 test-channel")
        print("  python discord_cli_simple.py send_message 1467357084843507782 Hello from CLI")
        print("  python discord_cli_simple.py get_channel_id 1467329846265909446 general")
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        if command == "list_channels":
            if len(sys.argv) != 3:
                print("Usage: python discord_cli_simple.py list_channels <guild_id>")
                sys.exit(1)
            asyncio.run(list_channels(sys.argv[2]))
        
        elif command == "create_channel":
            if len(sys.argv) != 5:
                print("Usage: python discord_cli_simple.py create_channel <guild_id> <category_id> <name>")
                sys.exit(1)
            asyncio.run(create_channel(sys.argv[2], sys.argv[3], sys.argv[4]))
        
        elif command == "send_message":
            if len(sys.argv) != 4:
                print("Usage: python discord_cli_simple.py send_message <channel_id> <content>")
                sys.exit(1)
            asyncio.run(send_message(sys.argv[2], sys.argv[3]))
        
        elif command == "get_channel_id":
            if len(sys.argv) != 4:
                print("Usage: python discord_cli_simple.py get_channel_id <guild_id> <channel_name>")
                sys.exit(1)
            asyncio.run(get_channel_id(sys.argv[2], sys.argv[3]))
        
        else:
            print(f"Unknown command: {command}")
            print(__doc__)
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()