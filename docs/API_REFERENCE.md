# discord-cli API Reference

Complete parameter documentation for all discord-cli commands.

---

## Channel Management Commands

### list_channels <guild_id>

Lists all channels in a Discord guild (server).

**Parameters:**
- `guild_id` (string, required) — Discord guild ID

**Returns:** Prints each channel with:
- Channel name
- Channel ID
- Channel type (text, voice, category, or unknown)

**Error Cases:**
- Bot lacks View Channels permission
- Guild ID is invalid
- Bot is not in the guild

**Example Output:**
```
Channels in guild 1467329846265909446:
  - general (ID: 1467329847201370124, type: text)
  - Voice Channels (ID: 1467329847201370123, type: voice)
  - OPENCLAW (ID: 1467364905383628852, type: category)
```

---

### create_channel <guild_id> <category_id> <name>

Creates a new text channel in a specific category.

**Parameters:**
- `guild_id` (string, required) — Discord guild ID
- `category_id` (string, required) — Category ID to place channel under
- `name` (string, required) — Channel name (lowercase, hyphenated recommended)

**Returns:** Prints created channel ID on success.

**Error Cases:**
- Bot lacks Manage Channels permission
- Category ID is invalid or bot lacks permission
- Channel name contains invalid characters
- Rate limit hit (5 channels/guild/5 minutes)

**Example Output:**
```
Created channel 'test-channel' (ID: 1482126965224902686)
```

---

### delete_channel <channel_id>

Deletes a Discord channel.

**Parameters:**
- `channel_id` (string, required) — Discord channel ID

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Manage Channels permission
- Channel ID is invalid
- Bot lacks permission for that channel

**Example Output:**
```
Deleted channel 1482126965224902686
```

---

### rename_channel <channel_id> <name>

Renames a Discord channel.

**Parameters:**
- `channel_id` (string, required) — Discord channel ID
- `name` (string, required) — New channel name

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Manage Channels permission
- Channel ID is invalid
- Rate limit hit (2 channel renames/guild/10 minutes)

**Example Output:**
```
Renamed channel 1482126965224902686 to 'new-name'
```

---

### move_channel <channel_id> <category_id>

Moves a channel to a different category.

**Parameters:**
- `channel_id` (string, required) — Discord channel ID
- `category_id` (string, required) — Target category ID

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Manage Channels permission
- Category ID is invalid
- Channel ID is invalid

**Example Output:**
```
Moved channel 1482126965224902686 to category 1467364905383628852
```

---

### set_slowmode <channel_id> <seconds>

Sets slowmode on a channel (users can only send one message every N seconds).

**Parameters:**
- `channel_id` (string, required) — Discord channel ID
- `seconds` (int, required) — Slowmode duration (0 to 21600 seconds)

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Manage Channels permission
- Channel ID is invalid
- Seconds out of range (0-21600)

**Example Output:**
```
Set slowmode on channel 1482126965224902686 to 5 seconds
```

---

### set_channel_topic <channel_id> <topic>

Sets the topic (description) of a channel.

**Parameters:**
- `channel_id` (string, required) — Discord channel ID
- `topic` (string, required) — Channel topic (max 1024 characters)

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Manage Channels permission
- Channel ID is invalid
- Topic exceeds 1024 characters

**Example Output:**
```
Set topic for channel 1482126965224902686
```

---

## Message Management Commands

### send_message <channel_id> <content>

Sends a message to a Discord channel.

**Parameters:**
- `channel_id` (string, required) — Discord channel ID
- `content` (string, required) — Message content (max 2000 characters, supports Markdown)

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Send Messages permission
- Channel ID is invalid
- Content exceeds 2000 characters
- Rate limit hit (~5 messages/second/guild)

**Example Output:**
```
Message sent to channel 1482126965224902686: Hello from discord-cli!
```

---

### edit_message <channel_id> <message_id> <content>

Edits an existing message.

**Parameters:**
- `channel_id` (string, required) — Discord channel ID
- `message_id` (string, required) — Discord message ID
- `content` (string, required) — New message content (max 2000 characters)

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Manage Messages permission
- Channel ID or message ID is invalid
- Not the message author
- Rate limit hit

**Example Output:**
```
Edited message 123456789 in channel 1482126965224902686
```

---

### delete_message <channel_id> <message_id>

Deletes a message.

**Parameters:**
- `channel_id` (string, required) — Discord channel ID
- `message_id` (string, required) — Discord message ID

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Manage Messages permission
- Channel ID or message ID is invalid
- Not the message author or message too old (>14 days)

**Example Output:**
```
Deleted message 123456789 from channel 1482126965224902686
```

---

### react_message <channel_id> <message_id> <emoji>

Adds a reaction to a message.

**Parameters:**
- `channel_id` (string, required) — Discord channel ID
- `message_id` (string, required) — Discord message ID
- `emoji` (string, required) — Emoji (Unicode or custom emoji name)

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Add Reactions permission
- Channel ID or message ID is invalid
- Emoji is invalid

**Example Output:**
```
Added reaction ✅ to message 123456789
```

---

### pin_message <channel_id> <message_id>

Pins a message to the channel.

**Parameters:**
- `channel_id` (string, required) — Discord channel ID
- `message_id` (string, required) — Discord message ID

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Manage Messages permission
- Channel ID or message ID is invalid
- Already pinned (50 pinned max per channel)

**Example Output:**
```
Pinned message 123456789 to channel 1482126965224902686
```

---

### get_messages <channel_id> <limit>

Retrieves message history from a channel.

**Parameters:**
- `channel_id` (string, required) — Discord channel ID
- `limit` (int, optional) — Number of messages to retrieve (default 50, max 100)

**Returns:** Prints each message with ID, author, content, and timestamp.

**Error Cases:**
- Bot lacks Read Message History permission
- Channel ID is invalid
- Rate limit hit

**Example Output:**
```
Messages in channel 1482126965224902686:
  - ID: 123456789, Author: Luke#1234, Content: Hello, Time: 2026-03-13T17:00:00.000Z
  - ID: 123456790, Author: Bot#5678, Content: World, Time: 2026-03-13T17:01:00.000Z
```

---

## Thread Management Commands

### create_thread <channel_id> <title> <message_id>

Creates a thread from an existing message.

**Parameters:**
- `channel_id` (string, required) — Discord channel ID
- `title` (string, required) — Thread title (max 100 characters)
- `message_id` (string, required) — Discord message ID to start thread from

**Returns:** Prints created thread ID on success.

**Error Cases:**
- Bot lacks Create Public Threads permission
- Channel ID or message ID is invalid
- Rate limit hit (~5 threads/channel/minute)

**Example Output:**
```
Created thread 'Discussion' (ID: 123456791)
```

---

### send_to_thread <thread_id> <content>

Sends a message to a thread.

**Parameters:**
- `thread_id` (string, required) — Discord thread ID
- `content` (string, required) — Message content (max 2000 characters)

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Send Messages in Threads permission
- Thread ID is invalid
- Thread is archived

**Example Output:**
```
Sent message to thread 123456791
```

---

### list_threads <channel_id>

Lists all threads in a channel.

**Parameters:**
- `channel_id` (string, required) — Discord channel ID

**Returns:** Prints each thread with ID, title, and message count.

**Error Cases:**
- Bot lacks Read Message History permission
- Channel ID is invalid

**Example Output:**
```
Threads in channel 1482126965224902686:
  - ID: 123456791, Title: Discussion, Messages: 5
  - ID: 123456792, Title: Help, Messages: 2
```

---

## Category Management Commands

### create_category <guild_id> <name> <position>

Creates a new category.

**Parameters:**
- `guild_id` (string, required) — Discord guild ID
- `name` (string, required) — Category name (max 100 characters)
- `position` (int, optional) — Sort position (default 0)

**Returns:** Prints created category ID on success.

**Error Cases:**
- Bot lacks Manage Channels permission
- Guild ID is invalid
- Category name contains invalid characters

**Example Output:**
```
Created category 'Reports' (ID: 1467364906226684112)
```

---

### list_categories <guild_id>

Lists all categories in a guild.

**Parameters:**
- `guild_id` (string, required) — Discord guild ID

**Returns:** Prints each category with ID, name, and position.

**Error Cases:**
- Bot lacks View Channels permission
- Guild ID is invalid

**Example Output:**
```
Categories in guild 1467329846265909446:
  - ID: 1467364905383628852, Name: OPENCLAW, Position: 1
  - ID: 1467364906226684112, Name: EXPERIMENTS, Position: 2
```

---

### delete_category <category_id>

Deletes a category.

**Parameters:**
- `category_id` (string, required) — Discord category ID

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Manage Channels permission
- Category ID is invalid
- Category contains channels (must delete channels first)

**Example Output:**
```
Deleted category 1467364906226684112
```

---

## Role Management Commands

### list_roles <guild_id>

Lists all roles in a guild.

**Parameters:**
- `guild_id` (string, required) — Discord guild ID

**Returns:** Prints each role with ID, name, and color.

**Error Cases:**
- Bot lacks View Channels permission
- Guild ID is invalid

**Example Output:**
```
Roles in guild 1467329846265909446:
  - ID: 987654321, Name: @everyone, Color: #000000
  - ID: 987654322, Name: Admin, Color: #e91e63
```

---

### create_role <guild_id> <name> <color>

Creates a new role.

**Parameters:**
- `guild_id` (string, required) — Discord guild ID
- `name` (string, required) — Role name (max 100 characters)
- `color` (string, optional) — Role color in hex (#RRGGBB, default #000000)

**Returns:** Prints created role ID on success.

**Error Cases:**
- Bot lacks Manage Roles permission
- Guild ID is invalid
- Role name contains invalid characters
- Rate limit hit (~5 roles/guild/hour)

**Example Output:**
```
Created role 'Bot' (ID: 987654323)
```

---

### assign_role <user_id> <role_id>

Assigns a role to a user.

**Parameters:**
- `user_id` (string, required) — Discord user ID
- `role_id` (string, required) — Discord role ID

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Manage Roles permission
- User ID or role ID is invalid
- Role is already assigned

**Example Output:**
```
Assigned role 987654323 to user 123456789
```

---

### remove_role <user_id> <role_id>

Removes a role from a user.

**Parameters:**
- `user_id` (string, required) — Discord user ID
- `role_id` (string, required) — Discord role ID

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Manage Roles permission
- User ID or role ID is invalid
- Role is not assigned to user

**Example Output:**
```
Removed role 987654323 from user 123456789
```

---

## Guild Management Commands

### get_guild_info <guild_id>

Gets information about a guild.

**Parameters:**
- `guild_id` (string, required) — Discord guild ID

**Returns:** Prints guild name, ID, owner, member count, etc.

**Error Cases:**
- Guild ID is invalid
- Bot lacks View Channels permission

**Example Output:**
```
Guild: OpenClaw Server (ID: 1467329846265909446)
Owner: Luke#1234
Members: 5
```

---

### list_guilds

Lists all guilds the bot is in.

**Parameters:** None

**Returns:** Prints each guild with ID and name.

**Error Cases:** None (if bot has no guilds, prints empty list)

**Example Output:**
```
Guilds:
  - ID: 1467329846265909446, Name: OpenClaw Server
  - ID: 987654324, Name: Test Server
```

---

## Emoji Management Commands

### list_emojis

Lists all custom emojis in the guilds the bot is in.

**Parameters:** None

**Returns:** Prints each emoji with name and ID.

**Error Cases:**
- Bot lacks View Channels permission

**Example Output:**
```
Emojis:
  - Name: status, ID: 123456789
  - Name: warning, ID: 123456790
```

---

### create_emoji <name> <image_url>

Creates a custom emoji.

**Parameters:**
- `name` (string, required) — Emoji name (2-32 characters)
- `image_url` (string, required) — URL to emoji image (256x256 PNG recommended)

**Returns:** Prints created emoji ID on success.

**Error Cases:**
- Bot lacks Manage Emojis and Stickers permission
- Emoji name is invalid
- Image URL is invalid
- Rate limit hit (~50 emojis/guild/day)

**Example Output:**
```
Created emoji 'status' (ID: 123456791)
```

---

## Webhook Management Commands

### create_webhook <channel_id> <name>

Creates a webhook for a channel.

**Parameters:**
- `channel_id` (string, required) — Discord channel ID
- `name` (string, required) — Webhook name (max 80 characters)

**Returns:** Prints webhook URL on success.

**Error Cases:**
- Bot lacks Manage Webhooks permission
- Channel ID is invalid
- Rate limit hit (~10 webhooks/guild)

**Example Output:**
```
Created webhook 'alerts': https://discord.com/api/webhooks/123456789/abc123...
```

---

### delete_webhook <webhook_url>

Deletes a webhook.

**Parameters:**
- `webhook_url` (string, required) — Discord webhook URL

**Returns:** Prints confirmation on success.

**Error Cases:**
- Bot lacks Manage Webhooks permission
- Webhook URL is invalid

**Example Output:**
```
Deleted webhook https://discord.com/api/webhooks/123456789/abc123...
```

---

## Common Error Messages

- `Error: Channel '<name>' not found` — Channel name not found in guild
- `Error: HTTP 403 Forbidden` — Bot lacks permission
- `Error: Rate limit hit, retry in <seconds> seconds` — Rate limit exceeded
- `Error: Invalid guild ID` — Guild ID format invalid
- `Error: Token invalid or expired` — Bot token is invalid

## Parameter Types

| Parameter | Type | Format | Example |
|-----------|------|--------|---------|
| guild_id | string | 18-19 digit snowflake | `1467329846265909446` |
| channel_id | string | 18-19 digit snowflake | `1482113021592735887` |
| category_id | string | 18-19 digit snowflake | `1467364905383628852` |
| message_id | string | 18-19 digit snowflake | `123456789` |
| thread_id | string | 18-19 digit snowflake | `123456791` |
| user_id | string | 18-19 digit snowflake | `123456789` |
| role_id | string | 18-19 digit snowflake | `987654321` |
| emoji | string | Unicode or custom name | `✅` or `status` |
| color | string | Hex color code | `#3498db` |
| webhook_url | string | Full Discord webhook URL | `https://discord.com/api/webhooks/...` |
| name | string | Alphanumeric with hyphens | `test-channel` |
| content | string | Text (Markdown supported) | `Hello **world**!` |
| limit | integer | 1-100 | `50` |
| seconds | integer | 0-21600 | `5` |
| position | integer | 0+ | `1` |

---

For more information, see:
- [Agent Integration Guide](AGENT_INTEGRATION.md)
- [Quick Reference](QUICK_REFERENCE.md)
- [README](../README.md)
