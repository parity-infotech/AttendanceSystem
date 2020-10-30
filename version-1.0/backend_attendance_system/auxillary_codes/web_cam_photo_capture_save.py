import cv2
from datetime import datetime

def web_cam_capture_image():
    time = datetime.now().time()
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Scanning your face....")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame.")
            break
        cv2.imshow("Scanning your face....", frame)
        k = cv2.waitKey(1)
        if k%256 == 27:
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            img_name = "opencv_frame__{}.jpg".format(str(time).split(".")[0].replace(":", "_"))
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            break
    cam.release()
    cv2.destroyAllWindows()
    return img_name 
    
