import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from coinbot import coinbot

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app) #SLACK_EVENTS_TOKEN

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN")) #SLACK_BOT_TOKEN

def find_song(channel, artist):
    """Craft the KanyeBot, find the song and send the message to the channel
    """
    # Create a new KanyeBot
    kanye_bot = kanyebot(channel, artist)

    # Get the onboarding message payload
    message = kanye_bot.get_message_payload(artist)

    # Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**message)


# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
    """Parse the message event, and if the activation string is in the text,
    get a song by Kanye West song and send the result.
    """

    # Get the event data from the payload
    event = payload.get("event", {})

    # Get the text from the event that came through
    text = event.get("text").split()
    band = ""
    for i in range(1, len(text) - 1):
        band += text[i] + "+"
    band = band + "discography"


    # Check and see if the activation phrase was in the text of the message.
    # If so, execute the code to flip a coin.
    if text[0].lower() == "play" and text[len(text)-1].lower() == "please":

        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        channel_id = event.get("channel")

        # Execute the flip_coin function and send the results of
        # flipping a coin to the channel
        return flip_coin(channel_id, band)

if __name__ == "__main__":
    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run our app on our externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', port=3000)