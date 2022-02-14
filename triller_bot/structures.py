class Auth:
    
    class general:
        token = None # Token for general authentication
        
    class live:
        result = None # JSON result of the Live Auth request;

class Me(object):
    def __init__(self):
        self.id       = None
        self.username = None
        self.auth     = Auth
        
class HTTP_Request:
       
    class Login:
        uri = "https://social.triller.co/v1.5/user/auth"
        headers = {
            "origin": "https://triller.co",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"
        }
        class Live:
            uri = "https://api.live.triller.co/_ah/api/halogen/v1/auth/triller"
            
    base_uri = "https://social.triller.co"
             