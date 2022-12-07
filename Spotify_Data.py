# Spotify_Data.py
from Environment_Variables import *

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials( 
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET)
spotify = spotipy.Spotify(auth_manager=auth_manager)

def getTopSongs(name: str, count: int ):
    top = []
    # encode_name = urlparse.quote(name)
    results = spotify.search(q= name, type='artist')
    rank = 1
    r = list(results.values())[0]['items'][0]

    data = spotify.artist_top_tracks( r['uri'] )

    # iterate over tracks, which will be the top 10 (or all songs if count < 10) 
    # according to spotify
    for track in data['tracks'][:count]:
        top.append( f'track {rank} :  {track["name"]}\n')
        rank += 1
        
    return top, (r['name'] , r['external_urls']['spotify']) 

# not implemented 
def getartistAlbums(name: str, count: int ):
    top = []    
    results = spotify.search(q= name, type='artist')
    rank = 1
    r = list(results.values())[0]['items'][0]
    data = spotify.artist_albums( r['uri'] )

    for album in data['albums'][:count]:
        top.append( f'album {rank} :  {album["name"]}\n')    
    return top, (r['name'] , r['external_urls']['spotify']) 

# modular function to replace getFollowing, getGenres, and getArtistiPopularity
# functions; to reference proj code from CS 171 look at the first commit
def getArtistSearchData(artistTitle, search_type: str):
    """
    get the data from spotify search functions, and get the first index 
    (ie first result) from part of the results json dictionary, where we see:    
    [
       {'external_urls': {
          'spotify': 'https://open.spotify.com/artist/1Xyo4u8uXC1ZmMpatF05PJ'}, 
          'followers': {'href': None, 'total': 35925362}, 
          'genres': ['canadian contemporary r&b', 'canadian pop', 'pop'], 
          'href': 'https://api.spotify.com/v1/artists/1Xyo4u8uXC1ZmMpatF05PJ', 
          'id': '1Xyo4u8uXC1ZmMpatF05PJ', 
          'images': [
             {'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5eb94fbdb362091111a47db337d', 'width': 640},
             {'height': 320, 'url': 'https://i.scdn.co/image/ab6761610000517494fbdb362091111a47db337d', 'width': 320}, 
             {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f17894fbdb362091111a47db337d', 'width': 160}], 
          'name': 'The Weeknd', 'popularity': 97, 'type': 'artist', 
          'uri': 'spotify:artist:1Xyo4u8uXC1ZmMpatF05PJ'
       },
       ..."""

    results = spotify.search(q= artistTitle, type='artist')
    r = list(results.values())[0]['items'][0]

    try:
        # search_types = ['followers', 'genres', 'popularity ]
        if search_type == 'followers':
            data = r[search_type]['total']
        else:
            data = r[search_type]

    except IndexError as err:
        print(f"Index Error: {err}")
        data = None  
    
    return data, (r['name'] , r['external_urls']['spotify']) if data != None else None
    
def getTrackData(songTitle: str, feature: str):
    
    # collect the first songs
    results = spotify.search(q= songTitle, type='track')
    r = list(results.values())[0]['items'][0]
    t_id = r["id"]

    try:
        # features = ['danceability', 'energy', 'tempo', 'valence', 'duration_ms']
        # 0-1 scale: danceability, energy, valence
        # int values: tempo, duration_ms
        data = spotify.audio_features(t_id)[0][feature]
        if feature == "duration_ms":      # time is in milliseconds so convert 
            data = data // 1000           # to seconds   
        
    except IndexError as err:
        print(f"Index Error: {err}")

    return data , (r['name'], r['artists'][0]['name'], r['external_urls']['spotify']) if data != None else None

# def getAlbumLength(albumTitle):
#     pass
# def getAlbumFromSongs(songTitle):
#     pass
# def getSongsFromAlbum(albumTitle):
#     pass


if __name__ == "__main__":
    # print(getTrackData("around the world daft punk", 'danceability' ))
    # print(getTrackData("the middle jimmy eat world", 'energy'))
    # print(getTrackData("get into it", 'tempo'))
    # print(getTrackData("star brockhampton", 'valence'))
    # print(getTrackData("blinding lights the weeknd", 'duration_ms'))
    # print(getArtistSearchData("dayglow", 'genres'))
    # print(getArtistSearchData("weeknd" , 'popularity'))
    # print(getArtistSearchData("weeknd", 'followers'))

    pass

