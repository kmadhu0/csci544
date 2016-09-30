#CSCI 544 Homework 6 - Python script to build the transition graph and calculate the emission probabilities
import sys
import re
from pprint import pprint
import json
split_data=[]
lookup={}
trans_counts={}
em_counts={}
graph={"q0":{}}
emission={}
postags_all=[]
with open(sys.argv[1],'r') as f:
    for data in f:
        postags_all.append(re.findall("/[A-Z][A-Z0-9] |/[A-Z][A-Z0-9]\\n", data))
        temp=data.split(" ")
        temp[-1]=temp[-1][:-1]
        split_data.append(temp)
        for i in range(0,len(temp)):
            emission[temp[i][:-3]]={}

#extract the list of POS tags used in the corpus
postags=[item for sublist in postags_all for item in sublist]

#removes \n from POS tags
for i in range(0,len(postags)):
    postags[i]=postags[i][1:3]

postags=list(set(postags))
postags.append("q0")

for i in range(0,len(postags)):
    lookup[postags[i]]=i
    trans_counts[postags[i]]=0.0
    if postags[i]!='q0':
        em_counts[postags[i]]=0
        graph['q0'][postags[i]]=0
        graph[postags[i]]={}
        for j in range(0,len(postags)):
            if postags[j]!="q0":
                graph[postags[i]][postags[j]]=0.0

#count the tag occurrences needed to build the transition graph
for i in range(0,len(split_data)):
    trans_counts['q0']+=1
    for j in range(0,len(split_data[i])-1):
        word=split_data[i][j][:-3]
        curr_tag=split_data[i][j][-2:]
        next_tag=split_data[i][j+1][-2:]
        if j==0:
            graph['q0'][curr_tag]+=1.0
        trans_counts[curr_tag]+=1
        em_counts[curr_tag]+=1
        graph[curr_tag][next_tag]+=1.0
        if curr_tag in emission[word]:
            emission[word][curr_tag]+=1.0
        else:
            emission[word][curr_tag]=1.0
    last_word=split_data[i][j+1][:-3]
    last_tag=split_data[i][j+1][-2:]
    em_counts[last_tag]+=1.0

#build the graph structure with the transition probabilities

for inittag in graph:
    for finaltag in em_counts:
        if graph[inittag][finaltag]==0:
            graph[inittag][finaltag]=1/(trans_counts[inittag]+len(em_counts))
        else:
            graph[inittag][finaltag]/=(trans_counts[inittag]+len(em_counts))

#calculate the emission probabilities
reverse_lookup={v: k for k, v in lookup.items()}
for word in emission:
    for tag in emission[word]:
        emission[word][tag]/=em_counts[tag]

with open('hmmmodel.txt', 'w') as fp:
    json.dump(reverse_lookup, fp)
    fp.write("\n")
    json.dump(graph,fp)
    fp.write("\n")
    json.dump(emission,fp)
