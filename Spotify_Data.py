import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.parse as urlparse
import datetime

auth_manager = SpotifyClientCredentials( client_id="15cd7aacd3c445029ba60aec55c911d5", client_secret="604b5edcb28547828d0410454d6d3519")
spotify = spotipy.Spotify(auth_manager=auth_manager)

def getTopSongs(name: str, count: int ):
    top = []
    # encode_name = urlparse.quote(name)
    results = spotify.search(q= name, type='artist')
    rank = 1
    r = list(results.values())[0]['items'][0]

    data = spotify.artist_top_tracks( r['uri'] )

    for track in data['tracks'][:count]:
        top.append( f'track {rank} :  {track["name"]}\n')
        rank += 1
        
    return top, (r['name'] , r['external_urls']['spotify']) 

# not implemented 
def getartistAlbums(name: str, count: int ):
    top = []
    # encode_name = urlparse.quote(name)
    results = spotify.search(q= name, type='artist')
    rank = 1
    r = list(results.values())[0]['items'][0]

    data = spotify.artist_albums( r['uri'] )

    for album in data['albums'][:count]:
        top.append( f'album {rank} :  {album["name"]}\n')
        
    return top, (r['name'] , r['external_urls']['spotify']) 

def getFollowing(artistTitle):
    results = spotify.search(q= artistTitle, type='artist')
    r = list(results.values())[0]['items'][0]
    followers = r['followers']['total']
    return followers, (r['name'] , r['external_urls']['spotify']) 

def getGenres(artistTitle):
    results = spotify.search(q= artistTitle, type='artist')
    r = list(results.values())[0]['items'][0]
    genres = r['genres']
    return genres, ( r['name'], r['external_urls']['spotify'] )

# 0-100 vals
def getArtistPopularity(artistTitle):
    results = spotify.search(q= artistTitle, type='artist')
    r = list(results.values())[0]['items'][0]
    pop = r['popularity']
    # print( pop, (r['name'],  r['external_urls']['spotify']) )
    return pop, ( r['name'], r['external_urls']['spotify'])

# 0-1
def getDanceability(songTitle):
    results = spotify.search(q= songTitle, type='track')
    r = list(results.values())[0]['items'][0]
    t_id = r["id"]
    dance = spotify.audio_features(t_id)[0]['danceability']
    return dance , (r['name'], r['artists'][0]['name'], r['external_urls']['spotify']) # danecability, (track name, artist)

# 0-1
def getEnergy(songTitle):
    results = spotify.search(q= songTitle, type='track')
    r = list(results.values())[0]['items'][0]
    t_id = r["id"]
    energy = spotify.audio_features(t_id)[0]['energy']
    return energy , (r['name'], r['artists'][0]['name'], r['external_urls']['spotify'])

# whatever tempo's are
def getTempo(songTitle):
    results = spotify.search(q= songTitle, type='track')
    r = list(results.values())[0]['items'][0]
    t_id = r["id"]
    tempo = spotify.audio_features(t_id)[0]['tempo']
    return tempo , (r['name'], r['artists'][0]['name'], r['external_urls']['spotify'])

# 0-1
def getHappiness(songTitle):
    results = spotify.search(q= songTitle, type='track')
    r = list(results.values())[0]['items'][0]
    t_id = r["id"]
    valence = spotify.audio_features(t_id)[0]['valence']
    # print(valence , (r['name'], r['artists'][0]['name']))
    return valence , (r['name'], r['artists'][0]['name'], r['external_urls']['spotify'])

# just time
def getSongLength(songTitle):
    results = spotify.search(q= songTitle, type='track')
    r = list(results.values())[0]['items'][0]
    t_id = r["id"]
    time = spotify.audio_features(t_id)[0]['duration_ms'] // 1000
    return time , (r['name'], r['artists'][0]['name'], r['external_urls']['spotify'])

# def getAlbumLength(albumTitle):
#     pass

# def getAlbumFromSongs(songTitle):
#     pass

# def getSongsFromAlbum(albumTitle):
#     pass


if __name__ == "__main__":
    # getDanceability("around the world daft punk")
    # getEnergy("the middle jimmy eat world")
    # user_input = "what is the tempo of another one bites the dust by queen"
    # getTempo(user_input)
    # getHappiness("star brockhampton")
    # getSongLength("blinding lights the weeknd")
    # getFollowing("weeknd")
    # print(getGenres("dayglow"))
    # getFollowing("weeknd")
    # getArtistPopularity("weeknd")
    

    pass

