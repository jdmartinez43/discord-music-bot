"""
sample code from https://lyricsgenius.readthedocs.io/en/master/reference/genius.html
was used to help build this project
"""
from lyricsgenius import Genius

CLIENT_ID = "712UHU3TY2BmfPIy9w0eo9Il2drR9Nh0-EM2lmi4dYJHPMEzCdAOAD1-GHAiuOpw"
CLIENT_SECRET = "3mN9Xh9J-a_ZXGh5tM_-kFFcPIFQVT4B0DA44RGjuN9b-dQr7DS5U0waQNbm_wjDoYrG0Uj4fMV3FfVi05eNVQ"
CLIENT_TOKEN = "S9dTm38YUImBFf5xqijCxoaVd_kiTDuys9elC560wH6G7M-ktEP62blPiDFAqBC4"

genius = Genius(CLIENT_TOKEN, verbose = False)

# NOT IMPLEMENTED YET
# least popular song according to genius
def getArtistLeastPopularSongs(artistName: str):

    # do search on artistName for artist id
    artistID = 0

    if artistID != None:
        page = 1 
        songs = []
        while page:
            request = genius.artist_songs(artistID, sort='popularity', per_page=50, page=page)

            songs = request['songs']
            page = request['next_page']

        least_popular_song = songs[-1]['title']
        return least_popular_song
    else:
        return None

def getArtistSongs(name: str, count: int) -> dict:
    artist = genius.search_artist(name, max_songs=count, sort="title")
    print(artist.songs)

def getLyrics(songTitle) -> str:
    s = genius.search_song(songTitle)
    if s == None:
        return None
    else:
        return s.lyrics, (s.title, s.artist)

def getReleaseDate(title) -> "str or None":
    s = genius.search_song(title)

    if s == None:
        return None
    else:
        songID = s._body['id']
        full_song = genius.song(songID, 'plain')

        return full_song['song']['release_date_for_display'] , (s.title, s.artist)

# how many people have viewed x song (maybe artist, albums?)
def getGeniusViews(song):
    pass

# ['song']['song_relationship'][x]
def getWhoSampled(songTitle:str):
    s = genius.search_song(songTitle)

    if s == None:
        return None
    else:
        songID = s._body['id']
        full_song = genius.song(songID, 'plain')
        
        sampled = full_song['song']['song_relationships'][1]
        p=[]
        # print("songs that sampled", songTitle, "\n")
        for sam in sampled['songs']:
            t = sam['title']
            a = sam['primary_artist']['name']
            x = f"{t} by {a}\n"
            # print(x)
            p.append(x)
        
        return p , (s.title, s.artist)

def getWhoInterpolated(songTitle:str):
    s = genius.search_song(songTitle)

    if s == None:
        return None
    else:
        songID = s._body['id']
        full_song = genius.song(songID, 'plain')

        interpolated = full_song['song']['song_relationships'][3]
        i =[]
        # print("songs that interpolated", songTitle, "\n")
        for sam in interpolated['songs']:
            t = sam['title']
            a = sam['primary_artist']['name']
            x = f"{t} by {a}\n"
            # print(x)
            i.append(x)

        return i, (s.title, s.artist)

def getWhoCovered(songTitle:str):
    s = genius.search_song(songTitle)

    if s == None:
        return None
    else:
        songID = s._body['id']
        full_song = genius.song(songID, 'plain')

        covers = full_song['song']['song_relationships'][5]
        c=[]
        # print("song covers of", songTitle, "\n")
        for sam in covers['songs']:
            t = sam['title']
            a = sam['primary_artist']['name']
            x = f"{t} by {a}\n"
            # print(c)
            c.append(x)
        
        return c, (s.title, s.artist)

def getWhoRemixed(songTitle:str):
    s = genius.search_song(songTitle)

    if s == None:
        return None
    else:
        songID = s._body['id']
        full_song = genius.song(songID, 'plain')

        remixes = full_song['song']['song_relationships'][7]
        r=[]
        # print("remixes of", songTitle, "\n")
        for sam in remixes['songs']:
            t = sam['title']
            a = sam['primary_artist']['name']
            x = f"{t} by {a}\n"
            # print(x)
            r.append(x)
        return r, (s.title, s.artist)

# who was featured on
# who has produced 
# who helped write for

if __name__ == "__main__":
    pass
    # getReleaseDate("around the world daft punk")
    # getLyrics("chandlier sia")
    # getWhoRemixed("chandlier sia")
    # getArtistSongs("Rina Sawayama", 1) # alphabetically gets songs from artists in data in this function
    # xd = geniusAPI.song(378195, text_format= 'plain')
    # full_song = genius.song(378195)
    # full_song['song']['album']['name']) < for a song's album name
