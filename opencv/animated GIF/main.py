import cv2
import imageio



# https://www.youtube.com/watch?v=yy6KqVNmWYM&t=722s



# 1. Get Images
cap = cv2.VideoCapture(0)


frames = []
image_count = 0

print('Press Kye "a" to add a picture')
print('Press Kye "q" to create the GIF file')
 


while True:
    ret, frame = cap.read()
    cv2.imshow("frame", frame)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    key = cv2.waitKey(0)
    if key == ord("a"):
        image_count += 1
        frames.append(rgb_frame)
        print("Adding new image:", image_count)
    
    elif key == ord("q"):
        break

print("Images added: ", len(frames))

# 2. Save GIF


print("Saving GIF file")
with imageio.get_writer("smiling.gif", mode="I") as writer:
    for idx, frame in enumerate(frames):
        print("Adding frame to GIF file: ", idx + 1)
        writer.append_data(frame)
        
        writer.append_data(frame)
        writer.append_data(frame)
        writer.append_data(frame)
        
        
        
        