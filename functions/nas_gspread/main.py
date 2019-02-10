from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

import csv
import os
import gspread
import tempfile


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


def get_credential():
    temp = tempfile.NamedTemporaryFile()
    gcs('at-auth-data', 'auth/peak-bit-229907-4fd2774d1c42.json', temp)
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        temp.name, scope)
    gc = gspread.authorize(credentials)
    return gc


def gcs(bucket_name, path, temp):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.get_blob(path)
    p = Path(temp.name)
    with p.open('wb') as fp:
        blob.download_to_file(fp)
    temp.flush()
    temp.seek(0)


def handlecsv(filepath):
    gc = get_credential()
    sh = gc.open_by_key('1rHAQa2d1sB3hef7GBO5APVvw7a7XoalrPtaeCa2j60w')
    worksheet = sh.get_worksheet(0)
    worksheet.clear()
    path = Path(filepath)
    with path.open() as fp:
        reader = csv.reader(fp)
        data = [row for row in reader]
    if not data or not data[0]:
        return
    data.sort(key=lambda x:x[0])
    cell_list = worksheet.range(1, 1, len(data), len(data[0]))
    for idx, cell in enumerate(cell_list):
        x = idx % len(data[0])
        y = idx // len(data[0])
        cell.value = data[y][x]
    worksheet.update_cells(cell_list)


def gsload(fileobj):
    temp = tempfile.NamedTemporaryFile()
    gcs(fileobj['bucket'], fileobj['name'], temp)
    handlecsv(temp.name)


def nas_gspread(filedata, eventdata):
    gsload(filedata)
