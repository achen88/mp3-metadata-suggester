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
    auth = ClientCredentialsFlow(**res, scope="user-read-private")
    self.sp = Spotify(auth)

  def search(self, raw, filter=False):
    # do some manipulation on raw
    query = raw
    if filter: 
      query = self.filter(query)
    try:
      res = self.sp.search(q=query).tracks.items[:4]
      artists = [[str(artist) for artist in res[i].artists] for i in range(len(res))]
      names = [obj.name for obj in res]
      return list(zip(artists, names))
    except:
      raise ValueError("song not found")

  def filter(self, raw):
    def parenrepl(matchobj):
      if matchobj and re.search('remix', matchobj.group(), re.IGNORECASE):
        return matchobj.group()
      return ''
    raw = re.sub('&', '', raw)
    raw = re.sub('[\(\[].*[\)\]]', parenrepl, raw)
    raw = re.sub('((ft\.)|(feat\.)|(featuring)).*-', '', raw, flags=re.IGNORECASE)
    raw = re.sub('((ft\.)|(feat\.)|(featuring)).*$', '', raw, flags=re.IGNORECASE)
    return raw
