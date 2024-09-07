import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QDesktopWidget, QPushButton, QVBoxLayout, QWidget, QDockWidget
from PyQt5.QtCore import QBasicTimer, Qt
from PyQt5.QtGui import QPainter, QColor

class IlonOyin(QFrame):
    """Ilon oyini wasd yoki <>^V tugmalari bilan ishlatish mumkun"""
    ENI = 300
    BALANDLIGI = 300
    BO_LAK = 10
    MAX_RAND_POS = 27

    def __init__(self):
        super().__init__()
        self.setFixedSize(300,300)
        self.setFocusPolicy(Qt.StrongFocus)  
        self.oyin_boshlash()

    def oyin_boshlash(self):
        self.timer = QBasicTimer()
        self.ilon = [[100, 100], [90, 100], [80, 100]]
        self.yonalish = Qt.Key_Right
        self.ovqat = [self.tasodifiy_joy(), self.tasodifiy_joy()]
        self.oyin_holat = True
        self.timer.start(100, self)

    def oyin_tugatish(self):
        quit()

    def tasodifiy_joy(self):
        return random.randint(0, self.MAX_RAND_POS) * self.BO_LAK

    def paintEvent(self, event):
        qp = QPainter(self)
        if self.oyin_holat:
            self.oyin_chizish(qp)
        else:
            self.oyin_yakun(qp)

    def oyin_chizish(self, qp):
        qp.setBrush(QColor(255, 0, 0))
        qp.drawRect(self.ovqat[0], self.ovqat[1], self.BO_LAK, self.BO_LAK)
        for pos in self.ilon:
            qp.setBrush(QColor(0, 255, 0))
            qp.drawRect(pos[0], pos[1], self.BO_LAK, self.BO_LAK)

    def oyin_yakun(self, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(self.font())
        qp.drawText(self.rect(), Qt.AlignCenter, "O'yin tugadi")

    def keyPressEvent(self, event):
        tugma = event.key()
        if tugma == Qt.Key_Left and self.yonalish != Qt.Key_Right or tugma == Qt.Key_A and self.yonalish != Qt.Key_D:
            self.yonalish = Qt.Key_Left
        elif tugma == Qt.Key_Right and self.yonalish != Qt.Key_Left or tugma == Qt.Key_D and self.yonalish != Qt.Key_A:
            self.yonalish = Qt.Key_Right
        elif tugma == Qt.Key_Up and self.yonalish != Qt.Key_Down or tugma == Qt.Key_W and self.yonalish != Qt.Key_S:
            self.yonalish = Qt.Key_Up
        elif tugma == Qt.Key_Down and self.yonalish != Qt.Key_Up or tugma == Qt.Key_S and self.yonalish != Qt.Key_W:
            self.yonalish = Qt.Key_Down

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.ilon_harakat()
        self.tekshiruv()
        self.repaint()

    def ilon_harakat(self):
        bosh = self.ilon[0][:]
        if self.yonalish == Qt.Key_Left:
            bosh[0] -= self.BO_LAK
        elif self.yonalish == Qt.Key_Right:
            bosh[0] += self.BO_LAK
        elif self.yonalish == Qt.Key_Up:
            bosh[1] -= self.BO_LAK
        elif self.yonalish == Qt.Key_Down:
            bosh[1] += self.BO_LAK
        self.ilon = [bosh] + self.ilon[:-1]
        if bosh == self.ovqat:
            self.ilon.append(self.ilon[-1])
            self.ovqat = [self.tasodifiy_joy(), self.tasodifiy_joy()]

    def tekshiruv(self):
        bosh = self.ilon[0]
        if bosh[0] < 0 or bosh[0] >= self.ENI or bosh[1] < 0 or bosh[1] >= self.BALANDLIGI:
            self.oyin_holat = False
        if bosh in self.ilon[1:]:
            self.oyin_holat = False

class IlonOyna(QMainWindow):
    def __init__(self):
        super().__init__()
        self.interfeys()

    def interfeys(self):
        self.ilonOyin = IlonOyin()

        self.markazlashtirish()
        self.setWindowTitle("Ilon O'yini")

        self.boshqaruvchi = QDockWidget()
        self.boshqaruvchi.setWindowTitle('Boshqaruv paneli')

        self.panelWidget = QWidget()
        self.layout = QVBoxLayout()

        
        self.startButton = QPushButton("O'yinni boshlash")
        self.stopButton = QPushButton("O'yinni tugatish")


        self.startButton.clicked.connect(self.ilonOyin.oyin_boshlash)
        self.stopButton.clicked.connect(self.ilonOyin.oyin_tugatish)

  
        self.layout.addWidget(self.startButton)
        self.layout.addWidget(self.stopButton)

        self.panelWidget.setLayout(self.layout)
        self.boshqaruvchi.setWidget(self.panelWidget)
        self.boshqaruvchi.setFixedHeight(100)   


        self.setCentralWidget(self.ilonOyin)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.boshqaruvchi)

        self.show()

    def markazlashtirish(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    ilova = QApplication(sys.argv)
    oyna = IlonOyna()
    sys.exit(ilova.exec_())

