from typing import List
import json
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from googleapiclient.discovery import build
from PlaylistTools.models import Video


API_KEY = os.environ.get('API_KEY')

search_predicates = ('views', 'title')

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# https://fastapi.tiangolo.com/advanced/templates/

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Root page
    """
    return templates.TemplateResponse("page.html", {"message": "Hello World"})

YOUTUBE = None


def main():
    """
    Main function
    """
    with build('youtube', 'v3', developerKey=API_KEY) as YOUTUBE:
        playlist_id = '' # get from user

        videos = playlist_to_videos(playlist_id)


def sort_playlist_by(videos: List[str], param: str, descending_order: bool = False):
    """
    Sorts the given playlist by the given parateter
    """
    videos.sort(key=lambda vid: vid[param], reverse=descending_order)


def export_playlist(playlist: List[Video], path: str):
    """
    Exports the given list of Videos to JSON
    """
    with open(path, 'w', encoding="UTF-8") as output_file:
        output_file.write(json.dumps(video.id for video in playlist))


def import_playlist(path) -> List[Video]:
    """
    Imports a list of Videos from a file
    """
    with open(path, 'r', encoding="UTF-8") as input_file:
        return ids_to_videos(json.loads(input_file.read()))


def ids_to_videos(video_ids: List[str]) -> List[Video]:
    """
    Returns a list of videos based on the given list of ids
    """

    video_dicts = YOUTUBE.videos().list(
        part="snippet,statistics",
        id=','.join(video_ids)).execute()['items']

    return [Video(video_dict) for video_dict in video_dicts]

def playlist_to_videos(playlist_id: str) -> List[Video]:
    """
    Takes the given playlist id and returns a list of Videos
    representing each video in the playlist
    :param playlist_id: id of a youtube playlist
    :return: a list of Videos representing each video in the playlist
    """
    return ids_to_videos(playlist_to_ids(playlist_id))


def playlist_to_ids(playlist_id: str) -> List[str]:
    """

    :return: a list of dictionaries; each dictionary represents info about a video
    """

    pl_response = YOUTUBE.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id
    ).execute()

    return [item['contentDetails']['videoId'] for item in pl_response['items']]


if __name__ == "__main__":
    main()