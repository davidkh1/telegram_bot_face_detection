#Back-end impmlemenation of Telegram bot for Thales demo
#Author: David Khosid
# Run: python online_face_detection_demo.py

import sys
import telegram
import urllib2
import cv2
from time import sleep


fromBotDir = 'images_from_bot'
toBotDir = 'images_to_bot'

botName = 'demo5dbot'
botToken = 'XXXXXX'	#Create bot with 'BotFather' from Telegram
baseUrl = 'https://api.telegram.org/bot%s' % botToken
longPoolingTimeoutSec = 60

cascadeFile = 'haarcascade_frontalface_default.xml'
sleepIntervalSec = 2
lastConsumedUpdateInit = 0	

def cascadeDetect(cascade, image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cascade.detectMultiScale(
        gray_image,
        scaleFactor = 1.15,
        minNeighbors = 5,
        minSize = (100, 100),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )

def detectionsDraw(image, detections):
    for (x, y, w, h) in detections:
        print("(({0}, {1}), ({2}, {3}))".format(x, y, x+w, y+h))
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


def detectFace(inputImFile, outImFile):
    cascade = cv2.CascadeClassifier(cascadeFile)
    image = cv2.imread(inputImFile)
    if image is None:
        print("ERROR: Image did not load.")
        return (0, "ERROR: Image did not load.")
        # return 2

    detections = cascadeDetect(cascade, image)
    detectionsDraw(image, detections)

    print("Found {0} objects!".format(len(detections)))
    print("saving into {}".format(outImFile))
    cv2.imwrite(outImFile, image)

    detectMsg = {}
    if len(detections)>0:
        detectMsg = "Found {0} objects!".format(len(detections))
    else:
        detectMsg = "None found"

    return (len(detections), detectMsg)

def botWorker(counter, lastConsumedUpdate):
    bot = telegram.Bot(token=botToken)
    # print bot.getMe()

    updates = bot.getUpdates(offset=lastConsumedUpdate+1, timeout=longPoolingTimeoutSec)
   
    numOfUpdates = len(updates)
    numOfNewUpdates = 0 if (numOfUpdates < 1) else updates[-1].update_id-lastConsumedUpdate #assumption of continuous counter of events

    if(numOfNewUpdates == 0):
        print('{}. No new updates'.format(counter))
        return lastConsumedUpdate
    else:
        print '{}. There are {} new updates'.format(counter, numOfNewUpdates)

    for u in updates:
        updateId = u.update_id
        if(updateId <= lastConsumedUpdate):
            break
        print 'updateId={}, date={}'.format(u.update_id, u.message.date)


    for u in updates:
        updateId = u.update_id

        if(updateId <= lastConsumedUpdate):
            continue

        print 'updateId={}, date={}'.format(u.update_id, u.message.date)

        if u.message.photo:
            print('There are {} photos in this update'.format(len(u.message.photo)))
            biggestPhoto = u.message.photo[-1]
            biggestPhotoFileId =  biggestPhoto.file_id
            print 'biggestPhoto= {}x{}, fileId={}'.format(biggestPhoto.height, biggestPhoto.width,  biggestPhoto.file_id)

            newFile = bot.getFile(biggestPhotoFileId)
            newFileUrl = newFile.file_path
            print(newFile)
            newFilePath = fromBotDir + '/' + str(updateId) + '.jpg' #build from updateId
            print('newFilePath={}').format(newFilePath)
            # bot.download(url, newFilePath)
            # newFile.download(newFilePath)

            photoFile = urllib2.urlopen(newFileUrl)
            output = open(newFilePath,'wb')
            output.write(photoFile.read())
            output.close()

            outImFile = toBotDir + '/' + str(updateId) + '_detected' + '.jpg'
            numFaces, detectMsg = detectFace(newFilePath, outImFile)

            # To reply messages you'll always need the chat_id
            chat_id = u.message.chat_id
            print('chat_id={}'.format(chat_id))
            print('outImFile={}'.format(outImFile))
            # bot.sendPhoto(chat_id, outImFile, caption='X faces detected')
            message = bot.sendPhoto(photo=open(outImFile, 'rb'), caption=detectMsg, chat_id=chat_id)
        lastConsumedUpdate = u.update_id

    # To reply messages you'll always need the chat_id
    # chat_id = bot.getUpdates()[-1].message.chat_id
    # bot.sendMessage(chat_id=chat_id, text="detecting ....")

    print 'Last consumed update: {}'.format(lastConsumedUpdate)
    return lastConsumedUpdate

def main(argv = None):
    print('Starting Telegram bot backend')

    lastConsumedUpdate = lastConsumedUpdateInit
    counter = 0
    while (True):
        counter = counter + 1
        lastConsumedUpdate = botWorker(counter, lastConsumedUpdate)
        sleep(sleepIntervalSec)

if __name__ == '__main__':
    sys.exit(main())
