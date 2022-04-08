import json
import numpy as np
import pandas as pd
from cleantext import clean
import re

def playlists_cleaning(text):
    # Remove [Sean Paul: ] parts
    text = re.sub("\[[^][]*]", "", text)
    text = re.sub("\(.*?\)", "", text)
    
    # Remove + signs
    text = re.sub("\+", "", text)
    
    # Remove "
    text = re.sub("""\"""", "", text)
    
    # Apply cleantext
    text = clean(
    text,
    fix_unicode=True,
    to_ascii=True,
    lower=True,
    normalize_whitespace=True,
    no_line_breaks=True,
    strip_lines=True,
    keep_two_line_breaks=False,
    no_urls=True,
    no_emails=True,
    no_phone_numbers=True,
    no_numbers=True,
    no_digits=True,
    no_currency_symbols=True,
    no_punct=False,
    no_emoji=True,
    replace_with_url='',
    replace_with_email='',
    replace_with_phone_number='',
    replace_with_number='',
    replace_with_digit='',
    replace_with_currency_symbol='',
    replace_with_punct=' ',
    lang='en')
    
    # Remove the song name + lyrics 
    text = re.sub("^.*?(?:lyrics )", "", text)
    
    return text
import sys
f = open("/home/freshpate/lyrics-analysis/data/mpd.slice.0-999.json")

data = json.load(f)

# print(data["playlists"][0])

token = "-q1tRGBZMEOk6JewZCC_KWZBxyFSg9nccGlX11Cb3MxpGpzWG4FBSJIXCJS33D3x"

from lyricsgenius import Genius

genius = Genius(token)
# artist = genius.search_artist("Andy Shauf", max_songs=3, sort="title")
# song = genius.search_song("To You", artist.name)
# artist.save_lyrics()
# a = song.lyrics
# li = []
for i in range(1000):
    # print(data["playlists"][i]["collaborative"])
    lyrics = []
    playlist_name = []
    if data["playlists"][i]["collaborative"] == 'false':
        # print("intrat")
        for track in data["playlists"][i]['tracks']:
            # print(track['track_name'])
            try:
                song = genius.search_song(track['track_name'], track['artist_name'])
                # maybe = song.lyrics
                # print("aici", playlists_cleaning(maybe))
                # print("incercare", playlists_cleaning(str(maybe)))
                # # sys.exit()
                lyrics.append(song.lyrics)
                playlist_name.append(data["playlists"][i]['name'])
                # aux.append([np.array(song.lyrics, dtype=str), np.array(data["playlists"][i]['name'], dtype=object)])
            except:
                continue

    name_dict = {
            'name': playlist_name,
            'lyrics': lyrics
          }

    # name_dict["lyrics"] = name_dict["lyrics"].apply(playlists_cleaning)
    df = pd.DataFrame(name_dict)
    df["lyrics"] = df["lyrics"].apply(playlists_cleaning)
    df.to_csv("/home/freshpate/playlist_lyrics/playlist-{}.csv".format(i))
            # print(song.lyrics
    print("Done with playlist!!!")
    # for_saving = np.array(aux, dtype=object)
    # np.savetxt("/home/freshpate/playlist_lyrics/playlist-{}.csv".format(i), for_saving, delimiter=",")
# li.append(a.replace("\n", " "))
# print(li)