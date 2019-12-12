import sys
import os
from mutagen.easyid3 import EasyID3
from searcher import Searcher

print()

fd = sys.stdin
searcher = Searcher()
#for artist, song in searcher.search("kaskade tight"):
#  print(artist, song)

if len(sys.argv) <= 1:
  print("ERR: include directory source, DIR=...")
  exit(-1)
filenames = os.listdir(sys.argv[1])
filepaths = list(map(lambda x:sys.argv[1] + "/" + x, filenames))
for i, filepath in enumerate(filepaths):
  #artist, title = match_name(searcher, filenames[i])
  audio = EasyID3(filepath)
  audio["title"] = "test" + str(i)
  audio.save()

def match_name(searcher, raw):
  return None
"""
else:
  print("Enter a youtube link and press enter, mp3s go to ./out/")
  print("This shell can also batch download from a list")
  print("  Control+C exits")

print("\n> ", end="", flush=True)

try:
  buff = ''
  while True:
    chunk = fd.read(1)
    buff += chunk
    if buff.endswith('\n'):
      res = searcher.search(buff[:-1])
      for obj in res:
        print(obj)
      buff = ''
      print("\n> ", end="")
      sys.stdout.flush()
    if not chunk:
      break
except KeyboardInterrupt:
  sys.stdout.flush()
  pass
"""
