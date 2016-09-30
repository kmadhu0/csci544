#CSCI 544 Homework 6 - Python script to calculate the POS tags of the unsees data using the Viterbi algorithm
import sys
import re
from pprint import pprint
from copy import deepcopy
import json

graph={}
emission={}

with open('hmmmodel.txt', 'r') as fp:
	lines = fp.readlines()

reverse_lookup=json.loads(lines[0])
graph = json.loads(lines[1])
emission=json.loads(lines[2])
fp.close()

f=open(sys.argv[1],"r")

f1=open("hmmoutput.txt",'w')
for sentence in f:
    sentence=sentence.strip()
    words=sentence.split()
    history={'q0':[1,'null']}
    current_tags={}
    level=0
    result=[]
    for word in words:
        current_tags={}
        #case when unknown word is seen in test data. Ignore the emission probability. Therefore, set to 1.
        if word not in emission:
            emission[word]={}
            for tag in graph:
              if tag!='q0':
                emission[word][tag]=1

        #Calculating the viterbi algorithm score
        for curr_tag in emission[word]:
            maxi=0
            max_parent=''
            for prev_tag in history:
                score=history[prev_tag][0]*graph[prev_tag][curr_tag]*emission[word][curr_tag]
                if score>=maxi:
                    maxi=score
                    max_parent=prev_tag
            current_tags[curr_tag]=[maxi,max_parent]
        result.insert(0,current_tags)
        level+=1
        history=deepcopy(current_tags)
    #Selecting the tag with highest score. This is done for each word
    i=0
    max_score=0
    max_tag=''
    final_tags=[]
    for item in result[i]:
        if max_score<= result[i][item][0]:
            max_score=result[i][item][0]
            max_tag=item
    final_tags.insert(0,max_tag)
    i+=1
    while i<level:
        final_tags.insert(0,result[i-1][max_tag][1])
        max_tag=result[i-1][max_tag][1]
        i+=1
    index=0

    #write the tagged sentences to file
    for word in words:
        f1.write(word)
        f1.write('/')
        f1.write(final_tags[index])
        index+=1
        f1.write(' ')
    f1.write('\n')
f1.close()
