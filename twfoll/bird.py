from tweepy.error import TweepError

from shared.bird import BaseRobot


class Robot(BaseRobot):

    @staticmethod
    def number(num, lim):
        num = abs(num)
        return min(num, lim) if num != 0 else lim

    def action(self, user_ids, *, mode):
        func, verb = (
            (self.api.create_friendship, 'followed')
            if mode else
            (self.api.destroy_friendship, 'unfollowed')
        )
        for user_id in user_ids:
            try:
                user = func(user_id)
                self._log.debug(
                    '%s id "%s" %s', verb, user_id, user.name
                )
            except TweepError as ex:
                self._log.exception(ex)

    def __call__(self, num_unfollow, num_tofollow):
        num_unfollow = self.number(
            num_unfollow, self.limit('/friendships/outgoing')
        )
        num_tofollow = self.number(
            num_tofollow, self.limit('/friendships/incoming')
        )

        self._log.debug(
            'will try to unfollow "%d" and follow "%d" accounts',
            num_unfollow, num_tofollow
        )

        following = set(self.api.friends_ids())
        followers = set(self.api.followers_ids())
        self._log.info(
            'following "%d", followers: "%d"',
            len(following), len(followers)
        )
        unfollow = list(following - followers)
        tofollow = list(followers - following)

        self.action(unfollow[:num_unfollow], mode=False)
        self.action(tofollow[:num_tofollow], mode=True)

        return True
