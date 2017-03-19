from urllib2 import urlopen
from bs4 import BeautifulSoup
import urllib
from PIL import Image
from operator import itemgetter
import os
html = urlopen("https://www.phpcaptcha.org/try-securimage/").read()
soup = BeautifulSoup(html, "html.parser")
images = [img for img in soup.findAll('img')]
print (str(len(images)) + " images found.")



img = soup.select("#captcha_one")
flink =  img[0]["src"]

ilink = "https://www.phpcaptcha.org"
link = ilink + flink + ".jpg"
print (link)

urllib.urlretrieve(link, "File1.jpg")

im = Image.open("File1.jpg").convert("LA")
im.show()
print im.getbands()
print im.mode
print im.getpixel((10,10))

his = im.histogram()

values = {}

for i in range(256):
  values[i] = his[i]

for j,k in sorted(values.items(), key=itemgetter(1), reverse=True)[:10]:
  print j,k


x = [0]
print len(x)
for i in range(0,1):
    print i
#os.path.basename(link)