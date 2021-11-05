import os
import pickle
import uuid


def chunk_data(data_filepath, name):
    if not os.path.exists("chunks/"):
        os.makedirs("chunks/")
    filepath = f"chunks/{name}/"
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    data = {}
    chunks = {}
    chunks_txt = 'Chuncks:\n'

    # load data
    try:
        with open(data_filepath, 'rb') as f:
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
