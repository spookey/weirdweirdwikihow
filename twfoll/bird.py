from random import choices

from tweepy.error import TweepError

from shared.bird import BaseRobot
from shared.conf import CODES_PASS


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
                if ex.api_code in CODES_PASS:
                    self._log.info('ignoring error: "%s"', ex)
                else:
                    self._log.exception(ex)

    def declutter(self, num_unfollow, num_tofollow):
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

    def stalk(self, num_tofollow, account_name):
        if not account_name:
            self._log.info(
                'no account name to fetch followers from specified. skipping.'
            )
            return True

        account_name = account_name.strip().lstrip('@')
        if not self.safe_get_user(account_name):
            self._log.error(
                'account name "@%s" does not exist', account_name
            )
            return False

        followers = self.api.followers(account_name)
        if not followers:
            self._log.warning(
                'nothing found to follow from "@%s"', account_name
            )
            return False

        num_tofollow = self.number(
            num_tofollow, self.limit('/friendships/incoming')
        )

        foll_ids = list(fol.id for fol in choices(followers, k=num_tofollow))
        self.action(foll_ids, mode=True)

        return True

    def __call__(self, num_unfollow, num_tofollow, account_name):
        if not self.declutter(num_unfollow, num_tofollow):
            return False

        if not self.stalk(num_tofollow, account_name):
            return False

        return True
