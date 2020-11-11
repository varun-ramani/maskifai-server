import cv2
import numpy as np
from keras.models import load_model
import time
model=load_model("../model2-001.model")

labels_dict={0:'without mask',1:'mask'}
color_dict={0:(0,0,255),1:(0,255,0)}

size = 4
# webcam = cv2.VideoCapture(0) #Use camera 0

# We load the xml file
classifier = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')

write = False # whether or not to write to a file (for testing purposes)

def test(data):
    t = time.time()
    # convert the raw image data to a cv2 image
    arr = np.fromstring(data, dtype='uint8')
    im = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    im = cv2.rotate(im, cv2.ROTATE_90_CLOCKWISE)
    
    # Resize the image to speed up detection
    mini = cv2.resize(im, (im.shape[1] // size, im.shape[0] // size))

    # detect MultiScale / faces
    faces = classifier.detectMultiScale(mini)

    faces = {}
    
    # Draw rectangles around each face
    for idx, f in enumerate(faces):
        (x, y, w, h) = [v * size for v in f] #Scale the shapesize backup
        #Save just the rectangle faces in SubRecFaces
        face_img = im[y:y+h, x:x+w]
        resized=cv2.resize(face_img,(150,150))
        normalized=resized/255.0
        reshaped=np.reshape(normalized,(1,150,150,3))
        reshaped = np.vstack([reshaped])
        result=model.predict(reshaped)
        #print(result)

        label=np.argmax(result,axis=1)[0]

        labels.append(label)

        faces[f'face_{idx}'] = {'rect': f, 'label': label}

        # add a rectangle (todo: send this back to maskif?)
        if write:
            cv2.rectangle(im,(x,y),(x+w,y+h),color_dict[label],2)
            cv2.rectangle(im,(x,y-40),(x+w,y),color_dict[label],-1)
            cv2.putText(im, labels_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

    if write: cv2.imwrite('received'+str(t)+'.png', im)

    # print('processed', time.time() - t)
    return faces
