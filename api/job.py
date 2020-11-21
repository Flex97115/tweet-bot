import os

import business.service.tweet_service as tweet_service
import business.service.config_service as config_service
import business.mapper.tweet_mapper as tweet_mapper
from starlette.responses import JSONResponse
from starlette.responses import Response

# As security, to control what will be retweet, save retweet query in env
tweet_query = os.getenv("TWEET_QUERY")


async def retweet_job(request):
    last_retweet_id = config_service.get_last_retweet_id()
    tweets = await tweet_service.lookup_and_retweet(tweet_query, last_retweet_id)
    # Save last tweet id
    last_tweet = tweet_service.get_latest_retweetable_tweet(tweets)
    if last_tweet:
        config_service.set_last_retweet_id(last_tweet.id)
    return JSONResponse(list(map(tweet_mapper.to_json, tweets)))


async def unretweet_job(request):
    tweets = await tweet_service.lookup_and_unretweet(tweet_query)
    return JSONResponse(list(map(tweet_mapper.to_json, tweets)))


async def initialise_job(request):
    cursor = tweet_service.simple_search(tweet_query)
    last_tweet = tweet_service.get_latest_retweetable_tweet(cursor.items())
    if last_tweet:
        config_service.set_last_retweet_id(last_tweet.id)
        return JSONResponse(last_tweet._json)
    response = Response('Not found', status_code=404)
    return response
