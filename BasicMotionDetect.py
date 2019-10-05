import cv2
import numpy as np

cap = cv2.VideoCapture('Video1.mp4')
ret, frame1 = cap.read()        #declaring 2 frames for comparison
ret, frame2 = cap.read()
statustext = 0

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 15, 255, cv2.THRESH_BINARY) #threshold values -- should vary
    cv2.line(frame1,(0,60),(200,60),(255,255,0),1)

    dilated = cv2.dilate(thresh, None, iterations=4)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #statustext = 'Idle'



    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 3000:
            continue

        print("left x, down y, right x, up y :", x,",", y , ",", x+w, ",", y+h)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0,255,0), 2)
        centerx = x+((x+w)-x)//2
        centery= y+((y+h)-y)//2
        print("Center Coordinates x,y:", centerx, centery)
        statustext = 'Active'
        cv2.putText(frame1, "Status: {}".format(statustext), (10,20), cv2.FONT_HERSHEY_SIMPLEX,
         1, (0, 0, 255), 3)


    cv2.imshow("feed",frame1)
    frame1 = frame2

    ret, frame2 = cap.read()


    if cv2.waitKey(40)== 27:
        break

cv2.destroyAllWindows()
cap.release()
