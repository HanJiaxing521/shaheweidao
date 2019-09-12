import copy
import random
import numpy as np


def distEclud(vecA, vecB):
    vecA = np.array(vecA)
    vecB = np.array(vecB)
    return np.sqrt(np.sum(np.power(vecA - vecB, 2)))


def randCent(dataSet, k):
    n = np.shape(dataSet)[1]
    centroids = np.zeros((k, n))
    for j in range(n):
        minj = []
        for s in dataSet:
            minj.append(s[j])
        minJ = min(minj)
        rangeJ = float(max(minj)-minJ)
        for m in range(k):
            centroids[m][j] = minJ + rangeJ * random.random()

    return centroids


def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = np.shape(dataSet)[0]
    clusterAssment = np.zeros((m, 2)).tolist()
    centroids = createCent(dataSet, k)

    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = np.inf
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j], dataSet[i])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i][0] != minIndex:
                clusterChanged = True
            clusterAssment[i] = [minIndex, minDist**2]
        for cent in range(k):
            ptsInClust = []
            for i in range(len(clusterAssment)):
                if clusterAssment[i][0] == cent:
                    ptsInClust.append(dataSet[i])
            centroids[cent] = np.mean(ptsInClust, axis=0)
    return centroids, clusterAssment


def biKmeans(dataSet, k, distMeas=distEclud):
    m = np.shape(dataSet)[0]
    clusterAssment = np.zeros((m, 2)).tolist()
    centroid0 = np.mean(dataSet, axis=0).tolist()
    centList = [centroid0]

    for j in range(m):
        clusterAssment[j][1] = distMeas(centroid0, dataSet[j])**2

    while len(centList) < k:
        print(len(centList))
        lowestSSE = np.inf
        for i in range(len(centList)):
            ptsInCurrCluster = []
            for j in range(len(clusterAssment)):
                if clusterAssment[j][0] == i:
                    ptsInCurrCluster.append(dataSet[j])

            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            sseSplit = np.sum(splitClustAss, axis=0)[1]
            sseNotSplit = 0
            for j in range(len(clusterAssment)):
                if clusterAssment[j][0] != i:
                    sseNotSplit += clusterAssment[j][1]
            print("sseSplit, and notSplit: ", sseSplit, sseNotSplit)
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = copy.deepcopy(splitClustAss)
                lowestSSE = sseSplit + sseNotSplit
        for clust in bestClustAss:
            if clust[0] == 1:
                clust[0] = len(centList)
            else:
                clust[0] = bestCentToSplit

        print("the bestCentToSplit is: ", bestCentToSplit)
        print("the len of bestClustAss is: ", len(bestClustAss))
        centList[bestCentToSplit] = bestNewCents[0, :]
        centList.append(bestNewCents[1, :])
        x = 0
        for ass in range(len(clusterAssment)):
            if clusterAssment[ass][0] == bestCentToSplit:
                clusterAssment[ass] = bestClustAss[x]
                x += 1
    return np.mat(centList), clusterAssment
