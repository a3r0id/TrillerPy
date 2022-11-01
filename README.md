# triller-bot
A small module to control a user-account on Triller (Triller.co).

*```I do not have any affiliation with Triller and hold no responsibility for ANYTHING caused by using this module. This is not an attempt to Adapt, alter, license, sublicense or translate the Platform (Triller/Triller.co) for personal or commercial use. Using this module is against Triller Terms of Service as it is not the intended way to access/use the Triller App/Triller.co platform and may result in legal/disciplinary actions taken against you/your account. This is merely a "proof of concept".```*

----

## Getting Started:

#### Import the Module
> `import triller_bot`

#### Initialize the Triller Object
> `triller = Triller(username, password, suppress_output=False)`
- `username`: Your Triller username.
- `password`: Your Triller password.
- `suppress_output`: Whether or not to suppress the output of the module - typically just the login flow/anomalies will output to the console but this may change in future updates.

#### Log in to Triller
> `triller.login(live_session=False)` | Logs in to Triller.
- `live_session`: If True, api.live.triller.co auth flow will be used as well. This works seamlessly but is disabled by default to add some headroom to the login process. This auth flow is used for granting access to the TrillerTV API as well as the Triller PubNub API.
----
## Methods:
#### Triller.get_user()
> `triller.get_user(username|user_id)` | Returns a dictionary with the user's info.
- `username|user_id`: The username or user_id of the user you want to get info on. `username` should be a string. `user_id` should be an integer.

#### Triller.get_user_videos()
> `triller.get_user_videos(username|user_id, limit=15, before_time=None)` | Returns a list of dictionaries with the user's videos (not live streams).
- `username|user_id`: The username or user_id of the user you want to get videos for. `username` should be a string. `user_id` should be an integer.
- `limit`: The number of videos to return.
- `before_time`: The time to get videos before. Format Ex.: `2020-10-05T01:26:21`

#### Triller.comment()
> `triller.comment(post_id, comment)` | Returns comment object or None
- `post_id`: The post_id of the post you want to comment on.
- `comment`: The comment you want to post.

#### Triller.follow()
> `triller.follow(username|user_id)` | Returns True or False, depending on success.
- `username|user_id`: The username or user_id of the user you want to follow. `username` should be a string. `user_id` should be an integer.

#### Triller.unfollow()
> `triller.unfollow(username|user_id)` | Returns True or False, depending on success.
- `username|user_id`: The username or user_id of the user you want to unfollow. `username` should be a string. `user_id` should be an integer.

#### Triller.recommend(self, page=1, limit=15)
> `triller.recommend(page=1, limit=15)` | Returns a list of dictionaries with the recommended users to follow.
- `page`: The page of results to return.
- `limit`: The number of results to return.

#### Triller.feed(self, limit=15)
> `triller.feed(limit=15)` | Returns a list of dictionaries with the YOUR feed.
- `limit`: The number of results to return.
----

## __Live (TrillerTV) API__:

##### *Enable live session - Work in progress*
`triller.login(live_session=True)`

----

## Live Methods:

**Work in progress*

#### Triller.Live.public_live_feed()
> `triller.Live.public_live_feed()` | Returns a list of dictionaries with the public live feed. This is not authed and will return some popular public live streams that are currently running.

#### Triller.Live.public_scheduled_feed()
> `triller.Live.public_scheduled_feed()` | Returns a list of dictionaries with the public scheduled feed. This is not authed and will return some popular public scheduled streams.

#### Triller.Live.balance()
> `triller.Live.balance()` | Returns a dictionary with your "Triller Coin" balance.

#### Triller.Live.stream()
> `triller.Live.stream(stream_id)` | Returns a [Stream Object](#stream-object).
- `stream_id`: The stream_id of the stream you want to get info on.`stream_id` should be a string.

----

## Triller Utilities

#### Import Triller Utilities
> `from triller_bot.utils import Utils`

#### Triller.Live.Utils.download()
> `triller.Live.Utils.download(url, filename)` | Simply Downloads a file from a url and saves it to the given filename. Returns True or False, depending on success.


----

## Stream Object:

#### Triller.stream.Stream(object)

> *Create a Stream Object by calling [`Triller.Live.stream(stream_id)`](#trillerlivestream).*

### Stream Object Properties:
- `Stream.info` | A dictionary with the stream's info.
- `Stream.creator` | A dictionary with the stream's creator's info.

### Stream Object Methods:
#### Stream.get_chat_messages() 
> `Stream.get_chat_messages(limit=128, filter_users_not_joined=False)` | Returns a list of dictionaries with the chat's messages.
- `limit`: The number of messages to return.
- `filter_users_not_joined`: If True, only messages from users that are currently in the stream will be returned.

#### Stream.get_m3u8()
> `Stream.get_m3u8()` | Returns a dictionary with the stream's m3u8 url.

Sets then returns the stream's [M3u8 Object](https://pypi.org/project/m3u8/). See the linked library for documentation on the M3u8 Object.

**Work in progress*












