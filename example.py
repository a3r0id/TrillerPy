from triller_bot import Triller

# Our username and password
username = "USERNAME"
password = "PASSWORD"

# A user to interact with
user     = "donaldjtrump"

# Create a new Triller object
triller  = Triller(username, password)

# Login to the Triller API
triller.login()

# Get the user's timeline (videos)
vids = triller.get_user_videos(user)
for vid in vids:
    print("Found video: {}".format(vid["video_url"]))
    
# Comment on the first video
triller.comment(vids[0]["id"], "Hello World!")
print("Commented on video: {}".format(vids[0]["video_url"]))
    
# Follow the user
triller.follow(user)

# Unfollow the user
#triller.unfollow(user)