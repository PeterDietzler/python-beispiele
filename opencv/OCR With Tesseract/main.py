
import cv2
import numpy as np
import pytesseract

filename = "OCR_picture2.jpg"
print('stat programm... ')

<<<<<<< HEAD
  
  
#pytesseract.pytesseract.tesseract_cmd = r"tesseract"
=======
#pytesseract.pytesseract.tesseract_cmd = r"tesseract"

>>>>>>> cacec9a4367c2ede0106cdee5cf476921a93d0bb
pytesseract.pytesseract.tesseract_cmd = r"C:\_PortableApps\Tesseract-OCR\tesseract.exe"

img = cv2.imread( filename )
text = pytesseract.image_to_string(img)
print(text)
        

# 1. Load the image
img = cv2.imread( filename )
text = pytesseract.image_to_string(img)
print("------------------------------------------ Standard Farbbild ------------------------------------------")
print(text)

# 2. Resize the image
img = cv2.resize(img, None, fx=0.5, fy=0.5)


# 3. Convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
text = pytesseract.image_to_string( gray)
print("------------------------------------------ Standard Graustufen Bild ------------------------------------------")
print(text)

# 4. Convert image to black and white (using adaptive threshold)
adaptive_threshold = cv2.adaptiveThreshold( gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)

config = "--psm 3"
text = pytesseract.image_to_string(adaptive_threshold, config=config, lang ="deu"  )
print("--------------------------   adaptive_threshold Bild ------------------------------------------")
print(text)
print("--------------------------   ENDE ------------------------------------------")

cv2.imshow("img",img)
cv2.imshow("gray", gray)
cv2.imshow("adaptive_threshold", adaptive_threshold)

cv2.waitKey(0)





