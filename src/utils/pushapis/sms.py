"""
    SMS API
"""
from twilio.rest import Client

class TwilioAPI:

    def push_update(self, message, phonenumber):
        try:
            ACCOUNT_SID = "AC7e5fa7fe8289c8f2babd788bc5fe7e7e"
            AUTH_TOKEN = "6df894e07c5d71127b2654932a082c30"
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            client.messages.create(
                to=phonenumber,
                # from_="+15403393178",
                from_="+15109240350",
                body=message
            )
            return True
        except Exception as e:
            print(e)
            return False
