import json
from googleapiclient.discovery import build


with open('key.json') as f:
    key = json.load(f)

DEVELOPER_KEY = key['dev_key']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def search_videos(search_string, pageToken,
                  order, videoLicense):
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        part="snippet",
        type="video",
        maxResults=500,
        q=search_string,
        pageToken=pageToken,
        order=order,
        videoLicense=videoLicense,
    ).execute()
    return search_response
