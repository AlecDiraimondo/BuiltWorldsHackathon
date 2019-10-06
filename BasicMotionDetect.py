import cv2
import numpy as np
import time

cap = cv2.VideoCapture('Video1.mp4')
ret, frame1 = cap.read()        #declaring 2 frames for comparison
ret, frame2 = cap.read()
statustext = 0
init_time = 0
status = False # machine not moving
centers_x = []
centers_y = []


while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 15, 255, cv2.THRESH_BINARY) #threshold values -- should vary
    cv2.line(frame1,(0,60),(200,60),(255,255,0),1)

    dilated = cv2.dilate(thresh, None, iterations=4)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #statustext = 'Idle'
    timer = time.clock()



    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 3000:
            continue
        status = True
        print("left x, down y, right x, up y :", x,",", y , ",", x+w, ",", y+h)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0,255,0), 2)
        centerx = x+((x+w)-x)//2
        centery= y+((y+h)-y)//2
        print("Center Coordinates x,y:", centerx, centery)
        centers_x.append(centerx)
        centers_y.append(centery)
        statustext = 'Active'
        cv2.putText(frame1, "Status: {}".format(statustext), (10,20), cv2.FONT_HERSHEY_SIMPLEX,
         1, (0, 0, 255), 2)
    cv2.putText(frame1, "Timer: {}".format(int(timer)), (10,50), cv2.FONT_HERSHEY_SIMPLEX,
         1, (250, 250, 500), 2 )

    cv2.imshow("feed",frame1)
    frame1 = frame2

    ret, frame2 = cap.read()


    if cv2.waitKey(40)== 27:
        break

cv2.destroyAllWindows()
cap.release()
