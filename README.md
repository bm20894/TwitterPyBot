# TwitterPyBot
A twitter bot using the python tweepy library. The bot account likes and retweets statuses from a list of users it is listening to.

## Installation
No credentials are included in this repository, for obvious reasons.
  If you choose to use this code with your own twitter account and credentials, install the tweepy library with `$ pip3 install tweepy`, and add a `keys.py` file with variables `consumer_key`, `consumer_secret`, `access_token`, `access_token_secret`. The variables should all be assigned a string value with their respective credentials from Twitter.

## Usage
To run the bot script, run `$ python3 bot.py`. To run the bot in the backround, use `$ ./start.sh`. All output from the bot script is logged into `bot.log` file.
