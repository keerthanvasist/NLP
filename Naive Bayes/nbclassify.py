import sys

testFile = open(sys.argv[1])

modelFile = open("nbmodel.txt",'r')
outputFile = open("nboutput.txt",'w')

probs = modelFile.readline()
probs = probs.split(" ")
pPos = float(probs[0])
pNeg = float(probs[1])
pTruth = float(probs[2])
pDec = float(probs[3])

map = {}

probs = modelFile.readline()
while(probs != ""):
    floatProbs =  probs.split()
    if len(floatProbs) > 0:
        word = floatProbs[0]
        for i in range(1,len(floatProbs)):
            if (i != 0):
                floatProbs[i-1] = float(floatProbs[i])
        floatProbs.remove(floatProbs[i])
        map[word] = floatProbs

    probs = modelFile.readline()
    outputString = ""

testReview = testFile.readline()

while (testReview != ""):
    finalProbs = []
    words = testReview.split(" ")
    sums = [0,0,0,0,""]
    for i in range(len(words)):
        if i == 0:
            sums[4] = words[i]
        else :
            if (map.get(words[i]) != None):
                probs = map.get(words[i])
                sums[0] = sums[0] + float(probs[0])
                sums[1] = sums[1] + float(probs[1])
                sums[2] = sums[2] + float(probs[2])
                sums[3] = sums[3] + float(probs[3])
    finalProbs.append(sums)
    #outputFile.write(words[0]+" ")
    outputString = outputString + words[0]+" "
    truthful = False
    positive = False
    if (sums[2] > sums[3]):
        truthful = True
    if sums[0] > sums[1]:
        positive = True

    if (truthful and positive):
        outputString = outputString +"truthful positive"
        #outputFile.write("truthful positive")
    elif (truthful):
        outputString = outputString +"truthful negative"
        #outputFile.write("truthful negative")
    elif (positive):
        outputString = outputString +"deceptive positive"
        #outputFile.write("deceptive positive")
    else:
        outputString = outputString+"deceptive negative"
        #outputFile.write("deceptive negative")
    outputString = outputString +"\n"
    testReview = testFile.readline()


outputString = outputString.rstrip("\n")
outputFile.write(outputString)
outputFile.close()

modelFile.close()