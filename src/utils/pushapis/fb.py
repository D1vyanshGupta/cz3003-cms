"""
    FB API
"""

import facebook


class FacebookAPI:

    def push_update(self, message):
        try:
            page_id = "197027533999861"
            page_access_token = "CAAYtJqL3ZAO8BAA0hzU5NNlNUxZCEgVXubfWTl4oxOgb5IaR9GhKq4DGMHWbFvvfXMLihMd3S8VAPCOtLOsRxX8sg5rAxAcML7aEQyC5r38l7ZCDPSJqRULIxA6lnR6eZBgZCbPZCQo1Nw3MzaJN1KO8s3SfVeGZBAKVUJPFBNNwcfek8PgiHEhg71T8facNmwZD"
            graph = facebook.GraphAPI(page_access_token)
            attachment = {}
            graph.put_wall_post(message, attachment=attachment)
            return True
        except Exception as e:
            print (e)
            return False

# fb = FacebookAPI()
# fb.pushUpdate("Testing again")
