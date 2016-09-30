from itertools import tee, islice,izip
from collections import Counter
import re
words = re.findall("\w+","the quick person did not realize his speed and the quick person bumped")
def ngrams(lst, n):
  tlst = lst
  while True:
    a, b = tee(tlst)
    l = tuple(islice(a, n))
    if len(l) == n:
      yield l
      next(b)
      tlst = b
    else:
      break

print Counter(ngrams(words,2))