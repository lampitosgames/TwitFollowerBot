TwitFollowerBot
===============

A python twitter bot (using tweepy) that is designed to create new twitter connections and expand an account's relevant circle of influence.

===============

This script allows you to follow a specefied number of users by keyword.  I've found that about 20% of these users will follow you back!  After whatever amount of time you deem fitting, you can use this script to unfollow all of the people who did not follow back.

"But Lampitos!  What if I don't want to unfollow people I'm currently following!?!?"
Good question.  This bot will only unfollow users it has followed, so your current friends list is safe.  If you want to be extra careful, you can whitelist your entire friends list, or individual twitter names (the bot will never unfollow them).

That is it!  It is super simple, but it is highly effective.  I don't use twitter a lot, so I don't use this.  I was paid to create this script for someone else, who then proceeded to get ~400 followers per week, haha!

REQUIREMENTS
===============
This python script assumes that you have Python 2.7 installed, with the Tweepy library availible for use (both are only a google search away).  There are extensive guides on how to get both of those, so I'll leave that up to you.

This script will save data in your %appdata% folder.  If you delete the data stored there, the program may re-follow people you've already unfollowed, and you will also need to re-authenticate the application.

TWITTER APPLICATION SETUP
===============

Once you have your python environment set up correctly, you will need a twitter developer account!  Head on over to dev.twitter.com to get started.  In the top-right corner, there is a 'sign in' option.  You can sign in with your current twitter account, or just create a new one.  No matter what account you use, this twitter bot will still be able to run for any other twitter account.

Once you are signed in, hover over your profile (where the 'sign in' button was before), and select 'My Applications'.  Click the 'Create New App' button!  Fill out everything except the callback url (you don't need that) and hit 'Create your Twitter application'.

On your app's page, you will find a bunch of info we do not need.  Across the top, click on the tab that says 'API Keys'.  Copy your API Key and API Secret to a text file or something, because we will need those.

The final setup phase is to place your keys into the script.  I assume you've downloaded my program by now, right?  If not, go ahead and do that, and open it up in your favorite editor.  The first two variables are where you need to place your API Key and API Secret respectively (they are labeled, don't worry).  Congradulations!  You are all set to run this bad boy!

===============

You will want to run this from the python command line, just because you need to make funciton calls manually.  Go ahead and place this script into your python scripts folder, and excecute the command 'import TwitFollowerBot'.

If this is your first time running the script, you will need to authenticate the application with your twitter account.  The script will send you to an authentication page where you will need to log in and hit "authorize".  A series of numbers will appear in bold.  Copy those into your python command line, hit 'enter', and you are good to go!

First thing is first, you will probably want to whitelist the people you are currently following.  Whitelisted users will never be unfollowed by this twitter bot.  There are two functions to do this with.

new_whitelist_member(name) - This will whitelist a user based on their twitter username (without the @ in front of it).

whitelist_following() - This will whitelist everyone you are currently following.

To delete whitelisted users, you will need to exit the script, and edit the whitelist file located at %appdata%/TwitFollowerBot

FUNCTION DESCRIPTIONS
===============
See the descriptions in the script for more details

new_auth() - Function to re-authenticate the user.  This is useful if the user is changing accounts/wants to use another account but data is already saved

search_tweets(query, numberOfTweets=100) - Function to return the past 100 tweets (default) with the specefied query phrase.  Returns a cursor of tweet objects.

auto_follow(phrase, count=25) - Function that follows the past COUNT users to use the specefied phrase (does not follow users previously followed)

new_whitelist_member(user) - Function that whitelists the specefied user

whitelist_following() - Function that whitelists all of the people the current user is following

unfollow_nonfollowers(days=7, max=50) - Function that unfollows people who have not followed you back within the pre-defined time period up to a maximum number of unfollows.
