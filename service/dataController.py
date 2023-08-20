from datetime import datetime

import time
from service.telegramBot import TelegramBot
import cv2
import os
from dotenv import load_dotenv

class DataController:

    #Initalise and start data collection
    def __init__(self):

        load_dotenv()
        self.report_id=datetime.now().strftime("d_%d_%m_%Y_t_%H_%M_%S")

        self.start_time=time.time()
        self.prev_time=self.start_time

        self.target_map_list={
                "vehicle":['car', 'truck'],
                "person":['person'],
                "bike":['bicycle']
                } #list of obj to detect. mapped to our own classifications

        self.max_captured_stuff={}
        
        self.telegramBot=TelegramBot(
            token = os.environ['TOKEN'],
            channel_id=os.environ['CHANNEL_ID']
        )

        self.img_path=f'captured_vechicle/{self.report_id}_{len(self.telegramBot.imgList)}.jpg'
        self.text=''
    
    def __del__(self):
        del self.start_time
        del self.prev_time
        del self.max_captured_stuff

        # del self.telegramBot



    def step(self, detected_obj, img):
        if sum(detected_obj.values())>0:

            if (time.time()-self.start_time>10 or len(self.telegramBot.imgList)>5):
                self.telegramBot.sendImgList()
                return False
            elif(time.time()-self.prev_time>0.5):
                self.update_max_captured_stuff_obj(detected_obj)
                self.update_text()
                self.update_img_path()
                if not cv2.imwrite(self.img_path, img*255):
                    raise Exception("Could not write image")
                self.telegramBot.addImg(img_path=self.img_path,text=self.text)
                os.remove(self.img_path)
                self.prev_time=time.time()
                return True


    def update_max_captured_stuff_obj(self, detected_obj):
        # Updates both 1) self.max_captured_stuff
        # Example
        # detected_obj={'person': 1, 'car':3}# 1 person and 3 cars detected
        captured_stuff={}
        for detection in detected_obj:
            for key in self.target_map_list.keys():
                if detection in self.target_map_list[key]:
                    print(detected_obj)
                    if key in captured_stuff:
                        captured_stuff[key]=captured_stuff[key]+detected_obj[detection]
                    else:
                        captured_stuff[key]=detected_obj[detection]
    
        for key in captured_stuff:
            if key in self.max_captured_stuff:
                self.max_captured_stuff[key]=max(self.max_captured_stuff[key],captured_stuff[key])
            else:
                self.max_captured_stuff[key]=captured_stuff[key]

    def update_text(self):
        self.text=''
        for key in self.max_captured_stuff: 
            self.text+=f'max {key} detected: {self.max_captured_stuff[key]}\n' 
        
    def update_img_path(self):
        self.img_path=f'captured_vechicle/{self.report_id}_{len(self.telegramBot.imgList)}.jpg'
    