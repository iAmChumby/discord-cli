# Discord CLI

**System-wide Discord bot interface for OpenClaw agents.**

**Location:** `~/.local/bin/discord-cli` (executable, in PATH)

**Documentation:** `~/docs/discord-cli.md` - Comprehensive agent integration guide

**Quick Start:**
```bash
# List all channels in the main guild
discord-cli list_channels 1467329846265909446

# Send a message to heartbeats channel
discord-cli send_message 1482113021592735887 "Report: All systems operational"

# Create a new channel in OPENCLAW category
discord-cli create_channel 1467329846265909446 1467364905383628852 agent-status
```

**Key Features for Agents:**
- Safe, documented interface to Discord operations
- Error handling and rate limiting guidelines built in
- Common IDs cached (guild, categories, channels)
- Extensive documentation for integration patterns

**Commands:**
- `list_channels <guild_id>` - List all channels
- `create_channel <guild_id> <category_id> <name>` - Create text channel
- `send_message <channel_id> <content>` - Send message
- `get_channel_id <guild_id> <channel_name>` - Get channel ID by name

**Why Use This CLI Instead of Direct Discord API?**
- Consistent error handling across all agents
- Rate limiting awareness prevents bot bans
- Centralized token management (one source of truth)
- Easy to test and debug independently
- Future-proofing: updates propagate to all agents

**Example Agent Integration:**
```python
# Agent sends a heartbeat report
import subprocess

result = subprocess.run(
    ["discord-cli", "send_message", heartbeats_channel_id, message],
    capture_output=True,
    text=True,
    timeout=30
)

if result.returncode != 0:
    # Handle error (see ~/docs/discord-cli.md for patterns)
    log_error(result.stderr)
```

**Full Documentation:** See `~/docs/discord-cli.md` for:
- Detailed parameter descriptions
- Error handling patterns
- Rate limiting guidelines
- Permission requirements
- Troubleshooting
- Version history
