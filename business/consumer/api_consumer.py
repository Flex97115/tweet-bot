from business.factory import build_api


class ApiConsumer:
    _api = None

    def __init__(self):
        self._api = build_api()
