# Code for CS 171, Winter, 2021
import Tree
from collections import defaultdict

verbose = False
# keep a track of when existing lexicon words appear, 
# if it's more than one then we use it to help build the music noun
# example: What are the lyrics for what is love by haddaway

def printV(*args):
    if verbose:
        print(*args)

# if a word ends in 's then add a 2-tuple with/without "'s" else add only 1-tuple
def tokenS(msg:[str]) -> [str]:
    tokens = []
    for word in msg:
        nos = word[-2:]
        if nos == "'s":
            tokens.append( (word, nos) )
        else:
            tokens.append( (word,) )
    return tokens

# used to find the index of when a certain str appears in a list
def lastOccured(l:list, kw: str) -> [int]:
	r = []
	for i in range(len(l)):
		if l[i] == kw:
			r.append(i)
	return r[-1] if r != [] else -1

def resetLexicon():
    for w in LEXICON:
        LEXICON[w] = 0

# given a user's message find the the strings that aren't in the 
# current lexicon (meaning that they're words for artists, songs, etc). 
def createMusic(msg:str) -> (dict, str):
    msg = msg.lower()
    msg = msg.split()
    musicWords = defaultdict(list)
    musicWord = 0
    getMusic = False      
    lastby   = lastOccured(msg , "by")
    by_check = True if msg.count("by") >= 2 else False # if true then ignore any "by" strings until it's the last one else collect strings as usual
    
    # reformed - str()
    seek = []
    temp = str()

    for w in range(len(msg)):

        word = msg[w]
        temp += f"{word} "
        if getMusic == False:
            seek.append(temp.rstrip())
            temp = str()

        if getMusic and word == "by" :
            # assuming there's 2+ by's, make sure we're not at the last by index to continue getting musicwords
            if by_check == True and w != lastby:
                getMusic = True
                musicWords[musicWord].append(word)                
            # otherwise when we see a by stop getting that music word
            else:
                getMusic = False
                b = temp[:-4]
                seek.append(b)                
                seek.append("by")
                temp = ""
                musicWord += 1

        elif word not in LEXI_KEYS or LEXICON[word] >= 1:
            getMusic = True        
            musicWords[musicWord].append(word)

        elif word != "by" and word in LEXI_KEYS:
            LEXICON[word] += 1
            
            # still parsing through regular sentence
            if getMusic == False:
                musicWord += 1
                if word == "for":
                    getMusic = True
                    seek.append(temp)
                    temp = ""
            # checking for stop words to evaluate in music nouns
            else:
                if word in STOP_WORDS:
                    musicWords[musicWord].append(word)

    # once for loop ends check final string
    else:
        if getMusic: seek[-1] += " " + temp.rstrip()    

    # compiles music nouns strings using lists
    # ex. turns  ["around", "the" "world"] into "around the world"
    joined_music = [" ".join( mw ) for n, mw in sorted(musicWords.items())]
    result = list()
    for i in seek:
        if i != '':
            i = i.strip()
            if i in joined_music or i not in LEXI_KEYS:
                result.append("[musicNoun]")
            else:
                result.append(i)

    resetLexicon() # necessary for making sure all phrases don't use previous data 
    return result, joined_music

# return dict of the parsed sentences and the music nouns for data retrieval
def compile_msg(msg:str):
    msg = msg.lower()
    query, musicNouns = createMusic(msg)
    parsed = CYKParse(query , getGrammar())
    # print(parsed)
    return parsed, musicNouns

# A Python implementation of the AIMA CYK-Parse algorithm in Fig. 23.5 (p. 837).
def CYKParse(words, grammar):
    T = {}
    P = {}
    # Instead of explicitly initializing all P[X, i, k] to 0, store
    # only non-0 keys, and use this helper function to return 0 as needed.
    def getP(X, i, k):
        key = str(X) + '/' + str(i) + '/' + str(k)
        if key in P:
            return P[key]
        else:
            return 0
    # Insert lexical categories for each word
    for i in range(len(words)):
        for X, p in getGrammarLexicalRules(grammar, words[i]):
            P[X + '/' + str(i) + '/' + str(i)] = p
            T[X + '/' + str(i) + '/' + str(i)] = Tree.Tree(X, None, None, lexiconItem=words[i])
    # printV('P:', P)
    # printV('T:', [str(t)+':'+str(T[t]) for t in T])
    # Construct X_i:j from Y_i:j + Z_j+i:k, shortest spans first
    for i, j, k in subspans(len(words)):
        for X, Y, Z, p in getGrammarSyntaxRules(grammar):
            printV('i:', i, 'j:', j, 'k:', k, '', X, '->', Y, Z, '['+str(p)+']', 
                    'PYZ =' ,getP(Y, i, j), getP(Z, j+1, k), p, '=', getP(Y, i, j) * getP(Z, j+1, k) * p)
            PYZ = getP(Y, i, j) * getP(Z, j+1, k) * p
            if PYZ > getP(X, i, k):
                printV('     inserting from', i, '-', k, ' ', X, '->', T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)],
                            'because', PYZ, '=', getP(Y, i, j), '*', getP(Z, j+1, k), '*', p, '>', getP(X, i, k), '=',
                            'getP(' + X + ',' + str(i) + ',' + str(k) + ')')
                P[X + '/' + str(i) + '/' + str(k)] = PYZ
                T[X + '/' + str(i) + '/' + str(k)] = Tree.Tree(X, T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)])
    print('T:', [str(t)+':'+str(T[t]) for t in T])
    return T, P

# Python uses 0-based indexing, requiring some changes from the book's
# 1-based indexing: i starts at 0 instead of 1
def subspans(N):
    for length in range(2, N+1):
        for i in range(N+1 - length):
            k = i + length - 1
            for j in range(i, k):
                yield i, j, k

# These two getXXX functions use yield instead of return so that a single pair can be sent back,
# and since that pair is a tuple, Python permits a friendly 'X, p' syntax in the calling routine.
def getGrammarLexicalRules(grammar, word):
    for rule in grammar['lexicon']:
        if rule[1] == word:
            yield rule[0], rule[2]

def getGrammarSyntaxRules(grammar):
    for rule in grammar['syntax']:
        yield rule[0], rule[1], rule[2], rule[3]
 
def getGrammar():
    return {
        'syntax' : [
            ['S', 'Greeting', 'S', 1 ],
            ['S', 'WQuestion', 'VP', 0.9 ],
            ['S', 'WQuestion', 'Verb', 0.5 ],
            ['S', 'WQuestion', 'S', 0.25 * 0.5],
            ['S', 'WQuestion', 'NP', 0.25 * 0.5],
            ['S', 'WQuestion', 'Noun', 0.25 * 0.5], 
            ['S', 'WQuestion', 'MusicNoun', 0.25 * 0.5],

            ['S', 'reject', 'S', 1 ],
            ['S', 'reject', 'VP', 0.9 ],
            ['S', 'reject', 'Verb', 0.9 ],
            ['S', 'reject', 'S', 0.25 * 0.5],
            ['S', 'reject', 'NP', 0.25 * 0.5],
            ['S', 'reject', 'Noun', 0.25 * 0.5], 
            ['S', 'reject', 'MusicNoun', 0.25 * 0.5], 

            ['S', 'S', 'NP', 0.9 * 0.45 * 0.6],
            ['S', 'S', 'Noun', 0.9 * 0.45 * 0.6],
            ['S', 'NP', 'VP', 0.9 * 0.45 * 0.6],
            ['S', 'Pronoun', 'VP', 0.9 * 0.25 * 0.6],
            ['S', 'Name', 'VP', 0.9 * 0.10 * 0.6],
            ['S', 'Noun', 'VP', 0.9 * 0.10 * 0.6],
            ['S', 'MusicNoun', 'VP', 0.9 * 0.10 * 0.6],
            ['S', 'NP', 'Verb', 0.9 * 0.45 * 0.4],
            ['S', 'Pronoun', 'Verb', 0.9 * 0.25 * 0.4],
            ['S', 'MusicNoun', 'Verb', 0.9 * 0.10 * 0.4],
            ['S', 'S', 'Conj+S', 0.1],
            ['S', 'S', 'Pronoun', 0.2],
            ['S', 'S', 'PP', 0.2],
            ['S', 'RelClause', 'VP', 0.9 * 0.10 * 0.6],
            ['S', 'RelClause', 'S', 0.9 * 0.10 * 0.6],

            ['Conj+S', 'Conj', 'S', 1.0],

            ['NP', 'Article', 'Noun', 0.25],
            ['NP', 'Article+Adjs', 'Noun', 0.15],
            ['NP', 'Article+Adjective', 'Noun', 0.05],
            # ['NP', 'Digit', 'Digit', 0.15],
            ['NP', 'NP', 'PP', 0.2],
            ['NP', 'NP', 'Prep', 0.2],
            ['NP', 'NP', 'MusicNoun', 0.2],
            ['NP', 'NP', 'RelClause', 0.15],
            ['NP', 'NP', 'Conj+NP', 0.05],

            ['NP', 'MusicNoun', 'Adjective', 0.2],
            ['NP', 'Adjective', 'Noun', 0.1],
            
            ['NP', 'Article', 'MusicNoun', 0.25],
            ['NP', 'Article+Adjs', 'MusicNoun', 0.15],
            ['NP', 'Article+Adjective', 'MusicNoun', 0.05],
            
            ['Article+Adjs', 'Article', 'Adjs', 1.0],
            ['Article+Adjective', 'Article', 'Adjective', 1.0],
            ['Conj+NP', 'Conj', 'NP', 1.0],
            ['VP', 'VP', 'NP', 0.6 * 0.55],
            ['VP', 'VP', 'Noun', 0.6 * 0.55],
            ['VP', 'VP', 'MusicNoun', 0.6 * 0.55],
            ['VP', 'VP', 'Adjective', 0.6 * 0.1],
            ['VP', 'VP', 'PP', 0.6 * 0.2],
            ['VP', 'VP', 'Adverb', 0.6 * 0.15],
            ['VP', 'VP', 'Article', 0.4 * 0.15],
            ['VP', 'Verb', 'NP', 0.4 * 0.55],
            ['VP', 'Verb', 'NP', 0.6 * 0.55],
            ['VP', 'Verb', 'MusicNoun', 0.6 * 0.55],
            ['VP', 'Verb', 'Adjective', 0.4 * 0.1],
            ['VP', 'Verb', 'PP', 0.4 * 0.2],
            ['VP', 'Verb', 'Adverb', 0.4 * 0.15],
            ['VP', 'Verb', 'Article', 0.4 * 0.15],
            ['Adjs', 'Adjective', 'Adjs', 0.8],
            ['PP', 'Prep', 'NP', 0.65],
            ['PP', 'Prep', 'VP', 0.65],
            ['PP', 'Prep', 'Pronoun', 0.2],
            ['PP', 'Prep', 'Name', 0.1],
            ['PP', 'Prep', 'Noun', 0.05],
            ['PP', 'Prep', 'MusicNoun', 0.25],
            ['RelClause', 'RelPro', 'VP', 0.6],
            ['RelClause', 'RelPro', 'Verb', 0.4],
            ['MusicNoun', 'MusicNoun', 'MusicNoun' , 1]
        ],
        'lexicon' : [
            ['MusicNoun', '[musicNoun]', 0.7 ],
            ['WQuestion', 'what', 0.5],
            ['WQuestion', 'when', 0.2],
            ['WQuestion', 'who', 0.2],
            ['Noun', 'lyrics', 0.5],
            ['Noun', 'song', 0.2],
            ['Noun', 'songs', 0.3],
            ['Noun', 'album', 0.3],
            ['Noun', 'albums', 0.3],
            ['Noun', 'remix', 0.3],
            ['Noun', 'covers', 0.3],
            ['Noun', 'interpolations', 0.5],
            ['Noun', 'date', 0.3],
            ['Verb', 'is', 0.2],
            ['Verb', 'was', 0.2],
            ['Verb', 'are', 0.1],
            ['Verb', 'released', 0.2],
            ['Verb', 'did', 0.3],
            ['Verb', 'has', 0.3],
            ['Adjective', 'best', 0.81],
            ['Adverb', 'sampled', 0.2],
            ['Adverb', 'most', 0.05],
            ['Adjective', 'played', 0.3],
            ['Adjective', 'popular', 0.3],
            ['Adjective', 'release', 0.3],
            ['Adjective', 'listened', 0.2],

            ['Adjective', 'follower', 0.2],
            ['Adjective', 'best', 0.2],
            ['Adjective', 'top', 0.2],
            ['Noun', 'type', 0.2],
            ['Noun', 'music', 0.2],
            ['Noun', 'length', 0.2],
            ['Noun', 'tempo', 0.2],
            ['Noun', 'happiness', 0.2],
            ['Noun', 'danceability', 0.2],
            ['Noun', 'energy', 0.2],
            ['Noun', 'popularity', 0.2],
            ['Noun', 'count', 0.2],
            ['Verb', 'make', 0.2],
            ['Adverb', 'does', 0.2],

            ['Pronoun', 'their', 0.1],
            ['Pronoun', 'his', 0.1],
            ['Pronoun', 'its', 0.1],
            ['Pronoun', 'her', 0.1],
            ['Pronoun', 'him', 0.1],
            ['Pronoun', 'she', 0.1],
            ['Pronoun', 'he', 0.1],
            ['Pronoun', 'they', 0.1],
            


            ['RelPro', 'that', 0.4],
            ['RelPro', 'when', 0.2],
            ['Article', 'the', 0.4],
            ['Article', 'a', 0.3],
            ['Article', 'an', 0.05],
            ['Article', 'every', 0.05],
            ['Prep', 'for', 0.4],
            ['Prep', 'from', 0.4],
            ['Prep', 'to', 0.2],
            ['Prep', 'of', 0.2],
            ['Prep', 'in', 0.1],
            ['Prep', 'on', 0.05],
            ['Conj', 'and', 0.5],
            ['Conj', 'or', 0.1],
            ['Prep', 'by', 1],
            ['Greeting' , 'hi', 0.5],
            ['Greeting' , 'hello', 0.5],
            ['reject' , 'Bye', 0.5]
        ]
    }

def getSentenceParse(T):
    sentenceTrees = { k: v for k,v in T.items() if k.startswith('S/0') }
    completeSentenceTree = max(sentenceTrees.keys())
    # print('getSentenceParse', completeSentenceTree)
    for leaf in T[completeSentenceTree].getLeaves():
        # dealing with what to search for
        print(leaf)
    return T[completeSentenceTree]

def lex_as_str():
    #lexicon as string helper function
    x = "{"
    for i in getGrammar()["lexicon"]:
        x += f" '{i[1]}' : 0  ,"
    x = x.rstrip(",")
    return x + "\n}"

STOP_WORDS = {"a", "an", "and", "are", "in", "is", "my", "on", "the", "that", "who", "what", "when"}
LEXICON = dict( [(s[1], 0) for s in getGrammar()['lexicon'] ])
LEXI_KEYS = set(LEXICON.keys())
# print(LEXICON)

# Unit testing code
if __name__ == '__main__':
    verbose = False

    # test cases for createMusic

    # createMusic("What are the lyrics for hand crushed by a mallet by 100 gecs")
    # createMusic("What are the lyrics for for you by leehi")
    # createMusic("What are the lyrics for and july by heize" )
    # createMusic("What are the lyrics for band on the run" )
    createMusic("what is the energy of mic drop by bts"  )
    # createMusic("What are the lyrics for reptilia by the strokes") 
    # createMusic("What are the lyrics for around the world by daft punk")
    # createMusic("What are the most listened songs by Drake")


    # user_input = "when was the release date for xs by rina sawayama"
    # user_input = "what is the following of The Weeknd"
    # user_input = "What are the lyrics for and july by heize" 
    # user_input = "what is his following count"
    # what type of music
    cykp, musicnouns = compile_msg(user_input)
    # getSentenceParse(t["CYK_PARSE"][0])
    print(cykp[0])
    # print(musicnouns)

