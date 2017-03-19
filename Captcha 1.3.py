def getCImage():
    html = urlopen("https://www.phpcaptcha.org/try-securimage/").read()
    soup = BeautifulSoup(html, "html.parser")
    images = [img for img in soup.findAll('img')]
    print (str(len(images)) + " images found.")

    img = soup.select("#captcha_one")
    flink = img[0]["src"]

    ilink = "https://www.phpcaptcha.org"
    link = ilink + flink + ".jpg"
    print (link)

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
                if (s > 0 and s < (im2.size[0] - 1) and t > 0 and t < (im2.size[1] - 1)):
                    if im2.getpixel((s,t))[0] == 255:
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
                        if (s > 0 and s < (im2.size[0] - 1) and t > 0 and t < (im2.size[1] - 1)) and \
                                        im2.getpixel((s, t))[
                                            0] != 255:
                            if (s, t) not in neigh:
                                neigh.append((s, t))

                    b = b + 1
                    if b >= len(neigh):
                        im2.putpixel((x, y), (255, 255))
                        done = 1
    print "Groups removed"
    return im2






def ColorWhitelist(im):    #Pixel seclection by colour
    BORDER_COLOR = 255
    temp = {}
    im2 = Image.new("LA",im.size,255)
    for x in range(im.size[1]):
      for y in range(im.size[0]):
        pix = im.getpixel((y,x))
        temp[pix] = pix
        if pix[0] == 140: # these are the numbers to get
          im2.putpixel((y,x),(0,255))
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
from PIL import Image, ImageDraw


CaptchaN = 0

width = 1200
height = 800
win = GraphWin(width=width, height=height)  # create a window
win.setCoords(0, 0, width, height)  # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)
#Segment and display 10 captcha's
for w in range(0,10):
    #Getting the Captcha from the Onlines
    getCImage()
    im = Image.open("File1.jpg").convert("LA")      #Opening Captcha and converting to Greyscale
    grps = Grouping(im,8)
    cimage = touchWhi(im,grps)

    cimage = ColorWhitelist(im)
    cimage = pixGroupRemove(cimage, 10)
    clustersx = clustify(cimage)
    sixclust = reduceTo(6, clustersx)
    im.save("temp1.gif")

    segments = []
    for i in range(0, 6):
        xmin = 300
        xmax = 0
        ymin = 300
        ymax = 0
        xcent = 0
        xtot = 0
        for (x,y) in sixclust[i]:
            if x < xmin:
                xmin = x
            if x > xmax:
                xmax = x
            if y < ymin:
                ymin = y
            if y > ymax:
                ymax = y
            xtot += x
        xcent = xtot / len(sixclust[i])
        print xcent
        xlen = xmax - xmin + 2
        ylen = ymax - ymin + 2
        image = Image.new("LA",(xlen,ylen),255)
        for (x, y) in sixclust[i]:
            image.putpixel((x - xmin + 1, y - ymin + 1), (0,255))
        segments.append((image, xcent))
        segments.sort(key=lambda tup: tup[1])








    captcha = Img(Point(im.size[0] / 2,height - ((im.size[1] / 2) + (im.size[1] * CaptchaN))), "temp1.gif")
    captcha.draw(win)

    widx = im.size[0]
    for tups in segments:
        image = tups[0]
        image.save("temp2.gif")
        tempSeg = Img(Point(widx + image.size[0] / 2, height - ((image.size[1] / 2) + (im.size[1] * CaptchaN))), "temp2.gif")
        widx += image.size[0] + 10
        tempSeg.draw(win)
    CaptchaN += 1
win.getMouse() # pause before closing