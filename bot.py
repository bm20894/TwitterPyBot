#!/usr/bin/python3
'''
python twitter bot that does stuff
'''
import tweepy, re, logging
from keys import *

# set up twitter credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# TODO: log when bot is killed
datefmt = '%d-%b-%y %H:%M:%S'
logging.basicConfig(filename='bot.log', level=logging.INFO,
	format='%(asctime)s: %(name)s - %(message)s', datefmt=datefmt)

# make an array of users to follow tweets for
watch = []

def log(s, end=''):
	logging.info('{}{}'.format(str(s), end))

def getUsers():
	# get users to watch from watchusers file
	with open('watchusers', 'r') as f:
		cont = f.read()
	users = re.findall(r'@([\w_-]+)\n?', cont)
	return users

def watchall():
	users = getUsers()
	for user in users:
		watchuser(user, add=False)

def watchuser(screen_name, add=True):
	# add user screen_name to watch
	global watch
	user = api.get_user(screen_name)
	# only add user if it is not already in watch
	if not screen_name in [user['screen_name'] for user in watch]:
		if add:
			with open('watchusers', 'a') as watch_file:
				watch_file.write('@{}\n'.format(screen_name))
		watch.append({'screen_name': user.screen_name, 'id': user.id_str})

# setKeyToken(consumer_secret, 'new secret token')
def setKeyToken(key, newkey):
	# change the credential keys in keys.py
	with open('keys.py', 'r') as key_file:
		original = key_file.read()
	newline = re.sub(key, newkey, original)
	with open('keys.py', 'w') as key_file:
		key_file.write(newline)

def like_retweet(status_id):
	# Favorite and Retweet a tweet with id id
	global api
	api.retweet(status_id)
	api.create_favorite(status_id)
	log('Favorited and Retweeted tweet: {}'.format(status_id))

# # Some 34 error from tweepy prevents this from working
# def sendDM(screen_name, text='U up?'):
# 	# sends a new direct message with message text to user screen_name
# 	global api
# 	api.send_direct_message(screen_name = screen_name, text = text)
# 	print('Sent DM to {}: {}'.format(screen_name, text))

# watch all users in watchusers file
watchall()
# # add SpaceX as a user
# watchuser('SpaceX')

# using streams of tweets
class StreamListener(tweepy.StreamListener):
	def on_status(self, status):
		# make sure the tweet is from a user in watch array
		for user in watch:
			user_id, screen_name = user['id'], user['screen_name']
			if status.user.id_str == user_id:
				log('Got a tweet from '+ status.user.screen_name)
				log(status.text, end='\n-------------------')
				status_id = status._json['id_str']
				# todo: do actions from multiple users
				like_retweet(status_id)

	def on_error(self, status_code):
		if status_code == 420:
			return False
		elif status_code == 327:
			log('Already retweeted this tweet.')
			pass
		elif status_code == 34:
			log('Sorry, that page does not exist.')
			return False

def main():
	# initialize twitter stream
	myStream = tweepy.Stream(auth=api.auth, listener=StreamListener())
	# filter the stream to user ids in watch[]
	myStream.filter(follow=[user['id'] for user in watch], async=True)
	users_str = ', '.join(user['screen_name'] for user in watch)
	log('Listening for tweets from: ' + users_str, end='\n-------------------')

if __name__ == '__main__':
	main()