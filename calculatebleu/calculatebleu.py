import sys
import math
import glob
import os
from itertools import tee, islice,izip
from collections import Counter
import re
candidate=[]
reference=[]

with open(sys.argv[1],'r') as fp:
	candidate=fp.read().splitlines()
index=0

if os.path.isfile(sys.argv[2]):
	with open(sys.argv[2],'r') as fp:
		reference.append(fp.read().splitlines())
	index+=1
else:
	for name in glob.glob(sys.argv[2]+"/*.txt"):
		with open(name,'r') as fp:
			reference.append(fp.read().splitlines())
		index+=1

def get_ngram(word_list, n):
  temp_list = word_list
  while True:
    split_1, split_2 = tee(temp_list)
    curr_ngram = tuple(islice(split_1, n))
    if len(curr_ngram) == n:
      yield curr_ngram
      next(split_2)
      temp_list = split_2
    else:
      break


#preprocessing - only case folding now
for i in range(0,len(candidate)):
	candidate[i]=candidate[i].split(" ")
	candidate[i]=filter(None,candidate[i])
	for j in range(0,len(candidate[i])):
		candidate[i][j]=candidate[i][j].lower()

#multiple reference files
for k in range(0,index):
	for l in range(0,len(reference[k])):
		reference[k][l]=reference[k][l].split(" ")
		reference[k][l]=filter(None,reference[k][l])
		for m in range(0,len(reference[k][l])):
			reference[k][l][m]=reference[k][l][m].lower()


unigram_can=[None]*len(candidate)
unigram_clip=[None]*len(candidate)
bigram_can=[None]*len(candidate)
bigram_clip=[None]*len(candidate)
trigram_can=[None]*len(candidate)
trigram_clip=[None]*len(candidate)
quadgram_can=[None]*len(candidate)
quadgram_clip=[None]*len(candidate)

#Multiple reference summaries
unigram_ref=[[]]*index
bigram_ref=[[]]*index
trigram_ref=[[]]*index
quadgram_ref=[[]]*index
for i in range(0,index):
	unigram_ref[i]=[None]*len(reference[i])
	bigram_ref[i]=[None]*len(reference[i])
	trigram_ref[i]=[None]*len(reference[i])
	quadgram_ref[i]=[None]*len(reference[i])

#Step 1: Count n-grams
#candidate summary counting
for i in range(0,len(candidate)):
	# unigram_can[i]={}
	# for j in range(0,len(candidate[i])):
	# 	if candidate[i][j] in unigram_can[i]:
	# 		unigram_can[i][candidate[i][j]]+=1
	# 	else:
	# 		unigram_can[i][candidate[i][j]]=1
	unigram_can[i]=dict(Counter(get_ngram(candidate[i],1)))
	bigram_can[i]=dict(Counter(get_ngram(candidate[i],2)))
	trigram_can[i]=dict(Counter(get_ngram(candidate[i],3)))
	quadgram_can[i]=dict(Counter(get_ngram(candidate[i],4)))

#reference summary counting
for k in range(0,index):
	for l in range(0,len(reference[k])):
		# unigram_ref[k][l]={}
		# for m in range(0,len(reference[k][l])):
		# 	if reference[k][l][m] in unigram_ref[k][l]:
		# 		unigram_ref[k][l][reference[k][l][m]]+=1
		# 	else:
		# 		unigram_ref[k][l][reference[k][l][m]]=1
		unigram_ref[k][l]=dict(Counter(get_ngram(reference[k][l],1)))
		bigram_ref[k][l]=dict(Counter(get_ngram(reference[k][l],2)))
		trigram_ref[k][l]=dict(Counter(get_ngram(reference[k][l],3)))
		quadgram_ref[k][l]=dict(Counter(get_ngram(reference[k][l],4)))

#Step 2: Count clip for each n-gram
for i in range(0,len(candidate)):
	unigram_clip[i]={}
	can_keys=unigram_can[i].keys()
	for item in unigram_can[i]:
		maxi=0.0
		for k in range(0,index):
			if item in unigram_ref[k][i]:
				maxi=max(unigram_ref[k][i][item],maxi)
		unigram_clip[i][item]=min(unigram_can[i][item],maxi)

for i in range(0,len(candidate)):
	bigram_clip[i]={}
	can_keys=bigram_can[i].keys()
	for item in bigram_can[i]:
		maxi=0.0
		for k in range(0,index):
			if item in bigram_ref[k][i]:
				maxi=max(bigram_ref[k][i][item],maxi)
		bigram_clip[i][item]=min(bigram_can[i][item],maxi)

for i in range(0,len(candidate)):
	trigram_clip[i]={}
	can_keys=trigram_can[i].keys()
	for item in trigram_can[i]:
		maxi=0.0
		for k in range(0,index):
			if item in trigram_ref[k][i]:
				maxi=max(trigram_ref[k][i][item],maxi)
		trigram_clip[i][item]=min(trigram_can[i][item],maxi)

for i in range(0,len(candidate)):
	quadgram_clip[i]={}
	can_keys=quadgram_can[i].keys()
	for item in quadgram_can[i]:
		maxi=0.0
		for k in range(0,index):
			if item in quadgram_ref[k][i]:
				maxi=max(quadgram_ref[k][i][item],maxi)
		quadgram_clip[i][item]=min(quadgram_can[i][item],maxi)


#Step 3: Add everything in Step 2
count_clip=[0.0]*4
for i in range(0,len(unigram_clip)):
	for item in unigram_clip[i]:
		count_clip[0]+=unigram_clip[i][item]

for i in range(0,len(bigram_clip)):
	for item in bigram_clip[i]:
		count_clip[1]+=bigram_clip[i][item]

for i in range(0,len(trigram_clip)):
	for item in trigram_clip[i]:
		count_clip[2]+=trigram_clip[i][item]

for i in range(0,len(quadgram_clip)):
	for item in quadgram_clip[i]:
		count_clip[3]+=quadgram_clip[i][item]


#Step 4: Count the number of candidate n-grams
count_total=[0.0]*4
for i in range(0,len(unigram_can)):
	for item in unigram_can[i]:
		count_total[0]+=unigram_can[i][item]

for i in range(0,len(bigram_can)):
	for item in bigram_can[i]:
		count_total[1]+=bigram_can[i][item]

for i in range(0,len(trigram_can)):
	for item in trigram_can[i]:
		count_total[2]+=trigram_can[i][item]

for i in range(0,len(quadgram_can)):
	for item in quadgram_can[i]:
		count_total[3]+=quadgram_can[i][item]

# print "Count clip is "+str(count_clip)
# print "Count total is "+str(count_total)

#Step 5: Calculate p_n
p_n=[0.0]*4
for i in range(0,4):
	p_n[i]=count_clip[i]/count_total[i]
# print p_n
#Step 6: Compute r and c
c=0.0
temp_c=[0.0]*len(candidate)
for i in range(0,len(candidate)):
	for item in unigram_can[i]:
		temp_c[i]+=unigram_can[i][item]

r=0.0
temp_r=[None]*index

for k in range(0,index):
	temp_r[k]=[0.0]*len(reference[k])
	for l in range(0,len(reference[k])):
		for item in unigram_ref[k][l]:
			temp_r[k][l]+=unigram_ref[k][l][item]


difference=[0.0]*len(candidate)
r_values=[0.0]*len(candidate)

for l in range(0,len(candidate)):
	difference[l]=abs(temp_c[l]-temp_r[0][l])
	r_values[l]=temp_r[0][l]

for k in range(0,index):
	for l in range(0,len(candidate)):
		test=abs(temp_c[l]-temp_r[k][l])
		if test<difference[l]:
			difference[l]=test
			r_values[l]=temp_r[k][l]

c=count_total[0]

for i in range(0,len(r_values)):
	r+=r_values[i]

#Step 7: Compute BP
if c>r:
	bp=1.0
else:
	bp=math.exp(1-(r/c))
print (c,r)
#Step 8: Compute BLEU
bleu=bp
w_n=1.0/4
inside=0.0
for i in range(0,4):
	inside+=(w_n*math.log(p_n[i]))

bleu=bp*math.exp(inside)
f=open('bleu_out.txt','w')
f.write(str(bleu))
f.close()
