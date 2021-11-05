from googleapiclient.discovery import build


DEVELOPER_KEY = 'AIzaSyA6f0FazZpLp_AWzg-T_okty0H-d3FcK3E'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def search_videos(search_string, pageToken,
                  order='rating', videoLicense='creativeCommon'):
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        part="snippet",
        type="video",
        maxResults=25,
        q=search_string,
        pageToken=pageToken,
        order=order,
        videoLicense=videoLicense,
    ).execute()
    return search_response
