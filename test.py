from searcher import Searcher

f = open('corpus.txt', 'r')
searcher = Searcher()
total = 0
failures = 0
for line in f:
  total += 1
  res = searcher.search(line[:-1])
  if res == '** could not find song': failures += 1
  print(line, res)
print('score: ' + str(total-failures) + '/' + str(total))
