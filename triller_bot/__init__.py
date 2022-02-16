from requests    import post, get
from threading   import Thread

from .structures import HTTP_Request, Me
from .checkin    import checkinWorker
from .live       import Live as LiveObject

class Triller(object):
    def __init__(self, username, password, suppress_output=False, check_in_interval_seconds=600):
        self.username        = username
        self.password        = password
        self.suppress_output = suppress_output
        self.me              = Me()
        self.user            = None
        
        self.isLiveSession   = False
        
        self.check_in_interval_seconds = check_in_interval_seconds
        self.checkin_thread  = Thread(target=checkinWorker, args=(self,))
                
        Live                 = None       
        
    def log(self, message):
        if not self.suppress_output:
            print(message)
        
    def login(self, live_session=False):

        r = post(HTTP_Request.Login.uri, json={"username": self.username, "password": self.password}, headers=HTTP_Request.Login.headers)

        login = r.json()        
                
        if login["status"]:
            self.me.auth.general.token = login["auth_token"]
            self.user                  = login["user"]
            if not self.suppress_output:            
                self.log(f"[+] Login Successful - Code: {login['code']}")
                self.log(f"[+] Logged in as: {self.user['username']}")
                self.checkin_thread.start()
                self.log(f"[+] Check-in thread started")
        else:
            if not self.suppress_output:            
                self.log(f"[-] Login Failed - Code:  {r.status_code}")
            return False
                
        if live_session:
            r = post(HTTP_Request.Login.Live.uri, json={"accessToken": self.me.auth.general.token, "devicePlatform": "web"}, headers=HTTP_Request.Login.headers)
            try:
                result = r.json()
                if not result["success"]:
                    if not self.suppress_output:            
                        self.log(f"[-] Live Login Failed - Code: {r.status_code}")
                    return False
                del result["success"]
                self.me.auth.live.result = result["result"]
                    
                    
                if not self.suppress_output:
                    self.log(f"[+] Live Session Successful - Code: {r.status_code}")
            except:
                if not self.suppress_output:                
                    self.log(f"[-] Live Login Failed - Code: {r.status_code}")
                return False
            self.isLiveSession = True
            self.Live = LiveObject(self)
        return True
                
    def comment(self, post_id, comment):
        """
        Returns comment object or None
        """
        r = post(
            HTTP_Request.base_uri + f"/v1.5/api/videos/{post_id}/comments",
            json={"body": comment},
            headers={"Authorization": f"Bearer {self.me.auth.general.token}"}
        )
        if r.status_code == 200:
            return r.json()
        else:
            return None
      
    def get_user(self, user):
        """
        Returns user object or None
        """        
        if type(user) == int:
            uri = HTTP_Request.base_uri + f"/v1.5/api/users/{user}"
        elif type(user) == str:
            uri = HTTP_Request.base_uri + f"/v1.5/api/users/by_username/{user}"
        else:
            raise TypeError("get_user() -> Error: user argument must be a user-id (int) or username (str)")    
        
        r = get(uri, headers={"Authorization": f"Bearer {self.me.auth.general.token}"})
        
        if r.status_code == 200:
            result = r.json()
            if result["status"]:
                return r.json()["user"]

        return None
    
    def get_user_videos(self, user, limit=15, before_time=None):
        """
        Returns list of videos by user or None
        - before_time: timestamp - ex: 2020-10-05T01:26:21
        """
        if type(user) == int:
            user_id = str(user)
        elif type(user) == str:
            user_id = self.get_user(user)["user_id"]
        else:
            raise TypeError("get_user_videos() -> Error: user argument must be a user-id (int) or username (str)") 
        
        before_time = "&before_time=" + str(before_time) if before_time else ""
        
        uri = HTTP_Request.base_uri + f"/v1.5/api/users/{user_id}/videos?limit={limit}{before_time}"

        r = get(uri, headers={"Authorization": f"Bearer {self.me.auth.general.token}"})
        
        if r.status_code == 200:
            result = r.json()
            if result["status"]:
                return r.json()["videos"]
    
        return None
    
    def follow(self, user):
        """
        Returns True if successful, False if not
        """        
        if type(user) == int:
            pass
        elif type(user) == str:
            user_id = self.get_user(user)["user_id"]
        else:
            raise TypeError("follow() -> Error: user argument must be a user-id (int) or username (str)")             
        r = post(
            HTTP_Request.base_uri + "/v1.5/api/users/follow",
            json={"follower_id":self.user["user_id"], "followed_ids":[user_id]},
            headers={"Authorization": f"Bearer {self.me.auth.general.token}"}
        )
        if r.status_code == 200:
            result = r.json()
            if result["status"] and str(user_id) in result["followed_by_me"]:
                return result["followed_by_me"][str(user_id)] == "true"
        return False
    
    def unfollow(self, user):
        """
        Returns True if successful, False if not
        """
        if type(user) == int:
            pass
        elif type(user) == str:
            user_id = self.get_user(user)["user_id"]
        else:
            raise TypeError("unfollow() -> Error: user argument must be a user-id (int) or username (str)")             
        r = post(
            HTTP_Request.base_uri + "/v1.5/api/users/follow/delete",
            json={"follower_id":self.user["user_id"], "followed_ids":[user_id]},
            headers={"Authorization": f"Bearer {self.me.auth.general.token}"}
        )
        if r.status_code == 200:
            result = r.json()
            if result["status"]:
                return True
        return False
            
    # New
    def recommend(self, page=1, limit=15):
        """
        Returns list of recommended profiles or None
        """
        r = get(HTTP_Request.base_uri + "/v1.5/api/users/follow/recommend?page={}&limit={}".format(page, limit), headers={"Authorization": f"Bearer {self.me.auth.general.token}"})
        
        if r.status_code == 200:
            result = r.json()
            if result["status"]:
                return result["profiles"]
            
        return None
    
    # New
    def feed(self, limit=15):
        """
        Returns {videos: [{}, ...], users: [{}, ...]} from feed or None
        """
        r = get(
            HTTP_Request.base_uri + f"/v1.5/api/users/{self.user['user_id']}/feed?limit={limit}", 
            headers={"Authorization": f"Bearer {self.me.auth.general.token}"})
        if r.status_code == 200:
            result = r.json()
            if result["status"]:
                return dict(
                    users = result["users"],
                    videos = result["videos"]
                )
        return None
    
    
    
