import business.service.tweet_service as tweet_service
import business.service.config_service as config_service
import business.mapper.tweet_mapper as tweet_mapper
from starlette.responses import JSONResponse


async def retweet_job(request):
    query = request.query_params['q']
    last_retweet_id = config_service.get_last_retweet_id()
    tweets = await tweet_service.lookup_and_retweet(query, last_retweet_id)
    # Save last tweet id
    last_tweet = tweet_service.get_latest(tweets)
    if last_tweet:
        config_service.set_last_retweet_id(last_tweet.id)
    return JSONResponse(list(map(tweet_mapper.to_json, tweets)))


async def unretweet_job(request):
    query = request.query_params['q']
    tweets = await tweet_service.lookup_and_unretweet(query)
    return JSONResponse(list(map(tweet_mapper.to_json, tweets)))
