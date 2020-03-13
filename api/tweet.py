import business.service.tweet_service as tweet_service
import business.mapper.tweet_mapper as tweet_mapper
from starlette.responses import JSONResponse


async def search(request):
    query = request.query_params['q']
    cursor = tweet_service.simple_search(query)
    tweets = tweet_mapper.flatten_cursor(cursor)
    return JSONResponse(list(map(tweet_mapper.to_json, tweets)))
