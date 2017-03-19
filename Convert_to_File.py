from PIL import Image, ImageDraw, ImageOps
import os
files = []

for file in os.listdir("letters"):
    if file.endswith(".gif"):
        print(file)
        files.append(file)

types = []
for fl in files:
    if fl[7] not in types:
        types.append(fl[7])

types.remove("V")
types.remove("S")
types.sort()
print types
print len(types)

dataSize = len(files)
trainDataSize = int(round(dataSize * 0.80))
testDataSize = dataSize - trainDataSize
print "Train: " + str(trainDataSize) + "Test: " + str(testDataSize)
outputd = open("dataset.data", 'r+')

outputd.seek(0,2)


let = ""
for f in range(0, trainDataSize):
    im = Image.open("letters/" + files[f])

    for x in range(0,im.size[0]):
        for y in range(0, im.size[1]):
            if (im.getpixel((x,y)) == 0):
                outputd.write("1 ")
            else:
                outputd.write("-1 ")
    outputd.write("\n\n")
    if files[f][7] == "V":
        let = "v"
    elif files[f][7] == "S":
        let = "s"
    else:
        let = files[f][7]
    outputlist = [-1] * 48
    for l in range(0,len(types)):
        if types[l] == let:
            outputlist[l] = 1

    for output in outputlist:
        outputd.write(str(output) + " ")
    outputd.write("\n\n")
outputd.seek(0,0)
outputd.write(str(trainDataSize - 1) + " 900 48\n\n")
outputd.close()









outputd = open("testdata.data", 'r+')

outputd.seek(0,2)


let = ""
for f in range(trainDataSize, len(files)):
    im = Image.open("letters/" + files[f])

    for x in range(0,im.size[0]):
        for y in range(0, im.size[1]):
            if (im.getpixel((x,y)) == 0):
                outputd.write("1 ")
            else:
                outputd.write("-1 ")
    outputd.write("\n\n")
    if files[f][7] == "V":
        let = "v"
    elif files[f][7] == "S":
        let = "s"
    else:
        let = files[f][7]
    outputlist = [-1] * 48
    for l in range(0,len(types)):
        if types[l] == let:
            outputlist[l] = 1

    for output in outputlist:
        outputd.write(str(output) + " ")
    outputd.write("\n\n")
outputd.seek(0,0)
outputd.write(str(testDataSize - 1) + " 900 48\n\n")
outputd.close()