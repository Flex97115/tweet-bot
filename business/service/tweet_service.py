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


def get_latest(tweets):
    tweets = [t for t in tweets if t]
    if tweets:
        tweets.sort(key=lambda t: t.id, reverse=True)
        return tweets[0]


def __create_tasks(cursor, action):
    for page in cursor.pages():
        print('{} tweets found'.format(len(page)))
        batches = __chunks(page, MAX_TWEET_NUMBER)
        return [asyncio.create_task(__do_action(b, action)) for b in batches]


async def __do_action(tweets, action):
    retweeted = []
    for tweet in tweets:
        if ACTION_RETWEET == action:
            if user_consumer.is_following_me(tweet.user) and not hasattr(tweet, 'retweeted_status'):
                print('User {} is a follower execute retweet'.format(tweet.user.screen_name))
                retweeted.append(tweet_consumer.retweet(tweet))
            else:
                print('User {} isnt a follower cannot retweet or tweet {} is a retweet'.format(tweet.user.screen_name, tweet.text))
        elif ACTION_UNRETWEET == action:
            retweeted.append(tweet_consumer.unretweet(tweet))
    return retweeted


def __chunks(iterable, n):
    for i in range(0, len(iterable), n):
        yield iterable[i:i+n]
