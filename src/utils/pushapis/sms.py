"""
    SMS API
"""
from twilio.rest import TwilioRestClient


class TwilioAPI:

    def push_update(self, message, phonenumber):
        try:
            ACCOUNT_SID = "AC70d34cdf60361f90def6d53941f7e50b"
            AUTH_TOKEN = "7d7c563de4b9c7eb0faf618dddd74e49"
            client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
            client.messages.create(
                to=phonenumber,
                from_="+15403393178",
                body=message
            )
            return True
        except:
            return False
