from starlette.applications import Starlette
from route import routes
import os

debug = bool(os.getenv("DEBUG"))

app = Starlette(debug=debug, routes=routes)
