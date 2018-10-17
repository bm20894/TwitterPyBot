'''
Add a user to watchusers file
'''
import re

# get input for user to add
newuser = input('Enter the screen name of the user to watch: ')
# newuser = 'milesboswell'
screen_name = f'@{newuser}'

# check if user is not in file already
with open('watchusers', 'r') as f:
	cont = f.read()
users = [user[:-1] for user in cont.split('@')[1:]]

# add user to watchusers if not in it already
if not newuser in users:
	with open('watchusers', 'a') as f:
		f.write(f'{screen_name}\n')
	print(f'Added {screen_name} to watchlist.')
else:
	print('User is already being watched.')