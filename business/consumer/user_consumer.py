from business.consumer.api_consumer import ApiConsumer


class UserConsumer(ApiConsumer):

    def user_by_name(self, name):
        return self._api.get_user(screen_name=name)

    def is_following_me(self, user):
        me = self._api.me()
        friendship = self._api.show_friendship(source_id=me['id'], target_id=user['id'])
        source = friendship['relationship']['source']
        return source['followed_by']