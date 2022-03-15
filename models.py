from typing import Callable, List
import json

# https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.videos.html#list

DOMAIN = "https://youtu.be/"


class Channel:
    """Represents a youtube channel"""

    def __init__(self, channel_id, title):
        self.channel_id = channel_id
        self.title = title

    def __str__(self) -> str:
        return self.title

    def link(self) -> str:
        """
        Generates a direct link to this youtube channel
        """
        return DOMAIN + self.channel_id


class Thumbnail:
    """Represents the thumbnail for a youtube video"""

    def __init__(self, url, height, width):
        self.url = url
        self.height = height
        self.width = width


class Video:
    """Represents a youtube video"""

    def __init__(self, data_dict):
        self.video_id = data_dict['id']
        snippet = data_dict['snippet']
        self.channel = Channel(snippet['channelID'], snippet['channelTitle'])
        self.title = snippet['title']
        self.description = snippet['description']
        self.thumbnail = Thumbnail(**snippet['thumbnails']['maxres'])
        self.duration = data_dict['contentdetails']['duration']
        self.viewcount = data_dict['statistics']['viewcount']

    def __str__(self) -> str:
        return self.title

    def link(self) -> str:
        """
        Generates a direct link to this youtube video
        """
        return DOMAIN + self.video_id


class Playlist:
    """
    Represents a list of videos
    """

    def __init__(self):
        self.playlist_id = ""
        self.videos = []


    def from_json(self, path: str, youtube):
        """
        Loads in this playlist from a json file
        """
        with open(path, 'r', encoding="UTF-8") as input_file:
            playlist_dict = json.loads(input_file.read())
        self.playlist_id = playlist_dict["playlist_id"]
        self.videos = self.fetch_videos(playlist_dict["video_ids"], youtube)
        return self


    def from_playlist_id(self, playlist_id: str, youtube):
        """
        Initializes this playlist from the playlist id
        """
        self.playlist_id = playlist_id
        pl_response = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id
        ).execute()

        video_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]

        self.videos = self.fetch_videos(video_ids, youtube)
        return self


    def fetch_videos(self, video_ids: List[str], youtube) -> List[Video]:
        """
        Fetches all videos from the given list of ids
        """
        video_dicts = youtube.videos().list(
            part="snippet,statistics",
            id=','.join(video_ids)).execute()['items']

        return [Video(video_dict) for video_dict in video_dicts]


    def export(self, path: str):
        """
        Exports the given list of Videos to JSON
        """
        output_dict = {"playlist_id" : self.playlist_id,
                       "videos_ids" : [video.video_id for video in self.videos]}

        with open(path, 'w', encoding="UTF-8") as output_file:
            output_file.write(json.dumps(output_dict))


    def __iter__(self) -> Video:
        for video in self.videos:
            yield video


    def sort_by(self, param: str, descending_order: bool = False):
        """
        Sorts the given playlist by the given parateter
        """
        self.videos.sort(key=lambda vid: vid[param], reverse=descending_order)


    def matches(self, predicate) -> List[Video]:
        """
        Returns all videos that match the given search predicate
        """
        return [video for video in self.videos if predicate(video)]


class Predicate:
    """
    Represents a search predicate
    """
    name_startswith = lambda x: x.title.startswith

    def create_title_startswith(self, string: str) -> Callable:
        """
        Creates a predicate that matches videos whose title starts with the given string
        """
        return lambda x: x.title.lower().startswith(string.lower())


    def create_title_contains(self, string: str) -> Callable:
        """
        Creates a predicate that matches videos whose title contains the given string
        """
        return lambda x: string.lower() in x.title.lower()


    def create_title_endswith(self, string: str) -> Callable:
        """
        Creates a predicate that matches videos whose title ends with the given string
        """
        return lambda x: x.title.lower().endswith(string.lower())


    def create_channel_matches(self, string: str) -> Callable:
        """
        Creates a predicate that matches videos whose channel name matches the given string
        """
        return lambda x: x.channel.name.lower() == string.lower()


    def create_longer_than(self, length: int) -> Callable:
        """
        Creates a predicate that matches videos whose length is at least as long as the given value
        """
        return lambda x: x.length >= length


    def create_shorter_than(self, length: int) -> Callable:
        """
        Creates a predicate that matches videos whose length is no greater than the given value
        """
        return lambda x: x.length <= length


    def create_and(self, predicates: List[Callable]) -> Callable:
        """
        Creates a predicate that matches videos who satisfy all the given predicates
        """
        return lambda x: all(predicate(x) for predicate in predicates)


    def create_or(self, predicates: List[Callable]) -> Callable:
        """
        Creates a predicate that matches videos who satisfy at least one of the given predicates
        """
        return lambda x: any(predicate(x) for predicate in predicates)


    def create_xor(self, predicate1: Callable, predicate2: Callable) -> Callable:
        """
        Creates a predicate that matches videos who satisfy one but not both of the given predicates
        """
        return lambda x: predicate1(x) != predicate2(x)




"""
"snippet":
    "channelId": "A String", # The ID that YouTube uses to uniquely identify the channel that the video was uploaded to.
    "channelTitle": "A String", # Channel title for the channel that the video belongs to.
    "description"
    "thumbnails":
        "maxres":
            "height"
            "url"
            "width"
    "title"
"contentdetails":
    "duration"
"statistics":
    "viewCount"
"""