from searcher import Searcher

f = open('corpus.txt', 'r')
searcher = Searcher()
total = 0
failures = 0
for line in f:
  total += 1
  res = ''
  try:
    artists, name = searcher.search(line[:-1], filter=True)[0]
    res = ', '.join(artists) + ' - ' + name
  except:
    res = '** could not find song'
    failures += 1
  print(line, res)
print('score: ' + str(total-failures) + '/' + str(total))
