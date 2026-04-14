#!/usr/bin/env python3
"""
Slack Reminder Bot
Sends periodic reminders to a Slack channel until a response is received or max messages sent.
"""

import os
import time
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configuration
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
CHANNEL_NAME = os.environ.get("SLACK_CHANNEL", "general")  # or specific channel
TARGET_USER = "Edwin Dijkstra"
MESSAGE = "Book your tickets"
INTERVAL_SECONDS = 30
MAX_MESSAGES = 20
STOP_KEYWORD = "done"


def get_channel_id(client, channel_name):
    """Get channel ID from channel name."""
    try:
        # Try to find the channel
        result = client.conversations_list()
        for channel in result["channels"]:
            if channel["name"] == channel_name:
                return channel["id"]

        print(f"Channel '{channel_name}' not found. Available channels:")
        for channel in result["channels"]:
            print(f"  - {channel['name']}")
        return None
    except SlackApiError as e:
        print(f"Error fetching channels: {e.response['error']}")
        return None


def send_reminder(client, channel_id, message, user_mention=None):
    """Send a reminder message to the channel."""
    try:
        full_message = f"@{user_mention} {message}" if user_mention else message
        response = client.chat_postMessage(
            channel=channel_id,
            text=full_message
        )
        return response["ts"]  # Return message timestamp
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")
        return None


def check_for_done_reply(client, channel_id, after_ts):
    """Check if anyone has replied with 'done' after the given timestamp."""
    try:
        result = client.conversations_history(
            channel=channel_id,
            oldest=after_ts,
            limit=100
        )

        for message in result["messages"]:
            text = message.get("text", "").lower()
            if STOP_KEYWORD in text:
                return True, message.get("user", "unknown"), text

        return False, None, None
    except SlackApiError as e:
        print(f"Error checking messages: {e.response['error']}")
        return False, None, None


def main():
    """Main function to run the reminder bot."""
    # Check for required environment variable
    if not SLACK_BOT_TOKEN:
        print("ERROR: SLACK_BOT_TOKEN environment variable not set!")
        print("\nTo set it:")
        print("  Windows: set SLACK_BOT_TOKEN=xoxb-your-token-here")
        print("  Linux/Mac: export SLACK_BOT_TOKEN=xoxb-your-token-here")
        return

    # Initialize Slack client
    client = WebClient(token=SLACK_BOT_TOKEN)

    print("=" * 60)
    print("Slack Reminder Bot Started")
    print("=" * 60)
    print(f"Target: {TARGET_USER}")
    print(f"Message: {MESSAGE}")
    print(f"Channel: {CHANNEL_NAME}")
    print(f"Interval: {INTERVAL_SECONDS} seconds")
    print(f"Max messages: {MAX_MESSAGES}")
    print(f"Stop keyword: '{STOP_KEYWORD}'")
    print("=" * 60)

    # Get channel ID
    channel_id = get_channel_id(client, CHANNEL_NAME)
    if not channel_id:
        return

    print(f"\nChannel ID: {channel_id}")
    print(f"\nStarting reminder loop...\n")

    messages_sent = 0
    start_ts = str(time.time())

    try:
        while messages_sent < MAX_MESSAGES:
            # Send the reminder
            messages_sent += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"[{timestamp}] Sending message {messages_sent}/{MAX_MESSAGES}...")

            msg_ts = send_reminder(client, channel_id, MESSAGE, TARGET_USER)

            if not msg_ts:
                print("Failed to send message. Exiting.")
                break

            print(f"  ✓ Message sent successfully")

            # Wait before checking for replies
            time.sleep(5)

            # Check for 'done' reply
            done_found, user, text = check_for_done_reply(client, channel_id, start_ts)

            if done_found:
                print(f"\n{'=' * 60}")
                print(f"✓ STOP CONDITION MET: '{STOP_KEYWORD}' detected!")
                print(f"  User: {user}")
                print(f"  Message: {text}")
                print(f"{'=' * 60}")
                print(f"\nTotal messages sent: {messages_sent}")
                print("Bot stopped successfully.")
                return

            # Wait for the interval before next message (minus the 5 seconds already waited)
            if messages_sent < MAX_MESSAGES:
                remaining_wait = INTERVAL_SECONDS - 5
                if remaining_wait > 0:
                    print(f"  Waiting {remaining_wait} seconds until next message...\n")
                    time.sleep(remaining_wait)

        # Max messages reached
        print(f"\n{'=' * 60}")
        print(f"✓ MAX MESSAGES REACHED: {MAX_MESSAGES} messages sent")
        print(f"{'=' * 60}")
        print("Bot stopped successfully.")

    except KeyboardInterrupt:
        print(f"\n\n{'=' * 60}")
        print("Bot stopped by user (Ctrl+C)")
        print(f"Total messages sent: {messages_sent}")
        print("=" * 60)


if __name__ == "__main__":
    main()
