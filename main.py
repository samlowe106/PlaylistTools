import os
import uvicorn
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from googleapiclient.discovery import build
from PlaylistTools.models import Playlist


API_KEY = os.environ.get('API_KEY')

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# https://fastapi.tiangolo.com/advanced/templates/

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Root page
    """
    return templates.TemplateResponse("page.html", {"message": "Hello World"})

YOUTUBE = None

@app.post("/", response_class=HTMLResponse)
def root_post(request: Request, playlist: str = Form(...), file: UploadFile = File(...)):
    """
    Root page post request
    """
    return templates.TemplateResponse("page.html", {"message": "Hello World"})


def main():
    """
    Main function
    """

    with build('youtube', 'v3', developerKey=API_KEY) as YOUTUBE:
        playlist_id = ''

        playlist = Playlist().from_playlist_id(playlist_id, YOUTUBE)




if __name__ == "__main__":
    uvicorn.run(app)