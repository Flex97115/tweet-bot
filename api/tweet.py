import business.service.tweet_service as tweet_service
import business.service.config_service as config_service
import business.mapper.tweet_mapper as tweet_mapper
from starlette.responses import JSONResponse


async def search(request):
    query = request.query_params['q']
    cursor = tweet_service.simple_search(query)
    tweets = tweet_mapper.flatten_cursor(cursor)
    return JSONResponse(list(map(tweet_mapper.to_json, tweets)))


async def since_search(request):
    query = request.query_params['q']
    last_retweet_id = config_service.get_last_retweet_id()
    cursor = tweet_service.simple_search(query, last_retweet_id)
    tweets = tweet_mapper.flatten_cursor(cursor)
    return JSONResponse(list(map(tweet_mapper.to_json, tweets)))