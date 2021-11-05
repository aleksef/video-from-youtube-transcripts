import pafy


filename = pafy.new("2lTAVDA0QXc").getbest().download("downloaded_vids/")
# download
# stream = video.getbest()
# filename = stream.download("downloaded_vids/")
# video = youtube.videos().list(
#     part="status, contentDetails",
#     id='%s' % (search_result['id']['videoId'])
# ).execute()
# print(video['items'][0]['status']['license'])