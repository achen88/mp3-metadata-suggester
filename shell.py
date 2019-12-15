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
    artist, title = match_name(searcher, filenames[i][:-4], infer=True)
    audio = EasyID3(filepath)
    audio["artist"] = artist
    audio["title"] = title
    audio.save()
    print()

def match_name(searcher, raw, infer=False):
  artists = ""
  title = ""
  hyphen = raw.find('-')
  infer = infer and hyphen != -1
  if infer:
    artists = raw[:hyphen].strip()
    title = raw[hyphen+1:].strip()
    print("Inferred artists: " + artists)
    print("Inferred title  : " + title)
    print()
  matches = searcher.search(raw, filter=True)
  for i, (match_artists, match_title) in enumerate(matches):
    print("[" + str(i+1) + "] " + ", ".join(match_artists) + " - " + match_title)
  print()
  print("Pick a number above to use as a template or a highlighter letter to:")
  if infer:
    print("  [u]se inferred artists + title,")
    print("  [e]dit inferred info as template,")
  print("  start a new Spotify [s]earch,")
  print("  or enter [c]ustom text:")
  print()

  valid_set = ["s", "c"]
  if infer:
    valid_set.extend(["u", "e"])
  for i in range(len(matches)):
    valid_set.append(str(i+1))

  option = input_loop(valid_set)
  if option == "s":
    query = input("Enter spotify query: ")
    print()
    return match_name(searcher, query)
  elif option == "c":
    artists = input("Enter artists: ")
    title = input("Enter title  : ")
    return artists, title
  elif option == "u" or option == "e":
    if option == "e":
      artists = input_with_prefill("Enter artists: ", artists)
      title = input_with_prefill("Enter title  : ", title)
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
      title = input_with_prefill("Enter title  : ", title)
    return artists, title
  else:
    raise ValueError("bad state")

def input_loop(valid_set):
  inp = input("Option: ")
  if inp in valid_set:
    return inp
  return input_loop(valid_set)

main()
