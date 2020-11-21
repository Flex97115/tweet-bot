from business.consumer.user_consumer import UserConsumer
from business.consumer.tweet_consumer import TweetConsumer
import asyncio
import itertools

tweet_consumer = TweetConsumer()
user_consumer = UserConsumer()

MAX_TWEET_NUMBER = 10

# Action
ACTION_RETWEET = 'RETWEET'
ACTION_UNRETWEET = 'UNRETWEET'


async def lookup_and_retweet(query, last_retweet_id):
    cursor = simple_search(query, last_retweet_id)
    tasks = __create_tasks(cursor, ACTION_RETWEET)
    results = await asyncio.gather(*tasks)
    return list(itertools.chain(*results))


async def lookup_and_unretweet(query):
    cursor = simple_search(query)
    tasks = __create_tasks(cursor, ACTION_UNRETWEET)
    results = await asyncio.gather(*tasks)
    return list(itertools.chain(*results))


def simple_search(query, since_id=None):
    return tweet_consumer.search(query, since_id)


def get_latest_retweetable_tweet(tweets):
    tweets = list(filter(__can_retweet, [t for t in tweets if t]))
    if tweets:
        tweets.sort(key=lambda t: t.id, reverse=True)
        return tweets[0]


def __create_tasks(cursor, action):
    tasks = []
    for page in cursor.pages():
        print('{} tweets found'.format(len(page)))
        batches = __chunks(page, MAX_TWEET_NUMBER)
        tasks = [asyncio.create_task(__do_action(b, action)) for b in batches]
    return tasks


async def __do_action(tweets, action):
    retweeted = []
    for tweet in tweets:
        if ACTION_RETWEET == action:
            if __can_retweet(tweet):
                print('Tweeting tweet {} of user {}'.format(tweet.text, tweet.user.screen_name))
                retweeted.append(tweet_consumer.retweet(tweet))
            else:
                print('Tweet {} of user {} does not meet the prerequisites to be retweet'
                      .format(tweet.text, tweet.user.screen_name))
        elif ACTION_UNRETWEET == action:
            retweeted.append(tweet_consumer.unretweet(tweet))
    return retweeted


def __can_retweet(tweet):
    return user_consumer.is_following_me(tweet.user) and tweet.in_reply_to_status_id is None


def __chunks(iterable, n):
    for i in range(0, len(iterable), n):
        yield iterable[i:i + n]
