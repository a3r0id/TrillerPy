from time import sleep
from requests import post
from threading import enumerate as threading_enumerate

from .structures import HTTP_Request

def check_in(self):
    r = post(
        HTTP_Request.base_uri + "/v1.5/user/checkin",
        headers={"Authorization": f"Bearer {self.me.auth.general.token}"}
    )
    if r.status_code == 200:
        result = r.json()
        if result["status"]:
            # Updates the token and user-object
            self.user                  = result["user"]
            self.me.auth.general.token = result["auth_token"]
            self.log(f"[+] Checked in! {self.user['username']}")

def checkinWorker(self):
    try:        
        while True:
            seconds_passed = 0
            while True:
                sleep(1)
                seconds_passed += 1
                if seconds_passed == self.check_in_interval_seconds:
                    check_in(self)
                    break
                if "MainThread" not in threading_enumerate():
                    exit(0)
                            
    except KeyboardInterrupt:
        exit()
    except SystemExit:
        exit()
        
