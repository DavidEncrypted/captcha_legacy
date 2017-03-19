def getCImage():
    html = urlopen("https://www.phpcaptcha.org/try-securimage/").read()
    soup = BeautifulSoup(html, "html.parser")
    images = [img for img in soup.findAll('img')]
    #print (str(len(images)) + " images found.")

    img = soup.select("#captcha_one")
    flink = img[0]["src"]

    ilink = "https://www.phpcaptcha.org"
    link = ilink + flink + ".jpg"
    #print (link)

    urllib.urlretrieve(link, "File1.jpg")




def Grouping(im2, grpsize):
    groups = []

    for x in range(im2.size[0]):
        for y in range(im2.size[1]):
            neigh = []
            temp = im2.getpixel((x, y))[0]
            if temp != 255:
                neigh.append((x, y))
                b = 0
                done = 0
                while len(neigh) < grpsize and done == 0:

                    for (s, t) in (
                            (neigh[b][0] + 1, neigh[b][1]), (neigh[b][0] - 1, neigh[b][1]),
                            (neigh[b][0], neigh[b][1] + 1),
                            (neigh[b][0], neigh[b][1] - 1)):
                        if (s > 0 and s < (im2.size[0] - 1) and t > 0 and t < (im2.size[1] - 1)) and \
                                        im2.getpixel((s, t))[0] == temp:
                            if (s, t) not in neigh:
                                neigh.append((s, t))

                    b = b + 1
                    if b >= len(neigh):
                        groups.append(neigh)
                        done = 1
    print "Groups found"

    return groups

def touchWhi(im2, groups):
    for group in groups:
        totWhi = 0
        for (x,y) in group:
            for (s,t) in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if (s > 0 and s < (im2.size[0]) and t > 0 and t < (im2.size[1])):
                    if (im2.getpixel((s,t))[0] == 255):
                        totWhi += 1
        if (totWhi > 1):
            for (x,y) in group:
                im2.putpixel((x,y),(255,255))
        else:
            for (x,y) in group:
                im2.putpixel((x,y),(140,255))
    return im2

def pixGroupRemove(im2,group):        #remove pixelgroups smaller than 'group'
    for x in range(im2.size[0]):
        for y in range(im2.size[1]):
            neigh = []
            temp = im2.getpixel((x, y))[0]
            if temp != 255:
                neigh.append((x, y))
                b = 0
                done = 0
                while len(neigh) < group and done == 0:

                    for (s, t) in (
                    (neigh[b][0] + 1, neigh[b][1]), (neigh[b][0] - 1, neigh[b][1]), (neigh[b][0], neigh[b][1] + 1),
                    (neigh[b][0], neigh[b][1] - 1)):
                        if (s >= 0 and s < (im2.size[0]) and t >= 0 and t < (im2.size[1] - 1)) and \
                                        im2.getpixel((s, t))[
                                            0] == temp:
                            if (s, t) not in neigh:
                                neigh.append((s, t))

                    b = b + 1
                    if b >= len(neigh):
                        im2.putpixel((x, y), (255, 255))
                        done = 1
    print "Groups removed"
    return im2

def colPs(ims, col):
    arrP = []
    for x in range(0,ims.size[0]):
        for y in range(0,ims.size[1]):
            if (ims.getpixel((x,y))[0] == col):
                arrP.append((x,y))
    return arrP



def lineRemove(ims, letP):
    #letP = []
    lineP = []

    for (s,t) in letP:
        whi = 0
        lin = 0
        for (v,w) in ((s+1, t),(s-1,t),(s,t+1),(s,t-1),(s-1,t-1),(s+1,t-1),(s-1,t+1),(s+1,t+1)):
            if (v > 0 and v < (ims.size[0] - 1) and (w > 0) and w < (ims.size[1] - 1)):
                if (ims.getpixel((v,w))[0] == 255):
                    whi += 1
                    #print(whi)
                elif (ims.getpixel((v,w))[0] == 112):
                    lin += 1
        if (whi > 0 and lin > 0):
            lineP.append((s,t))
    return lineP


def randLinePts(ims, amount, linP):


    step = round(len(linP) / amount)
    print (step)
    rPoints = []
    for i in range(0,amount):
        rPoints.append(linP[int(step * i)])
    print("amount wanted:", amount, "amount got:",len(rPoints))
    return rPoints

def growLet(ims, edgePS, corners, dis):
    for (rx,ry) in edgePS:
        lineCoords = []
        runt = 0
        if (ims.getpixel((rx, ry))[0] == 112):
            #print("point")
            lineCoords.append((rx,ry))
            while (len(lineCoords) > 0 and runt < 15):
                runt += 1
                (x,y) = lineCoords[0]
                for (s, t) in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if (s >= 0 and s < (ims.size[0]) and t >= 0 and t < (ims.size[1] - 1)):
                        if (ims.getpixel((s,t))[0] == 112):
                            dx = abs(s - rx)
                            dy = abs(t - ry)
                            dc = (dx*dx) + (dy*dy)
                            #print(dc)

                            if (dc < dis):
                                if (s,t) not in lineCoords:
                                    lineCoords.append((s,t))
                                #print("yip")
                ims.putpixel((x, y), (140, 255))
                lineCoords.pop(0)
                #print(len(lineCoords))
            #print("thats one")
    return ims


def getllps(ims, linP, corners):
    foundP = []

    for (s, t) in linP:
        whi = 0
        let = 0
        for (v, w) in ((s + 1, t), (s - 1, t), (s, t + 1), (s, t - 1), (s - 1, t - 1), (s + 1, t - 1), (s - 1, t + 1), (s + 1, t + 1)):

            if (v > 0 and v < (ims.size[0] - 1) and (w > 0) and w < (ims.size[1] - 1)):
                if (ims.getpixel((v, w))[0] == 255):
                    whi += 1
                    # print(whi)
                elif (ims.getpixel((v, w))[0] == 140):
                    let += 1
        if (whi <= 0 and let > 1):

            bdc = 10000
            for (xc, yc) in corners:
                dx = abs(s - xc)
                dy = abs(t - yc)
                dc = (dx * dx) + (dy * dy)
                # print(dc)
                if (dc < bdc): bdc = dc
            if (bdc > 3):
                foundP.append((s, t))
    return foundP

def ColorWhitelist(ims, color):    #Pixel seclection by colour
    BORDER_COLOR = 255
    color = list(color)
    temp = {}
    im2 = Image.new("LA",im.size,255)
    for x in range(ims.size[0]):
      for y in range(ims.size[1]):
        pix = ims.getpixel((x,y))

        temp[pix] = pix
        for i in range(0,len(color)):
            if pix[0] == color[i][0]: # these are the numbers to get
              im2.putpixel((x,y),(color[i][1],255))
    print "ColorWhitelisted"
    return im2


def clustify(im2):
    clusterss = []
    def floodfill(x, y):
        # "hidden" stop clause - not reinvoking for "c" or "b", only for "a".
        if im2.getpixel((x, y))[0] == 0:
            clustr.append((x, y))
            im2.putpixel((x, y), (100, 255))
            # recursively invoke flood fill on all surrounding cells:
            if x > 0:
                floodfill(x - 1, y)
            if x < im2.size[0] - 1:
                floodfill(x + 1, y)
            if y > 0:
                floodfill(x, y - 1)
            if y < im2.size[1] - 1:
                floodfill(x, y + 1)

    #Put all black pixels in a list
    black = []
    for x in range(0,215):
        for y in range(0,80):
            if (im2.getpixel((x,y))[0] != 255):
                black.append((x,y))
    print "Blackt"


    #Floodfill pixels to get pixel collections
    while len(black) > 0:
        for clusts in clusterss:
            black = set(black) - set(clusts)
        if len(black) > 0:
            clustr = []
            floodfill(list(black)[0][0], list(black)[0][1])
            if (len(clustr) != 0):
                clusterss.append(clustr)

    #clusters.append(clustr)
    print "Pixels collected"

    #Sort groups small to big
    clusterss.sort(key=len)
    return clusterss

def reduceTo(amount, clusters):
    # Add smallest to groups to the closest groups untill 'amount' groups left
    while (len(clusters) > amount):
        mx = []
        my = []
        for (s, t) in clusters[0]:
            mx.append(s)
            my.append(t)
        medx = numpy.median(numpy.array(mx))
        medy = numpy.median(numpy.array(my))

        cdist = (1000, 0)
        for n in range(1, len(clusters)):
            for coords in clusters[n]:
                x1 = medx
                y1 = medy
                x2 = coords[0]
                y2 = coords[1]
                tempdist = ((x1 - x2) ** 2) + (((y1 - y2) ** 2) / 2)
                if tempdist < cdist[0]:
                    cdist = (tempdist, n)
        clusters[cdist[1]] = clusters[0] + clusters[cdist[1]]
        clusters.pop(0)
        clusters.sort(key=len)
    print "Reduced to: ", amount
    return clusters


from graphics import *
from urllib2 import urlopen
from bs4 import BeautifulSoup
import urllib
import numpy
import math
from PIL import Image, ImageDraw


CaptchaN = 0
cSegmY = 0
cSegmX = 0
width = 1200
height = 800
#win = GraphWin(width=width, height=height)  # create a window
#win.setCoords(0, 0, width, height)  # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)
win2 = GraphWin(width=width, height=height)
win2.setCoords(0, 0, width, height)
#Segment and display 10 captcha's
for USELESS in range(0,100):
    #Getting the Captcha from the Onlines
    getCImage()
    im = Image.open("File1.jpg").convert("LA")      #Opening Captcha and converting to Greyscale
    grps = Grouping(im,15)
    cimage = touchWhi(im,grps)
    cimage = ColorWhitelist(cimage, ((140,140),(112,112)))
    cimage = pixGroupRemove(cimage, 10)
    letarrP = colPs(cimage, 140)
    linarrP = colPs(cimage, 112)


    trips = lineRemove(cimage, letarrP)
    #randlPS = randLinePts(cimage, 200, linarrP)
    #cimage = growDis(cimage, randlPS, trips, 5)
    letLinePS = getllps(cimage, linarrP, trips)
    cimage = growLet(cimage, letLinePS, trips, 5)
    #cimage.show()
    print("trips LENGTH:", len(trips))
    temptest = []
    temptest.append((140,0))
    cimage = ColorWhitelist(cimage, ((140, 0), (112, 255)))
    cimage = pixGroupRemove(cimage, 10)
    clustersx = clustify(cimage)
    sixclust = reduceTo(6, clustersx)


    for (xt,yt) in letLinePS:
        for (ut,it) in ((xt+1,yt),(xt-1,yt),(xt,yt+1),(xt,yt-1)):
            cimage.putpixel((xt,yt), (0,255))
            cimage.putpixel((ut,it), (0, 255))


    im.save("temp_ori.gif")
    cimage.save("temp1.gif")

    segments = []
    for i in range(0, len(sixclust)):
        xmin = 300
        xmax = 0
        ymin = 300
        ymax = 0
        xcent = 0
        xtot = 0
        for (xcl,ycl) in sixclust[i]:
            if xcl < xmin:
                xmin = xcl
            if xcl > xmax:
                xmax = xcl
            if ycl < ymin:
                ymin = ycl
            if ycl > ymax:
                ymax = ycl
            xtot += xcl
        xcent = xtot / len(sixclust[i])
        print xcent
        xlen = xmax - xmin + 2
        ylen = ymax - ymin + 2
        image = Image.new("LA",(xlen,ylen),255)
        for (xsc, ysc) in sixclust[i]:
            image.putpixel((xsc - xmin + 1, ysc - ymin + 1), (0,255))
        segments.append((image, xcent))
        segments.sort(key=lambda tup: tup[1])



    #captcha_or = Img(Point(im.size[0] / 2, height - ((im.size[1] / 2) + (im.size[1] * CaptchaN))),"temp_ori.gif")
    #captcha_or.draw(win)
    #captcha = Img(Point(im.size[0] / 2 + im.size[0],height - ((im.size[1] / 2) + (im.size[1] * CaptchaN))), "temp1.gif")
    #captcha.draw(win)

    widx = im.size[0] * 2
    for tups in segments:
        image = tups[0]

        image.save("temp2.gif")
        #tempSeg = Img(Point(widx + image.size[0] / 2, height - ((image.size[1] / 2) + (im.size[1] * CaptchaN))), "temp2.gif")
        widx += image.size[0] + 10
        #tempSeg.draw(win)
        tempSeg2 = Img(Point(image.size[0] / 2 + (cSegmX),height - (50) - (50 * cSegmY)), "temp2.gif")
        #tempSeg2.setOutline((0,0,255))
        tempSeg2.draw(win2)
        lin = Line(Point(cSegmX,height - (50) - (50 * cSegmY) -25),Point(cSegmX, height - (50) - (50 * cSegmY) + 25))
        lin.draw(win2)
        if (cSegmX < width):
            cSegmX += image.size[0]
        else:
            cSegmX = 0
            cSegmY += 1
    CaptchaN += 1
print "Done"
win2.getMouse() # pause before closing