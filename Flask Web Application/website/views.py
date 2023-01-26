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

def videoToframes(interview_id):
    cap = cv2.VideoCapture('interviews/interview.webm')
    i = 1
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        if i % 1800 == 0:
            cv2.imwrite('interviews/'+str(interview_id)+'.jpg',frame)
          #  frame= InterviewFrames() #store in database
            break
        i += 1
    cap.release()
    cv2.destroyAllWindows()
    
def prediction(interview_id):
    facenet_model= DeepFace.build_model('Facenet')
    facenet_model.load_weights('facenet_weights.h5')
    facenet_ext = Model(inputs=facenet_model.input, outputs=facenet_model.get_layer('Mixed_7a').output)
    model = pickle.load(pickle.read('INT_Model_1.pkl', 'rb'))

    #image = data_image # From database
    image = Image.fromarray('interviews/'+str(interview_id)+'.jpg')  

    # Fit to the model
    img_dim = (160,160)
    image = ImageOps.fit(image,(img_dim[0],img_dim[1]),Image.ANTIALIAS,centering=(0.5, 0.5));
    image = np.array(image).reshape(img_dim[1],img_dim[0],3) 
    X = [];
    X.append(image)
    X = np.array(X)

    res= facenet_ext.predict(X)

    pred=model.predict(res)
    return(pred)
