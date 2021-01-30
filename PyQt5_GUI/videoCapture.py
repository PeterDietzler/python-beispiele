import numpy as np
import cv2
import time

print('videoCapture')


class videoCapture():
    def __init__(self):
        super().__init__()
        self.simulation = False
        
    def open(self, cam_id, simulation=False):
        print("openCam()")
        self.simulation = simulation
        
        if self.simulation == True:
            return 0

        try: 
            print( "openCam:",cam_id )
            self.camera = cv2.VideoCapture( cam_id ) ### <<<=== SET THE CORRECT CAMERA NUMBER
            self.camera.set(3,960)             # set frame width
            self.camera.set(4,720)              # set frame height
            self.camera.set(10,160)             # set britnes
            time.sleep(0.5)
            print( self.camera.get(3), self.camera.get(4))
            print( self.camera.get(5))
            if not self.camera.isOpened():
                print("Cannot open camera")
        except Exception:
            print("can not open Cam:", self.Cam_id )
            
    def getFrame(self):
        
        if self.simulation == True: return 0
        
        (self.grabbed, self.frame) = self.camera.read()
        # end of feed
        if not self.grabbed:
            print("camera.read -> rabbed") 
        else:
            # gray frame
            self.frame1 = cv2.cvtColor( self.frame, cv2.COLOR_BGR2GRAY)
            return self.frame1

    def showFrame(self):
        #print("showFrame()")
        if self.simulation == True:
            return 0
        
        (self.grabbed, self.frame0) = self.camera.read()
        
        # end of feed
        if not self.grabbed:
            print("camera.read -> grabbed")
            return -1 
        else:
            # gray frame
            #self.frame1 = cv2.cvtColor( self.frame0, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Frame0: Raw", self.frame0)
            if cv2.waitKey(1) == ord('q'):
                return False
            return True


if __name__ == "__main__":
    vc= videoCapture()
    vc.open(0, simulation=False)
    while 1: 
        res = vc.showFrame()
        if res==False:
            break
    vc.release()
    cv2.destroyAllWindows()
"""
    cap = cv2.VideoCapture(0)
    cap.set(3,640)             # set frame width
    cap.set(4,480)              # set frame height
    time.sleep(0.5)
    print( cap.get(3), cap.get(4))
    print( cap.get(5))
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv2.imshow('Frame: raw ', frame)
        cv2.imshow('Frame: gray', gray)
        
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
"""




