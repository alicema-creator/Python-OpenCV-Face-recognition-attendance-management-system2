from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
import tkinter
import cv2
import time
import db

def set_win_center(root, curWidth='', curHight=''):
    '''
    设置窗口大小，并居中显示
    :param root:主窗体实例
    :param curWidth:窗口宽度，非必填，默认200
    :param curHight:窗口高度，非必填，默认200
    :return:无
    '''
    if not curWidth:
        '''获取窗口宽度，默认200'''
        curWidth = root.winfo_width()
    if not curHight:
        '''获取窗口高度，默认200'''
        curHight = root.winfo_height()
    # print(curWidth, curHight)

    # 获取屏幕宽度和高度
    scn_w, scn_h = root.maxsize()
    # print(scn_w, scn_h)

    # 计算中心坐标
    cen_x = (scn_w - curWidth) / 2
    cen_y = (scn_h - curHight) / 2
    # print(cen_x, cen_y)

    # 设置窗口初始大小和位置
    size_xy = '%dx%d+%d+%d' % (curWidth, curHight, cen_x, cen_y)
    root.geometry(size_xy)

def check( names):
    cam = cv2.VideoCapture(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('face_trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            if confidence < 70:
                username = names[idnum-1]
                confidence = "{0}%".format(round(100 - confidence))


                cv2.putText(img, str(username), (x + 5, y - 5), font, 1, (0, 0, 255), 1)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 0), 1)
                cv2.imshow('camera', img)
                time.sleep(2)

                while True:
                    db.record().insert_record(username)  # 签到信息插入数据库
                    cam.release()
                    cv2.destroyAllWindows()

                    root = Tk()
                    root.title('检测结果')
                    root.update()  # 必须
                    set_win_center(root, 300, 200)
                    ft2 = tkFont.Font(family='Microsoft YaHei', size=18, weight=tkFont.BOLD, underline=0, overstrike=0)
                    Label(root, text=('检测通过'), font=ft2).pack(padx=0,pady=60)

                    root.mainloop()     


                return
            else:

                idnum = "unknown"
                confidence = "{0}%".format(round(100 - confidence))
                cv2.putText(img, str(idnum), (x + 5, y - 5), font, 1, (0, 0, 255), 1)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 0), 1)

                '''
                root = Tk()
                root.title('检测结果')
                root.update()  # 必须
                set_win_center(root, 300, 200)
                ft2 = tkFont.Font(family='Microsoft YaHei', size=18, weight=tkFont.BOLD, underline=0, overstrike=0)
                Label(root, text=('检测不通过'), font=ft2).pack(padx=0,pady=30)

                btn3 = tkinter.Button(root, text='退出',font = ('microsoft yahei',14,''),width=10,height=2, command=root.quit).pack(padx=0,pady=0)

                root.mainloop() 
                '''


        cv2.imshow('camera', img)
        '''
        k = cv2.waitKey(10)
        if k == 27:
            break
        '''
        if cv2.waitKey(10) == ord('e'):
            break       
        


    cam.release()
    cv2.destroyAllWindows()



 