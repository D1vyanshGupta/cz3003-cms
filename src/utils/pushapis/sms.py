"""
    SMS API
"""
from twilio.rest import Client

class TwilioAPI:

    def push_update(self, message, phonenumber):
        try:
            ACCOUNT_SID = "AC71b92a1c39db3d9e19594c06927fcea5"
            AUTH_TOKEN = "55a8c21532f5678598264ca990409b6b"
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            client.messages.create(
                to=phonenumber,
                # from_="+15403393178",
                from_="+12059003909",
                body=message
            )
            return True
        except Exception as e:
            print(e)
            return False
