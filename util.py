import cv2
import pywt  
import pickle
import joblib
import numpy as np


def haar_cascade(img):
    
    face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(img,1.3,5)
    
    (x,y,w,h) = faces[0]
    face_img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_color = face_img[y:y+h,x:x+w]

    return roi_color



def w2d(img, mode='haar', level=1):

    img_array = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img_array = np.float32(img_array)

    height, width, channels = img.shape
    img_array /= height

    coeffs          = pywt.wavedec2(img_array, mode, level)
    coeffs_list     = list(coeffs)
    coeffs_list[0] *= 0  

    img_array_h  = pywt.waverec2(coeffs_list, mode)
    img_array_h *= 255
    img_array_h  = np.uint8(img_array_h)

    return img_array_h


def stack(img):
    normal_scal = cv2.resize(img, (32, 32))

    discret_img = w2d(img, 'db1', 5)
    discret_img = cv2.cvtColor(discret_img, cv2.COLOR_RGBA2RGB) if discret_img.shape[2] == 4 else discret_img[:, :, :3]

    discret_scal = cv2.resize(discret_img, (32, 32))
    
    normal_scal_flat = normal_scal.flatten()
    discret_scal_flat = discret_scal.flatten()
    
    combined_img = np.hstack((normal_scal_flat, discret_scal_flat))

    return combined_img


def predict(img):
        
    loaded_model = joblib.load('model.pkl')

    predictions = loaded_model.predict(img.reshape(1, -1))
    probability = loaded_model.predict_proba(img.reshape(1, -1))
    
    
    return probability[0]