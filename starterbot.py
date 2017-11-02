import os
import time
import requests
from pymongo import MongoClient
from slackclient import SlackClient  # http://python-slackclient.readthedocs.io/en/latest/

# bot's id and api token as env variables
BOT_ID = os.environ.get("BOT_ID")
BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

# constants
AT_BOT = "<@" + BOT_ID + ">"
GET_CONVERSATION_HISTORY = "scrape"

# instantiate Slack client
slack_client = SlackClient(BOT_TOKEN)

# channel info
channel_list = slack_client.api_call("channels.list")['channels']
channel_ids = { c['name'] : c['id'] for c in channel_list }

# Mongo client
mongo_client = MongoClient()


def get_conversation_history(channel):
    endpoint = "https://api.slack.com/api/conversations.history?"
    page_root = endpoint+"token="+BOT_TOKEN+"&channel="+channel # first page
    r = requests.get(page_root).json()
    data = r['messages'] # this will hold all the messages in our conversation history
    has_more = r['has_more']
    next_cursor = ""

    # check whether you are on last page
    if has_more:
        next_cursor = r['response_metadata']['next_cursor']

    while has_more:
        next_page = requests.get(page_root+"&cursor="+next_cursor).json()
        next_cursor = next_page['response_metadata']['next_cursor']
        data += next_page['messages']
        has_more = next_page['has_more']

    print("Conversation History Loaded")
    return data

# def retrieve_conversation_history(users):

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Invalid command"

    # scrape command: get entire history of messages in the current channel
    if command.startswith(GET_CONVERSATION_HISTORY):
        # package json messages into list
        data = get_conversation_history(channel)
        # insert messages into our conversations collection
        conversations = mongo_client.slackbot_demo.conversations
        conversations.insert_many(data)
        response = "Updated "+str(conversations.name)+" with "+str(len(data))+" records"

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")