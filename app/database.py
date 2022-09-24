# Database and Database models
from app import app, db
from app.models import Download, Upload

# Helper libraries
import pathlib
import pandas as pd
import dropbox
import gzip
import os
import json

def dropbox_storage():      # Callable from routes.py - Filters and stores NDT7 data from dropbox into a database 
    # Dropbox authentication
    dbx = dropbox.Dropbox(
                app_key = app.config['APP_KEY'],
                app_secret = app.config['APP_SECRET'],
                oauth2_refresh_token = app.config['OAUTH2_REFRESH_TOKEN']
            )

    path = '/ndt-server/datadir/ndt7'       # Path to NDT7 files
    upload = []                             # Stores NDT7 upload filenames
    download = []                           # Stores NDT7 download filenames

    # Extracts NDT7 upload and download filenames from all subdirectories in 'path'
    for year in dbx.files_list_folder(path).entries:
        for month in dbx.files_list_folder(path + '/' + year.name).entries:
            for day in dbx.files_list_folder(path + '/' + year.name + '/' + month.name ).entries:
                for filename in dbx.files_list_folder(path + '/' + year.name + '/' + month.name + '/' + day.name).entries:
                    if 'upload' in filename.name:
                        upload.append(filename.name)
                    else:
                        download.append(filename.name)

    def db_storage(metric):             # 'metric' points to a database entity
        if metric == 'upload':          # NDT7 upload data
            metric = upload             # Upload filenames
            db_attr = Upload            # Upload db entity
        elif metric == 'download':      # NDT7 download data
            metric = download           # Download filenames
            db_attr = Download          # Download db entity

        for fn in metric:               # Checks existing filename in the db entity
            if db_attr.query.filter_by(filename=fn).first() != None:
                continue
            
            dropbox_dir = '/ndt-server/datadir/ndt7/'       # Same as 'path'

            index = fn.find('-', fn.find('-') + 1)
            year = fn[index + 1: index + 5]                 # Extract the year from the filename  
            month = fn[index + 5 : index + 7]               # Extract the month from the filename
            day = fn[index + 7 : index + 9]                 # Extract the day from the filename

            with open('tmp.gz', 'wb') as f:         # Retrieve NDT7 JSON.GZIP data from dropbox and write as a temporary GZIP 
                metadata, result = dbx.files_download(path='{}/{}/{}/{}/{}'.format(path, year, month, day, fn))
                f.write(result.content)
                f.close() 

            with gzip.open('tmp.gz', "rb") as f:    # Unzip temporary GZIP as a JSON into 'd'
                d = json.loads(f.read().decode("ascii"))
                f.close()
            os.unlink("tmp.gz")             # Removes temporary GZIP

            df = pd.DataFrame(d.items())    # Converts JSON in 'd' into a dataframe
            
            start_time = (df[1].iloc[8]['StartTime'])   # Retrieve start time of NDT7 test from 'df'
            year = start_time[0:4]                      # Retrieve year of NDT7 test
            month = start_time[5:7]                     # Retrieve month of NDT7 test
            day = start_time[8:10]                      # Retrieve day of NDT7 test
            time = start_time[11:19]                    # Retrieve time in UTC of NDT7 test

            server_data = (df[1].iloc[8]['ServerMeasurements']) # Retrieve measurement data from 'df'
            
            if server_data == None:     # Checks if test was dropped
                client_ip = ''
                server_ip = ''
                busy_time = float("nan")
                bytes_acked = float("nan")
                bytes_received = float("nan")
                bytes_sent = float("nan")
                bytes_retrans = float("nan")
                elapsed_time = float("nan")
                min_rtt = float("nan")
                rtt = float("nan")
                rtt_var = float("nan")
                rwnd_limited = float("nan")
                snd_buf_limited = float("nan")

            else:
                server_measurements = (server_data[-1])     # Last recorded measurement

                connection_info = server_measurements['ConnectionInfo']
                client_ip = connection_info['Client']       # Client IP address
                server_ip = connection_info['Server']       # Server IP address

                # NDT7 metadata - https://github.com/m-lab/ndt-server/blob/main/spec/ndt7-protocol.md
                tcp_info = server_measurements['TCPInfo']
                busy_time = tcp_info['BusyTime']
                bytes_acked = tcp_info['BytesAcked']
                bytes_received = tcp_info['BytesReceived']
                bytes_sent = tcp_info['BytesSent']
                bytes_retrans = tcp_info['BytesRetrans']
                elapsed_time = tcp_info['ElapsedTime']
                min_rtt = tcp_info['MinRTT']
                rtt = tcp_info['RTT']
                rtt_var = tcp_info['RTTVar']
                rwnd_limited = tcp_info['RWndLimited']
                snd_buf_limited = tcp_info['SndBufLimited']

            u = db_attr(                        # Write data to a temporary instance of the db entity
                    year = year,
                    month = month,
                    day = day, 
                    filename = fn,
                    time = time,
                    client_ip = client_ip,
                    server_ip = server_ip,
                    busy_time = busy_time,
                    bytes_acked = bytes_acked,
                    bytes_received = bytes_received,
                    bytes_sent = bytes_sent,
                    bytes_retrans = bytes_retrans,
                    elapsed_time = elapsed_time,
                    min_rtt = min_rtt,
                    rtt = rtt,
                    rtt_var = rtt_var,
                    rwnd_limited = rwnd_limited,
                    snd_buf_limited = snd_buf_limited
                )

            # Add entries to the database and commit the changes.
            db.session.add(u)
            db.session.commit()

    # Function Calls
    db_storage('download')
    db_storage('upload')