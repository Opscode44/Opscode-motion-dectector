import cv2, time, pandas
from datetime import datetime


first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start","End"])

#Instantiate video streaming object
video = cv2.VideoCapture(0)

while True:
    #read video stream
    check, frame = video.read()
    status = 0

    #convert to gray scale and Gaussianblue for accuracy in detecting object motion
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21),0)

    #save first frame in a variable: later to check difference between this frame and following frames
    if first_frame is None:
        first_frame = gray
        continue

    #difference between following frames and first frame, save as deltaframe, calculate threshold(30) convert all pixels above threshold to white
    delta_frame = cv2.absdiff(first_frame,gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    #thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    #calculate contours using thresh frame, all contours with area>10000 are classified as motion objects
    (cnts,_)=cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1
        #draw rectangle above threshold
        (x,y,w,h)= cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

    #calculate time objects enters and exits video
    status_list.append(status)

    status_list = status_list[-2:]

    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    #show videos
    cv2.imshow("Gray Frame", frame)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)

    #exit frame on press of key q
    key = cv2.waitKey(1)
    if key == ord("q"):
        if status == 1:
            times.append(datetime.now())
        break
    print(times)
    print(status_list)

for i in range(0,len(times), 2):
    df = df._append({"Start":times[i], "End":times[i+1]}, ignore_index=True)

df.to_csv("Times.csv")
video.release()
cv2.destroyAllWindows
