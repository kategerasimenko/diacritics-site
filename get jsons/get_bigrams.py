import re
import json
import itertools
import time
import os

def bigram_freq(words,alphlet):
    d = {}
    for i in range(1,len(words)):
            word = words[i]
            word = word.strip('.,:;!?')
            if re.search('[^'+alphlet+']',word) == None and word != '':
                if words[i-1] == words[i-1].strip('.,:;!?') and re.search('[^'+alphlet+']',words[i-1]) == None and words[i-1] != '':
                    if words[i-1]+' '+word in d:
                        d[words[i-1]+' '+word] += 1
                    else:
                        d[words[i-1]+' '+word] = 1
    freql = sorted(d, key=d.get, reverse=True)
    if len(freql) > 150000:
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

def read_file(name):
    f = open(name,'r',encoding='utf-8-sig')
    text = f.read()
    return text

def write_json(text,name):
    s = json.dumps(text,indent=2,ensure_ascii=False)
    f = open(name,'w',encoding='utf-8-sig')
    f.write(s)
    f.close()

langs = ['buryat','chuvash','bashkir','komi','mari','hill mari','tatar','udmurt','kalmyk','veps']
for lang in langs:
    print(lang)
    words = read_file('./'+lang+'/output_sent.txt')
    alphs = read_file('./'+lang+'/alphs.csv').split(';')
    alph = alphs[0]
    alph_no_dia = alphs[1]
    dia = alphs[2]
    no_dia = alphs[3]
    n = 3

    bifreqlist = bigram_freq(words.split(),alph)
    write_json(bifreqlist,'./'+lang+'/bigram_freqlist.json')
