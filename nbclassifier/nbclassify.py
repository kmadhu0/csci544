from sys import *
import re
import os
from glob import *
import math
from pprint import pprint
import string

if argv[1][-1]=='/':
    argv[1]=argv[1][0:len(argv[1])-1]

def remove_stop_words(sentences):
    #read the stop words
    with open("stop_words.txt",'r') as f:
        stop_words=f.readlines()
    for i in range (0,len(stop_words)):
        stop_words[i]=stop_words[i].replace('\n','')
    ret=[]

    #remove stop words,numbers,empty strings and convert to lowercase
    for i in range(0,len(sentences)):
        sentences[i]=[x for x in sentences[i] if x]
        temp=[val for val in sentences[i] if val not in stop_words]
        temp=[item for item in temp if not item.isdigit()]
        ret.append(temp)
    return ret

def remove_punct(sentences):
    ret=[]
    table = string.maketrans("","")
    for i in range(0,len(sentences)):
        sentences[i]=sentences[i].replace('.','. ')
        sentences[i]=sentences[i].replace(',',', ')
        sentences[i]=sentences[i].replace('!','! ')
        sentences[i]=sentences[i].replace('^','^ ')
        sentences[i]=sentences[i].replace('*','* ')
        sentences[i]=sentences[i].replace('(','( ')
        sentences[i]=sentences[i].replace(')',') ')
        sentences[i]=sentences[i].replace('-','- ')
        sentences[i]=sentences[i].replace('_','_ ')
        sentences[i]=sentences[i].replace('+','+ ')
        sentences[i]=sentences[i].replace('-','- ')
        sentences[i]=sentences[i].replace('=','= ')
        sentences[i]=sentences[i].replace('~','~ ')
        sentences[i]=sentences[i].replace('[','[ ')
        sentences[i]=sentences[i].replace(']','] ')
        sentences[i]=sentences[i].replace('{','{ ')
        sentences[i]=sentences[i].replace('}','} ')
        sentences[i]=sentences[i].replace('\\','\\ ')
        sentences[i]=sentences[i].replace('|','| ')
        sentences[i]=sentences[i].replace(';','; ')
        sentences[i]=sentences[i].replace(':',': ')
        sentences[i]=sentences[i].replace('\'','\' ')
        sentences[i]=sentences[i].replace('\"','\" ')
        sentences[i]=sentences[i].replace('<','< ')
        sentences[i]=sentences[i].replace('>','> ')
        sentences[i]=sentences[i].replace('?','? ')
        sentences[i]=sentences[i].replace('/','/ ')
        sentences[i]=sentences[i].replace('@','@ ')
        sentences[i]=sentences[i].replace('&','& ')
        sentences[i]=sentences[i].translate(table,string.punctuation.replace("'",''))
        sentences[i]=sentences[i].lower()
        ret.append(sentences[i])
    return ret

def count_words(words):
    wc={}
    for word in words:
        wc[word]=wc.get(word,0.0)+1.0
    return wc

#count the features in each class and also perform add-one smoothing
def count_features(features,wc_pos,wc_neg,wc_tru,wc_dec):
    ret=[None]*len(features)
    for i in range(0,len(features)):
        ret[i]=(features[i],wc_pos[features[i]]+1.0,wc_neg[features[i]]+1.0,wc_tru[features[i]]+1.0,wc_dec[features[i]]+1.0)
    return ret


strings=[]
paths=[]
testdir=argv[1]+"/*/*/*/*.txt"

for name in glob(testdir):
    with open(name,'r') as file1:
        paths.append(name)
        strings.append(file1.read().replace('\n',''))

#remove punctuations and lowercase the strings
sentences=remove_punct(strings)

#tokenize the strings
for i in range(0,len(sentences)):
    sentences[i]=sentences[i].split(' ')

#remove the stop words
final_sentences=remove_stop_words(sentences)

f=open('nbmodel.txt','r')
lines=f.readlines()
column_names=lines[0].strip().split(' ')
priors=lines[1].strip().split(' ')
priors=priors[1:]

for i in range(0,len(priors)):
    priors[i]=float(priors[i])

features={}
for i in range(2,len(lines)):
    lines[i]=lines[i].strip().split(' ')
    features[lines[i][0]]=(float(lines[i][1]),float(lines[i][2]),float(lines[i][3]),float(lines[i][4]))

f=open('nboutput.txt','w')
p_pos=0.0
p_neg=0.0
p_dec=0.0
p_tru=0.0
for i in range(0,len(final_sentences)):
    p_pos=priors[0]
    p_neg=priors[1]
    p_tru=priors[2]
    p_dec=priors[3]
    label_a=""
    label_b=""
    for j in range(0,len(final_sentences[i])):
        if final_sentences[i][j] in features:
            p_pos+=features[final_sentences[i][j]][0]
            p_neg+=features[final_sentences[i][j]][1]
            p_tru+=features[final_sentences[i][j]][2]
            p_dec+=features[final_sentences[i][j]][3]
    if p_pos>p_neg:
        label_b="positive"
    else:
        label_b="negative"
    if p_tru>p_dec:
        label_a="truthful"
    else:
        label_a="deceptive"
        
    f.write(label_a+" "+label_b+" "+paths[i]+"\n")
    p_pos=0.0
    p_neg=0.0
    p_dec=0.0
    p_tru=0.0



#read the model file to determine the prior probabilities and the P(text|class) probabilities
#read the testing data into strings
#remove stop words
#tokenize the data
#stem the data
#lemmatize the data
#calculate the probabilities
#assign classes and write result to nboutput.txt
