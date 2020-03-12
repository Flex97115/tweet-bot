import tweepy
from business.consumer.api_consumer import ApiConsumer


class TweetConsumer(ApiConsumer):

    # Search tweet with query
    # https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
    def search(self, query):
        if query is None:
            raise Exception("Empty query will not pursue search")
        print('Search for {}'.format(query))
        #TODO: use cursor http://docs.tweepy.org/en/latest/cursor_tutorial.html
        return self._api.search(q=query, count=100)

    def retweet(self, tweet):
        try:
            print('ACTION retweet : {}'.format(tweet['text']))
            self._api.retweet(tweet['id'])
            return tweet
        except tweepy.error.TweepError as te:
            print("Error {} occur during retweeting {}".format(te, tweet))

    def unretweet(self, tweet):
        try:
            print('ACTION unretweet : {}'.format(tweet['text']))
            self._api.unretweet(tweet['id'])
            return tweet
        except tweepy.error.TweepError as te:
            print("Error {} occur during unretweeting {}".format(te, tweet))

    def like_tweet(self, tweet):
        try:
            print('ACTION like : {}'.format(tweet['text']))
            self._api.create_favorite(tweet['id'])
        except tweepy.error.TweepError as te:
            print("Error {} occur during create favorite {}".format(te, tweet))
