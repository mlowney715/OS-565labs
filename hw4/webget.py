#! python3
#
# M. Phil Lowney, ID#01191051, ECE565F2016 HW#4-6
#
# webget.py - Obtains a local copy of a website, ignoring circular and
# broken links.
#
Usage = "Usage: webget <web address>"

import sys
import requests
import bs4
import io
import os

if len(sys.argv) == 2:
    # Get web address from CL
    address = ''.join(sys.argv[1:])
else:
    print(Usage)
    quit()

# Attempt to obtain the index file
res = requests.get(address)
try:
    res.raise_for_status()
except Exception as exc:
    print("There was a problem: %s" % (exc))
    quit()

# Make the html index
index = open('index.html', 'wb')
print("Downloading index.html...")

for chunk in res.iter_content(32768):
    # Write the index in chunk at a time
    index.write(chunk)

# Close the file for writing
index.close()
# Open the file for reading
index = io.open('index.html',encoding='ISO-8859-1')

# Create an index of CCS Tags
tags = bs4.BeautifulSoup(index.read(), "lxml")

suffix = len(address)
prefix = address[:suffix-5]

# Make the directory unless it is already there
try:
    os.mkdir('ece565')
except:
    pass

# All URLs have the tag 'a'
links = tags.select('a')
for item in links:
    pathname = str(item.get('href'))
    # Only grab the word docs and powerpoints
    if pathname.endswith(('.docx', '.ppt')):
        filename = os.path.basename(pathname)
        print("Downloading %s..." % (filename))
        fileURL = ''.join([prefix,'/',filename])
        # Attempt to grab the file
        res = requests.get(fileURL)
        try:
            res.raise_for_status()
        except Exception as exc:
            print("Error Downloading %s: %s" % (filename, exc))
            break
        # Attempt to save the file
        try:
            imageFile = open(os.path.join('ece565',
                os.path.basename(fileURL)), 'wb')
            for chunk in res.iter_content(32768):
                imageFile.write(chunk)
            imageFile.close()
        except:
            print("Write error... skipping file")
            continue
