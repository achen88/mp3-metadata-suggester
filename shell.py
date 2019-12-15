import sys
import os
import readline
from mutagen.easyid3 import EasyID3
from searcher import Searcher

def input_with_prefill(prompt, text):
  def hook():
    readline.insert_text(text)
    readline.redisplay()
  readline.set_pre_input_hook(hook)
  result = input(prompt)
  readline.set_pre_input_hook()
  return result

def main():
  print()

  fd = sys.stdin
  searcher = Searcher()

  if len(sys.argv) <= 1:
    print("ERR: include directory source, DIR=...")
    exit(-1)
  filenames = os.listdir(sys.argv[1])
  filepaths = list(map(lambda x:sys.argv[1] + "/" + x, filenames))
  for i, filepath in enumerate(filepaths):
    print("Labeling:")
    print("  " + filenames[i])
    print()
    artist, title = match_name(searcher, filenames[i][:-4])
    audio = EasyID3(filepath)
    audio["artist"] = artist
    audio["title"] = title
    audio.save()
    print()

def match_name(searcher, raw):
  matches = searcher.search(raw, filter=True)
  for i, (artists, title) in enumerate(matches):
    print("[" + str(i+1) + "] " + ", ".join(artists) + " - " + title)
  print()
  print("Pick a number above to use as a template or a highlighter letter to:")
  print("  start a new Spotify [s]earch,")
  print("  or enter [c]ustom text:")
  print()

  valid_set = ["s", "c"]
  for i in range(len(matches)):
    valid_set.append(str(i+1))

  option = input_loop(valid_set)
  if option == "s":
    query = input("Enter spotify query: ")
    print()
    return match_name(searcher, query)
  elif option == "c":
    artists = input("Enter artists: ")
    title = input("Enter title: ")
    return artists, title
  elif option.isdigit() and 0 < int(option) <= len(matches):
    artists, title = matches[int(option)-1]
    artists = ", ".join(artists)
    print(artists + " - " + title)
    print()
    print("[u]se existing artists + title,")
    print("  or [e]dit fields:")
    print()
    option = input_loop(["u", "e"])
    if option == "e":
      artists = input_with_prefill("Enter artists: ", artists)
      title = input_with_prefill("Enter title: ", title)
    return artists, title
  else:
    raise ValueError("bad state")

def input_loop(valid_set):
  inp = input("Option: ")
  if inp in valid_set:
    return inp
  return input_loop(valid_set)

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
main()
