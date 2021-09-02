import Genius_Data
import Spotify_Data

requestInfo = {
        'most'   : False,
        'song'   : False,
        'songs'  : False,
        'album' : False,
        'albums' : False,
        'lyrics' : False,
        'release' : False,
        'popular': False,
        'remix' : False,
        'interpolations': False,
        'covers' : False,
        'sampled' : False, 
        'following': False,
        'best' : False,
        'top' : False,
        'type' : False,
        'length' : False,
        'tempo' : False,
        'happiness' : False, 
        'danceability' : False,
        'energy' : False,
        'popularity': False,
}
haveGreeted = False
useSpotify = False
useGenius = False
errored = False
currentMusicData = []
lastMusicMention = []




# Format a reply to the user, based on what the user wrote.
def formReply() -> str:
    global requestInfo, haveGreeted, currentMusicData, useSpotify, errored, useGenius

    # print(requestInfo)
    composed = ""  
    if haveGreeted: 
        composed += "Hello. "

    if requestInfo['lyrics']:
        music_data = Genius_Data.getLyrics( " ".join(currentMusicData) )
        if music_data == None:
            composed += "Hm, Genius.com doesn't seem to have data on that song. Try a different song?"
            errored = True
        else:
            lyrics, (title, artist) = music_data
            composed += f"Okay here are the lyrics for {title} by {artist}\n{lyrics}\n"
            # requestInfo['music_noun'] = [title, artist] # for using in future parts
            currentMusicData = [title, artist]
            useGenius = True
        return composed
    
    elif requestInfo['release']:
        music_data = Genius_Data.getReleaseDate( " ".join(currentMusicData))
        if music_data == None:
            composed += "Hm, Genius.com doesn't seem to have data on that song. Try a different song?"
            errored = True
        else:
            date, (title, artist) = music_data
            composed += f"{title} by {artist} was released on {date}\n"
            # requestInfo['music_noun'] = [title, artist] # for using in future parts
            currentMusicData = [title, artist]
            useGenius = True
        return composed
    
    elif requestInfo['top'] or (requestInfo['most'] and requestInfo['popular']):
        if requestInfo['song']:
            try:
                music_data = Spotify_Data.getTopSongs( " ".join(currentMusicData) , 1)
                # print(type(music_data))
                song , (artist, link ) = music_data
                composed += f"Here is {artist}'s top song:\n {song[0]}"
                # requestInfo['music_noun'] = [artist,link]
                currentMusicData = [artist, link]
                useSpotify = True
            except:
                composed = "Hm. I couldn't find anything on Spotify. Try something else?"
                errored = True
            finally:
                return composed

        elif requestInfo['songs']:
            try:
                music_data = Spotify_Data.getTopSongs( " ".join(currentMusicData) , 10)
                songs, (artist, link ) = music_data
                # print(songs)
                composed += f"Here are {artist}'s top songs:\n{ ''.join([s for s in songs]) }"
                # requestInfo['music_noun'] = [artist,link]
                currentMusicData = [artist, link]
                useSpotify = True
            except:
                composed = f"Hm. I couldn't find anything on Spotify for that. Let's try something else? "
                errored = True
            finally:
                return composed
    
    elif requestInfo['remix']:
        music_data = Genius_Data.getWhoRemixed( " ".join(currentMusicData) )
        if music_data == None:
            composed += "Hm, Genius.com doesn't seem to have data on that song. Try a different song?"
            errored = True
        else:
            data, (title, artist) = music_data
            if data != []:
                composed += f"Here are all the remixes of {title} by {artist}\n{' '.join(data)}\n"
            else:
                composed += f"{title} by {artist} has not been remixed by anyone\n"
            # requestInfo['music_noun'] = [title, artist] # for using in future parts
            currentMusicData = [title, artist]
            useGenius = True
        return composed
    
    elif requestInfo['interpolations']:
        music_data = Genius_Data.getWhoInterpolated( " ".join(currentMusicData) )
        if music_data == None:
            composed += "Hm, Genius.com doesn't seem to have data on that song. Try a different song?"
            errored = True
        else:
            data, (title, artist) = music_data
            if data != []:
                composed += f"Here are the known interpolations of {title} by {artist}\n{' '.join(data)}\n"
            else:
                composed += f"{title} by {artist} has not been interpolated by anyone\n"
            # requestInfo['music_noun'] = [title, artist] # for using in future parts
            currentMusicData = [title, artist]
            useGenius = True
        return composed
    
    elif requestInfo['covers']:
        music_data = Genius_Data.getWhoCovered( " ".join(currentMusicData) )
        if music_data == None:
            composed += "Hm, Genius.com doesn't seem to have data on that song. Try a different song?"
            errored = True
        else:
            data, (title, artist) = music_data
            if data != []:
                composed += f"Here are the known covers of {title} by {artist}\n{' '.join(data)}\n"
            else:
                composed += f"{title} by {artist} has not been covered by anyone\n"            
            # requestInfo['music_noun'] = [title, artist] # for using in future parts
            useGenius = True
            currentMusicData = [title, artist]
        return composed
    
    elif requestInfo['sampled']:
        music_data = Genius_Data.getWhoSampled( " ".join(currentMusicData) )
        if music_data == None:
            composed += "Hm, Genius.com doesn't seem to have data on that song. Try a different song?"
            errored = True
        else:
            data, (title, artist) = music_data
            if data != []:
                composed += f"Here are the known songs that sample {title} by {artist}\n{' '.join(data)}\n"
            else:
                composed += f"{title} by {artist} has not been sampled by anyone\n"            
            # requestInfo['music_noun'] = [title, artist]
            useGenius = True
            currentMusicData = [title, artist]
        return composed

    elif requestInfo['type']:
        try:
            music_data = Spotify_Data.getGenres( " ".join(currentMusicData) )
            genres , (artist, link ) = music_data
            composed += f"{artist} makes music for these genres: {genres}\n"
            # requestInfo['music_noun'] = [artist,link]
            currentMusicData = [artist, link]
            useSpotify = True
        except:
            composed = "Hm. I couldn't find anything on Spotify. Try something else?"
            errored = True
        finally:
            return composed
    
    elif requestInfo['following']:
        try:
            music_data = Spotify_Data.getFollowing( " ".join(currentMusicData) )
            x , (artist, link ) = music_data
            composed += f"{artist} has {x} many followers\n"
            # requestInfo['music_noun'] = [artist,link]
            currentMusicData = [artist, link]
            useSpotify = True
        except:
            composed = "Hm. I couldn't find anything on Spotify. Try something else?"
            errored = True
        finally:
            return composed
    
    elif requestInfo['popularity']:
        try:
            music_data = Spotify_Data.getArtistPopularity( " ".join(currentMusicData) )
            pop , ( artist, link ) = music_data
            if pop > 75:
                composed += f"{artist} is pretty popular! Out of a 0-100 popularity scale their score is: {pop}\n"
            elif pop > 50:
                composed += f"{artist} is averagely popular. Out of a 0-100 popularity scale their score is: {pop}\n"
            elif pop > 25:
                composed += f"{artist} is a little popular. Out of a 0-100 popularity scale their score is: {pop}\n"
            else:
                composed += f"{artist} is not very popular. Out of a 0-100 popularity scale their score is: {pop}\n"

            # requestInfo['music_noun'] = [artist,link]
            currentMusicData = [artist, link]
            useSpotify = True
        except:
            composed = "Hm. I couldn't find anything on Spotify. Try something else?"
            errored = True
        finally:
            return composed

    elif requestInfo['danceability']:
        try:
            music_data = Spotify_Data.getDanceability( " ".join(currentMusicData) )
            dance , (track, artist, link ) = music_data
            if dance > 0.75:
                composed += f"{track} by {artist} is pretty danceable! Out of a 0-1 scale it's danceability is: {dance}\n"
            elif dance > 0.5:
                composed += f"{track} by {artist} is kinda danceable. Out of a 0-1 scale it's danceability is: {dance}\n"
            elif dance > 0.25:
                composed += f"{track} by {artist} is not very danceable. Out of a 0-1 scale it's danceability is: {dance}\n"
            else:
                composed += f"{track} by {artist} is not danceable. Out of a 0-1 scale it's danceability is: {dance}\n"

            # requestInfo['music_noun'] = [track, artist, link]
            currentMusicData = [track, artist, link]
            useSpotify = True

        except:
            composed = "Hm. I couldn't find anything on Spotify. Try something else?"
            errored = True
        finally:
            return composed

    elif requestInfo['energy']:
        try:
            music_data = Spotify_Data.getEnergy( " ".join(currentMusicData) )
            energy , ( track, artist, link ) = music_data
            if energy > .75:
                composed += f"{track} by {artist} is very energetic! On a 0-1 scale their score is: {energy}\n"
            elif energy > .50:
                composed += f"{track} by {artist} is pretty energetic. On a 0-1 scale their score is: {energy}\n"
            elif energy > .25:
                composed += f"{track} by {artist} is kinda energetic. On a 0-1 scale their score is: {energy}\n"
            else:
                composed += f"{track} by {artist} is not very energetic. On a 0-1 scale their score is: {energy}\n"

            # requestInfo['music_noun'] = [track, artist, link]
            currentMusicData = [track, artist, link]
            useSpotify = True
        except:
            composed = "Hm. I couldn't find anything on Spotify. Try something else?"
            errored = True
        finally:
            return composed

    elif requestInfo['tempo']:
        try:
            music_data = Spotify_Data.getTempo( " ".join(currentMusicData) )
            t , ( track, artist, link ) = music_data
            composed += f"{track} by {artist} has a tempo of {t}.\n"
            # requestInfo['music_noun'] = [track, artist, link]
            currentMusicData = [track, artist, link]
            print(currentMusicData)
            useSpotify = True
        except:
            composed = "Hm. I couldn't find anything on Spotify. Try something else?"
            errored = True
        finally:
            return composed
            
    elif requestInfo['happiness']:
        try:
            music_data = Spotify_Data.getHappiness( " ".join(currentMusicData) )
            t , ( track, artist, link ) = music_data
            composed += f"{track} by {artist} has a happiness of {t}.\n"
            # requestInfo['music_noun'] = [track, artist, link]
            currentMusicData = [track, artist, link]
            useSpotify = True
        except:
            composed = "Hm. I couldn't find anything on Spotify. Try something else?"
            errored = True
        finally:
            return composed

    elif requestInfo['length']:
        try:
            music_data = Spotify_Data.getSongLength( " ".join(currentMusicData) )
            t , ( track, artist, link ) = music_data
            composed += f"{track} by {artist} is {t} seconds long.\n"
            # requestInfo['music_noun'] = [track, artist, link]
            currentMusicData = [track, artist, link]
            useSpotify = True
        except:
            composed = "Hm. I couldn't find anything on Spotify. Try something else?"
            errored = True
        finally:
            return composed

    errored = True
    return "Sorry, I couldn't quite understand that. Can you rephrase your question?"

# resets everything but the last mentioned music data which may want to be kept
def resetInfo():
    global requestInfo, haveGreeted, errored, useSpotify, currentMusicData, useGenius
    for i in requestInfo:
        if i != "music_noun":
            requestInfo[i] = False
        else:
            i = []
    haveGreeted = False
    errored = False
    useSpotify = False
    useGenius = False
    currentMusicData = []

def chat(user_input) -> str:
    global requestInfo, currentMusicData, useGenius, useSpotify, lastMusicMention, errored

    # print("_______________________________________")
    reply = ""

    bye = {"bye", "goodbye", "farewell"}
    for b in bye:
        if b == user_input.lower():
            return "Goodbye!"

    cykp, musics = Parsing.compile_msg(user_input)
    currentMusicData = musics

    # use previous data if user didnt specify
    if currentMusicData == []: 
        currentMusicData = lastMusicMention
    
    #  if no existing data to work with then theres something wrong
    if currentMusicData == []:
        errored = True

    try:
        
        # TODO: DECODE THE SENTENCE AND UPDATE THE GLOBAL VARIABLES

        reply = formReply()


        if errored == False:
            if useSpotify:
                ask = " or ".join(currentMusicData[:-1])
                reply += f"Here's a spotify link with music you might like {currentMusicData[-1]}\n" 
                reply += f"Would you like to know more about {ask}?"
                useSpotify = False
                lastMusicMention = currentMusicData[:-1]
            elif useGenius:
                ask = " or ".join(currentMusicData)
                reply += f"Would you like to know more about {ask}?"
                useGenius = False
                lastMusicMention = currentMusicData
    except:
        reply += "Hm, I couldn't parse the response you gave. Can you try rewording it?"
    resetInfo()
    # print("lmma after delete", lastMusicMention)
    return reply

if __name__ == "__main__":
    pass


    