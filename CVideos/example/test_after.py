from imutils.video import VideoStream

import time
import imutils
import cv2
import array
import numpy as np
import math

from CVideos import videofeed

def trimmean(arr, dev):
    arr_mean, arr_std = np.nanmean(arr), np.std(arr)
    cut_off = arr_std * dev
    lower, upper = arr_mean-cut_off, arr_mean + cut_off
    newArr = [x for x in arr if x >=lower and x <= upper]
    if math.isnan(np.nanmean(newArr)):
        return -1
    else:
        return int(np.nanmean(newArr))

# Masks the video based on a range of hsv colors
# Takes in a frame, range of color, and a blurred frame, returns a masked frame
def threshold_video(lower_color, upper_color, blur):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # hold the HSV image to get only red colors
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Returns the masked imageBlurs video to smooth out image
    return mask


#Should be able to be set with a switch
#Desired HSV Upper and Lower Bounds (Red)
#lower_bound = np.array([0, 166, 60])
#upper_bound = np.array([25, 255, 255])

#Desired HSV Upper and Lower Bounds (Blue)
lower_bound = np.array([99, 76, 142])
upper_bound = np.array([106, 165, 255])


#Creates a videostream and waits for the camera to turn on
#vs = VideoStream(usePiCamera=True).start()
#time.sleep(2.0)

#while True:
	#Creates the frame to be displayed and resizes it. I think we want it to be 240 pixels in width?
#	frame = vs.read()

center_coordinates = (0, 0)
historicalX = array.array('I')
historicalY = array.array('I')
#Anytime there is drastic movement, count needs to be reset (like if the turret or robot swings wildly)
#Manual reset also could work
count = 0
failXCount = 0
failYCount = 0

def test(frame):
    global count
    global failXCount
    global failYCount
    global historicalX
    global historicalY
    global center_coordinates

    centerX = array.array('I')
    centerY = array.array('I')
    frame = imutils.resize(frame, width=300)
    grey = threshold_video(lower_bound, upper_bound, frame)
    grey = cv2.bilateralFilter(grey, 11, 17, 17)
    edge = cv2.Canny(grey, 30, 200)
    cnts,_ = cv2.findContours(edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)

    screenHeight, screenWidth = edge.shape
    screenCnt = None
    frameCopy = frame.copy()
    minX = screenWidth
    maxX = 0
    minY = screenHeight
    maxY = 0

    for c in cnts:
        spacing = 5
        x,y,w,h = cv2.boundingRect(c)
        if (y - spacing) >= 0:
            yB = y - spacing
        else:
            yB = 0
        if (y + h + spacing) < screenHeight:
            yT = y + h + spacing
        else:
            yT = screenHeight - 1
        if (x - spacing) >= 0:
            xB = x - spacing
        else:
            xB = 0
        if (x + w + spacing) < screenWidth:
            xT = x + w + spacing
        else:
            xT = screenWidth - 1
        framecopy = cv2.rectangle(frameCopy, (xB, yB), (xT, yT), (255, 255, 0), 1)
        M = cv2.moments(c)
        if M["m00"] != 0:
            centerX.append(int(M["m10"] / M["m00"]))
            centerY.append(int(M["m01"] / M["m00"]))
        if x < minX:
            minX = x
        if y < minY:
            minY = y
        if (x + w) > maxX:
            maxX = x + w  
        if (y + h) > maxY:
            maxY = y + h     

    

    if (count > 20):
        print("Done Collecting")
        lower, upper =  np.mean(historicalX) - 50 if (np.mean(historicalX) - 50) >= 0 else 0, np.mean(historicalX) + 50 if (np.mean(historicalX) + 50) <= screenWidth else screenWidth
        testX = trimmean(centerX, 1)

        if testX != -1 and testX >= lower and testX <= upper:
            center_coordinates = (trimmean(centerX, 1), center_coordinates[1])
            historicalX.append(trimmean(centerX, 1))
            failXCount = 0
        else:
            failXCount += 1
            print("X Fail")
            if failXCount > 5:
                for x in historicalX:
                    historicalX.remove(x)
                failXCount = 0
                count = 0
                print("Cleared X")
        lower, upper = np.mean(historicalY) - 50 if (np.mean(historicalY) - 50) >= 0 else 0, np.mean(historicalY) + 50 if (np.mean(historicalY) + 50) <= screenHeight else screenHeight
        testY = trimmean(centerY, 1)

        if testY != -1 and testY >= lower and testY <= upper:
            center_coordinates = (center_coordinates[0], trimmean(centerY, 1))
            historicalY.append(trimmean(centerY, 1))
            failYCount = 0
        else:
            failYCount += 1
            print("Y Fail")
            if failYCount > 5:
                for y in historicalY:
                    historicalY.remove(y)
                failYCount = 0
                count = 0
                print("Cleared Y")

        if len(historicalX) > 19:
            historicalX.pop(0)
        if len(historicalY) > 19:
            historicalY.pop(0)
    else:
         if trimmean(centerX, 1) != -1:
            center_coordinates = (trimmean(centerX, 1), center_coordinates[1])
            historicalX.append(trimmean(centerX, 1))
         if trimmean(centerY, 1) != -1:
            center_coordinates = (center_coordinates[0], trimmean(centerY, 1))
            historicalY.append(trimmean(centerY, 1))

    count = count + 1
    img2 = cv2.rectangle(frameCopy.copy(), (minX, minY), (maxX - minX, maxY - minY), (255, 0, 0), 1)
    image = cv2.circle(img2, center_coordinates, 10, (255, 255, 0), 1)
    return image

videofeed(test, sidebyside=True)