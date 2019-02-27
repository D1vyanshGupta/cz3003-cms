"""
    FB API
"""

import facebook


class FacebookAPI:

    def push_update(self, message):
        try:
            page_id = '805386113142326'
            page_access_token = 'EAAIQxUVl6hYBAHciCx0h9u4IRmMAoUGWvvNZAYoOlxTD2h2vRauCSItlpN9D2YI7Qh99rFtbTAHFWUgmoNnxrNmiBPqbuhNul4tfhi5NZA3sJCL6yTd6jABJd4g9ss0HSZBdZCM1FRmKfDuVZCOZCdoNLZBEmbEWAZCn6ZBX1XEooPpnY9TDXVbIA7WA2JkZC0HJIZD'
            graph = facebook.GraphAPI(page_access_token)
            graph.put_object(parent_object='805386113142326', connection_name='feed', message=message)
            return True
        except Exception as e:
            print (e)
            return False

# fb = FacebookAPI()
# fb.pushUpdate("Testing again")
