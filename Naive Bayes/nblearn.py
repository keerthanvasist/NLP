import math
import sys

args = sys.argv

trainFile = open(args[1])
labelFile = open(args[2])


review = trainFile.readline()
map = {}
while review != "":
    review = review.strip("\n")
    words = review.split(" ")
    map[words[0]] = [review]
    review = trainFile.readline()

labels = labelFile.readline()


while labels != "":
    words = labels.split(" ")
    if map.get(words[0]) != None:
        word = map.get(words[0])
        word.append([words[1],words[2]])
        map[words[0]] = word
    labels = labelFile.readline()


totals = [0,0,0,0]

replaceCount = 0

stopwords = set()
stopList = ['a','about','above','be','because','again','been','before','being','after','against','all','am','an','and','any','are','arent','as','at','below','between','both','but','by','cant','cannot','could','couldnt','did','didnt','do','does','doesnt','doing','dont','down','during','each','few','for','from','further','had','hadnt','has','hasnt','have','havent','having','he','hed','hell','hes','her','here','heres','hers','herself','him','himself','his','how','hows','i','id','ill','im','ive','if','in','into','is','isnt','it','its','its','itself','lets','me','more','most','mustnt','my','myself','no','nor','not','of','off','on','once','only','or','other','ought','our','ours','ourselves','out','over','own','same','shant','she','shed','shell','shes','should','shouldnt','so','some','such','than','that','thats','the','their','theirs','them','they','theyd','theyll','theyre','theyve','this','until','up','very','was','themselves','then','there','theres','these','wasnt','we','wed','well','were','weve','those','through','to','too','under','were','who','whos','whom','why','whys','with','wont','would','wouldnt','you','youd','youll','werent','what','whats','when','whens','where','wheres','which','while','youre','youve','your','yours','yourself','yourselves']
#stopList = []
for words in stopList:
    stopwords.add(words)

wordMap = {}
totalLines = 0
totalWords = 0
for key in map:
    value = map.get(key)
    labels = value[1]
    review = value[0]
    totalLines+=1
    count = [False,False,False,False]

    if (labels[0].strip() == "deceptive"):
        count[3] = True
    else:
        count[2] = True
    if (labels[1].strip() == "positive"):
        count[0] = True
    else:
        count[1] = True

    review = review.split(" ")
    for i in range(1,len(review)):
        if review[i] not in stopList:
            totalWords += 1
            if count[0]:
                totals[0] += 1
            if count[1]:
                totals[1] += 1
            if count[2]:
                totals[2] += 1
            if count[3]:
                totals[3] += 1
            if (wordMap.get(review[i]) == None):
                wordCount = [1,1,1,1]
                if count[0]:
                    wordCount[0] += 1
                if count[1]:
                    wordCount[1] += 1
                if count[2]:
                    wordCount[2] += 1
                if count[3]:
                    wordCount[3] += 1
                wordMap[review[i]] = wordCount
            else:
                wordCount = wordMap.get(review[i])
                if count[0]:
                    wordCount[0] += 1
                if count[1]:
                    wordCount[1] += 1
                if count[2]:
                    wordCount[2] += 1
                if count[3]:
                    wordCount[3] += 1
                wordMap[review[i]] = wordCount



total = totals[0]+totals[1]+totals[2]+totals[3]

outFile = open("nbmodel.txt",'w')

outFile.truncate()

outFile.write(str(totals[0]/total) + " ")
outFile.write(str(totals[1]/total) + " ")
outFile.write(str(totals[2]/total) + " ")
outFile.write(str(totals[3]/total)+"\n")


for word in wordMap:
    features = wordMap.get(word)
    outFile.write(word+" ")
    feats = [0,0,0,0]
    for i in range(len(features)):
        try:
            feats[i] = math.log(features[i]) - math.log(totals[i])
            outFile.write(str(feats[i])+" ")
        except Exception as e:
            exit(-1)

    wordMap[word] = feats
    outFile.write("\n")


#outFile.wr

outFile.close()
labelFile.close()
trainFile.close()
