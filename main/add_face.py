import os
import cv2
from PIL import Image, ImageTk
import numpy as np
import db

def makeDir():
    if not os.path.exists("face_trainer"):
        os.mkdir("face_trainer")
    if not os.path.exists("FaceData"):
        os.mkdir("FaceData")


def getFace(name):
    cap = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    count = 0
    while True:
        sucess, img = cap.read()  # 从摄像头读取图片
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0))
            count += 1
            cv2.imwrite("FaceData/User." + name.get() +'.' + str(count) + '.jpg', gray[y: y + h, x: x + w])
            cv2.imshow('image', img)
        # 保持画面的持续。
        k = cv2.waitKey(1)
        if k == 27:   # 通过esc键退出摄像
            break
        elif count >= 13:  # 得到1000个样本后退出摄像
            break
    cap.release()
    cv2.destroyAllWindows()


def getImagesAndLabels(path,detector, usernames):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')
            username = os.path.split(imagePath)[-1].split(".")[1]
            id = 1
            for x in usernames:
                if username == x:
                    break
                else:
                    id += 1

            faces = detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x: x + w])
                ids.append(id)
        return faceSamples, ids


def trainFace(names):
    # 人脸数据路径
    path = 'FaceData'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces, ids = getImagesAndLabels(path, detector, names)
    recognizer.train(faces, np.array(ids))
    recognizer.write(r'face_trainer\trainer.yml')


def add_face(name, names):
    makeDir()
    getFace(name)

    trainFace(names)
    user = db.record()
    user.insert_name(name.get())