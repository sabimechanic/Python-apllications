import cv2, time
#import pandas
from datetime import datetime

first_frame=None
status_list=[None, None]
times = []
#df=pandas.DataFrame(columns=["Start", "End"])

#capturing the first frame
video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    status=0

    #applying grayscale and gaussian blur to the captured image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    #store the captured first frame in the first_frame variable
    if first_frame is None:
        first_frame=gray
        continue

    #calculate the difference btw the first frame and the current frame
    delta_frame = cv2.absdiff(first_frame,gray)
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)

    #find contours
    (cnts,_) =cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status=1

        (x, y, w, h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

    status_list.append(status)
    #applying a conditional to check for the difference between the last to entry to identify when the status changes from 0 to 1 and from 1 to 0. The aim is to record the timestamp of this change
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key=cv2.waitKey(1)

    if key==ord('q'):
        #adding a conditional if the q key is pressed while an image is in the frame
        if status==1:
            times.append(datetime.now())
        break
    
print(status_list)
print(times)

#iteration through a range of the number of items in times, annd appending the ith and the ith+1 index to our dataframe and saving it to a csv file
for i in range(0,len(times),2):
    df.df.append({"Start":times[i], "End":times[i+1]}, ignore_index=True)

#df.to_csv("motion_detector_times.csv")
    
video.release()
cv2.destroyAllWindows