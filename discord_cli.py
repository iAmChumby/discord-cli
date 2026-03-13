#!/home/chumby/.openclaw/mcp-servers/discord/.venv/bin/python
"""
Simple Discord CLI using discord.py directly (no MCP).

Usage:
    python discord_cli_simple.py list_channels <guild_id>
    python discord_cli_simple.py create_channel <guild_id> <category_id> <name>
    python discord_cli_simple.py delete_channel <channel_id>
    python discord_cli_simple.py send_message <channel_id> <content>
    python discord_cli_simple.py delete_message <channel_id> <message_id>
    python discord_cli_simple.py get_last_message <channel_id> [limit]
    python discord_cli_simple.py kick <guild_id> <user_id> [reason]
    python discord_cli_simple.py ban <guild_id> <user_id> [reason] [delete_message_days]
    python discord_cli_simple.py timeout <guild_id> <user_id> <minutes> [reason]
    python discord_cli_simple.py list_roles <guild_id>
    python discord_cli_simple.py create_role <guild_id> <name>
    python discord_cli_simple.py delete_role <guild_id> <role_id>
    python discord_cli_simple.py add_role <guild_id> <user_id> <role_id>
    python discord_cli_simple.py remove_role <guild_id> <user_id> <role_id>
    python discord_cli_simple.py user_info <guild_id> <user_id>
    python discord_cli_simple.py get_channel_id <guild_id> <channel_name>
"""

import asyncio
import discord
from discord.ext import commands

# Bot token - set via DISCORD_BOT_TOKEN environment variable
import os
TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
if not TOKEN:
    print("Error: DISCORD_BOT_TOKEN environment variable not set")
    print("Set it with: export DISCORD_BOT_TOKEN='your-token-here'")
    exit(1)

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

async def delete_message(channel_id: str, message_id: str):
    """Delete a message from a channel."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            channel = bot.get_channel(int(channel_id))
            if channel is None:
                print(f"Error: Channel {channel_id} not found")
                await bot.close()
                return
            
            message = await channel.fetch_message(int(message_id))
            await message.delete()
            print(f"Deleted message {message_id} from channel {channel_id}")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def kick_user(guild_id: str, user_id: str, reason: str = ""):
    """Kick a user from the guild."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            guild = bot.get_guild(int(guild_id))
            if guild is None:
                guild = await bot.fetch_guild(int(guild_id))
            
            user = await guild.fetch_member(int(user_id))
            if user is None:
                print(f"Error: User {user_id} not found in guild {guild_id}")
                await bot.close()
                return
            
            await user.kick(reason=reason)
            print(f"Kicked user {user.display_name} ({user_id}) from guild {guild_id}")
            if reason:
                print(f"Reason: {reason}")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def ban_user(guild_id: str, user_id: str, reason: str = "", delete_message_days: int = 0):
    """Ban a user from the guild."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            guild = bot.get_guild(int(guild_id))
            if guild is None:
                guild = await bot.fetch_guild(int(guild_id))
            
            user = await guild.fetch_member(int(user_id))
            if user is None:
                print(f"Error: User {user_id} not found in guild {guild_id}")
                await bot.close()
                return
            
            await user.ban(reason=reason, delete_message_days=delete_message_days)
            print(f"Banned user {user.display_name} ({user_id}) from guild {guild_id}")
            if reason:
                print(f"Reason: {reason}")
            if delete_message_days > 0:
                print(f"Deleted messages from last {delete_message_days} days")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def timeout_user(guild_id: str, user_id: str, minutes: int, reason: str = ""):
    """Timeout (mute) a user for specified minutes."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            guild = bot.get_guild(int(guild_id))
            if guild is None:
                guild = await bot.fetch_guild(int(guild_id))
            
            user = await guild.fetch_member(int(user_id))
            if user is None:
                print(f"Error: User {user_id} not found in guild {guild_id}")
                await bot.close()
                return
            
            import datetime
            until = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=minutes)
            await user.timeout(until, reason=reason)
            print(f"Timed out user {user.display_name} ({user_id}) for {minutes} minutes")
            if reason:
                print(f"Reason: {reason}")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def list_roles(guild_id: str):
    """List all roles in a guild."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            guild = bot.get_guild(int(guild_id))
            if guild is None:
                guild = await bot.fetch_guild(int(guild_id))
            
            print(f"Roles in guild {guild_id}:")
            for role in sorted(guild.roles, key=lambda r: r.position, reverse=True):
                members = len([m for m in guild.members if role in m.roles])
                print(f"  - {role.name} (ID: {role.id}, position: {role.position}, members: {members})")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def get_last_message(channel_id: str, limit: int = 5):
    """Get recent messages from a channel."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            channel = bot.get_channel(int(channel_id))
            if channel is None:
                print(f"Error: Channel {channel_id} not found")
                await bot.close()
                return
            
            messages = []
            async for msg in channel.history(limit=limit):
                messages.append(msg)
            
            print(f"Last {len(messages)} messages in channel {channel_id}:")
            for msg in messages:
                print(f"  [{msg.created_at}] {msg.author.name}: {msg.content[:100]}{'...' if len(msg.content) > 100 else ''} (ID: {msg.id})")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def delete_channel(channel_id: str):
    """Delete a channel permanently."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            channel = bot.get_channel(int(channel_id))
            if channel is None:
                print(f"Error: Channel {channel_id} not found")
                await bot.close()
                return
            
            channel_name = channel.name
            await channel.delete()
            print(f"Deleted channel '{channel_name}' (ID: {channel_id})")
        
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

async def add_role(guild_id: str, user_id: str, role_id: str):
    """Add a role to a user."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            guild = bot.get_guild(int(guild_id))
            if guild is None:
                guild = await bot.fetch_guild(int(guild_id))
            
            user = await guild.fetch_member(int(user_id))
            if user is None:
                print(f"Error: User {user_id} not found in guild {guild_id}")
                await bot.close()
                return
            
            role = guild.get_role(int(role_id))
            if role is None:
                print(f"Error: Role {role_id} not found in guild {guild_id}")
                await bot.close()
                return
            
            await user.add_roles(role)
            print(f"Added role '{role.name}' ({role.id}) to user {user.display_name} ({user_id})")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def remove_role(guild_id: str, user_id: str, role_id: str):
    """Remove a role from a user."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            guild = bot.get_guild(int(guild_id))
            if guild is None:
                guild = await bot.fetch_guild(int(guild_id))
            
            user = await guild.fetch_member(int(user_id))
            if user is None:
                print(f"Error: User {user_id} not found in guild {guild_id}")
                await bot.close()
                return
            
            role = guild.get_role(int(role_id))
            if role is None:
                print(f"Error: Role {role_id} not found in guild {guild_id}")
                await bot.close()
                return
            
            await user.remove_roles(role)
            print(f"Removed role '{role.name}' ({role.id}) from user {user.display_name} ({user_id})")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def user_info(guild_id: str, user_id: str):
    """Show detailed information about a user."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            guild = bot.get_guild(int(guild_id))
            if guild is None:
                guild = await bot.fetch_guild(int(guild_id))
            
            user = await guild.fetch_member(int(user_id))
            if user is None:
                print(f"Error: User {user_id} not found in guild {guild_id}")
                await bot.close()
                return
            
            import datetime
            print(f"User: {user.display_name} ({user.id})")
            print(f"  Name: {user.name}#{user.discriminator}")
            print(f"  Nickname: {user.nick}")
            print(f"  Created: {user.created_at}")
            print(f"  Joined: {user.joined_at}")
            print(f"  Status: {user.status}")
            print(f"  Roles ({len(user.roles)}):")
            for role in sorted(user.roles, key=lambda r: r.position, reverse=True):
                if role.name != "@everyone":
                    print(f"    - {role.name} (ID: {role.id}, position: {role.position})")
            print(f"  Top Role: {user.top_role.name}")
            print(f"  Bot: {user.bot}")
            print(f"  Avatar URL: {user.avatar.url if user.avatar else 'None'}")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def create_role(guild_id: str, name: str):
    """Create a new role in a guild."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            guild = bot.get_guild(int(guild_id))
            if guild is None:
                guild = await bot.fetch_guild(int(guild_id))
            
            role = await guild.create_role(name=name)
            print(f"Created role '{role.name}' (ID: {role.id})")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def delete_role(guild_id: str, role_id: str):
    """Delete a role from a guild."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            guild = bot.get_guild(int(guild_id))
            if guild is None:
                guild = await bot.fetch_guild(int(guild_id))
            
            role = guild.get_role(int(role_id))
            if role is None:
                print(f"Error: Role {role_id} not found in guild {guild_id}")
                await bot.close()
                return
            
            await role.delete()
            print(f"Deleted role '{role.name}' ({role.id})")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def purge_channel(channel_id: str, limit: int = 100):
    """Delete the last N messages from a channel."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            channel = bot.get_channel(int(channel_id))
            if channel is None:
                print(f"Error: Channel {channel_id} not found")
                await bot.close()
                return
            
            deleted = await channel.purge(limit=limit)
            print(f"Purged {len(deleted)} messages from channel {channel_id}")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def find_user(guild_id: str, query: str):
    """Search for users by name or nickname."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            guild = bot.get_guild(int(guild_id))
            if guild is None:
                guild = await bot.fetch_guild(int(guild_id))
            
            members = await guild.query_members(query, limit=10)
            if not members:
                print(f"No users found matching '{query}'")
                await bot.close()
                return
            
            print(f"Users matching '{query}':")
            for member in members:
                roles_str = ', '.join([r.name for r in member.roles if r.name != '@everyone'])
                print(f"  - {member.display_name} ({member.name}#{member.discriminator}, ID: {member.id})")
                if member.nick:
                    print(f"    Nickname: {member.nick}")
                if roles_str:
                    print(f"    Roles: {roles_str}")
                print(f"    Joined: {member.joined_at}")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def lock_channel(channel_id: str):
    """Lock a text channel by denying @everyone send messages."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            channel = bot.get_channel(int(channel_id))
            if channel is None:
                print(f"Error: Channel {channel_id} not found")
                await bot.close()
                return
            
            # Get @everyone role
            everyone = channel.guild.default_role
            overwrite = channel.overwrites_for(everyone)
            overwrite.send_messages = False
            await channel.set_permissions(everyone, overwrite=overwrite)
            print(f"Locked channel {channel_id} (@everyone cannot send messages)")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def unlock_channel(channel_id: str):
    """Unlock a text channel by resetting @everyone send messages."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            channel = bot.get_channel(int(channel_id))
            if channel is None:
                print(f"Error: Channel {channel_id} not found")
                await bot.close()
                return
            
            # Get @everyone role
            everyone = channel.guild.default_role
            overwrite = channel.overwrites_for(everyone)
            overwrite.send_messages = None  # Reset to default
            await channel.set_permissions(everyone, overwrite=overwrite)
            print(f"Unlocked channel {channel_id} (@everyone send messages reset to default)")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.close()
    
    await bot.start(TOKEN)

async def change_nickname(guild_id: str, user_id: str, nickname: str):
    """Change a user's nickname."""
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        try:
            guild = bot.get_guild(int(guild_id))
            if guild is None:
                guild = await bot.fetch_guild(int(guild_id))
            
            user = await guild.fetch_member(int(user_id))
            if user is None:
                print(f"Error: User {user_id} not found in guild {guild_id}")
                await bot.close()
                return
            
            await user.edit(nick=nickname)
            print(f"Changed nickname for {user.display_name} ({user_id}) to '{nickname}'")
        
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
        print("  python discord_cli_simple.py delete_message 1467357084843507782 1234567890123456789")
        print("  python discord_cli_simple.py get_last_message 1482137267224186980")
        print("  python discord_cli_simple.py kick 1467329846265909446 123456789012345678 \"Spam\"")
        print("  python discord_cli_simple.py ban 1467329846265909446 123456789012345678 \"Spam\" 7")
        print("  python discord_cli_simple.py timeout 1467329846265909446 123456789012345678 60 \"Rude behavior\"")
        print("  python discord_cli_simple.py list_roles 1467329846265909446")
        print("  python discord_cli_simple.py create_role 1467329846265909446 Moderator")
        print("  python discord_cli_simple.py delete_role 1467329846265909446 1234567890123456789")
        print("  python discord_cli_simple.py add_role 1467329846265909446 659118969445416961 1467364553154236500")
        print("  python discord_cli_simple.py remove_role 1467329846265909446 659118969445416961 1467364553154236500")
        print("  python discord_cli_simple.py user_info 1467329846265909446 659118969445416961")
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
        
        elif command == "delete_channel":
            if len(sys.argv) != 3:
                print("Usage: python discord_cli_simple.py delete_channel <channel_id>")
                sys.exit(1)
            asyncio.run(delete_channel(sys.argv[2]))
        
        elif command == "send_message":
            if len(sys.argv) != 4:
                print("Usage: python discord_cli_simple.py send_message <channel_id> <content>")
                sys.exit(1)
            asyncio.run(send_message(sys.argv[2], sys.argv[3]))

        elif command == "delete_message":
            if len(sys.argv) != 4:
                print("Usage: python discord_cli_simple.py delete_message <channel_id> <message_id>")
                sys.exit(1)
            asyncio.run(delete_message(sys.argv[2], sys.argv[3]))
        
        elif command == "kick":
            if len(sys.argv) < 4:
                print("Usage: python discord_cli_simple.py kick <guild_id> <user_id> [reason]")
                sys.exit(1)
            reason = sys.argv[4] if len(sys.argv) >= 5 else ""
            asyncio.run(kick_user(sys.argv[2], sys.argv[3], reason))
        
        elif command == "ban":
            if len(sys.argv) < 4:
                print("Usage: python discord_cli_simple.py ban <guild_id> <user_id> [reason] [delete_message_days]")
                sys.exit(1)
            reason = sys.argv[4] if len(sys.argv) >= 5 else ""
            delete_days = int(sys.argv[5]) if len(sys.argv) >= 6 else 0
            asyncio.run(ban_user(sys.argv[2], sys.argv[3], reason, delete_days))
        
        elif command == "timeout":
            if len(sys.argv) < 5:
                print("Usage: python discord_cli_simple.py timeout <guild_id> <user_id> <minutes> [reason]")
                sys.exit(1)
            minutes = int(sys.argv[4])
            reason = sys.argv[5] if len(sys.argv) >= 6 else ""
            asyncio.run(timeout_user(sys.argv[2], sys.argv[3], minutes, reason))
        
        elif command == "list_roles":
            if len(sys.argv) != 3:
                print("Usage: python discord_cli_simple.py list_roles <guild_id>")
                sys.exit(1)
            asyncio.run(list_roles(sys.argv[2]))
        
        elif command == "add_role":
            if len(sys.argv) != 5:
                print("Usage: python discord_cli_simple.py add_role <guild_id> <user_id> <role_id>")
                sys.exit(1)
            asyncio.run(add_role(sys.argv[2], sys.argv[3], sys.argv[4]))
        
        elif command == "remove_role":
            if len(sys.argv) != 5:
                print("Usage: python discord_cli_simple.py remove_role <guild_id> <user_id> <role_id>")
                sys.exit(1)
            asyncio.run(remove_role(sys.argv[2], sys.argv[3], sys.argv[4]))
        
        elif command == "user_info":
            if len(sys.argv) != 4:
                print("Usage: python discord_cli_simple.py user_info <guild_id> <user_id>")
                sys.exit(1)
            asyncio.run(user_info(sys.argv[2], sys.argv[3]))
        
        elif command == "create_role":
            if len(sys.argv) != 4:
                print("Usage: python discord_cli_simple.py create_role <guild_id> <name>")
                sys.exit(1)
            asyncio.run(create_role(sys.argv[2], sys.argv[3]))
        
        elif command == "delete_role":
            if len(sys.argv) != 4:
                print("Usage: python discord_cli_simple.py delete_role <guild_id> <role_id>")
                sys.exit(1)
            asyncio.run(delete_role(sys.argv[2], sys.argv[3]))
        
        elif command == "purge_channel":
            if len(sys.argv) != 4:
                print("Usage: python discord_cli_simple.py purge_channel <channel_id> <limit>")
                sys.exit(1)
            asyncio.run(purge_channel(sys.argv[2], int(sys.argv[3])))
        
        elif command == "find_user":
            if len(sys.argv) != 4:
                print("Usage: python discord_cli_simple.py find_user <guild_id> <query>")
                sys.exit(1)
            asyncio.run(find_user(sys.argv[2], sys.argv[3]))
        
        elif command == "lock_channel":
            if len(sys.argv) != 3:
                print("Usage: python discord_cli_simple.py lock_channel <channel_id>")
                sys.exit(1)
            asyncio.run(lock_channel(sys.argv[2]))
        
        elif command == "unlock_channel":
            if len(sys.argv) != 3:
                print("Usage: python discord_cli_simple.py unlock_channel <channel_id>")
                sys.exit(1)
            asyncio.run(unlock_channel(sys.argv[2]))
        
        elif command == "change_nickname":
            if len(sys.argv) != 5:
                print("Usage: python discord_cli_simple.py change_nickname <guild_id> <user_id> <nickname>")
                sys.exit(1)
            asyncio.run(change_nickname(sys.argv[2], sys.argv[3], sys.argv[4]))
        
        elif command == "get_last_message":
            if len(sys.argv) != 4:
                print("Usage: python discord_cli_simple.py get_last_message <channel_id> [limit]")
                sys.exit(1)
            limit = int(sys.argv[3]) if len(sys.argv) >= 4 else 5
            asyncio.run(get_last_message(sys.argv[2], limit))
        
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