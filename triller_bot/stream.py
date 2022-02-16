from requests import get, post
import m3u8

class Stream(object):
    def __init__(self, base, live, stream_id):
        self.ctx     = base
        self.live    = live
        
        self.info    = None
        self.infoaux = None
        self.creator = None
        self.m3u8    = None
        
        ## Get stream info
        r = post("https://api.live.triller.co/_ah/api/halogen/v1/post/fetch",       
            headers={
                "X-Halogen-Session-Id": self.ctx.me.auth.live.result["sessionId"],
                "X-Halogen-Session-Secret": self.ctx.me.auth.live.result["sessionSecret"]
            },
            json={
                "consistent": False,
                "postId": stream_id
            })       
        
        if r.status_code == 200:
            result = r.json()
            if result["success"]:
                del result["success"]
                self.info = result["result"]   
                
        if self.info is None:
            return
        
        # Aquire Access to the stream
        r = post("https://api.live.triller.co/_ah/api/halogen/v1/video/chat/acquire_access",
                headers={
                "X-Halogen-Session-Id": self.ctx.me.auth.live.result["sessionId"],  
                "X-Halogen-Session-Secret": self.ctx.me.auth.live.result["sessionSecret"]
                },
                json={
                    "postId": self.info['id']
            })
            
        if r.status_code == 200:
            result = r.json()
            if result["success"]:
                del result["success"]
                self.infoaux = result["result"]
                
        if self.infoaux is None:
            return
        
        ## Get creator's info 
        self.creator = get("https://social.triller.co/v1.5/api/users/by_uuid/" + self.info["creator"]["id"]).json()
        
    def get_m3u8(self):
        ## Fetch m3u8 and initialize m3u8 parser
        self.m3u8 = m3u8.load(self.infoaux["postVideo"]["streamUrl"])    
        return self.m3u8
        
    def get_chat_messages(self, limit=128, filter_users_not_joined=False):
        uri = f"https://api.live.triller.co/_ah/api/halogen/v1/stream/{self.info['id']}/chat_messages?limit={limit}&sort=time_desc" 
        + "&filter=not_users_joined" if filter_users_not_joined else ""    
        r = get(uri, 
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


    """
    def enter_chat(self):
        pn_sub    = self.ctx.me.auth.live.result["pubnubSubscribeKey"]
        stream_id = self.info['id']
        
        uri = f"https://halogen.pubnub.com/v2/presence/sub-key/{pn_sub}/channel/pn.{stream_id}_stream_live/uuid/{?}/data"
            
    """
        
        
        
        
        