import random
import praw
import time
import os
from datetime import datetime
from bot_config import *

print("Initializing...") #initializing the good-guy bot we all truly love
choices = ["rock", "paper","scissors"] #0 = rock, 1 = paper, 2 = scissors
cache = []
subreddit_array = ["FreeKarma"]#["FreeKarma","Test","python","learnprogramming","programming"]
botCallingWords = ["cia_bot","/u/cia_bot"]
p1_choice = ""
state = ""
bot_pick = 0
i = 3

print("Logging in as %s..." %REDDIT_USERNAME)
# Create the Reddit instance
user_agent = ("Automated Begging for /u/"+REDDIT_USERNAME)
r = praw.Reddit(user_agent=user_agent)
# and login
r.login(REDDIT_USERNAME, REDDIT_PASS,disable_warning=True)


def rng(i):
	random_choice = random.randrange(i) #number that is either 0, 1, or 2
	#print(str(random_choice))
	return random_choice

def referee(choice):
	global state
	global i
	global bot_pick
	bot_pick = rng(i)
	#print("Your Opponent chose: %s" %choices[bot_pick])
	if(choices[bot_pick] == choice):
		state = "tied!"
	elif(bot_pick == 0): # bot  = rock
		if(choice == "paper"):
			state = "won"
		else:
			state = "lost"
	elif(bot_pick == 1): # bot = paper
		if(choice == "rock"):
			state = "lost"
		else:
			state = "won"
	else:				# bot = scissprs
		if(choice == "rock"):
			state = "won"
		else:
			state = "lost"

def RockPaperScissors(choice):
	global p1_choice
	p1_choice = choice
	#what did player 1 choose?
	#p1_choice = input("Type either rock, paper, or scissors: ").lower()
	if(choice not in choices):
		print("You choice was not valid. Exitting....")
		exit(1)
	#print("You chose %s" %choice)
	referee(choice)
	#call function with player 1's choice and return whether they won or not
		#player 2 == bot so call random()
	#either player 1 or player 2 won

def run_bot():
	global i
	global p1_choice
	if not os.path.isfile("bot_config.py"): #if this godly bot forgot some damn information
		print("Please check that the configuration file is created.") #say something like this ^
		exit(1) #Quitter.
	running = True #lets just say, we don't start by walking ;)
	n = 1 #Because starting at 0 is lame.
	while running: #  >>> while walking:
		try: #because do: isn't acceptable by this snake-program-language-thingy
			for nth_subreddit in subreddit_array: #for each subreddit within that thing called an array
				print("Grabbing subreddit %s..." %nth_subreddit) #print and act like you're doing something
				comments = r.get_comments(nth_subreddit) #grab dat subreddit by the...[NSFW]

				for comment in comments: #for each comment in the comments grabbed from the subreddit
					#print("Comments yeahhhh")
					Player_Comment = comment.body.lower() #typecast the string in lowercase
					Calls_Bot = any(string in Player_Comment for string in botCallingWords) #did they call the bot?
					Has_Chosen = any(string in Player_Comment for string in choices) #did they choose?
					if comment.id not in cache and Calls_Bot: #if the comment isnt in the cache and fits the other conditions
						#print("See me CALLINGGGGGG~~~")
						if Has_Chosen:
							#print("Comment called you and has chosen you~~~ " + str(comment.id))
							comment.upvote() #upvote them for trying
							if "RPS" in comment.body: #e.g. /u/CIA_Bot RPS Rock
								i = 3
								if "rock" in Player_Comment:#if they choose something, use that then
									RockPaperScissors("rock")
								elif "paper" in Player_Comment:
									RockPaperScissors("paper")
								elif "scissors" in Player_Comment:
									RockPaperScissors("scissors")
								else:
									print("Invalid Input--dammit Grant.")
								comment.reply("You chose: " + p1_choice + "\n\nThe bot chose: " + choices[bot_pick] + "\n\nYou " + state + "!!!")
								print("\n\nPlayer " + str(n) + " chose: " + p1_choice + "\nThe bot chose: " + choices[bot_pick] + "\nThey " + state + "!!!\n\n") #Send Feedback to terminal
								n = n + 1 #increment n people
					cache.append(comment.id) #add it to the cache
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
