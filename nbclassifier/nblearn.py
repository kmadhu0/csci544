from sys import *
import re
import os
from glob import *
import math
import string
from pprint import pprint

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

#remove punctuations
def remove_punct(sentences):
    ret=[None]*len(sentences)
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
        ret[i]=sentences[i]
    return ret

def count_words(words):
    wc={}
    for word in words:
        wc[word]=wc.get(word,0.0)+1.0
    return wc

#count the features in each class and also perform add-one smoothing
def count_features(features,c1,c2):
    ret=[None]*len(features)
    for i in range(0,len(features)):
        ret[i]=[features[i],c1[features[i]]+1.0,c2[features[i]]+1.0]
    return ret

#read the documents as strings
negative_strings=[]
positive_strings=[]
deceptive_strings=[]
truthful_strings=[]

negdir=argv[1]+"/negative_polarity/*/*/*.txt"
posdir=argv[1]+"/positive_polarity/*/*/*.txt"
trudir1=argv[1]+"/negative_polarity/truthful_from_Web/*/*.txt"
trudir2=argv[1]+"/positive_polarity/truthful_from_TripAdvisor/*/*.txt"
decdir1=argv[1]+"/negative_polarity/deceptive_from_MTurk/*/*.txt"
decdir2=argv[1]+"/positive_polarity/deceptive_from_MTurk/*/*.txt"
for name in glob(negdir):
    with open(name,'r') as file1:
        negative_strings.append(file1.read().replace('\n',''))

for name in glob(posdir):
    with open(name,'r') as file1:
        positive_strings.append(file1.read().replace('\n',''))

for name in glob(trudir1):
    with open(name,'r') as file1:
        truthful_strings.append(file1.read().replace('\n',''))
for name in glob(trudir2):
    with open(name,'r') as file1:
        truthful_strings.append(file1.read().replace('\n',''))
for name in glob(decdir1):
    with open(name,'r') as file1:
        deceptive_strings.append(file1.read().replace('\n',''))
for name in glob(decdir2):
    with open(name,'r') as file1:
        deceptive_strings.append(file1.read().replace('\n',''))

#remove punctuations and lowercase the strings
negative=remove_punct(negative_strings)
positive=remove_punct(positive_strings)

truthful=remove_punct(truthful_strings)
deceptive=remove_punct(deceptive_strings)

#tokenize the strings
for i in range(0,len(negative)):
    negative[i]=negative[i].split(' ')
for i in range(0,len(positive)):
    positive[i]=positive[i].split(' ')
for i in range(0,len(truthful)):
    truthful[i]=truthful[i].split(' ')
for i in range(0,len(deceptive)):
    deceptive[i]=deceptive[i].split(' ')

#remove the stop words
final_neg=remove_stop_words(negative)
final_pos=remove_stop_words(positive)

final_tru=remove_stop_words(truthful)
final_dec=remove_stop_words(deceptive)

neg_counts=[]
pos_counts=[]
tru_counts=[]
dec_counts=[]

#build the unique set of features
pos_union=set().union(*final_pos)
neg_union=set().union(*final_neg)
tru_union=set().union(*final_tru)
dec_union=set().union(*final_dec)

#list of features
features= list(set(pos_union | neg_union))
features1= list(set(tru_union | dec_union))

for i in range(0,len(negative)):
    neg_counts.append(count_words(final_neg[i]))
    pos_counts.append(count_words(final_pos[i]))

for i in range(0,len(truthful)):
    tru_counts.append(count_words(final_tru[i]))
    dec_counts.append(count_words(final_dec[i]))


wc_neg = dict(neg_counts[0].items() + neg_counts[1].items() +
    [(k, neg_counts[0][k] + neg_counts[1][k]) for k in set(neg_counts[1]) & set(neg_counts[0])])
wc_pos = dict(pos_counts[0].items() + pos_counts[1].items() +
    [(k, pos_counts[0][k] + pos_counts[1][k]) for k in set(pos_counts[1]) & set(pos_counts[0])])
wc_dec = dict(dec_counts[0].items() + dec_counts[1].items() +
    [(k, dec_counts[0][k] + dec_counts[1][k]) for k in set(dec_counts[1]) & set(dec_counts[0])])
wc_tru = dict(tru_counts[0].items() + tru_counts[1].items() +
    [(k, tru_counts[0][k] + tru_counts[1][k]) for k in set(tru_counts[1]) & set(tru_counts[0])])

for i in range(2,len(neg_counts)):
    wc_neg = dict(wc_neg.items() + neg_counts[i].items() +
        [(k, wc_neg[k] + neg_counts[i][k]) for k in set(wc_neg) & set(neg_counts[i])])
    wc_pos = dict(wc_pos.items() + pos_counts[i].items() +
        [(k, wc_pos[k] + pos_counts[i][k]) for k in set(wc_pos) & set(pos_counts[i])])
    wc_dec = dict(wc_dec.items() + dec_counts[i].items() +
        [(k, wc_dec[k] + dec_counts[i][k]) for k in set(wc_dec) & set(dec_counts[i])])
    wc_tru = dict(wc_tru.items() + tru_counts[i].items() +
        [(k, wc_tru[k] + tru_counts[i][k]) for k in set(wc_tru) & set(tru_counts[i])])

#In all classes, give 0 frequency to words that aren't present in that class. count_features will perform add-one smoothing
pos_diff=list(set(dict(wc_neg))-set(dict(wc_pos)))
for i in range(0,len(pos_diff)):
    wc_pos[pos_diff[i]]=0.0

neg_diff=list(set(dict(wc_pos))-set(dict(wc_neg)))
for i in range(0,len(neg_diff)):
    wc_neg[neg_diff[i]]=0.0

tru_diff=list(set(dict(wc_dec))-set(dict(wc_tru)))
for i in range(0,len(tru_diff)):
    wc_tru[tru_diff[i]]=0.0

dec_diff=list(set(dict(wc_tru))-set(dict(wc_dec)))
for i in range(0,len(dec_diff)):
    wc_dec[dec_diff[i]]=0.0

feature_counts=count_features(features,wc_pos,wc_neg)
feature_counts1=count_features(features1,wc_tru,wc_dec)

#prior probabilities
neg_prior=math.log((len(negative_strings)/(len(negative_strings)+len(positive_strings)+0.0)))
pos_prior=math.log((len(positive_strings)/(len(negative_strings)+len(positive_strings)+0.0)))
dec_prior=math.log((len(deceptive_strings)/(len(deceptive_strings)+len(truthful_strings)+0.0)))
tru_prior=math.log((len(truthful_strings)/(len(deceptive_strings)+len(truthful_strings)+0.0)))

total_neg=0
total_pos=0
total_tru=0
total_dec=0

for i in range(0,len(feature_counts)):
    total_pos+=feature_counts[i][1]
    total_neg+=feature_counts[i][2]
    total_tru+=feature_counts1[i][1]
    total_dec+=feature_counts1[i][2]

#calculate log probabilities of P(word|class)
for i in range(0,len(feature_counts)):
    feature_counts[i][1]=math.log(feature_counts[i][1]/total_pos)
    feature_counts[i][2]=math.log(feature_counts[i][2]/total_neg)
    feature_counts1[i][1]=math.log(feature_counts1[i][1]/total_tru)
    feature_counts1[i][2]=math.log(feature_counts1[i][2]/total_dec)

for i in range(0,len(feature_counts)):
    feature_counts[i]=tuple(feature_counts[i])
    feature_counts1[i]=tuple(feature_counts1[i])

feature_counts.sort()
feature_counts1.sort()
feature_counts=feature_counts[82:]
feature_counts1=feature_counts1[82:]

#write data to file
f=open('nbmodel.txt','w')
f.write("Column1 Pos Neg Tru Dec\n")
f.write("Priors "+str(pos_prior)+" "+str(neg_prior)+" "+str(tru_prior)+" "+str(dec_prior)+"\n")
for i in range(0,len(feature_counts)):
    f.write(feature_counts[i][0]+" "+str(feature_counts[i][1])+" "+str(feature_counts[i][2])+" "+str(feature_counts1[i][1])+" "+str(feature_counts1[i][2])+"\n")
