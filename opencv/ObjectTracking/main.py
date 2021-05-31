import cv2
import frame_draw
import platform
import globalvars

global PicturePath
global imageName
global roi_frame

PicturePath = 'Picture'
imageName = 'RangeOfIntrest'

def draw_circle(event,x,y,flags,param):
    global mouseX , mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(roi_frame,(x,y),100,(255,0,0),-1)
        mouseX,mouseY = x,y
        print('DBLCLK x = %d, y = %d'%(mouseX,mouseY))
        
    elif event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(roi_frame,(x,y),100,(255,0,0),-1)
        mouseX,mouseY = x,y
        print('DOWN  x = %d, y = %d'%(mouseX,mouseY))
        
    elif event == cv2.EVENT_MOUSEMOVE:
        cv2.circle(roi_frame,(x,y),100,(255,0,0),-1)
        mouseX,mouseY = x,y
        print('MOVE x = %d, y = %d'%(mouseX,mouseY))
        #print(mouseX,mouseY)

def savePicture(Filename, FrameName):
    print('Save picture')
    cv2.imwrite( PicturePath +'/' + Filename, FrameName)
    
# camera setup
camera_source = 0
camera_width, camera_height = 1920,1080
#camera_frame_rate = 30
#camera_fourcc = cv2.VideoWriter_fourcc(*"MJPG")

uname = platform.uname()
hostname = uname.node
print('Hostname = ' +hostname)

if hostname == 'SEL-0163':# LMP800
    #camera_width, camera_height = 1920,1080
    camera_width, camera_height = 1280,720
    cap = cv2.VideoCapture(camera_source, cv2.CAP_DSHOW)
    #cap = cv2.VideoCapture(camera_source)
    rotate_window = 1
elif hostname == 'NB-0028': #Laptop
    camera_width, camera_height = 1280,720
    cap = cv2.VideoCapture(camera_source, cv2.CAP_DSHOW)
    rotate_window = 0
else:
    cap = cv2.VideoCapture(camera_source)
    rotate_window = 0



cap.set(3,camera_width)
cap.set(4,camera_height)
#cap.set(5,camera_frame_rate)
#cap.set(6,camera_fourcc)

width = cap.get(3)
height= cap.get(4)
frate = cap.get(5)


#-------------------------------
# frame drawing/text module 
#-------------------------------

draw = frame_draw.DRAW()
draw.width = width
draw.height = height

print('CAMERA:',"id:",camera_source, " Breite:",width,"px Höhe:",height,"px Fps:",frate)

cv2.namedWindow( imageName)
cv2.setMouseCallback( imageName, draw_circle)
   

while True:
    text = []
    #text.append(f'CAMERA: {camera_source} {width}x{height} {frate}FPS')
    text.append(f'LAST CLICK: NONE')
    #1. read frame
    ret, frame0 = cap.read()
    if ret == False:
        print('cap.read() return False')
        break
    
    #height, width, _ = frame.shape
    if rotate_window == 1:
        frame1 = cv2.rotate(frame0, cv2.ROTATE_180)
    else:
        frame1 = frame0
        
    # 2. Extract Region of interest
    x1,y1   = 0, 0
    x2,y2 = int(width), int(height-200)
    roi_frame = frame1[y1: y2, x1: x2]

    # 3. convert to gray frame
    gray_frame = cv2.cvtColor( roi_frame,cv2.COLOR_BGR2GRAY)

    # 4. threshold frame n out of 255 (85 = 33%)
    _, threshold_frame = cv2.threshold( gray_frame, 115, 140, cv2.THRESH_BINARY)

    # 5. Object Detection
    contours, _ = cv2.findContours( threshold_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   
    for cnt in contours:
        #print( cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        #print(area)
        if x > 90 and x < 1250:
            if y > 120 and y < 330:
                if 500 < area < 1200:
                    if w < 100 and w > 70:
                        if h < 20 and h > 10:
                            cv2.polylines( roi_frame, [cnt], True, (0,255,0), 1)#grüner Rahmen
                            #cv2.drawContours( roi_frame, [cnt], -1, (0, 255, 0), 1)         #grün#
                            #v2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                            #print(cnt)
                            #print( x, y, w, h )
                            pass
                
        '''        
        if 600 < area < 1100:
            #print(area)
            print(x, y, w, h)
            #cv2.drawContours( roi_frame, [cnt], -1, (0, 255, 0), 3)          #grün     
            #cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
            cv2.polylines( roi_frame, [cnt], True, (0,255,0), 2)#grüner Rahmen
            #cv2.polylines( roi_frame, [cnt], True, (0,0,255), 2) #roter Rahmen
            pass
        '''    

    draw.add_text_top_left(roi_frame ,text)
 
    #cv2.imshow("1. Frame0", frame0)
    
    cv2.imshow( imageName, roi_frame)
    #cv2.imshow("3. gray_frame", gray_frame)
    #cv2.imshow("4. threshold_frame", threshold_frame)
    #calling the mouse click event
    
    
    
    #key = cv2.waitKey(30) 
    #if key == 27:    # ESC
    #    break 
    
    key = cv2.waitKey(1)
    if key == 27:    # ESC
        break 
    key = key %256    
    if key == ord('r'):
        print('Press Butten R')
        if rotate_window == 0:
            rotate_window = 1
        else:
            rotate_window = 0
    elif key == ord('p'):
        print('x = %d, y = %d'%(mouseX , mouseY)) # mouseX,mouseY)
    elif key == ord('w'):
        savePicture( imageName +'.jpg', roi_frame)
    elif key == 255:  # normally -1 returned,so don't print it
        continue
    else:
        print('Press Kye = ', repr(chr(key%256)) )   # else print its value
        #print('You pressed %d (0x%x), LSB: %d (%s)' % (key, key, key % 256,
        #repr(chr(key%256)) if key%256 < 128 else '?'))

cap.release()
cv2.destroyAllWindows()   






