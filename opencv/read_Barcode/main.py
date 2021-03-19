import cv2
import frame_draw
import numpy as np
from pyzbar.pyzbar import decode



# camera setup
camera_source = 0
#camera_width, camera_height = 650,480
#camera_width, camera_height = 1280,720
camera_width, camera_height = 1920,1080
#camera_frame_rate = 30
#camera_fourcc = cv2.VideoWriter_fourcc(*"MJPG")


#cap = cv2.VideoCapture(camera_source, cv2.CAP_DSHOW)
cap = cv2.VideoCapture(camera_source)
cap.set(3,camera_width)
cap.set(4,camera_height)
#cap.set(5,camera_frame_rate)
#cap.set(6,camera_fourcc)


#-------------------------------
# frame drawing/text module 
#-------------------------------

draw = frame_draw.DRAW()
draw.width = camera_width
draw.height = camera_height


width = cap.get(3)
height= cap.get(4)
frate = cap.get(5)


print('CAMERA:',"id:",camera_source, " Breite:",width,"px Höhe:",height,"px Fps:",frate)

with open('BarCodePassList.txt') as f:
    myPassList = f.read().splitlines()
    
print(myPassList)



while 1:
    
    text = []
    #text.append(f'CAMERA: {camera_source} {width}x{height} {frate}FPS')
    text.append(f'LAST CLICK: NONE')
    
    #1. read frame
    ret, frame0 = cap.read()
    '''
    #height, width, _ = frame.shape
    frame1 = cv2.rotate(frame0, cv2.ROTATE_180)
    # 2. Extract Region of interest
    x1,y1   = 0, 0
    x2,y2 = int(width), int(height-200)
    roi_frame = frame1[y1: y2, x1: x2]

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
            cv2.drawContours( roi_frame, [cnt], -1, (0, 255, 0), 1)          #grün     
            cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
            pass
    '''
    for barcode in decode(frame0):     
        #text.append(str(barcode.data))
        #print(barcode)
        myBarCode = barcode.data.decode('utf-8')
        print(myBarCode)
        if myBarCode in myPassList:
            #print('Pass')
            myOutput = 'PASS'
            myColor = (0,255,0)
        else:
            #print('Fail')
            myOutput = 'FAIL'
            myColor = (0,0, 255)
        pts = np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines( frame0, [pts], True, myColor, 5)
        pts2 = barcode.rect
        cv2.putText( frame0 ,myBarCode + myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor,2)
    
    
    draw.add_text_top_left(frame0 ,text)

    cv2.imshow("1. Frame0", frame0)
    #cv2.imshow("2. Region of interest", roi_frame)
    #cv2.imshow("3. gray_frame", gray_frame)
    #cv2.imshow("4. threshold_frame", threshold_frame)
   
    key = cv2.waitKey(1)
    if key == 27:    # ESC
        break 
    
cap.release()
cv2.destroyAllWindows()   






