# discord-cli

> A system-wide Discord bot interface for OpenClaw agents and automation.

**discord-cli** provides a safe, documented CLI for Discord operations (send messages, manage channels, threads, roles, etc.) designed for integration with OpenClaw agents and automation workflows.

## Features

- 🚀 **System-wide installation** — Install once, use anywhere
- 📖 **Agent-focused documentation** — Extensive docs for AI agent integration
- 🛡️ **Rate limiting aware** — Built-in guidelines to prevent bot bans
- 📝 **Error handling patterns** — Documented error handling for reliable automation
- 🔒 **Token management** — Centralized Discord bot token (single source of truth)
- 🧪 **Channel management** — Create, delete, rename, move channels and categories
- 💬 **Message operations** — Send, edit, delete messages, add reactions
- 🧵 **Thread support** — Create and manage Discord threads
- 👥 **Role management** — Assign and remove Discord roles
- 📊 **Webhook support** — Create and manage webhooks for external services

## Installation

### Prerequisites

- Python 3.12+ 
- `discord.py` library (>=2.0.0)
- Discord bot token with required permissions

### Quick Install

```bash
# Clone the repo
git clone https://github.com/iAmChumby/discord-cli.git
cd discord-cli

# Copy to system-wide location
sudo cp discord_cli.py /usr/local/bin/discord-cli
sudo chmod +x /usr/local/bin/discord-cli

# Or install to user bin (recommended)
cp discord_cli.py ~/.local/bin/discord-cli
chmod +x ~/.local/bin/discord-cli
```

### Via pip (future)

```bash
pip install discord-cli
```

## Quick Start

```bash
# List all channels in a guild
discord-cli list_channels <guild_id>

# Send a message
discord-cli send_message <channel_id> "Hello from discord-cli!"

# Create a new channel
discord-cli create_channel <guild_id> <category_id> "new-channel"

# Get channel ID by name
discord-cli get_channel_id <guild_id> "general"
```

## Documentation

- **[Full Agent Integration Guide](docs/AGENT_INTEGRATION.md)** — Comprehensive guide for AI agents
- **[Quick Reference](docs/QUICK_REFERENCE.md)** — Command cheat sheet
- **[API Reference](docs/API_REFERENCE.md)** — Detailed parameter documentation

## Usage by Agents

### Example: Heartbeat Reporter

```python
import subprocess

# Agent sends a heartbeat report
result = subprocess.run(
    ["discord-cli", "send_message", heartbeats_channel_id, "All systems operational"],
    capture_output=True,
    text=True,
    timeout=30
)

if result.returncode != 0:
    # Handle error (see docs for patterns)
    log_error(result.stderr)
```

### Example: Channel Management

```python
# Agent creates a status channel
result = subprocess.run(
    ["discord-cli", "create_channel", guild_id, category_id, "agent-status"],
    capture_output=True,
    text=True
)

# Extract channel ID from output
if "Created channel" in result.stdout:
    channel_id = result.stdout.split("(ID: ")[1].split(")")[0]
```

### Example: Rate Limiting

```python
import time

# Agent sends multiple messages with delays
messages = ["Report 1", "Report 2", "Report 3"]
for msg in messages:
    subprocess.run(["discord-cli", "send_message", channel_id, msg])
    time.sleep(1)  # Respect rate limits
```

## Commands

### Channel Management

| Command | Description | Example |
|---------|-------------|---------|
| `list_channels <guild_id>` | List all channels | `discord-cli list_channels 1467329846265909446` |
| `create_channel <guild_id> <category_id> <name>` | Create text channel | `discord-cli create_channel 1467329846265909446 1467364905383628852 test-channel` |
| `delete_channel <channel_id>` | Delete a channel | `discord-cli delete_channel 1482113021592735887` |
| `rename_channel <channel_id> <name>` | Rename channel | `discord-cli rename_channel 1482113021592735887 heartbeats-v2` |
| `move_channel <channel_id> <category_id>` | Move to category | `discord-cli move_channel 1482113021592735887 1467364905383628852` |
| `set_slowmode <channel_id> <seconds>` | Set slowmode | `discord-cli set_slowmode 1482113021592735887 5` |
| `set_channel_topic <channel_id> <topic>` | Set topic | `discord-cli set_channel_topic 1482113021592735887 "Automated heartbeat reports"` |

### Message Management

| Command | Description | Example |
|---------|-------------|---------|
| `send_message <channel_id> <content>` | Send message | `discord-cli send_message 1482113021592735887 "Hello!"` |
| `edit_message <channel_id> <message_id> <content>` | Edit message | `discord-cli edit_message 1482113021592735887 123456789 "Updated"` |
| `delete_message <channel_id> <message_id>` | Delete message | `discord-cli delete_message 1482113021592735887 123456789` |
| `react_message <channel_id> <message_id> <emoji>` | Add reaction | `discord-cli react_message 1482113021592735887 123456789 ✅` |
| `pin_message <channel_id> <message_id>` | Pin message | `discord-cli pin_message 1482113021592735887 123456789` |
| `get_messages <channel_id> <limit>` | Get history | `discord-cli get_messages 1482113021592735887 50` |

### Thread Management

| Command | Description | Example |
|---------|-------------|---------|
| `create_thread <channel_id> <title> <message_id>` | Create thread | `discord-cli create_thread 1482113021592735887 "Discussion" 123456789` |
| `send_to_thread <thread_id> <content>` | Reply in thread | `discord-cli send_to_thread 123456789 "Reply"` |
| `list_threads <channel_id>` | List threads | `discord-cli list_threads 1482113021592735887` |

### Category Management

| Command | Description | Example |
|---------|-------------|---------|
| `create_category <guild_id> <name> <position>` | Create category | `discord-cli create_category 1467329846265909446 "Reports" 1` |
| `list_categories <guild_id>` | List categories | `discord-cli list_categories 1467329846265909446` |
| `delete_category <category_id>` | Delete category | `discord-cli delete_category 1467364905383628852` |

### Role Management

| Command | Description | Example |
|---------|-------------|---------|
| `list_roles <guild_id>` | List roles | `discord-cli list_roles 1467329846265909446` |
| `create_role <guild_id> <name> <color>` | Create role | `discord-cli create_role 1467329846265909446 "Bot" #3498db` |
| `assign_role <user_id> <role_id>` | Assign role | `discord-cli assign_role 123456789 987654321` |
| `remove_role <user_id> <role_id>` | Remove role | `discord-cli remove_role 123456789 987654321` |

### Guild Management

| Command | Description | Example |
|---------|-------------|---------|
| `get_guild_info <guild_id>` | Get guild info | `discord-cli get_guild_info 1467329846265909446` |
| `list_guilds` | List all guilds | `discord-cli list_guilds` |

### Emoji Management

| Command | Description | Example |
|---------|-------------|---------|
| `list_emojis` | List custom emojis | `discord-cli list_emojis` |
| `create_emoji <name> <image_url>` | Create emoji | `discord-cli create_emoji status https://example.com/status.png` |

### Webhook Management

| Command | Description | Example |
|---------|-------------|---------|
| `create_webhook <channel_id> <name>` | Create webhook | `discord-cli create_webhook 1482113021592735887 alerts` |
| `delete_webhook <webhook_url>` | Delete webhook | `discord-cli delete_webhook https://discord.com/api/webhooks/...` |

## Error Handling

All commands follow this pattern:

- **Success:** Prints result/confirmation
- **Error:** Prints `Error: <reason>` and exits with code 1

Agents should:

1. Capture stderr/stdout for parsing
2. Check exit code (non-zero = failure)
3. Retry on transient errors (rate limits, network issues)
4. Log errors for debugging

### Example Error Handling

```python
import subprocess
import time

def send_with_retry(channel_id: str, content: str, max_retries: int = 3):
    for attempt in range(max_retries):
        result = subprocess.run(
            ["discord-cli", "send_message", channel_id, content],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return True
        
        # Check for rate limit error
        if "rate limit" in result.stderr.lower():
            time.sleep(30 * (attempt + 1))  # Exponential backoff
            continue
        
        # Log and retry
        print(f"Attempt {attempt + 1} failed: {result.stderr}")
    
    return False
```

## Rate Limiting Guidelines

**Discord Rate Limits:**

- Message sending: ~5 messages per second per guild
- Channel creation: ~5 channels per guild per 5 minutes
- Thread creation: ~5 threads per channel per minute
- Role updates: ~5 role changes per guild per hour

**Agent Best Practices:**

- Add 1-second delay between bulk operations
- Use `list_channels` to cache channel IDs (don't call per operation)
- For frequent reports (heartbeats), send consolidated messages
- Respect channel cooldowns after creation (2-3 seconds before using)
- Use exponential backoff on errors

## Permissions Required

The Discord bot must have these permissions:

- **View Channels** — `list_channels`, `get_channel_id`, `get_messages`
- **Manage Channels** — `create_channel`, `delete_channel`, `rename_channel`, `move_channel`, `set_slowmode`
- **Send Messages** — `send_message`, `edit_message`, `delete_message`, `react_message`
- **Manage Threads** — `create_thread`, `send_to_thread`, `list_threads`
- **Manage Roles** — `create_role`, `assign_role`, `remove_role`
- **Manage Webhooks** — `create_webhook`, `delete_webhook`

## Configuration

The Discord bot token is stored in the source file (`discord_cli.py`):

```python
TOKEN = "YOUR_BOT_TOKEN_HERE"
```

**For security:**

- Never commit the actual token to Git
- Use environment variables (future version will support `DISCORD_BOT_TOKEN`)
- Restrict token scope to only needed permissions
- Rotate tokens periodically

## Testing

```bash
# Verify installation
discord-cli list_guilds

# Test message sending
discord-cli send_message <test_channel_id> "Test from discord-cli"

# Test channel creation
discord-cli create_channel <guild_id> <category_id> test-channel
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Created by Luke Edwards (@iAmChumby)
- Built for OpenClaw agent ecosystem
- Inspired by need for safe, documented Discord automation

## Support

For issues or questions:

1. Check the [documentation](docs/)
2. Search existing [GitHub issues](https://github.com/iAmChumby/discord-cli/issues)
3. Open a new issue with detailed information

## Roadmap

- [ ] Environment variable support for token
- [ ] PyPI package installation
- [ ] Configuration file support
- [ ] Async API for direct Python integration
- [ ] Web dashboard for monitoring
- [ ] Plugin system for custom commands
