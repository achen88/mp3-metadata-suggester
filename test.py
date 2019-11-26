from simple_spotify.api import Spotify
from simple_spotify.authorization import ClientCredentialsFlow
import os

clientId = os.environ.get('SPOTIFY_CLIENT_ID')
clientSecret = os.environ.get('SPOTIFY_CLIENT_SECRET')

if (clientId == None or clientSecret == None):
  print('Error: SPOTIFY_CLIENT_ID + SPOTIFY_CLIENT_SECRET environment variables are required')
  exit(-1)

res = ClientCredentialsFlow.token_request(clientId, clientSecret)

auth = ClientCredentialsFlow(**res)
sp = Spotify(auth)

results = sp.search(q='Joji - SLOW DANCING IN THE DARK (Loud Luxury Remix)')

result = results.tracks.items[0]
for a in result.artists:
  print(a)
print(result.name)
print(result.album)

