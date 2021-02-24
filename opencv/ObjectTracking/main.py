import cv2

cap = cv2.VideoCapture(0)

while True:
    #1. read frame
    ret, frame0 = cap.read()
    #height, width, _ = frame.shape

    # 2. Extract Region of interest
    x1,y1   = 0, 0
    x2,y2 = 500, 450
    roi_frame = frame0[y1: y2, x1: x2]

    # 3. convert to gray frame
    gray_frame = cv2.cvtColor( roi_frame,cv2.COLOR_BGR2GRAY)

    # 4. threshold frame n out of 255 (85 = 33%)
    _, threshold_frame = cv2.threshold( gray_frame, 90, 200, cv2.THRESH_BINARY)

    # 5. Object Detection
    contours, _ = cv2.findContours( threshold_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   
    for cnt in contours:
        #print( cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        #print(area)
        if 150 < area < 3500:
            #print(area)
            cv2.drawContours( roi_frame, [cnt], -1, (255, 0, 0), 1)          #blau     
            cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
            pass
        elif  3500 < area < 7000:          
            #print(area)
            cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 1) #grün
            cv2.drawContours( roi_frame, [cnt], -1, (0, 255, 0), 1)
            pass
        elif  area > 7000:          
            cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 0, 255), 1)  #Rot
            cv2.drawContours( roi_frame, [cnt], -1, (0, 0, 255), 1)
            pass
   
   
   
    #cv2.imshow("1. Frame0", frame0)
    cv2.imshow("2. Region of interest", roi_frame)
    #cv2.imshow("3. gray_frame", gray_frame)
    #cv2.imshow("4. threshold_frame", threshold_frame)
   
    key = cv2.waitKey(30)
    if key == 27:    # ESC
        break 
    
cap.release()
cv2.destroyAllWindows()   






