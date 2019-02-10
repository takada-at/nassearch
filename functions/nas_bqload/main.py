from google.cloud import bigquery
from google.cloud import storage
from pathlib import Path

import os
import pandas
import tempfile

PROJECT = 'peak-bit-229907'
table_schema = [
    dict(name='title', type='STRING'),
    dict(name='path', type='STRING'),
    dict(name='url', type='STRING'),
]


def pandasload(fileobj):
    client = storage.Client()
    bucket = client.get_bucket(fileobj['bucket'])
    fname = os.path.basename(fileobj['name'])
    blob = bucket.get_blob(fileobj['name'])
    temp = tempfile.NamedTemporaryFile()
    p = Path(temp.name)
    with p.open('wb') as fp:
        blob.download_to_file(fp)
    temp.flush()
    temp.seek(0)
    df = pandas.read_csv(temp.name,
                         names=['title', 'path', 'url'])
    if len(df) <= 1:
        return
    df.to_gbq('nas_data.raw_data',
              if_exists='replace',
              table_schema=table_schema,
              project_id=PROJECT)


def nas_bqload(filedata, eventdata):
    pandasload(filedata)

