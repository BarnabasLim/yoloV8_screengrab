from PIL import Image
from ultralytics import YOLO


import numpy as np


# Load a model
#Pose Extimation
# model = YOLO('models/yolov8n-pose.pt')  # load an official model
#Object Detection
model = YOLO('models/yolov8n.pt')  # pretrained YOLOv8n model


# Predict with the model
results = model('https://ultralytics.com/images/bus.jpg')  # predict on an image

# Show the results
for r in results:
    im = r.plot()  # plot a BGR numpy array of predictions

    print("Check im shape: ",np.array(im).shape)
    print("Check im shape: ",np.array(im[..., ::-1]).shape)
    im = Image.fromarray(im[..., ::-1])  # RGB PIL image
    im.show()  # show image
    im.save('output/results.jpg')  # save image

print("__getitem__()", results.__getitem__(0))
print("__len__()",results.__len__())
print("names", results[0].names)
print("names", results[0].boxes)
xyxy=results[0].boxes.xyxy.cpu().numpy()
confidence=results[0].boxes.conf.cpu().numpy()
class_id=results[0].boxes.cls.cpu().numpy().astype(int)
print(xyxy)
print(confidence)
print(class_id)
detected_item={}
names=results[0].names
for i in class_id:
    if names[i] in detected_item:
        detected_item[names[i]]=detected_item[names[i]]+1
    else:
        detected_item[names[i]]=1
print(detected_item)
