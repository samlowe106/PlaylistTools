from typing import Dict

# https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.videos.html#list

DOMAIN = "https://youtu.be/"

class Channel:
    """Represents a youtube channel"""

    def __init__(self, id, title):
        self.id = id
        self.title = title

    def __str__(self) -> str:
        return self.title

    def link(self) -> str:
        return DOMAIN + self.id

class Thumbnail:
    """Represents the thumbnail for a youtube video"""

    def __init__(self, url, height, width):
        self.url = url
        self.height = height
        self.width = width

class Video:
    """Represents a youtube video"""

    def __init__(self, data_dict):
        self.id = data_dict['id']
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
        return DOMAIN + self.id


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