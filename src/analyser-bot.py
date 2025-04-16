import slack
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter  # To handle events from Slack
from modules.github_handler import Repository

# Load environment variables
load_dotenv(dotenv_path="./.env")

# Initialise a Flask server
app: Flask = Flask(__name__)
slack_events_adapter: SlackEventAdapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], "/slack/events", app) # `/slack/events` is the endpoint that will receive events from Slack; app - events are sent to this running web server

# Initialise a Slack WebClient instance
client: slack.WebClient = slack.WebClient(token=os.environ['SLACK_TOKEN'])   # Initialise an instance of the Slack WebClient interface to interract later with Slack API
BOT_ID = client.api_call("auth.test")['user_id']                             # Get the bot's user ID                     

USED_LANGUAGES = ["solidity", "rust"]     


def check_language_exists(message: str) -> bool:
    """
    Check if the message contains a needed programming language from the USED_LANGUAGES list
    Args:
        message (str): The message to check
    Returns:
        bool: True if the message contains a needed programming language, False otherwise
    """
    message: str = message.lower()
    for language in USED_LANGUAGES:
        if language in message:
            return True
    return False


def message_to_dict(message:str) -> dict:
    """
    Convert a message to a dictionary
    Args:
        message (str): The message to convert
    Returns:
        dict: The dictionary representation of the message
    """
    data_dict: dict = {}
    for line in message.split("\n"):
        if ":*" in line or "*" in line:
            key, value = line.split(":", 1)
            key = key.replace("*", "").strip()
            value = value.replace("*", "").strip()  # Remove asterisks from value as well
            data_dict[key] = value
    return data_dict


@slack_events_adapter.on("message")
def handle_message(payload) -> None:
    """
    Handle messages from users in the #test-bot channel
    Args:
        payload (dict): The payload containing the event data
    Returns:
        None
    """
    event: dict = payload.get("event", {})
    channel_id: str = event.get("channel")
    user_id: str = event.get("user")
    text: str = event.get("text")
    
    # Parse the text into a dictionary
    data_dict:dict = message_to_dict(text)

    if user_id != None and user_id != BOT_ID and check_language_exists(text):
        ts: str = event.get("ts")
        repository: Repository = Repository(data_dict["Repo"], data_dict["Client"], data_dict["Language"], data_dict["Branch"], data_dict["Commit"], data_dict["Scope"])
        path:str = repository.clone_repo(data_dict["Repo"])
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text=path) # Reply in thread if a solidity message was found



if __name__ == '__main__':   # If we run this file directly - then start the server     
    app.run(debug=True)

      