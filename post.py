from PIL import Image
from ultralytics import YOLO

import cv2
import numpy as np
import mss #for screenshot

from yoloV8.utils import *

from service.dataController import DataController

# Load a model
#Pose Extimation
# model = YOLO('models/yolov8n-pose.pt')  # load an official model
#Object Detection
model = YOLO('models/yolov8n.pt')  # pretrained YOLOv8n model

def getwindowgeometry():
    x=80
    y=0
    w=800
    h=640
    return x, y, w, h

def detect_count(results):
    detected_item={}
    class_id=results[0].boxes.cls.cpu().numpy().astype(int)
    names=results[0].names

    for i in class_id:
        if names[i] in detected_item:
            detected_item[names[i]]=detected_item[names[i]]+1
        else:
            detected_item[names[i]]=1
    print(detected_item)
    return detected_item

sct = mss.mss()
x, y, w, h = getwindowgeometry()

dataController=None
continueStep=False
detected_item={}
classes=[0, 1,2,3,4,5,7,8,9,15,16,24]
while True:

    #Step 1: Capture screen grab
    img = np.array(sct.grab({"top": y-30, "left": x, "width": w, "height": h, "mon": -1}))

    #Step 2: Preprocess Images
    image_data = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    print("Check im 1 shape: ",np.array(image_data).shape, np.array(image_data.max()))

    #uncomment to resize image
    # input_size=416
    # image_data = image_preprocess(image_data, [input_size, input_size])*255
    #print("Check im 2 shape: ",np.array(image_data).shape, np.array(image_data.max()))

    # Predict with the model
    results = model.predict(source=image_data, classes=classes)
    # model(image_data)  # predict on an image

    # Show the results
    detected_item=detect_count(results)
    result=results[0]
    im = result.plot()  # plot a BGR numpy array of predictions
    #print("Check im 5 shape: ",np.array(im).shape, np.array(im.max()))
    im=np.array(im)/255


    cv2.imshow("OpenCV/Numpy normal", im)
    if continueStep==False or dataController==None:
        del dataController
        dataController=None
        dataController=DataController()
        continueStep=dataController.step(detected_item, img=im)
    else:
        continueStep=dataController.step(detected_item, img=im)

        

    if cv2.waitKey(25) & 0xFF == ord("q"):
        if(dataController!=None):
            del dataController
        cv2.destroyAllWindows()
        break
