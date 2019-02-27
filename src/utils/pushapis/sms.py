"""
    SMS API
"""
from twilio.rest import Client

class TwilioAPI:

    def push_update(self, message, phonenumber):
        try:
            ACCOUNT_SID = "ACf401eb7dd6f0ba7266721a6cb6fe4bab"
            AUTH_TOKEN = "68fba372d386efdca76bd6d6348381d7"
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            client.messages.create(
                to=phonenumber,
                # from_="+15403393178",
                from_="+19523147416",
                body=message
            )
            return True
        except Exception as e:
            print(e)
            return False
