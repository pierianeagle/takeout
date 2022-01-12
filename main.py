# %%

import os
import sys
import requests

import pandas as pd

from bs4 import BeautifulSoup, SoupStrainer

from backoff import retry

# %%

@retry
def get_video_name(id: str):
    url = f'https://youtube.com/watch?v={id}'

    try:
        res = requests.get(url)
        res.raise_for_status()
    except:
        raise

    soup = BeautifulSoup(
        res.content,
        'lxml',
        parse_only=SoupStrainer('title')
    )

    if soup.title is not None:
        return soup.title.string
    return 'Video Deleted'

# %%

if __name__ == '__main__':
    path = sys.argv[1]

    # reads data
    df = pd.read_csv(path, header=2)

    # probably should write in chunks
    df['Title'] = df['Video ID'].apply(lambda id: get_video_name(id))

    # remove metadata
    df.to_csv(path, index=False)
