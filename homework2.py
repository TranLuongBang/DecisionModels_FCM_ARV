# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

def readData(filename):
    data = np.genfromtxt(filename, delimiter=',')
    return data

def getPreferenceMatrix(experts):
    preList = []
    n = len(experts)
    
    for i in range(n):
        filename = input("Input file name of preference matrix of expert "+ str(i+1) + ": ")
        matrix = readData(filename)
        print("Preference matrix of expert " + str(i+1) + ":")
        print(matrix)
        preList.append(matrix)
            
    return preList
        

def calSimilarityMatrix(preList):
    simList = []
    n = len(preList)
    for i in range(0,n-1):
        for j in range(i+1,n):
            sm = 1 - abs(preList[i]-preList[j])
            simList.append(sm)
            print('The similarity matrix between expert '+ str(i+1) +' and expert ' + str(j+1))
            print(sm)
    
    return simList
        
def calConsensusMatrix(simList):
    n = len(simList)
    cm = np.sum(simList, axis=0)/n
    print('The Consensus Matrix:')
    print(np.round_(cm,3))
    return cm

def calConsensusAlternatives(cm):
    caList = []
    n = len(cm)
    print('Consensus Degree on Alternative:')
    for i in range(n):
        ca = (np.sum(cm[i,:]) + np.sum(cm[:,i])-2)/(2*(n-1))
        caList.append(ca)
        print('ca'+ str(i+1) + '=', np.round_(ca,3))
    return caList

def calConsensusMeasure(caList):
    n = len(caList)
    cr = np.sum(caList)/n
    print('The Final Consensus Mesuare: cr = ', np.round_(cr,3))
    return float(cr)

def calCollectivePreferenceM(preList):
    n = len(preList)
    pc = np.sum(preList, axis = 0)/n
    
    print('Collective Preference Matrix: pc =')
    print(pc)
    return pc

def calCollectiveSimilarityMatrix(preList,pc):
    pp = lambda preList, pc: 1 - abs(preList - pc)
    return np.array(pp(preList,pc))

def calCollectiveSimilarityMeasure(pp):
    paList = []
    n = len(pp)
    print('Collective Similarity Measure:')
    for i in range(n):
        ppi = pp[i]
        paei = []
        for j in range(len(ppi)):
            pa = (np.sum(ppi[j,:]) + np.sum(ppi[:,j])-2)/(2*(len(ppi)-1))
            paei.append(pa)
        print('pa'+str(i+1)+'=', np.round_(paei,3))
        paList.append(paei)
    return paList

def calAggregatedColSimMeasure(paList):
    prList = []
    print('Aggregated Collective Similarity Measure:')
    for i in range(len(paList)):
        pa = paList[i]
        pr = np.sum(pa)/len(pa)
        prList.append(pr)
        print('pr'+ str(i+1) + '=', np.round_(prList[i],3))
    return np.array(prList)

def classifyExperts(ex, ld1, ld2):
    low = ex[:,1] < ld1
    high = ex[:,1] >= ld2
    med = np.logical_and(ex[:,1] < ld2, ex[:,1] >= ld1)
    
    groups = {}
    
    if np.any(high):
        groups['high'] = np.where(high)[0]
        print('High important experts:', ex[high])
    else: 
        groups['high'] = []
        print('There is no high important expert')
    
    if np.any(med):
        groups['med'] = np.where(med)[0]
        print('Medium important experts:', ex[med])
    else:
        groups['med'] = []
        print('There is no medium important expert')
    
    if np.any(low):
        groups['low'] = np.where(low)[0]
        print('Low important experts:', ex[low])
    else: 
        groups['low'] = []
        print('There is no low important expert')
    
    return groups
    
def calAlpha1Threshold(cm):
    n = len(cm)
    alpha1 = (np.sum(cm) - n)/(n*n-n)
    return alpha1

def calAlpha2Threshold(caList):
    n = len(caList)
    alpha2 = np.sum(caList)/n
    return alpha2

def calBeta1Threshold(paList):
    beta1 = np.sum(paList, axis = 0)/len(paList)
    return beta1

def calBeta2Threshold(pp, P):
    n = len(pp)
    beta2 = []
    
    for i in P:
        sum = 0
        for csmatrix in pp:
            sum = sum + csmatrix[i[0],i[1]]
        b2 = sum/n
        beta2.append(b2)
    return np.array(beta2)

def adviceToChange(preMa, PCH, pc):
    n = len(preMa)
    newPre = [ ["="] * n for i in range(n) ]
    for index in PCH:
        a = index[0]
        b = index[1]
        if(preMa[a,b] < pc[a,b]):
            newPre[a][b] = "+"
            newPre[b][a] = "-"
        if(preMa[a,b] > pc[a,b]):
            newPre[a][b] = "-"
            newPre[b][a] = "+"
    return newPre
    
def calS(i,arr):
    s = 0
    for j in range(len(arr)):
        s = s + arr[j][i]
    return s

def ARV(preList):
    print('------Average Rating Value-----')
    n = np.shape(preList)[0]
    m = np.shape(preList)[1]
    arr = []
    for pre in preList:
        r = np.sum(pre, axis = 1)/m
        arr.append(r)
    arr = np.array(arr)
    print('arr:', arr)
    out_arr = np.argsort(arr)
    ##print ("Output sorted array indices : ", out_arr) 
    
    sorted_arr1 = - np.sort(-arr, axis =1)
    print ("Sorted arr  : ", sorted_arr1) 
    
    sorted_arr = np.sort(arr, axis = 1)
    v1 = []
    for r in sorted_arr:
        s = [1]
        for i in range(1,len(r)):
            if r[i] == r[i-1]:
                s.append(s[i-1])
            else: s.append(s[i-1]+1)
        v1.append(s)

    a = [ [-1] * m for i in range(n) ]
    for i in range(n):
        for j in range(m):
            b = out_arr[i][j]
            a[i][b] = v1[i][j]
            
    print('vij', np.array(a))
    
    v2 = np.sum(a, axis = 0)
    print('Score V for each alternative: ', v2)
    
    ranking = np.argsort(-v2)
    print('Final Ranking is: ',ranking+1)

    k = 0
    ind1 = 0
    for i in range(m-1):
            if(v2[ranking[i]]==v2[ranking[i+1]]):
                ind1 = i
                s1 = calS(ranking[i],arr)
                s2 = calS(ranking[i+1],arr)
                if np.round_(s1,2) < np.round_(s2,2):
                    k = 1
    if k==1:
        r = ranking[ind1]
        ranking[ind1] = ranking[ind1+1]
        ranking[ind1+1] = r
        print('Definitive Ranking is: ',ranking+1)

def main():
    
    experts = pd.read_csv(input('Input expert file: '))
    print(experts)
    
    alternative = pd.read_csv(input('Input alternative file: '))
    print(alternative)
    
    preList = getPreferenceMatrix(experts)
    
    print('-----Input FCM Parameter-----')
    cl = float(input('Input Consensus Level: '))
    rounds = int(input('Input number of rounds: '))
    ld1 = float(input('Input lambdas 1: '))
    ld2 = float(input('Input lambdas 2: '))
    
    
    while(rounds>0): 
        
        simList = calSimilarityMatrix(preList)
        cm = calConsensusMatrix(simList)
        caList = calConsensusAlternatives(cm)
        cr = calConsensusMeasure(caList)
        print('cl = ', cl)
        if cr > cl:
            print('The consensus is achieved')
            ARV(preList)
        else: 
            print('The consensus is not achieved')
            print('Feedback machenism activated')
            groups = classifyExperts(experts.values,ld1, ld2)
            
            pc = calCollectivePreferenceM(preList)
            
            pp = calCollectiveSimilarityMatrix(preList, pc)
            
            paList = calCollectiveSimilarityMeasure(pp)
            
            calAggregatedColSimMeasure(paList)
            
        
            print('--------Low Group------')
            
            alpha1 = calAlpha1Threshold(cm)
            print("alpha 1: ", alpha1)
            
            Plow =  np.argwhere(cm < alpha1)
            print('Plow = ', Plow+1)
            
            PCHlow = Plow
            print('PCH low = ', PCHlow+1)
            
            low = groups.get('low')
            if len(low) == 0:
                print('There is no expert in low group')
            else:
                print('Low Group contains experts ', low+1)
                for i in low:
                    print('Advice to change preference matric of expert ' + str(i+1))
                    preMa = preList[i]
                    newPre = adviceToChange(preMa,PCHlow,pc)
                    print(np.array(newPre))
                    
            print('--------Medium Group------')
            
            alpha2 = calAlpha2Threshold(caList)
            print("alpha 2: ", alpha2)
            
            XCH = np.where(np.array(caList) < alpha2)[0]
            print('XCH = ', XCH+1)
            Pmed = []
            index = []
            for i in Plow:
                for j in XCH:
                    if i[0] == j:
                        Pmed.append(i)
                        if j not in index:
                            index.append(j)
            ## print('Index', index)
            print('Pmed = ', np.array(Pmed)+1)
            beta1 = calBeta1Threshold(paList)
            print('beta1 = ', beta1)
            
            med = groups.get('med')
            if len(med) == 0:
                print('There is no expert in medium group')
            else:
                print('Medium Group contains experts ', med+1)
                for i in med:
                    print('Advice to change preference matric of expert ' + str(i+1))
                    PCHmed = []
                    for j in index:
                        pa = paList[i]
                        ##print(pa[j])
                        ##print(beta1[i])
                        if pa[j] < beta1[i]:
                            for n in Pmed:
                                if n[0] == j:
                                    PCHmed.append(n)
                    PCHmed = np.array(PCHmed)
                    print("PCHmed = ", PCHmed+1)
                    preMa = preList[i]
                    newPre = adviceToChange(preMa,PCHmed,pc)
                    print(np.array(newPre))
                        
            print('--------High Group------')
            XCH = np.where(np.array(caList) < alpha2)[0]
            print('XCH = ', XCH+1)
            Phigh = Pmed
            print('Phigh = ', np.array(Phigh)+1)
            
            beta2 = calBeta2Threshold(pp, Phigh)
            print('beta2:', beta2)
            
            high = groups.get('high')
            if len(high) == 0:
                print('There is no expert in high group')
            else:
                print('High Group contains expert ', high+1)
                for i in high:
                    print('Advice to change preference matric of expert ' + str(i+1))
                    count = 0
                    PCHhigh = []
                    for index in Phigh:
                        p = pp[i]
                        ##print('ppij:',p[index[0], index[1]])
                        ##print(beta2[count])
                        if p[index[0], index[1]] < beta2[count]:
                            PCHhigh.append(index)
                        count = count+1
                    PCHhigh = np.array(PCHhigh)
                    print("PCH high:", PCHhigh+1)
                    preMa = preList[i]
                    newPre = adviceToChange(preMa,PCHhigh,pc)
                    print(np.array(newPre))
        rounds = rounds -1
        break

main()
            