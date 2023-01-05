from bearer import return_access_token
from spotifyApi import *

searchTerm = "ocean man"

Bearer = open("token.tkn","r").read() # very simple way of storing bearer token, would reccomend encryption of some sort but i cba so

if searchTrack(Bearer,searchTerm).get('tracks') == None:
    Bearer = return_access_token()
    open("token.tkn","w").write(Bearer)

trackId = searchTrack(Bearer,searchTerm)['tracks']['items'][0]['id']

print(playTrack(Bearer,trackId))
