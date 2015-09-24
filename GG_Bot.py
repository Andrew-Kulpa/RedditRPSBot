import praw
import time
import os
from datetime import datetime
from bot_config import *

print("Initializing...") #initializing the good-guy bot we all truly love
cache = []
subreddit_array = ["FreeKarma","Test","python","learnprogramming","programming"]

print("Logging in as %s..." %REDDIT_USERNAME)
# Create the Reddit instance
user_agent = ("Automated Begging for /u/"+REDDIT_USERNAME)
r = praw.Reddit(user_agent=user_agent)
# and login
r.login(REDDIT_USERNAME, REDDIT_PASS,disable_warning=True)

def run_bot():
	if not os.path.isfile("bot_config.py"): #if this godly bot forgot some damn information
		print("Please check that the configuration file is created.") #say something like this ^
		exit(1) #Quitter.
	running = True #lets just say, we don't start by walking ;)
	n = 1 #Because starting at 0 is lame.
	while running: #  >>> while walking:
		try: #because do: isn't acceptable by this snake-program-language-thingy
			for nth_subreddit in subreddit_array: #for each subreddit within that thing called an array
				print("Grabbing subreddit %s..." %nth_subreddit) #print and act like you're doing something
				subreddit = r.get_subreddit(nth_subreddit) #grab dat subreddit by the...[NSFW]
				new_submissions = subreddit.get_new() #look upon your new disciples and ready the blessing

				for submission in new_submissions: #for each disciple, we shall throw an up-arrow
					if submission.id not in cache: #if not already blessed
						submission.upvote() #doing gods work here
						cache.append(submission.id) #appends the submission to the cache
						print("Doing God's work to %s people." %str(n)) #swiggity swag
						n = n + 1 #increment n people
			print("Taking a break~~")
			time.sleep(60) #sleep for 60 seconds
		except KeyboardInterrupt:
			running = False
		except Exception as e: #if something random happens like just say "nahhhh" for 10 minutes.
			print('Error: ', e)
			print('Going to sleep for ' + str(10) + ' minutes...\n')
			time.sleep(600)


#LET THE BLESSING BEGIN \o/
run_bot()