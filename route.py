from starlette.routing import Route
import api.tweet as tweet_api
import api.job as job_api

routes = [
    # Tweet API
    Route('/tweet/search', tweet_api.search),
    # Job API
    Route('/job/retweet', job_api.retweet_job),
    Route('/job/unretweet', job_api.unretweet_job)
]
