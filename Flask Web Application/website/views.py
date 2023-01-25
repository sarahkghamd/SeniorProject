from flask import Blueprint, render_template
from flask_login import login_required, current_user
import cv2
from deepface import DeepFace
from PIL import Image,ImageOps
import pickle
import numpy as np
from keras.models import Model
from .models import InterviewVideo,InterviewFrames


views = Blueprint('views', __name__)

@views.route('/')
@login_required #so you can not get to the home page unless you login
def home():
    return render_template("home.html", user=current_user)

def videoToframes(file):
    cap = cv2.VideoCapture(file)
    i = 1
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        if i % 1800 == 0:
            cv2.imwrite('interview/'+str(i)+'.jpg',frame)
            frame= InterviewFrames()
            break
        i += 1
    cap.release()
    cv2.destroyAllWindows()
    
def prediction(data_image):
    facenet_model= DeepFace.build_model('Facenet')
    facenet_model.load_weights('static/facenet_weights.h5');
    facenet_ext = Model(inputs=facenet_model.input, outputs=facenet_model.get_layer('Mixed_7a').output)
    model = pickle.load(open('static/INT_Model_1.pkl', 'rb'))

    image = data_image # From database
    image = Image.fromarray(image)  

    # Fit to the model
    img_dim = (160,160);
    image = ImageOps.fit(image,(img_dim[0],img_dim[1]),Image.ANTIALIAS,centering=(0.5, 0.5));
    image = np.array(image).reshape(img_dim[1],img_dim[0],3) 
    X = [];
    X.append(image);
    X = np.array(X);

    res= facenet_ext.predict(X)

    pred=model.predict(res)
    return(pred)


