from starlette.responses import Response
from starlette.responses import JSONResponse


async def health_check(request):
    response = Response('Healthy', status_code=200)
    return response


async def homepage(request):
    return JSONResponse({"message": "Welcome in tweet bot app"})
