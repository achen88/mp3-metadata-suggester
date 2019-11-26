from simple_spotify.api import Spotify
from simple_spotify.authorization import ClientCredentialsFlow
import os
import re

class Searcher:
  def __init__(self):
    clientId = os.environ.get('SPOTIFY_CLIENT_ID')
    clientSecret = os.environ.get('SPOTIFY_CLIENT_SECRET')

    if (clientId == None or clientSecret == None):
      print('Error: SPOTIFY_CLIENT_ID + SPOTIFY_CLIENT_SECRET environment variables are required')
      exit(-1)

    res = ClientCredentialsFlow.token_request(clientId, clientSecret)
    auth = ClientCredentialsFlow(**res)
    self.sp = Spotify(auth)

  def search(self, raw):
    # do some manipulation on raw
    query = raw
    out = ""
    try:
      res = self.sp.search(q=query).tracks.items[0]
      out = ', '.join(res.artists) + ' - ' + res.name
    except:
      out = "**could not find song"
    return out

