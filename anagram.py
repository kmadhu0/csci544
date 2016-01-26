from pprint import pprint
from sys import argv
results=[]

def anagram(s,x,y):
	if x==y:
		results.append(''.join(s))
	else:
		for i in range(x,y+1):
			s[x],s[i]=s[i],s[x]
			anagram(s,x+1,y)
			s[x],s[i]=s[i],s[x]

s=argv[1]
f=argv[2]
anagram(list(s),0,len(s)-1)
results.sort()
file1 = open(f, 'w')
for i in range(0,len(results)):
	if i!=len(results)-1:
		file1.write(results[i]+"\n")
	else:
		file1.write(results[i])
