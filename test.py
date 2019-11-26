from searcher import Searcher

f = open('corpus.txt', 'r')
searcher = Searcher()
for line in f:
  print(line, searcher.search(line))
