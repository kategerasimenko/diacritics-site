import re
import json
import itertools
import os

def read_file(name):
    f = open(name,'r',encoding='utf-8-sig')
    text = f.read()
    return text

#выбор из частотного словаря варианта, если он единственный
def select(obs,prevobs,freqlist,dias,no_dias):
    mark = True
    gotobi = False
    var = insert_dia(obs.lower(),dias,no_dias)
    indices = []
    for i in var:
        try:
            indices.append(freqlist.index(prevobs.lower()+i))
        except:
            indices.append(-1)
    maxvar = max(indices)
    if maxvar == -1:
        mark = False
        return obs,mark,gotobi
    else:
        if len(indices) > 1 and sorted(indices)[-2] != -1:
            mark = False
            gotobi = True
            return obs,mark,gotobi
        else:
            varn = var[indices.index(maxvar)]
            newvar = ''
            for i in range(len(obs)):
                if obs[i] == obs[i].upper():
                    newvar += varn[i].upper()
                else:
                    newvar += varn[i]
            return newvar,mark,gotobi

        
#Витерби, где состояния генерируются на ходу (все варианты расстановки диакритик в данной триграмме)
def not_viterbi(start_p,trans_p,inp,n,dias,no_dias):
    V = [{}]
    obs = inp.lower()
    varstates = insert_dia(obs[:n],dias,no_dias)
    for i in varstates:
        try:
            V[0][i] = start_p[i]
        except:
            continue
    if inp[n-1] == inp[n-1].upper():
        path = {x: x.upper() for x in varstates}
    else:
        path = {x: x for x in varstates}
    for t in range(1, len(obs)-(n-1)):
        a = 0
        V.append({})
        newpath = {}
        varstates = insert_dia(obs[t:(t+n)],dias,no_dias)
        prevvarstates = insert_dia(obs[(t-1):(t+n-1)],dias,no_dias)
        for y in varstates:
            probarr = []
            for y0 in prevvarstates:
                try:
                    prob = V[t-1][y0] * trans_p[y0][y]
                    probarr.append((prob,y0))
                except:
                    continue
            try:
                (prob,state) = max(probarr)
                V[t][y] = prob
                if inp[t+n-1] == inp[t+n-1].upper():
                    newpath[y] = path[state] + y[-1].upper()
                else:
                    newpath[y] = path[state] + y[-1]
                a += 1
            except:
                continue
        if a == 0:
            prevprob = []
            for y in prevvarstates:
                try:
                    prevprob.append((V[t-1][y],y))
                except:
                    continue
            V[t][obs[t:(t+n)]] = max(prevprob)[0]      
            if inp[t+n-1] == inp[t+n-1].upper():
                newpath[obs[t:(t+n)]] = path[max(prevprob)[1]] + obs[t+n-1].upper()
            else:
                newpath[obs[t:(t+n)]] = path[max(prevprob)[1]] + obs[t+n-1]
        path = newpath
    n = len(obs) - n
    probs = []
    for y in varstates:
        try:
            probs.append((V[n][y],y))
        except:
            continue
    (prob, state) = max(probs)
    return path[state]      

#генерация вариантов с диакритиками для Витерби
def insert_dia(text,dias,no_dias):
    var = ['']
    for i in text:
        if i in no_dias:
            var = var * 2
            for j in range(len(var)):
                if j+1 > (len(var) / 2):
                    var[j] += dias[no_dias.index(i)]
                else:
                    var[j] += i
        else:
            var = list(map(lambda x: x + i,var))
    return var


def write_file(text,name):
    f = open(name,'w',encoding='utf-8-sig')
    f.write(text)
    f.close()

def write_json(text,name):
    s = json.dumps(text,indent=2,ensure_ascii=False)
    f = open(name,'w',encoding='utf-8-sig')
    f.write(s)
    f.close()


def read_json(name):
    f = open(name,'r',encoding='utf-8-sig')
    s = f.read()
    obj = json.loads(s)
    return obj


def crutch(text,alph):
    text = text.replace('ə','ә')
    text = text.replace('Ə','Ә')
    text = re.sub('(['+alph+alph.upper()+']+)h','\\1һ',text)
    text = re.sub('h(['+alph+alph.upper()+']+)','һ\\1',text)
    text = re.sub('(['+alph+alph.upper()+']+)[vy]','\\1ү',text)
    text = re.sub('[vy](['+alph+alph.upper()+']+)','ү\\1',text)
    text = re.sub('[VY](['+alph+alph.upper()+']+)','Ү\\1',text)    
    return text


#общая функция, чтобы ее вызывать в views.py
def everything(text,lang): 
    alphs = read_file('app\\'+lang+'\\alphs.csv').split(';')
    alph = alphs[0]
    alph_no_dia = alphs[1]
    dia = alphs[2]
    no_dia = alphs[3]
    n = 3
    
    freqlist = read_json('app\\'+lang+'\\freqlist.json')
    bifreqlist = read_json('app\\'+lang+'\\bigram_freqlist.json')
    start_p = read_json('app\\'+lang+'\\start_'+str(n)+'.json')
    trans_p = read_json('app\\'+lang+'\\trans_'+str(n)+'.json')
    
    if lang == 'Коми':
        text = re.sub('([дзлнстДЗЛНСТ])i','\\1і',text)

    text = crutch(text,alph)
    
    observ = re.findall('['+alph+alph.upper()+']+|[^'+alph+alph.upper()+']+',text)
    if lang == 'Вепсский':
        observ = list(map(lambda x: x.replace('\'','’'),observ))
    output = []
    if observ != []:
        if re.search('['+alph+alph.upper()+']',observ[0]) == None:
            j = 1
            output.append(observ[0])
        else:
            j = 0
        for m in range(len(observ)-j):
            i = m+j
            if m%2 == 0 and re.search('[^'+alph+alph.upper()+']',observ[i]) == None:
                mark = False
                gotobi = False
                new_observ,mark,gotobi = select(observ[i],'',freqlist,dia,no_dia)
                bimark = False
                if m > 1 and mark == False and gotobi and output[-1] == ' ':
                    new_observ,bimark,ignore = select(observ[i],output[-2]+' ',bifreqlist,dia,no_dia)
                if mark == False and (gotobi == False or bimark == False):
                    observ[i] = '#'*(n-1)+observ[i]
                    output.append(not_viterbi(start_p,trans_p,observ[i],n,dia,no_dia)[(n-1):])
                else:
                    output.append(new_observ)
            else:
                output.append(observ[i])
    else:
        output = []
    outdias = list(set(dia))
    for i in range(len(outdias)):
        outdias[i] = outdias[i].upper()+outdias[i]
    return ''.join(output),', '.join(outdias)
