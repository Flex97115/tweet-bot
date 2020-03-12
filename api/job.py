import business.service.tweet_service as tweet_service
from starlette.responses import JSONResponse


async def retweet_job(request):
    query = request.query_params['q']
    results = await tweet_service.lookup_and_retweet(query)
    return JSONResponse(results)


async def unretweet_job(request):
    query = request.query_params['q']
    results = await tweet_service.lookup_and_unretweet(query)
    return JSONResponse(results)
