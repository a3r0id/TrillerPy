from .stream import Stream

from requests import get

# Live API Functions
class Live(object):
    
    # Inherit self from base class as $ctx
    def __init__(self, base):
        self.ctx = base
    
    def public_live_feed(self):
        return get("https://api.live.triller.co/_ah/api/halogen/v1/content/public/liveFeed").json()
        
    def public_scheduled_feed(self):
        return get("https://api.live.triller.co/_ah/api/halogen/v1/content/public/scheduledFeed").json()

    def balance(self):
        r = get("https://api.live.triller.co/_ah/api/halogen/v1/purchase/balance",
        headers={
            "X-Halogen-Session-Id": self.ctx.me.auth.live.result["sessionId"],
            "X-Halogen-Session-Secret": self.ctx.me.auth.live.result["sessionSecret"]
        })
        if r.status_code == 200:
            result = r.json()
            if result["success"]:
                del result["success"]
                return result["result"]
        return None
    
    def stream(self, stream_id):
        return Stream(self.ctx, self, stream_id)
       
    """    def get_user_streams(self, user):        
        uri = "/_ah/api/halogen/v1/content/public/userScheduledFeed/1a5479f1-c3b8-467f-be28-880f457daf8a"""