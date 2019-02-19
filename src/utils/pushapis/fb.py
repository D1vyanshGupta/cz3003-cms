"""
    FB API
"""

import facebook


class FacebookAPI:

    def push_update(self, message):
        try:
            page_id = '805386113142326'
            page_access_token = 'EAAIQxUVl6hYBAD5uZBujwUGuRAqzSRpxe9nBD86xGakdRLrCmZBtbTKpW3O63OXPwomJKVcaqyAk1sVpjGOpOr6hK2IDtXDbLsqa0c5F0SwPK1dr0JHZANUWpIZC78aakmibI6mZAWcyZCncTTDAFLlyFi5sZACV1JqiPCL3G8f4VhTrvkD40JDVGhDZCllSzNv7q0r67phJ9Ru3VZCMbfGBM'
            graph = facebook.GraphAPI(page_access_token)
            graph.put_object(parent_object='805386113142326', connection_name='feed', message=message)
            return True
        except Exception as e:
            print (e)
            return False

# fb = FacebookAPI()
# fb.pushUpdate("Testing again")
