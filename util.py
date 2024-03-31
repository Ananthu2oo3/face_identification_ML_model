import cv2
import pywt  
import pickle
import numpy as np

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
    
    normal_img      = cv2.imread(img)
    normal_scal     = cv2.resize(normal_img, (32, 32))  
    
    discret_img     = w2d(normal_img, 'db1', 5)  
    discret_img     = cv2.cvtColor(discret_img, cv2.COLOR_RGBA2RGB) if discret_img.shape[2] == 4 else discret_img[:, :, :3]  
    
    discret_scal    = cv2.resize(discret_img, (32, 32))
    combined_img    = np.vstack((normal_scal.reshape(32*32*3, 1), discret_scal.reshape(32*32*3, 1)))

    return combined_img


def predict(img):

    with open('model.pkl', 'rb') as file:  
        model   = pickle.load(file)
        predict = model.predict(img)
        return predict