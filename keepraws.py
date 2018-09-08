#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# keepraws.py
# Mike Bickerton
# 25.08.2018
#
# Look at a folder containing processed jpeg images, and collect the corresponding
#   raw files for safe keeping.  It's assumed that there is a JPEGs folder, a RAWs folder,
#   and this program will create a keepers folder containing the required raw images.
#   filenames of the jpeg images will look like this:-
#   2017-09-21_21-40-00_MB__1435.jpg
#   2017-09-21_21-40-00_MB__1435_01.jpg
#   2017-09-21_21-46-53_MB__1442.jpg
#   filenames of the corresponding raw images will look like this:-
#   MB__1435.CR2
#   MB__1435.CR2.xmp
#   MB__1435_01.CR2.xmp
#   MB__1442.CR2
#   MB__1442.CR2.xmp
#

import os
import shutil
import re

jpegFolder   = 'JPEGs'
rawFolder    = 'RAWs'
keeperFolder = 'KeptRaws'

# regex for a valid jpeg filename:
imageRegex = re.compile(r'MB__\d{4}(_\d+)?\.(jpg|JPG)$')

print('Current dir is', os.getcwd())

if (os.path.isdir(rawFolder)):
    # Raw Folder exists, safe to continue
    if (os.path.isdir(jpegFolder)):
        imageList = os.listdir(jpegFolder)
        print(jpegFolder + ' directory found containing ' + str(len(imageList)) + ' images')  #Assumption: all files in directory are images!

        if (os.path.isdir(keeperFolder)):
            print(keeperFolder + ' directory already exists, skipping creation')
        else:
            print('Creating ' + keeperFolder + ' directory')
            os.makedirs(keeperFolder)

        for image in imageList:
            if imageRegex.search(image) == None:
                print('\n' + image + ' isnt a valid filename.')
                break
            else:
                print('\nJpeg: ' + image)
                rawName = imageRegex.search(image).group()[:8] + '.CR2'
                rawNamePath = os.path.join(rawFolder, rawName)
                xmpName = imageRegex.search(image).group()[:-4] + '.CR2.xmp'
                xmpNamePath = os.path.join(rawFolder, xmpName)

                print('Looking for ' + rawName, end = ' ')
                if (os.path.isfile(rawNamePath)):
                    print('...found')
                    shutil.copy(rawNamePath, keeperFolder)
                    print('Looking for ' + xmpName, end = ' ')
                    if (os.path.isfile(xmpNamePath)):
                        print('...found')
                        shutil.copy(xmpNamePath, keeperFolder)
                    else:
                        print('... ' + xmpName + ' NOT FOUND.')
                else:
                    print('...' + rawName + ' NOT FOUND. Skipping.')

        print('\nDone')
    else:
        print(jpegFolder + ' DIRECTORY NOT FOUND!')
        print('Exiting')
else:
    print(rawFolder + ' DIRECTORY NOT FOUND!')
    print('Exiting')