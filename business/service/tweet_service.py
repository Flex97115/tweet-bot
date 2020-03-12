from business.consumer.user_consumer import UserConsumer
from business.consumer.tweet_consumer import TweetConsumer
import asyncio
import itertools

tweet_consumer = TweetConsumer()
user_consumer = UserConsumer()


MAX_TWEET_NUMBER = 4

# Action
ACTION_RETWEET = 'RETWEET'
ACTION_UNRETWEET = 'UNRETWEET'


async def lookup_and_retweet(query):
    tasks = __create_tasks(query, ACTION_RETWEET)
    results = await asyncio.gather(*tasks)
    return list(itertools.chain(*results))


async def lookup_and_unretweet(query):
    tasks = __create_tasks(query, ACTION_UNRETWEET)
    results = await asyncio.gather(*tasks)
    return list(itertools.chain(*results))


def simple_search(query):
    return tweet_consumer.search(query)


def __create_tasks(query, action):
    results = tweet_consumer.search(query)
    statuses = results['statuses']
    print('{} tweets found'.format(len(statuses)))
    batches = __chunks(statuses, MAX_TWEET_NUMBER)
    return [asyncio.create_task(__do_action(b, action)) for b in batches]


async def __do_action(tweets, action):
    retweeted = []
    for tweet in tweets:
        if ACTION_RETWEET == action:
            if user_consumer.is_following_me(tweet['user']):
                print('User {} is a follower execute retweet'.format(tweet['user']['screen_name']))
                retweeted.append(tweet_consumer.retweet(tweet))
            else:
                print('User {} isnt a follower cannot retweet'.format(tweet['user']['screen_name']))
        elif ACTION_UNRETWEET == action:
            retweeted.append(tweet_consumer.unretweet(tweet))
    return retweeted


def __chunks(iterable, n):
    for i in range(0, len(iterable), n):
        yield iterable[i:i+n]
