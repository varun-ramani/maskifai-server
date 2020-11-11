import cv2
import numpy as np
from keras.models import load_model

model = load_model("model2-002.model")

labels_dict = {0: 'without',
               1: 'with'}

color_dict = {0: (0, 0, 255),
              1: (0, 255, 0)}

size = 4
classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def classifybytes(imagedata):
    # Turn the image into a format that we can use with OpenCV
    image_array = np.frombuffer(imagedata, np.uint8)
    im = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Flip the image
    im = cv2.flip(im, 1, 1)

    # Resize the image to speed up detection
    mini = cv2.resize(im, (im.shape[1] // size, im.shape[0] // size))

    faces = classifier.detectMultiScale(mini)

    results = []

    for face in faces:
        (x, y, w, h) = [v * size for v in face]

        face_img = im[y:y+h, x:x+w]
        resized = cv2.resize(face_img, (150, 150))
        normalized = resized/255.0
        reshaped = np.reshape(normalized, (1, 150, 150, 3))
        reshaped = np.vstack([reshaped])
        result = np.argmax(model.predict(reshaped))

        results.append(result)

    return results


classifier_history = []
lock_status = False


def feed_image(imagedata):
    # If this method returns true, then enough images have been classified
    # in order to make decisions about locking and unlocking.
    classifier_history.append(classifybytes(imagedata))

    if len(classifier_history) < 6:
        return False

    classifier_history.pop(0)
    return True


def should_lock():
    for result in classifier_history:
        if 0 not in result:
            return False

    return True


def should_unlock():
    for result in classifier_history:
        if 0 in result:
            return False

    return True