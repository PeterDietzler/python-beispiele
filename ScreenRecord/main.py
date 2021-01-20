

import cv2, numpy, pyautogui, keyboard
import platform
from screeninfo import get_monitors
import tkinter as tk



uname = platform.uname()
print(f"System   : {uname.system}")
print(f"Hostname : {uname.node}")
print(" ")
 
for m in get_monitors():
    print(str(m))
print(" ")

 
root = tk.Tk()


 
if uname.system == 'Linux':
	if (uname.node == 'peter-desktop' ):
		print('Linux')

elif uname.system == 'Window': 
	if uname.node == 'peter-desktop': 
		print('Windows')

else: 
	print('unknow hostname or system')
	exit()

print(" ")


screen_width  = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

print('width  = ', screen_width, 'px')
print('height = ', screen_height, 'px')

filename = "record"
file_type = cv2.VideoWriter_fourcc(*'mp4v')
fps = 25
SCREEN_SIZE = (screen_width, screen_height)

vid = cv2.VideoWriter( filename + ".mp4",  file_type,  fps, (SCREEN_SIZE))


print("Starte Aufnahme ( Hauptbildschirm ).....Press x to Stop recording")

while True:
	img = pyautogui.screenshot()
	numpy_frame = numpy.array(img)
	cv2.waitKey(50)
	frame = cv2.cvtColor(numpy_frame, cv2.COLOR_BGR2RGB)
	vid.write(frame)
	if keyboard.is_pressed('x'):
		#if cv2.waitKey(1) & 0xFF == ord('x'):
		print("Stoppe Aufnahme")
		break

cv2.destroyAllWindows()
vid.release()
