import business.service.tweet_service as tweet_service
from starlette.responses import JSONResponse


async def search(request):
    query = request.query_params['q']
    return JSONResponse(tweet_service.simple_search(query))
