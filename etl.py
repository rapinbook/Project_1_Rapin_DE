import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Insert data from song_file json to song and artist table
    
    Keyword arguments:
    cur -- cursor for database connection
    filepath -- string of path to song_file 
    
    """
    # open song file

    inputData = pd.read_json(filepath, lines=True)
    song_df = pd.DataFrame(data=inputData)
    song_df.head()
   

    # insert song record
    song_data = song_df[['song_id', 'title', 'artist_id','year','duration']].values
    for i, row in song_df.iterrows():
        cur.execute(song_table_insert, song_data[i])
        
    
    # insert artist record
    
    artist_data = song_df[['artist_id', 'artist_name', 'artist_location','artist_latitude','artist_longitude']].values
    for i, row in song_df.iterrows():
        cur.execute(artist_table_insert, artist_data[i])
        
    


def process_log_file(cur, filepath):
    """
    Insert data from log_file json to time, user and songplay table
    
    Keyword arguments:
    cur -- cursor for database connection
    filepath -- string of path to log_file 
    
    """
    # open log file
    datalog = pd.read_json(filepath, lines=True)

    df = pd.DataFrame(data=datalog)
    df.head()

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_log = []
    column_labels = ('start time','hour','day','week of year','month','year','weekday')
    index = 0
    for timestamp in t:
        time_data = (t[index],t.dt.hour[index],t.dt.day[index],t.dt.week[index],t.dt.month[index],t.dt.year[index],t.dt.weekday[index])
        time_log.append(time_data)
        index = index + 1
        
    time_df = pd.DataFrame.from_dict(time_log)
    #print(time_df)
    time_df.head()


    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))
        

    # load user table
    user_df_data = df[['userId', 'firstName', 'lastName','gender','level']].values
    user_df = pd.DataFrame.from_dict(user_df_data)

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
        
    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'),row.userId,row.level,songid,artistid,row.sessionId,row.location,row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)
        
    


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)
    conn.commit()

    conn.close()


if __name__ == "__main__":
    main()