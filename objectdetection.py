import numpy as np
import os
import cv2
import json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from keras.applications.vgg16 import preprocess_input, decode_predictions
from glob import glob

model = load_model('vgg16Model.h5')

class ObjectDetection(object):
    
    def __init__(self):
        self.objects = []
        
    def to_frames(self, video_upload):
        cap = cv2.VideoCapture(video_upload)
        if not os.path.exists('data'):
            os.makedirs('data')
        count = 0
        while(True):
          ret, frame = cap.read()
          if not ret: 
                break
          if cv2.waitKey(1) & 0xFF == ord('q'):
            break
          name = 'static/video_frames/' + 'raw' + str(count) + '.jpg'
       
          cv2.imwrite(name, frame)
          count += 1
      
    def detect_object(self):
        for item in self.get_frames():  
            image = load_img(item, target_size=(224, 224))
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image = preprocess_input(image)
            y_pred = model.predict(image)
            label = decode_predictions(y_pred)
            self.objects.append(label[0][1][1])
        with open('detected_objects.txt', 'w') as f:
            f.write(json.dumps(self.objects))
            
    def get_objects(self):
        return self.objects
    
    def get_frames(self):
        FRAMES_ARR =  glob("static/video_frames/*.jpg")
        return FRAMES_ARR
    
    def search_for(self, _object):
        with open('detected_objects.txt', 'r') as f:
            objects = list(json.loads(f.read()))
        results = []
        if _object in set(objects):
            for i in range(len(objects)):
                if _object.__eq__(objects[i]):
                    frame_path = self.get_frames()[i]
                    frame_path = frame_path.split('\\')[1]
                    results.append(frame_path)
        else:
            return "no file seen in this query"
        return results