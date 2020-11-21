from starlette.routing import Route
import api.tweet as tweet_api
import api.job as job_api
import api.default as default_api

routes = [
    # Default API
    Route('/', default_api.homepage),
    Route('/health-check', default_api.health_check),

    # Tweet API
    Route('/tweet/search', tweet_api.search),
    Route('/tweet/since-search', tweet_api.since_search),

    # Job API
    Route('/job/init', job_api.initialise_job, methods=["POST"]),
    Route('/job/retweet', job_api.retweet_job, methods=["POST"]),
    Route('/job/unretweet', job_api.unretweet_job, methods=["POST"])
]
