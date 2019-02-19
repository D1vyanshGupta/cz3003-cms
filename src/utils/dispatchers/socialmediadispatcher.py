"""
    Module that dispatches information to social media
"""
from ..pushapis.fb import FacebookAPI
from ..pushapis.twitter import TwitterAPI


class SocialMediaDispatcher:

    """
        Dispatcher for public information to Social Media platforms
    """

    def __init__(self, crisis_update):
        """
            Initiate class with crisis update log object
        """
        self.update = crisis_update

    def construct_message(self):
        """
            Construct message to update public based on crisis update
        """
        return 'Crisis level in %s has been changed to Level %s. Please take care.' % (self.update.district, self.update.new_crisis)

    def dispatch(self):
        """
                Construct update message and dispatch to social media platforms
        """
        try:
            message = self.construct_message()
            # FacebookAPI().push_update(message)
            TwitterAPI().push_update(message)
            return True
        except:
            return False
