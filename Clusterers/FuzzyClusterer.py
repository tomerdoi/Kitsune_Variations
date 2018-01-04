#import theano

from numpy import *


#implements Incremental dendogram
#data: 2d array dataset recordsXfeatures

def clusterUsingIncrementalFuzzyDendogram(data, maxSizeOfCluster=10, maxFuz=3):


    data=np.transpose(data)
    clusters=[]
    centroids=[]
    featuresIndexes=[]
    for j,featureRow in enumerate(data):
        featuresIndexes.append([j])
        clusters.append([featureRow])
        centroids.append(np.average(featureRow))

    actualSizeOfCluster=max([len(clusters[i]) for i in range(len(clusters))])

    while (actualSizeOfCluster<maxSizeOfCluster):
        minDist=np.inf
        distAr=[]
        indexesAr=[]
        for c1 in range(len(centroids)):
            for c2 in range(len(centroids)):
                if c1!=c2:

                    c1c2Diff=np.abs(centroids[c1]-centroids[c2])



                    if c1c2Diff<minDist:


                        minDist=c1c2Diff
                        minC1=c1
                        minC2=c2

        for c2 in range(len(centroids)):
            if c2!=minC1:
                c1c2Diff = np.abs(centroids[minC1] - centroids[c2])
                distAr.append(c1c2Diff)
                indexesAr.append(c2)


        indexesAr = [x for _, x in sorted(zip(distAr, indexesAr))]

        for idx in range(maxFuz):

            if idx<maxFuz-1:
                mergeClusters(clusters,featuresIndexes,centroids,minC1,indexesAr[idx],False)
            else:
                mergeClusters(clusters,featuresIndexes, centroids, minC1, indexesAr[idx], True)


        actualSizeOfCluster = max([len(clusters[i]) for i in range(len(clusters))])
    print('finished clustering...')


def mergeClusters(clusters,featuresIndexes,centroids,c1,c2, isLast=False):
    clusters[c1].extend(clusters[c2])
    featuresIndexes[c1].extend(featuresIndexes[c2])
    centroids[c1]=np.average(clusters[c1])

    if isLast==True:
        del clusters[c2]
        del centroids[c2]
        del featuresIndexes[c2]
