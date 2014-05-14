import tweepy
import webbrowser
import os
import datetime
import json

#Twitter API keys
#================
#API Key goes here!!!
ctoken = ''
#API Secret goes here!!!
csecret = ''


#don't worry about these
atoken = ''
asecret = ''
twitterhandle = ''

auth = tweepy.OAuthHandler(ctoken, csecret)
#data file path (to appdata folder)
DataPath = "%s\\TwitFollowerBot\\" % os.environ['APPDATA']
#filepaths of data saves
authDataFile = "%stwitterAuthenticationData.csv" % DataPath
followedFile = "%sfollowedUsers.csv" % DataPath
whitelistFile = "%swhitelistedUsers.csv" % DataPath
#whitelist
whitelist = []

try:
	#if the file path to stored data doesn't exist, create it, and create a data file
	if not os.path.exists(DataPath):
		os.makedirs(DataPath)
	if not os.path.isfile(authDataFile):
		with open(authDataFile, "w") as out_file:
			out_file.write("")
	#read the data file
	authFile = open(authDataFile)
	userdata = authFile.read()
	authFile.close()
	
	
	#if the whitelist file does not exist, create it
	if not os.path.isfile(whitelistFile):
		with open(whitelistFile, "w") as out_file:
			out_file.write("")
	#open the whitelist file, and read all the names into the whitelist global variable
	with open(whitelistFile) as file:
		whitelist = file.readlines()
	
	#if it is blank, it means the user has not input an access key yet.  Get that from them and save to file
	if userdata == '':
		#redirect to authorization url
		print "Authorization not found, redirecting to twitter to get encryption key!  Return to app when you have it."
		#get the verification key from the user
		while True:
			try:
				redirect_url = auth.get_authorization_url()
				webbrowser.open(redirect_url, new=2)
				verifier = raw_input("Please enter verification key: ")
				auth.get_access_token(verifier)
				print 'Key was valid'
				break
			except tweepy.TweepError, e:
				print 'Invalid key, generating new authentication...'
		
		#set authentication keys, aquired via user verification
		atoken = auth.access_token.key
		asecret = auth.access_token.secret
		#save data to file
		userVerification = str({'token': atoken, 'secret': asecret})
		authFile = open(authDataFile, "w")
		authFile.write(userVerification)
		authFile.close()
	#Else, if userdata was already stored
	else:
		#parse it into a dictionary
		userdata = eval(userdata)
		#set the authentication keys
		atoken = userdata['token']
		asecret = userdata['secret']
		print "loaded verification data"

except tweepy.TweepError, e:
	print 'Error!  Failed to get access token. Program will not work!'

#set access tokens from the authentication data we just got
auth.set_access_token(atoken, asecret)

#try to set up an api instance
try:
	api = tweepy.API(auth)
except tweepy.TweepError, e:
	print "ERROR: Error while authenticating the user"
#get the current user's data
currentUser = tweepy.API.me(api)
twitterhandle = currentUser.screen_name
print "Authentication successful for " + twitterhandle + "!"

"""
	Function to re-authenticate the user.  This is useful if the user is changing accounts/wants to use another account but data is already saved
"""
def new_auth():
	print "Redirecting to verification page at twitter.com..."
	#get the verification key from the user
	while True:
		try:
			#generate verification url
			redirect_url = auth.get_authorization_url()
			#redirect the user to the url
			webbrowser.open(redirect_url, new=2)
			verifier = raw_input("Please enter verification key: ")
			auth.get_access_token(verifier)
			print 'Key was valid'
			break
		except tweepy.TweepError, e:
			print 'Invalid key, generating new authentication url...'
	
	#set authentication keys, aquired via user verification
	atoken = auth.access_token.key
	asecret = auth.access_token.secret
	#save data to file
	userVerification = str({'token': atoken, 'secret': asecret})
	authFile = open(authDataFile, "w")
	authFile.write(userVerification)
	authFile.close()
	#set up globals and api instance for the new user
	auth.set_access_token(atoken, asecret)
	api = tweepy.API(auth)
	currentUser = tweepy.API.me(api)
	twitterhandle = currentUser.screen_name

"""
	Funciton to return the past 100 tweets (default) with the specefied query phrase
	@params:
		query :: String - word, phrase, or hashtag to filter tweets by
		numberOfTweets :: Int - Optional - Change the number of results
	@return :: Cursor of tweet objects that the function searched for
"""
def search_tweets(query, numberOfTweets=100):
	#try to search tweets, put them into a cursor object
	try:
		tweets = tweepy.Cursor(api.search, q=query, result_type="recent").items(numberOfTweets)
	except tweepy.TweepError, e:
		print "ERROR: Error while searching!"
	return tweets;

"""
	Function that follows the past 100 users to use the specefied phrase that the authenticated user is not already following
	@params:
		phrase :: String - a string of characters to filter tweets by
		count :: Int - max number of people to follow (default is 25)
"""
def auto_follow(phrase, count=25):
	#try to get which people the authenticated user is already following
	try:
		following = api.friends_ids(screen_name=twitterhandle)
	except tweepy.TweepError, e:
		print "ERROR: Could not get users the authenticated user is following"
	
	#make sure that the "already followed" file exists
	if not os.path.isfile(followedFile):
		with open(followedFile, "w") as out_file:
			out_file.write("")
	#read all the users that the bot has followed in the past
	with open(followedFile) as file:
		doNotFollow = file.readlines()
	
	#search tweets for phrase
	tweetsRaw = search_tweets(phrase, numberOfTweets=count)
	
	#list to store followed id's in
	newlyFollowed = []
	#loop through returned tweets and follow all tweeters that aren't in the following or doNotFollow variables
	for tweet in tweetsRaw:
		try:
			userID = tweet.user.id
			#if the userid isn't the authenticated user's id (don't follow yourself)
			if (tweet.user.screen_name != twitterhandle and
					userID not in following and
					userID not in doNotFollow):
				#try to friend them
				try:
					api.create_friendship(userID)
				except tweepy.TweepError, e:
					print "ERROR: Could not follow " + str(userID)
				#add to followed file
				dateNow = datetime.date.today()
				newlyFollowed.append(json.dumps({'user': userID, 'date': dateNow.strftime("%m-%d-%y")}))
				print "Followed %s with userID %s" % (tweet.user.screen_name, userID)
		
		except tweepy.TweepError, e:
			print "error when trying to follow " + tweet.user.screen_name + ": id=" + user
	
	#save all newly followed followers to file
	with open(followedFile, 'a') as file:
		for id in newlyFollowed:
			file.write(str(id) + "\n")

"""
	Function that whitelists the specefied user
	@params:
		user :: String - the twitter handle of the user to whitelist (this program does not unfollow whitelisted users)
"""
def new_whitelist_member(user):
	#try to get the user's account ID
	try:
		userID = api.get_user(screen_name=user).id
	except tweepy.TweepError, e:
		print "ERROR: Could not get the authenticated users user_id"
	#if the whitelist file does not exist, create it
	if not os.path.isfile(whitelistFile):
		with open(whitelistFile, "w") as file:
			file.write("")
	#open the whitelist file for append, and add the user's ID number to it
	with open(whitelistFile, 'a') as file:
		file.write(str(userID) + "\n")
	#open the whitelist file for read, and read all the names into the whitelist global variable
	with open(whitelistFile) as file:
		whitelist = file.readlines()

"""
	Function that whitelists all of the people the current user is following
	NOTE: On an auth_change, the chached whitelist data does not go away.  In order to have new whitelist data, the %appdata%/dtTwitBot/whitelistedUsers.csv file needs to be deleted, and
	the script needs to be restarted.
"""
def whitelist_following():
	#try to get the list of users the authenticated user follows
	try:
		users = api.friends_ids(screen_name=twitterhandle)
	except tweepy.TweepError, e:
		print "ERROR: Could not get list of people the authenticated user follows"
	#if the whitelist file does not exist, create it
	if not os.path.isfile(whitelistFile):
		with open(whitelistFile, "w") as file:
			file.write("")
	#open the whitelist file for append, and add the user's ID number to it
	with open(whitelistFile, 'a') as file:
		for userID in users:
			file.write(str(userID) + "\n")
	
	#open the whitelist file for read, and read all the names into the whitelist global variable
	with open(whitelistFile) as file:
		whitelist = file.readlines()

"""
	Function that unfollows people who have not followed you back within the pre-defined time period
	NOTE: This function only unfollows people that this bot has followed in the past.  It will not modify your existing list of people you follow
	@params:
		days :: Int - number of days a followed user has to have been followed with no response to unfollow that user.  -1 unfollows all
		max :: Int - maximum number of people this function will unfollow
"""
def unfollow_nonfollowers(days=7, max=50):
	#if the followedFile does not exist (it should, unless they deleted it while the program was running)
	if not os.path.isfile(followedFile):
		#create it
		with open(followedFile, "w") as out_file:
			out_file.write("")
	#open the followedFile for read, and read all the lines into the followingRaw variable
	with open(followedFile) as file:
		followingRaw = file.readlines()
	#try to get all of the authenticated user's friends
	try:
		followingNow = api.friends_ids(screen_name=twitterhandle)
	except tweepy.TweepError, e:
		print "ERROR: Could not get authenticated users 'following' list"
	#following variable to store parsed data for users the authenticated user is actually following
	following = []
	#loop through the raw following data
	for user in followingRaw:
		#parse from json per-user
		newuser = json.loads(user)
		#if the newuser is both in the followedFile and on the authenticated user's following list
		#(To explain a little more, once a user is followed by the bot, even if they get unfollowed, the file keeps record of following them.  That way, the bot doesn't 'spam' someone if
		#they happen to use a hashtag a lot)
		if newuser['user'] in followingNow:
			#parse the date into a datetime object
			newdate = datetime.datetime.strptime(newuser['date'], "%m-%d-%y")
			newuser['date'] = newdate
			#append newuser data to the following variable
			following.append(newuser)
	
	#try to get all users following the authenticated user
	try:
		followers = api.followers(screen_name=twitterhandle)
	except tweepy.TweepError, e:
		print "ERROR: Could not get users following the authenticated user"
	#get all followers id's from the tweepy user object they are a part of
	followersIDs = []
	for user in followers:
		followersIDs.append(user.id)
	
	#get all users who the authenticated user is following, but who are not following the authenticated user
	toUnfollow = [user for user in following if user['user'] not in followersIDs]
	
	#store how many people the program unfollows (to keep the number of users being unfollowed under the maximum, we don't want to make twitter angry!)
	unfollowedSoFar = 0
	
	#loop through the toUnfollow list
	for user in toUnfollow:
		#if the number of unfollowed users during this function call is less than the specefied maximum,
		#and the user is not in the whitelist array,
		#and the user has been followed for more than the specefied number of days
		if unfollowedSoFar < max and user['user'] not in whitelist and user['date'] + datetime.timedelta(days=days) <= datetime.datetime.now():
			#try to unfollow the user
			try:
				api.destroy_friendship(id=user['user'])
				print "Unfollowed " + str(user['user'])
			except tweepy.TweepError, e:
				"ERROR: Could not unfriend " + str(user['user'])
