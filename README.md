# triller-bot
A small module to communicate with Triller's API.
I plan to add more features/methods in the future.

*`I do not have any affiliation with Triller and hold no responsibility for ANYTHING caused by using this module.`*

----

## Basic Usage:
#### Initialize the Triller Object
> `triller = Triller(username, password, suppress_output=False)`

#### Login to Triller
> `triller.login()`
----
## Methods:
#### Triller.get_user()
> `triller.get_user(username|user_id)` | Returns a dictionary with the user's info.

#### Triller.get_user_videos()
> `triller.get_user_videos(username|user_id)` | Returns a list of dictionaries with the user's videos.

#### Triller.comment()
> `triller.comment(post_id, comment)` | Returns comment object or None

#### Triller.follow()
> `triller.follow(username|user_id)` | Returns True or False, depending on success.

#### Triller.unfollow()
> `triller.unfollow(username|user_id)` | Returns True or False, depending on success.