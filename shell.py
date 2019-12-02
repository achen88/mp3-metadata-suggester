import sys
from searcher import Searcher

print()

fd = sys.stdin
searcher = Searcher()
"""
if len(sys.argv) > 1:
  print("Reading from file...")
  fd = open(sys.argv[1], 'r')
else:
  print("Enter a youtube link and press enter, mp3s go to ./out/")
  print("This shell can also batch download from a list")
  print("  Control+C exits")
"""
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

