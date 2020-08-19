import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True)
ap.add_argument("-c", "--count", type=int, default=200)

args = vars(ap.parse_args())

class TwitterClient(object): 
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''
	def __init__(self): 
		''' 
		Class constructor or initialization method. 
		'''
		# keys and tokens from the Twitter Dev Console 
		consumer_key = '8muaRM7Rl1hXLNWixja16fx3B'
		consumer_secret = '3ZPKaW6ZeDl6uB8Tm8LNlc974jlxEUNkcDFC67WqY1miKNsFKP'
		access_token = '1162576645-2bSubX0dcIOB54qSoCoNsjnoj6XUvyPmrVS3tsI'
		access_token_secret = 'Kt6qFCVsyBxozYQkMM8kiGtpw124l1Pz6XJoNyCbGPLKi'

		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		''' 
		Utility function to clean tweet text by removing links, special characters 
		using simple regex statements. 
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 
		''' 
		Utility function to classify sentiment of passed tweet 
		using textblob's sentiment method 
		'''
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet)) 
		print(analysis.sentiment.polarity)
		# set sentiment 
		if analysis.sentiment.polarity > 0.5: 
			return 'strong positive'
		elif analysis.sentiment.polarity > 0:
			return 'weak positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		elif analysis.sentiment.polarity < 0.5: 
			return 'strong negative'
		else: 
			return 'weak negative'

	def get_tweets(self, query, count = 10): 
		''' 
		Main function to fetch tweets and parse them. 
		'''
		# empty list to store parsed tweets 
		tweets = [] 

		while count != 0 :
			try: 
				# call twitter api to fetch tweets 
				fetched_tweets = self.api.search(q = query, count = count) 
				#print(len(fetched_tweets))
				count = count - len(fetched_tweets)

				# parsing tweets one by one 
				for tweet in fetched_tweets: 
					# empty dictionary to store required params of a tweet 
					parsed_tweet = {} 
	
					# saving text of tweet 
					parsed_tweet['text'] = tweet.text 
					# saving sentiment of tweet 
					parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
	
					# appending parsed tweet to tweets list 
					if tweet.retweet_count > 0: 
						# if tweet has retweets, ensure that it is appended only once 
						if parsed_tweet not in tweets: 
							tweets.append(parsed_tweet) 
					else: 
						tweets.append(parsed_tweet) 
			
			except tweepy.TweepError as e: 
			# print error (if any) 
				print("Error : " + str(e))

		# return parsed tweets 
		return tweets 

		 

def main(): 
	# creating object of TwitterClient Class 
	api = TwitterClient() 
	print(args['query'])
	# calling function to get tweets 
	tweets = api.get_tweets(query = args['query'], count = args['count']) 
	print("Unique tweets downloaded: {} ".format(len(tweets)))

	# picking positive tweets from tweets 
	sptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'strong positive']
	wptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'weak positive']  
	# percentage of positive tweets 
	print("Strong Positive tweets percentage: {} %".format(100*len(sptweets)/len(tweets))) 
	print("Weak Positive tweets percentage: {} %".format(100*len(wptweets)/len(tweets))) 
	# picking negative tweets from tweets 
	sntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'strong negative']
	wntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'weak negative']
	# percentage of negative tweets 
	print("Strong Negative tweets percentage: {} %".format(100*len(sntweets)/len(tweets)))
	print("Weak Negative tweets percentage: {} %".format(100*len(wntweets)/len(tweets)))
	# percentage of neutral tweets 
	print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(sntweets) - len(sptweets) - len(wntweets) - len(wptweets))/len(tweets)))

	# printing first 5 positive tweets 
	#print("\n\nPositive tweets:") 
	#for tweet in ptweets[:10]: 
		#print(tweet['text']) 

	# printing first 5 negative tweets 
	#print("\n\nNegative tweets:") 
	#for tweet in ntweets[:10]: 
		#print(tweet['text']) 

if __name__ == "__main__": 
	# calling main function 
	main() 

