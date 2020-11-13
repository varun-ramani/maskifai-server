import cv2
import numpy as np
from keras.models import load_model

model = load_model("model2-009.model")

labels_dict = {0: 'without',
               1: 'with'}

color_dict = {0: (0, 0, 255),
              1: (0, 255, 0)}

size = 4
classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def classify(image):
    # Flip the image
    im = cv2.flip(image, 1, 1)

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


def classifybytes(imagedata):
    # Turn the image into a format that we can use with OpenCV
    image_array = np.frombuffer(imagedata, np.uint8)
    im = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    return classify(im)


classifier_history = []
lock_status = False


def feed_image(imagedata):
    global classifier_history

    # If this method returns true, then enough images have been classified
    # in order to make decisions about locking and unlocking.
    classifier_history.append(classify(imagedata))

    if len(classifier_history) < 12:
        return False

    classifier_history.pop(0)

    print(classifier_history)
    return True


def count_frames_without_mask():
    global classifier_history

    num_without = 0
    for result in classifier_history:
        if 0 in result:
            num_without += 1

    return num_without


def should_lock():
    return count_frames_without_mask() > 8

def should_unlock():
    return not should_lock()