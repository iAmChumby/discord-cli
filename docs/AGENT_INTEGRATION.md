# Discord CLI - Agent Documentation

**Purpose:** System-wide Discord bot interface for OpenClaw agents. Provides safe, documented access to Discord operations (send messages, list channels, create channels, etc.).

**Location:** `~/.local/bin/discord-cli` (executable, system-wide)

**Usage by Agents:** Agents should use `discord-cli` for Discord operations instead of calling Discord API directly. This ensures consistent error handling, rate limiting awareness, and future maintainability.

---

## Available Commands

### 1. `list_channels <guild_id>`
List all channels in a Discord guild (server).

**Parameters:**
- `guild_id` (string) - Discord guild ID (required)

**Returns:** Prints each channel with:
- Channel name
- Channel ID
- Channel type (text, voice, category, or unknown)

**Example:**
```bash
discord-cli list_channels 1467329846265909446
```

**Agent Usage Pattern:**
```python
# When an agent needs to find a channel ID or verify a channel exists
channels_output = exec.run(["discord-cli", "list_channels", guild_id])
# Parse output to find target channel
```

---

### 2. `create_channel <guild_id> <category_id> <name>`
Create a new text channel in a specific category.

**Parameters:**
- `guild_id` (string) - Discord guild ID (required)
- `category_id` (string) - Category ID to place channel under (required)
- `name` (string) - Channel name (required, no spaces recommended)

**Returns:** Prints created channel ID on success.

**Example:**
```bash
discord-cli create_channel 1467329846265909446 1467364905383628852 test-channel
```

**Agent Usage Pattern:**
```python
# When an agent needs to create a channel for automation
result = exec.run(["discord-cli", "create_channel", guild_id, category_id, channel_name])
# Extract channel ID from output: "Created channel 'test-channel' (ID: 123456789)"
```

**Important:**
- Channel names should be lowercase, hyphenated (e.g., `heartbeats` not `Heartbeats`)
- Category must exist; agent should verify category ID first via `list_channels`
- Bot must have MANAGE_CHANNELS permission

---

### 3. `send_message <channel_id> <content>`
Send a message to a Discord channel.

**Parameters:**
- `channel_id` (string) - Discord channel ID (required)
- `content` (string) - Message content (required)

**Returns:** Prints confirmation on success.

**Example:**
```bash
discord-cli send_message 1482113021592735887 "Heartbeat report: All systems operational"
```

**Agent Usage Pattern:**
```python
# When an agent needs to report status, send alerts, or communicate
exec.run(["discord-cli", "send_message", channel_id, message_content])
```

**Important:**
- Messages longer than 2000 characters will fail silently
- Bot must have SEND_MESSAGES permission
- Consider message formatting: Discord supports Markdown
- Rate limiting: Agent should not send more than 5 messages per minute without delays

---

### 4. `get_channel_id <guild_id> <channel_name>`
Get a channel's ID by its name.

**Parameters:**
- `guild_id` (string) - Discord guild ID (required)
- `channel_name` (string) - Exact channel name (case-sensitive) (required)

**Returns:** Prints channel ID on success, error message if not found.

**Example:**
```bash
discord-cli get_channel_id 1467329846265909446 general
```

**Agent Usage Pattern:**
```python
# When an agent knows the channel name but needs the ID for API calls
result = exec.run(["discord-cli", "get_channel_id", guild_id, "general"])
# Parse output: "Channel 'general' ID: 1467329847201370124"
```

**Important:**
- Channel name is case-sensitive (General != general)
- If channel name has spaces, it must be quoted: `"general chat"`
- Returns None on failure; agent should handle gracefully

---

## Common IDs Reference

**Known Guild ID:** `1467329846265909446` (Main development server)

**Known Categories:**
- `🤖 OPENCLAW` (ID: `1467364905383628852`) - Agent automation channels
- `🧪 EXPERIMENTS` (ID: `14673649062266841112`) - Experimental features
- Text Channels (ID: `1467329847201370122`) - General channels

**Known Channels:**
- `heartbeats` (ID: `1482113021592735887`) - Automated heartbeat reports
- `general` (ID: `1467329847201370124`) - General discussion

---

## Error Handling

**All commands follow this pattern:**
- On success: Print result/confirmation
- On error: Print `Error: <reason>` and exit with code 1

**Agents should:**
1. Capture stderr/stdout for parsing
2. Check exit code (non-zero = failure)
3. Retry on transient errors (rate limits, network issues)
4. Log errors for debugging

**Example Error Handling (pseudo):**
```python
import subprocess

try:
    result = subprocess.run(
        ["discord-cli", "send_message", channel_id, content],
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode != 0:
        # Parse error from stderr/stdout
        if "Error:" in result.stderr or "Error:" in result.stdout:
            # Handle known error
            pass
        else:
            # Unknown error, log and retry
            pass
except subprocess.TimeoutExpired:
    # Timeout, retry
    pass
```

---

## Rate Limiting Guidelines

**Discord Rate Limits:**
- Message sending: ~5 messages per second per guild
- Channel creation: ~5 channels per guild per 5 minutes

**Agent Best Practices:**
- Add 1-second delay between bulk operations
- Use `list_channels` to cache channel IDs; don't call per operation
- For frequent reports (heartbeats), send consolidated messages rather than many small ones
- Respect channel cooldowns after creation (2-3 seconds before using)

---

## Permissions Required

The Discord bot token (stored in `~/.local/bin/discord-cli`) has the following permissions:

**Guild Permissions:**
- View Channels (allows `list_channels`, `get_channel_id`)
- Manage Channels (allows `create_channel`)
- Send Messages (allows `send_message`)
- Read Message History (for future features)

**If bot lacks permission, agent will receive `Error:` response.**

---

## Testing Your Integration

**Before deploying to production:**

1. **Verify guild ID is correct**
   ```bash
   discord-cli list_channels <your_guild_id>
   ```

2. **Test message sending**
   ```bash
   discord-cli send_message <test_channel_id> "Test message from agent"
   ```

3. **Test channel creation** (in test category)
   ```bash
   discord-cli create_channel <guild_id> <test_category_id> agent-test-channel
   ```

4. **Verify output parsing** - Agent should correctly parse CLI output format

---

## Troubleshooting

**Error: "Error: Channel 'name' not found"**
- Channel name is case-sensitive
- Channel may be in a different guild
- Bot may not have View Channels permission

**Error: "Error:" with no message**
- Bot token may be invalid or expired
- Network connectivity issue (retry with backoff)
- Rate limit hit (wait 30 seconds and retry)

**Error: "Error: HTTP 403 Forbidden"**
- Bot lacks required permission for that operation
- Token has incorrect scope
- Channel is in a private/archived server bot cannot access

---

## Version History

**v1.0.0** (2026-03-13) - Initial release
- Core commands: list_channels, create_channel, send_message, get_channel_id
- Extensive documentation for agent integration
- Tested with OpenClaw agent ecosystem

---

## Maintenance

**To update the CLI:**
1. Edit source at `/home/chumby/.openclaw/workspace/discord_cli_simple.py`
2. Copy to `~/.local/bin/discord-cli`
3. Update this documentation
4. Test with `discord-cli list_channels <test_guild>`

**To add new commands:**
1. Add function to source following existing patterns
2. Add command handling in `main()`
3. Document in this file
4. Add to CLI's help text

---

## Support

For issues with the Discord CLI:
1. Check Discord bot status via Discord Developer Portal
2. Verify bot token has required permissions
3. Test with manual CLI execution before agent use
4. Check OpenClaw logs for detailed error traces

**Source:** `/home/chumby/.openclaw/workspace/discord_cli_simple.py`  
**Bot Token Location:** Source file (do not expose token in logs)  
**Documentation:** `~/docs/discord-cli.md` (this file)
