#!/usr/bin/python3
'''
python twitter bot that does stuff
TODO: 
    [ ] Log when bot is killed
    [ ] Implement user log in
    [ ] Make a User class, instead of using functions
    	    This class will make it easy to have multiple
	    users preform actions (notabot and milesboswell
	    like and retweet a tweet)
    [ ] Send Direct Messages
'''
import tweepy, re, logging, threading
from keys import *

# set up twitter credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

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

def update(s):
	def setInterval(func, sec):
		t = threading.Timer(sec, func)
		t.start()
		# return the Timer object, just in case it needs to be canceled
		return t
	return setInterval(lambda: update(s), s)
# setKeyToken(consumer_secret, 'new secret token')
def setKeyToken(key, newkey):
	'''setKeyToken will be used to change credentials in keys.py
	   when another user is logged in. If user log in is implemented,
	   other twitter accounts (different than notabot) will be able to 
	   like, retweet, or do any other activity from their account. consumer_key
	   and consumer_secret don't have to be changed to switch users; notabot
	   is still the host of the application.'''
	with open('keys.py', 'r') as key_file:
		original = key_file.read()
	newcreds = re.sub(key, newkey, original)
	with open('keys.py', 'w') as key_file:
		key_file.write(newcreds)

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
		# make sure the tweet is from a user in watch array, not mentioning that user
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
	# # update periodically from watchusers file
	# update(5* 60) # update every 5 minutes
	# initialize twitter stream
	myStream = tweepy.Stream(auth=api.auth, listener=StreamListener())
	# filter the stream to user ids in watch[]
	myStream.filter(follow=[user['id'] for user in watch], async=True)
	users_str = ', '.join(user['screen_name'] for user in watch)
	log('Listening for tweets from: ' + users_str, end='\n-------------------')

if __name__ == '__main__':
	main()
