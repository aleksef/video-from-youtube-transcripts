import os
import argparse
import pickle
import pafy

from youtube_transcript_api import YouTubeTranscriptApi

from search import search_videos


# Load data file if it exists
data = {}
try:
    with open('data/data.pickle', 'rb') as f:
        data = pickle.load(f)
    print('📙 Data file loaded.')
except FileNotFoundError:
    # mkdir
    if not os.path.exists("data/"):
        os.makedirs("data/")
    print('⚠️ Data file not found. Proceeding...')


def collect_data(options):
    parsed_amount = 0
    next_token = ''
    print('Starting to parse videos...')
    while parsed_amount < args.amount:
        # Search videos
        search_response = search_videos(search_string=args.search_string,
                                        pageToken=next_token,
                                        order=args.order,
                                        videoLicense=args.license)
        next_token = search_response.get('nextPageToken', [])
        items = search_response.get('items', [])
        if not items:
            print('😅 Found nothing for your request.')
            break

        for i, search_result in enumerate(items):
            print(f"Parsing video {i}/{len(items)}")
            if parsed_amount == args.amount:
                break
            if search_result['id']['videoId'] in data:
                print("👌 Video already exists. 👌")
                parsed_amount += 1
                continue
            if search_result['id']['kind'] == 'youtube#video':
                v_id = search_result['id']['videoId']
                video = None
                try:
                    video = pafy.new(v_id)
                except BaseException:
                    print("🤔 Its probably Pafy's fault.")
                    continue
                duration_sec = video.length

                if duration_sec < args.sec:
                    try:
                        trs = YouTubeTranscriptApi.get_transcripts(
                            [v_id],
                            languages=['en'])
                        transcripts = next(iter(trs[0].values()))
                        # update data dict
                        data.update(
                            {v_id:
                                {'filepath': '',
                                 'transcripts': transcripts,
                                 }})
                        print('👌 Got transcripts! 👌')
                        # save
                        with open('data/data.pickle', 'wb') as f:
                            pickle.dump(data, f)
                        parsed_amount += 1
                    except BaseException:
                        print('🤔 No transcripts :(')
                else:
                    print('🤔 Video is too long.')
            else:
                print('🤔 Not a video?')
        if not next_token:
            break
        print('Parsing next page')
    print(f"Finished parsing. Got transcripts from {parsed_amount} videos.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search and collect data.')
    parser.add_argument(
        '--amount',
        type=int,
        default=5,
        help='Amount od videos to parse(default: 5)'
    )
    parser.add_argument(
        '--sec',
        type=int,
        default=60,
        help='Video max length in seconds (default: 60)'
    )
    parser.add_argument(
        '--search_string',
        type=str,
        default="fun",
        help='Search string (default="fun")'
    )
    parser.add_argument(
        '--order',
        type=str,
        default="rating",
        help='Set order (default="rating")'
    )
    parser.add_argument(
        '--license',
        type=str,
        default="youtube",
        help='Set license type (default="youtube")'
    )
    args = parser.parse_args()

    try:
        collect_data(args)
    except BaseException as e:
        print('An error %d occurred:\n%s' % (e.resp.status, e.content))
