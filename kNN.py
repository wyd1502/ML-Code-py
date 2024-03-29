from numpy import *
import operator 
import os

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberofLines = len(arrayOLines)
    returnMat = zeros((numberofLines,3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine [0:3]
        if listFromLine[-1]=='didntLike':
             classLabelVector.append(1)
        elif listFromLine[-1]=='smallDoses':
             classLabelVector.append(2)
        else :
             classLabelVector.append(3)
        index += 1
    return returnMat,classLabelVector

def classify0(inX,dataSet,labels,k) :
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k) :
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def autoNorm(dataSet) :
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals,(m,1))
    normDataSet= normDataSet/tile(ranges, (m,1))
    return normDataSet, ranges, minVals

def datingClassTest():
    hoRatio = 0.10
    datingDataMat,datingLabels = file2matrix("datingTestSet.txt")
    normMat,ranges,MinVals=autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs= int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],7);
        print("the classifier came back with : %d, the real answer is : %d" % (classifierResult, datingLabels[i]))
        if (classifierResult != datingLabels[i]): errorCount +=1;print("wrong!")
    print("the total error rate is: %f" %(errorCount/float(numTestVecs)))
    
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr= fr.readline()
        for j in range(32):
            returnVect[0][32*i+j] = int(lineStr[j])
    return returnVect

def handwritingClassTest():
    hwLabels = []
    trainingFileList = os.listdir('trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros((m,1024));
    errorCount = 0
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int (fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = os.listdir('testDigits')
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest,trainingMat,hwLabels,3)
        print("the classifier came back with: %d, the real answer is %d" %(classifierResult, classNumStr))
        if (classifierResult != classNumStr): errorCount+=1.0
    print("\n the total number of errors is: %d" % errorCount)
    print("\n the total error rate is: %f" %(errorCount/float(mTest)))
        
        