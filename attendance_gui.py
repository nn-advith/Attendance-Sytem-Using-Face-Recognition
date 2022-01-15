import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import face_recognition
import os
from datetime import datetime
import numpy as np
from batchResize import resize

students = {
    '1MS19CS042': 'Deepthi Peter',
    '1MS19CS046': 'Goutham Suresh',
    '1MS19CS064': 'Maan Ali Ba Fayadh',
    '1MS19CS067': 'ManojBP',
    '1MS19CS077': 'N N Advith',
    '1MS19CS082': 'Neha N Murthy',
    '1MS19CS090': 'Praneeth Shetty',
    '1MS19CS111': 'Sharath H',
    '1MS19CS134': 'Trishi T',
    '1MS19CS149': 'Gosu Dileep Reddy',
    '1MS20CS408': 'Pavan Kerakalamatti',
    '1MS20CS411': 'Vikramaditya',
    '1MS19CV067': 'Mohd Khan',
    '1MS19CV111': 'Siddharth Singh',
    '1MS19CV128': 'Yash Asthana',
    '1MS20EE405': 'Vinod R',
    '1MS19EI012': 'Bhuvana B M',
    '1MS19EI033': 'M Ponni',
    '1MS19EI046': 'Sachin Kudlagi',
    '1MS19EI065': 'Deepak Joshi',
    '1MS20EI404': 'Pavithra M N',
    '1MS20EI405': 'Soumya A',
    '1MS20IM404': 'Nikhil M',
    '1MS18IS052': 'Mohammad Akhtar',
    '1MS19IS029': 'Bhuvan M',
    '1MS19IS033': 'Chandana Tanikella',
    '1MS19IS054': 'Jitesh Kamnani',
    '1MS19IS093': 'Pranay Kumar Andra',
    '1MS19IS118': 'Spoorthi Mohan Naik',
    '1MS18ME013': 'Akaash Kulkarni',
    '1MS19ME116': 'Nitish Kumar R',
    '1MS19ME136': 'R Sumanth',
    '1MS19ME145': 'S Anand',
    '1MS19ME185': 'Tathagat Raj',
    '1MS19ME192': 'Vijey Shrinivas N',
    '1MS19ET032': 'Madhuri Prasad',
    '1MS19ET042': 'R Kumar', }

path = 'resized'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
# strength = []
present = []
absent = []


class window(QWidget):
    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(10, 10, 700, 550)
        self.setWindowTitle("Attendance")
        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        self.label.setText("Attendance using Face Recgnition")
        self.label.setFont(QFont('Arial', 20))
        self.present = QLabel(self)
        self.present.setText("Present")
        self.present.setFont(QFont('Arial', 16))
        self.absent = QLabel(self)
        self.absent.setText("Absent")
        self.absent.setFont(QFont('Arial', 16))
        self.b1 = QPushButton(self)
        self.b1.setText("Add Photo")
        self.b1.clicked.connect(self.deleteNames)
        self.b1.clicked.connect(self.loadImage)
        self.image_frame = QLabel()
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        hSpacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        vbox1 = QVBoxLayout()
        self.vbox2 = QVBoxLayout()
        self.vbox3 = QVBoxLayout()

        self.vbox2.addWidget(self.present)
        self.vbox3.addWidget(self.absent)

        hbox = QHBoxLayout()
        hbox1 = QHBoxLayout()
        hbox.addWidget(self.b1)
        hbox.addItem(hSpacer)

        hbox1.addLayout(self.vbox2)
        hbox1.addItem(hSpacer)
        hbox1.addLayout(self.vbox3)
        hbox1.addItem(hSpacer)

        vbox1.addWidget(self.label)
        vbox1.addLayout(hbox)
        vbox1.addWidget(self.image_frame)
        vbox1.addItem(self.verticalSpacer)
        vbox1.addLayout(hbox1)
        vbox1.addItem(self.verticalSpacer)
        self.setLayout(vbox1)

    def loadImage(self):
        present = []
        absent = []
        self.fname = QFileDialog.getOpenFileName(self, 'Load Image', '/home/PycharmProjects/IP_FaceRec')
        # self.image = face_recognition.load_image_file(self.fname[0])
        self.image = cv2.imread(self.fname[0])
        self.image = cv2.resize(self.image, (500, 500), interpolation=cv2.INTER_AREA)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(self.image)
        encodeCurrame = face_recognition.face_encodings(self.image, faceCurFrame)

        for encodeFace, faceLoc in zip(encodeCurrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            facedis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(facedis)
            matchIndex = np.argmin(facedis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                # print(name)
                y1, x2, y2, x1 = faceLoc
                # y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(self.image, (x1, y1), (x2, y2), (255, 255, 0), 2)
                cv2.rectangle(self.image, (x1, y2 - 25), (x2, y2), (255, 255, 0), cv2.FILLED)
                cv2.putText(self.image, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (0, 0, 0), 2)
                # print(name)
                if name not in present:
                    present.append(name)
                markAttendance(name)

        for i in students.keys():
            if i not in present and i not in absent:
                absent.append(i)

        self.image = QImage(self.image.data, self.image.shape[1], self.image.shape[0],QImage.Format_RGB888)
        self.image_frame.setPixmap(QPixmap.fromImage(self.image))

        for i in present:
            self.pres = QLabel(self)
            self.pres.setText(i + "-" + students[i])
            self.vbox2.addWidget(self.pres)

        for i in absent:
            self.abs = QLabel(self)
            self.abs.setText(i + "-" + students[i])
            self.vbox3.addWidget(self.abs)

        self.vbox2.addItem(self.verticalSpacer)
        self.vbox3.addItem(self.verticalSpacer)

    def deleteNames(self):
        i = 1
        while self.vbox2.itemAt(i):
            try:
                self.vbox2.itemAt(i).widget().deleteLater()
            except:
                i = i + 1
                pass
            i = i + 1
        i = 1
        while self.vbox3.itemAt(i):
            try:
                self.vbox3.itemAt(i).widget().deleteLater()
            except:
                i = i + 1
                pass
            i = i + 1


def main():
    app = QApplication(sys.argv)
    ex = window()
    ex.show()
    sys.exit(app.exec_())


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
        except:
            pass
        encodeList.append(encode)


    return encodeList


def markAttendance(name):
    with open('attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            date = datetime.now().date()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{students[name]},{date}, {dtString}')


def getNames():
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    # print(classNames)


if __name__ == '__main__':
    resize()
    getNames()
    encodeListKnown = findEncodings(images)
    print('Encoding Complete...')
    main()