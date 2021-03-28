import io
import json
import cv2
import numpy as np
import requests
import os

from globalvars import myOCR_KEY 

# https://www.youtube.com/watch?v=fswR5cbmq-c&t=1523s

filename="OCR_picture2.jpg"

# 1 make a picture

def makePicture():

    camera_width, camera_height = 1280,720
    #camera_width, camera_height = 1920,1080

    cap = cv2.VideoCapture(0)
    
    cap.set(3,camera_width)
    cap.set(4,camera_height)
    
    while True:
        res, img = cap.read()
       
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite( filename, img)
            break
        if key == ord('q'):
            break
        
        cv2.imshow("1. Frame0", img)
   
    print ('Ende..')
    os.system('pix ' + filename)




#makePicture()

    # 2. 

img = cv2.imread( filename )


height, width, _ = img.shape

# Cutting image
roi = img[0: height, 0: width]



# 2) Set the OCR engine
url_api = "https://api.ocr.space/parse/image"
_, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
file_bytes = io.BytesIO(compressedimage)


result = requests.post( url_api,
              files = { filename: file_bytes},
              data = {"apikey": myOCR_KEY ,"language": "ger"})

# 3) Read the Result
result = result.content.decode()
result = json.loads(result)
#print(result)

parsed_results = result.get("ParsedResults")[0]
#print(parsed_results)
text_detected = parsed_results.get("ParsedText")
print(text_detected)

cv2.imshow("roi",roi)
cv2.imshow("img",img)
cv2.waitKey(0)


cap.release()
cv2.destroyAllWindows()           
        