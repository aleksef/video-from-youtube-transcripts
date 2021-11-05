import os
import pickle
import argparse
import uuid


def chunk_data(options):
    if not os.path.exists("chunks/"):
        os.makedirs("chunks/")
    filepath = f"chunks/chunks_{uuid.uuid1()}/"
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    data = {}
    chunks = {}
    chunks_txt = 'Chuncks:\n'

    # load data
    try:
        with open(args.filepath, 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        print('⚠️ Data file not found. Stopping script.')
        return

    # parse
    for key in data.keys():
        for transcript in data[key]['transcripts']:
            chunk_id = uuid.uuid1()
            chunks.update({chunk_id:
                          {'text': transcript['text'],
                           'start': transcript['start'],
                           'duration': transcript['duration'],
                           'v_title': data[key]['title'],
                           'v_id': key,
                           'v_filepath': data[key]['filepath'],
                           'c_filepath': '',
                           }})

            with open(f"{filepath}chunks.pickle", 'wb') as f:
                pickle.dump(chunks, f)

            chunks_txt += f"{chunk_id}: {transcript['text']}\n"
            with open(f"{filepath}chunks.txt", "w") as text_file:
                text_file.write(chunks_txt)
    print(f"Done. Chunked data to {filepath}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make chunks from data file.')
    parser.add_argument(
        'filepath',
        type=str,
        help='Search data filepath.'
    )
    args = parser.parse_args()

    try:
        chunk_data(args)
    except BaseException as e:
        print('An error %d occurred:\n%s' % (e.resp.status, e.content))
