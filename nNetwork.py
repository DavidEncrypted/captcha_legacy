#from Captcha_2_0 import *

#def getLetter():


#def getTable():



import pybrain
from pybrain.datasets import *
from PIL import Image, ImageDraw, ImageOps

from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
import pickle

import os
files = []
allInputs = []
allOutputs = []
for file in os.listdir("letters"):
    if file.endswith(".gif"):
        #print(file)
        files.append(file)

im = Image.open("letters/" + files[0])
print "Input Data Size: " + str(len(files))


inputSize = im.size[0] * im.size[1]
print im.size[0], im.size[1], inputSize
outputSize = 1

ds = SupervisedDataSet(inputSize, 1)
turn = 0
for f in files:

    im = Image.open("letters/" + f)
    preDS = []
    for x in range(0,im.size[0]):
        for y in range(0, im.size[1]):
            if (im.getpixel((x,y)) == 0):
                preDS.append(1)
            else:
                preDS.append(0)

    #print len(preDS)
    preTarget = 0

    if (f[7] == "A"):
        preTarget = 1
        allOutputs.append(1)
    else:
        allOutputs.append(0)
    ds.addSample(preDS, (preTarget,))
    allInputs.append(preDS)
#print allInputs
net = buildNetwork(inputSize, 80, 20, outputSize, bias=True)
print "Net Built"
trainer = BackpropTrainer(net, ds, learningrate=0.01, momentum=0.99)
trainer.trainUntilConvergence( verbose = True, validationProportion = 0.15, maxEpochs = 1000, continueEpochs = 10 )
trainer.testOnData()

for i in range(0,len(allInputs)):
    print net.activate(allInputs[i]), "Should be: " + str(allOutputs[i])