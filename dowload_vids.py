import os
import argparse
import uuid
import pafy
import pickle


def download_vids(options):
    # mkdir
    if not os.path.exists("downloaded_vids/"):
        os.makedirs("downloaded_vids/")
    # load data
    try:
        with open(args.filepath, 'rb') as f:
            data = pickle.load(f)
        print('Data file loaded.')
    except FileNotFoundError:
        print('Data file not found.')
        return
    # download videos
    print(f"Files to download: {len(data.keys())}")
    for key in data.keys():
        # check if video is already downloaded
        if os.path.exists(data[key]['filepath']):
            print("File already exists.")
            continue
        # download
        video = pafy.new(key)
        print(video.title)
        try:
            video.getbest().download("downloaded_vids/")
            # rename file
            filename = uuid.uuid1()
            os.rename(f"downloaded_vids/{video.title}.mp4",
                      f"downloaded_vids/{filename}.mp4")
            data[key]['filepath'] = f"downloaded_vids/{filename}.mp4"
            # save data
            with open('data/data.pickle', 'wb') as f:
                pickle.dump(data, f)

        except BaseException:
            print("Download error.")
        finally:
            if not os.path.exists(data[key]['filepath']):
                data[key]['filepath'] = ""
                print("File wasn't downloaded. Maybe try again later?")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download videos from collected data.')
    parser.add_argument(
        '--filepath',
        type=str,
        default='data/data.pickle',
        help='Path to data file'
    )
    args = parser.parse_args()

    try:
        download_vids(args)
    except BaseException as e:
        print(e.content)
