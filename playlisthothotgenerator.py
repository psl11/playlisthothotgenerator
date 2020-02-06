import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
cid = "bd4f9694cc634dd1ba46e76f0cf5cbde"
secret = "2eff96794dbe4bf09f9990397b5f1d1b"

# Spotify Data
userID = "1137611647"
playlistID = "7EtgqevzsxnS85BgJCJrwd"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 
sp.trace = False

# Genres Families


# FUNCTIONS AREA

# Generic Functions

# Search a specific word in a string
def search_word_in_string(needle, the_string):
	haystack = the_string.split() 
	
	for word in haystack:
		if word == needle:
			return True

	return False

# Search a substring
def search_substr_in_string(needle, haystack):
  return needle in haystack


# Specific functions

# Get the full Playlist (withou pagination)
def get_playlist_tracks(username,playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    return tracks

# Gives a list of simplified genres based on a list of genres and subgenres
def get_simple_genres(song_genres):
	simple_genres = []
	for genre in song_genres:
		if is_electronic(genre):
			simple_genres.append("electronic")
		if is_jazz(genre):
			simple_genres.append("jazz")
		if is_metal(genre):
			simple_genres.append("metal")
		if is_hip_hop(genre):
			simple_genres.append("hip-hop")
		if is_pop(genre):
			simple_genres.append("pop")
		if is_pop_rock(genre):
			simple_genres.append("pop-rock")
		if is_rock(genre):
			simple_genres.append("rock")
		if is_trap(genre):
			simple_genres.append("trap")

	simple_genres = list(dict.fromkeys(simple_genres))			# Eliminate duplicated elements
	return simple_genres

def is_electronic(genre):
	return search_word_in_string("edm", genre) or search_substr_in_string("electro", genre)

def is_jazz(genre):
	return search_word_in_string("jazz", genre) or search_word_in_string("blues", genre) or search_substr_in_string("r&b", genre) 

def is_metal(genre):
	return search_substr_in_string("metal", genre) or search_substr_in_string("hard rock", genre) or search_word_in_string("grunge", genre)

def is_hip_hop(genre):
	return search_substr_in_string("rap", genre) or search_substr_in_string("hip hop", genre)

def is_pop(genre):
	return search_substr_in_string("pop", genre)

def is_pop_rock(genre):
	return search_substr_in_string("punk", genre) or search_substr_in_string("pop rock", genre) or search_word_in_string("indie", genre)

def is_rock(genre):
	return search_substr_in_string("rock", genre)

def is_trap(genre):
	return search_word_in_string("trap", genre)


# CODE AREA    
songs = get_playlist_tracks(userID, playlistID)
genres_counter = {}
simple_genres_counter = {}

# We creathe this dictionary in order to get the genres from an artist only once from the API
artists_genres = {}

# Genres List
playlists = {}
playlists["electronic"] = []
playlists["jazz"] = []
playlists["metal"] = []
playlists["hip-hop"] = []
playlists["pop"] = []
playlists["pop-rock"] = []
playlists["rock"] = []
playlists["trap"] = []


print("Total de canciones: " + str(len(songs)))

# Create the playlist by genres
for song in songs:
	if song["track"]["artists"][0]["id"] is not None:
		artist_id = song["track"]["artists"][0]["id"]			# TODO different artist in the same track
		
		if artist_id in artists_genres:							# Check if we already have the artist saved
			genres = artists_genres[artist_id]
		else:
			genres = sp.artist(artist_id)["genres"]				# Get the artist genres from the API
			artists_genres[artist_id] = genres

		simple_genres = get_simple_genres(genres)				# Simplify the genres

		for genre in simple_genres:
			playlists[genre].append(song["track"]["id"])		# Add the track in the specific new playlist by Genre

			if genre in simple_genres_counter:
			 	simple_genres_counter[genre] += 1
			else:
			    simple_genres_counter[genre] = 1				# Initialize the counter in 1


sorted_genres = sorted(simple_genres_counter.items(), key=lambda x: x[1])

print(sorted_genres)
print(playlists["rock"])

