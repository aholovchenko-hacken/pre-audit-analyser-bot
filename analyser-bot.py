import slack
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter  # To handle events from Slack

# Load environment variables
env_path: str = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Initialise a Flask server
app: Flask = Flask(__name__)
slack_events_adapter: SlackEventAdapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], "/slack/events", app) # `/slack/events` is the endpoint that will receive events from Slack; app - events are sent to this running web server

# Initialise a Slack WebClient instance
client: slack.WebClient = slack.WebClient(token=os.environ['SLACK_TOKEN'])   # Initialise an instance of the Slack WebClient interface to interract later with Slack API
BOT_ID = client.api_call("auth.test")['user_id']                             # Get the bot's user ID                     

USED_LANGUAGES = ["solidity", "rust"]     

# Check if the message contains a needed programming language from the USED_LANGUAGES list
def check_language_exists(message: str) -> bool:
    message = message.lower()
    for language in USED_LANGUAGES:
        if language in message:
            return True
    return False


# Define a function(event handler) to handle messages from users in the #test-bot channel
@slack_events_adapter.on("message")
def handle_message(payload) -> None:
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    print(text)

    if user_id != None and user_id != BOT_ID and check_language_exists(text):
        ts = event.get("ts")
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text="Solidity was found!)") # Reply in thread if a solidity message was found



if __name__ == '__main__':   # If we run this file directly - then start the server     
    app.run(debug=True)

      