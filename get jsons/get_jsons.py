import re
import json
import itertools
import time
import os


def read_file(name):
    f = open(name,'r',encoding='utf-8-sig')
    text = f.read()
    return text

def freq(words):
    d = {}
    for word in words:
        if word in d:
            d[word] += 1
        else:
            d[word] = 1
    freql = sorted(d, key=d.get, reverse=True)
    if len(freql) > 35000:
        a = d[freql[0]]
        i = 0
        alph = []
        while a >= 3:
            alph.append(freql[i])
            i += 1
            a = d[freql[i]]
    else:
        alph = freql
    return alph

def n_grams(alph,n):
    ngrams = list(itertools.product(alph,repeat=n))
    ngrams = list(map(lambda x:''.join(x),ngrams))
    ngrams.sort()
    return ngrams
            
def more_trans_prob(probs,alph,words):
    a = 0
    for letter in alph:
        totalnum = len(re.findall(letter,words))
        if totalnum != 0:
            probs[letter] = {}
            for nextletter in alph:
                if nextletter.startswith(letter[1:]):
                    prob = len(re.findall(letter+nextletter[-1],words)) / totalnum
                    if prob != 0:
                        probs[letter][nextletter] = prob
    return probs


def trans_prob(words,alph,n,alphlet,alphlet_no_dia):
    probs = {}
    hashngrams = []
    for i in range(1,n):
        ngrams = n_grams(alphlet,i)
        nextngrams = n_grams(alphlet,i+1)
        for ngram in ngrams:
            ngramstrbegin = '#'*(n-i)+ngram
            hashngrams.append(ngramstrbegin)
    probs = more_trans_prob(probs,alph,words)
    return probs


def no_dia_vars(ngram,alph,alph_no_dia):
    emitvar = ['']
    for letter in ngram:
        num = len(re.findall(letter,alph))
        emitvar = emitvar * num
        for i in range(num):
            emitvar[int((i*(len(emitvar) / num))):int(((i+1)*(len(emitvar) / num)))] = \
                                         list(map(lambda x: x + alph_no_dia[alph.index(letter)+i],emitvar[int((i*(len(emitvar) / num))):int(((i+1)*(len(emitvar) / num)))]))
    return emitvar
       


def start_prob(words,ngrams,alph,n):
    start_prob = {}
    totalnum = len(re.findall('\\b\\w',words))
    a = 0
    for letter in alph:
        start_prob['#'*(n-1)+letter] = len(re.findall('\\b'+letter,words)) / totalnum
    return start_prob

def write_json(text,name):
    s = json.dumps(text,indent=2,ensure_ascii=False)
    f = open(name,'w',encoding='utf-8-sig')
    f.write(s)
    f.close()

langs = ['buryat','chuvash','bashkir','komi','mari','hill mari','tatar','udmurt','kalmyk','veps']
for lang in langs:
    print(lang)
    words = read_file('./'+lang+'/input_new.txt')
    alphs = read_file('./'+lang+'/alphs.csv').split(';')
    alph = alphs[0]
    alph_no_dia = alphs[1]
    dia = alphs[2]
    no_dia = alphs[3]
    n = 3

    freqlist = freq(words.split('#'*(n-1)))
    write_json(freqlist,'./'+lang+'/freqlist.json')
    print('freq done')
    
    ngrams = set(n_grams(alph,n))
    print('ngrams done')
    
    start_p = start_prob(words,ngrams,alph,n)
    write_json(start_p,'./'+lang+'/start_'+str(n)+'.json')
    print('start_p done')

    trans_p = trans_prob(words,ngrams,n,alph,alph_no_dia)
    write_json(trans_p,'./'+lang+'/trans_'+str(n)+'.json')
    print('trans_p done')
