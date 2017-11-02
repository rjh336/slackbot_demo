## Slackbot demo  
I have created a basic slackbot that will scrape the channels to which it has access. Additionally, it can store this data in a MongoDB database for later analysis. This bot is implemented in Python and utilizes the [*slackclient*](http://python-slackclient.readthedocs.io/en/latest/) API wrapper as well as [*pymongo*](https://api.mongodb.com/python/current/) for storage.  

### Requirements:  
In order to run the bot you will need Python 3 and downloads for the following packages:
```
pip install pymongo
pip install slackclient
```

### Get Started:
*Note:* you will need to set up mongodb on your local computer for the code to run. If you have mongodb set up on a remote host, then you will need to modify ```mongo_client = MongoClient()``` in starterbot.py to include your hosts info.  

1. Sign up and create your own Slack Team [here](https://api.slack.com/).
2. Go [here](https://api.slack.com/bot-users) and click **creating a bot user**.
3. Create a bot and copy its API Token.
4. Save the API Token in an environment variable
```export SLACK_BOT_TOKEN='your token'```
5. Install the requirements listed above.
6. ```git clone``` this repo.
7. Edit print_bot_id.py and make BOT_NAME match the name of your bot.
8. Run ```python print_bot_id.py``` and then copy the bot's ID into an environment variable 
```export BOT_ID='bot id'```
9. Run ```python starterbot.py``` and start talking to your bot.

### Commands:
As of now, the bot I have made will recognize one command to scrape the current channel's conversation history and store the data in a mongodb collection called conversations. The command should be run from your slack group like so:  
```@[name of bot] scrape```