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

clusters = []
clustr = []
def floodfill(image, x, y):

    #"hidden" stop clause - not reinvoking for "c" or "b", only for "a".
    if image.getpixel((x, y))[0] == 0:
        clustr.append((x,y))
        image.putpixel((x,y), (100,255))
        #recursively invoke flood fill on all surrounding cells:
        if x > 0:
            floodfill(image,x-1,y)
        if x < image.size[0] - 1:
            floodfill(image,x+1,y)
        if y > 0:
            floodfill(image,x,y-1)
        if y < image.size[1] - 1:
            floodfill(image,x,y+1)


from graphics import *
from urllib2 import urlopen
from bs4 import BeautifulSoup
import urllib
import math
import numpy
from PIL import Image, ImageDraw

from operator import itemgetter
import os
#Getting the Captcha from the Onlines
getCImage()


#Opening Captcha and converting to Greyscale
im = Image.open("File1.jpg").convert("LA")
#im.show()
print im.getbands()
print im.mode
print im.getpixel((10,10))
print im.size
im2 = Image.new("LA",im.size,255)

BORDER_COLOR = 255
temp = {}





#Pixel seclection by colour
for x in range(im.size[1]):
  for y in range(im.size[0]):
    pix = im.getpixel((y,x))
    temp[pix] = pix
    if pix[0] == 140: # these are the numbers to get
      im2.putpixel((y,x),(0,255))




#remove pixelgroups smaller than 10
for x in range(im2.size[0]):
    for y in range(im2.size[1]):
        neigh = []
        temp = im2.getpixel((x,y))[0]
        if temp != 255:
            neigh.append((x,y))
            b = 0
            done = 0
            while len(neigh) < 5 and done == 0:

                for (s, t) in ((neigh[b][0] + 1, neigh[b][1]), (neigh[b][0] - 1, neigh[b][1]), (neigh[b][0], neigh[b][1] + 1), (neigh[b][0], neigh[b][1] - 1)):
                    if (s > 0 and s < (im2.size[0] - 1) and t > 0 and t < (im2.size[1] - 1)) and im2.getpixel((s, t))[
                        0] != 255:
                        if (s,t) not in neigh:
                            neigh.append((s,t))

                b = b+1
                if b >= len(neigh):
                    im2.putpixel((x, y), (255, 255))
                    done = 1







#Put all black pixels in a list
black = []
for x in range(0,215):
    for y in range(0,80):
        if (im2.getpixel((x,y))[0] != 255):
            black.append((x,y))



#Floodfill pixels to get pixel collections
while len(black) > 0:
    for clusts in clusters:
        black = set(black) - set(clusts)
    if len(black) > 0:
        clustr = []
        floodfill(im2, list(black)[0][0], list(black)[0][1])
        clusters.append(clustr)

clusters.append(clustr)


#Sort groups small to big
clusters.sort(key=len)





im3 = Image.new("LA",im.size,255)


#Add smallest to groups to the closest groups untill 6 groups left
while (len(clusters) > 6):
    mx = []
    my = []
    for (s,t) in clusters[0]:
        mx.append(s)
        my.append(t)
    medx = numpy.median(numpy.array(mx))
    medy = numpy.median(numpy.array(my))
    print medx, medy

    cdist = (1000,0)
    for n in range(1, len(clusters)):
        for coords in clusters[n]:
            x1 = medx
            y1 = medy
            x2 = coords[0]
            y2 = coords[1]
            tempdist = ((x1 - x2)**2) + (((y1 - y2)**2) / 2)
            if tempdist < cdist[0]:
                cdist = (tempdist, n)
    clusters[cdist[1]] = clusters[0] + clusters[cdist[1]]
    clusters.pop(0)
    clusters.sort(key=len)
    print cdist


# for i in range (0, len(clusters)):
#     for u in clusters[i]:
#         im3.putpixel(u, ((10 + (20 * i)), 255))


segments = []
for i in range(0, 6):
    xmin = 300
    xmax = 0
    ymin = 300
    ymax = 0
    for (x,y) in clusters[i]:
        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y
    print xmin, xmax, "X"
    print ymin, ymax, "Y"
    xlen = xmax - xmin + 2
    ylen = ymax - ymin + 2
    image = Image.new("LA",(xlen,ylen),255)
    for (x, y) in clusters[i]:
        image.putpixel((x - xmin + 1, y - ymin + 1), (0,255))
    segments.append(image)

#for image in segments:
    #image.show()
width = 800
height = 600
im.save("temp1.gif")
win = GraphWin(width = width, height = height) # create a window
win.setCoords(0, 0, width, height) # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)
#mySquare = Rectangle(Point(1, 1), Point(9, 9)) # create a rectangle from (1, 1) to (9, 9)
#mySquare.draw(win) # draw it to the window
captcha = Img(Point(im.size[0] / 2,height - (im.size[1] / 2)), "temp1.gif")

captcha.draw(win)
widx = im.size[0]
for image in segments:
    image.save("temp2.gif")
    tempSeg = Img(Point(widx + image.size[0] / 2, height - (image.size[1] / 2)), "temp2.gif")
    widx += image.size[0] + 10
    tempSeg.draw(win)
win.getMouse() # pause before closing