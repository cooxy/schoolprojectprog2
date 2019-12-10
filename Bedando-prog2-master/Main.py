from PyQt5 import QtCore, QtGui, QtWidgets
from gameDialog import GameWindow


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(405, 149)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 20, 71, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 50, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 80, 81, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(130, 20, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(130, 50, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(130, 80, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 22, 75, 71))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 405, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)                                  #meghívja az átírást
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.startGame)                 #startgomb megnyomásával elindítja a játékot

    def retranslateUi(self, MainWindow):                                #átírja a neveket
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ötödölő"))
        self.label.setText(_translate("MainWindow", "Tábla méret:"))
        self.label_2.setText(_translate("MainWindow", "Játékos 1 neve:"))
        self.label_3.setText(_translate("MainWindow", "Játékos 2 neve:"))
        self.pushButton.setText(_translate("MainWindow", "START"))

    def startGame(self):
        messageBox = QtWidgets.QMessageBox()
        if not self.lineEdit.text().isdigit():                          #ha nem szánot ír be méretnek
            messageBox.setWindowTitle("ERROR")
            messageBox.setText("A méretnek számnak kell lennie!")
            messageBox.exec()
        elif int(self.lineEdit.text()) < 5 or int(self.lineEdit.text()) > 50:       #a méretnek 5 és 50 közöttinek kell lennie
            messageBox.setWindowTitle("ERROR")
            messageBox.setText("A méretnek 5 és 50 között kell lennie!")
            messageBox.exec()
        elif self.lineEdit_2.text() == "" or self.lineEdit_3.text() == "":          #ha nem ad meg játékos nevet
            messageBox.setWindowTitle("ERROR")
            messageBox.setText("A Játékos név mezők nem lehetnek üresek!")
            messageBox.exec()
        else:
            self.gameWindow = QtWidgets.QMainWindow()
            self.game = GameWindow()
            self.game.setupUi(self.gameWindow, int(self.lineEdit.text()), self.lineEdit_2.text(), self.lineEdit_3.text())
            self.gameWindow.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
