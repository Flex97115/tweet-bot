import tweepy
from business.consumer.api_consumer import ApiConsumer


class TweetConsumer(ApiConsumer):

    # Standard search tweet with query
    # https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
    def search(self, query, since_id):
        if query is None:
            raise Exception("Empty query will not pursue search")
        print('Search for {}'.format(query))
        #TODO: create a request builder, its ugly...
        if since_id:
            return tweepy.Cursor(self._api.search, q=query, count=10, since_id=since_id)
        else:
            return tweepy.Cursor(self._api.search, q=query, count=10)

    def retweet(self, tweet):
        try:
            print('ACTION retweet : {}'.format(tweet.text))
            self._api.retweet(tweet.id)
            return tweet
        except tweepy.error.TweepError as te:
            print("Error {} occur during retweeting {}".format(te, tweet.text))

    def unretweet(self, tweet):
        try:
            print('ACTION unretweet : {}'.format(tweet.text))
            self._api.unretweet(tweet.id)
            return tweet
        except tweepy.error.TweepError as te:
            print("Error {} occur during unretweeting {}".format(te, tweet.text))

    def like_tweet(self, tweet):
        try:
            print('ACTION like : {}'.format(tweet.text))
            self._api.create_favorite(tweet.id)
        except tweepy.error.TweepError as te:
            print("Error {} occur during create favorite {}".format(te, tweet.text))
