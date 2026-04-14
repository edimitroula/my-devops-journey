# Slack Reminder Bot Setup Guide

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Slack workspace** access (viasat workspace)
3. **Slack App** with Bot Token

## Step 1: Create a Slack App

1. Go to https://api.slack.com/apps
2. Click **"Create New App"** → **"From scratch"**
3. Name it: `Reminder Bot`
4. Select your workspace: **viasat**

## Step 2: Configure Bot Permissions

1. In your app settings, go to **"OAuth & Permissions"**
2. Under **"Scopes"** → **"Bot Token Scopes"**, add these permissions:
   - `chat:write` - Send messages
   - `channels:history` - Read channel messages
   - `channels:read` - List channels
   - `users:read` - Read user information

## Step 3: Install the App to Your Workspace

1. Go to **"Install App"** in the sidebar
2. Click **"Install to Workspace"**
3. Authorize the app
4. Copy the **"Bot User OAuth Token"** (starts with `xoxb-`)

## Step 4: Invite the Bot to Your Channel

1. In Slack, go to the channel where you want to send reminders
2. Type: `/invite @Reminder Bot`
3. Note the channel name (e.g., `general`, `team-notifications`, etc.)

## Step 5: Install Python Dependencies

Open your terminal and run:

```bash
cd C:\Users\Eirini Dimitroula\claude-playground
pip install -r requirements.txt
```

## Step 6: Set Your Slack Bot Token

### Windows (Command Prompt):
```cmd
set SLACK_BOT_TOKEN=xoxb-your-token-here
set SLACK_CHANNEL=general
```

### Windows (PowerShell):
```powershell
$env:SLACK_BOT_TOKEN="xoxb-your-token-here"
$env:SLACK_CHANNEL="general"
```

### Linux/Mac:
```bash
export SLACK_BOT_TOKEN=xoxb-your-token-here
export SLACK_CHANNEL=general
```

**Replace:**
- `xoxb-your-token-here` with your actual Bot User OAuth Token
- `general` with your target channel name

## Step 7: Run the Script

```bash
python slack_reminder.py
```

## How It Works

The script will:
1. ✅ Send "Book your tickets" message to Edwin Dijkstra every 30 seconds
2. ✅ Monitor the channel for any message containing "done"
3. ✅ Stop when either:
   - Someone replies with "done" (in any message)
   - 20 messages have been sent
4. ✅ Display progress in the terminal

## Stop the Script Early

Press `Ctrl + C` to stop the script manually at any time.

## Troubleshooting

### "SLACK_BOT_TOKEN environment variable not set"
- Make sure you've set the environment variable in your current terminal session
- The variable only persists in the current session

### "Channel 'xyz' not found"
- Check the channel name is correct
- Make sure the bot is invited to the channel (`/invite @Reminder Bot`)
- The script will list all available channels

### "Error sending message: not_in_channel"
- Invite the bot to the channel: `/invite @Reminder Bot`

### Permission errors
- Verify all required scopes are added in the Slack App settings
- Reinstall the app after adding new scopes

## Configuration

Edit these variables in `slack_reminder.py`:

```python
CHANNEL_NAME = "general"          # Your channel name
TARGET_USER = "Edwin Dijkstra"    # User to mention
MESSAGE = "Book your tickets"     # Message to send
INTERVAL_SECONDS = 30             # Seconds between messages
MAX_MESSAGES = 20                 # Max messages before stopping
STOP_KEYWORD = "done"             # Keyword to stop the bot
```

## Security Note

⚠️ **Never commit your Slack Bot Token to version control!**

Consider adding to `.gitignore`:
```
.env
*.token
```
