from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from functools import partial


class GameWindow(object):
    def setupUi(self, MainWindow, size, playerOne, playerTwo):
        MainWindow.setObjectName("MainWindow")
        self.gridSize = 600                                         #a pálya mérete
        self.size = size
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        MainWindow.resize(self.gridSize + 20, self.gridSize + 110)  #a pályamérethez igazodik az ablak mérete
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QRect(10 + (self.gridSize % self.size) / 2, 10, self.gridSize, self.gridSize))        #pálya középreigazítása az ablakon
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setSpacing(0)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setGeometry(QRect(40, self.gridSize + 30, 47, 13))
        self.label_4.setObjectName("label_4")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setGeometry(QRect(20, self.gridSize + 30, 16, 13))
        self.label_3.setObjectName("label_3")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QRect(20, self.gridSize + 60, 16, 13))
        self.label_2.setObjectName("label_2")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(40, self.gridSize + 60, 47, 13))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 540, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        self.current_turn = 1                                                               #megadja, hogy épp melyik játékos következik(1 és -1 között vátakozik)
        self.positions = [[0 for i in range(self.size)] for j in range(self.size)]          #a megadott mérethez igazodva csinál rgy mátrixot
        self.gombok = []                                                                    #pushbutton lista
        self.maxMarks = self.size ** 2                                                      #max ennyi lépés van
        self.currentMarks = 0                                                               #számolja, hogy eddig hány lépés volt
        self.gameEnded = False                                                              #ha True akkor vége a játéknak
        self.label_4.setText(self.playerOne)                                                #alulra labelbe írja az 1. játékos nevét
        self.label_4.setStyleSheet("color: red")                                 #pirosra színezi az 1. játékos nevét, mivel piros színnel jelzi, hogy éppen ki jön
        self.label.setText(self.playerTwo)                                                  #a 2. játékos neve
        self.setupTable()

    def retranslateUi(self, MainWindow):                                                    #átnevezi a labeleket
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ötödölő"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "X - "))
        self.label_2.setText(_translate("MainWindow", "O - "))
        self.label.setText(_translate("MainWindow", "TextLabel"))

    def setupTable(self):
        for i in range(self.size):
            for j in range(self.size):
                widget = QPushButton()
                widget.setFixedSize(QSize(self.gridSize / self.size, self.gridSize / self.size))        #a pushbuttonokat méretezi, hogy kitöltsék a pályát
                font = QFont()
                font.setPointSize(self.gridSize / self.size)                #a betűméretet átállítja
                widget.setFont(font)
                widget.clicked.connect(partial(self.putMark, widget))       #függvény nem hívható --> referenciát adunk át
                widget.setStyleSheet("background-color: red; border: 1px solid black")      #a pushbuttonok színét és a határaik színét állítja át
                self.gombok.append(widget)                          #a gombok listához hozzáadja a push buttonokat
                self.gridLayout.addWidget(widget, i, j)             #gombok megjelenítése a játékteren (gridlayouton)

    def clear(self):
        self.positions = [[0 for i in range(self.size)] for j in range(self.size)]      #az összes pozíciót visszaállítja 0-ra
        for i in range(self.gridLayout.count()):                                        #végigmegy az összes push buttonon?????
            self.gridLayout.itemAt(i).widget().setText("")                              #a text-jét visszaállítja ""-re
        self.gameEndDialog.accept()                                                     #????????????????????????
        msgBox = QMessageBox()                                                          #ablakban kiírja, hogy új játék kezdődött
        msgBox.setText("Új játék kezdődött!")
        msgBox.setWindowTitle("INFO")
        msgBox.exec()
        self.currentMarks = 0                                                           #lenullázza a jelenlegi lépések számát
        self.current_turn *= -1                                                         #a vesztes következik
        self.gameEnded = False

    def putMark(self, button):
        index = self.gombok.index(button)                       #indexeli a pushbuttonokat
        x = index // self.size                                  #egész osztással megkapjuk a vízszintes sorokat
        y = index % self.size                                   #maradékos osztással megkapjuk a függőleges oszlopokat
        if not self.gameEnded:                                  #ha nincs vége a játéknak
            if self.positions[x][y] == 0:                       #ha az x és y indexű pushbutton 0 értékű
                if self.current_turn == 1:                      #ha az 1. játékos jön
                    self.positions[x][y] = self.current_turn    #az x és y indexű pushbuttont 1-re írja át
                    self.gombok[index].setText("X")             #a pushbutton text-jét X-re átírja
                    self.label_4.setStyleSheet("color: black")  #az 1. játékos nevét feketére változtatja
                    self.label.setStyleSheet("color: red")      #a 2. játékos nevét pirosra változtatja
                    if self.checkWin(x, y):                     #leellenőrzi, hogy nyert-e az 1. játékos
                        msgBox = QMessageBox()
                        msgBox.setText("A nyertes játékos '{}' játékos!".format(self.playerOne))    #kiírja az első játékos nevét egy új ablakban, hogy nyert
                        msgBox.setWindowTitle("INFO")
                        msgBox.exec()
                        self.gameEnded = True
                        self.gameEndingDialog()
                        self.saveData()                 #elmenti a játékot
                        return
                    self.current_turn *= -1             #ha nem nyert az 1. játékos, akkor -1 állítja a self.current_turn-t, hogy a 2. játékos jöhessen
                    self.currentMarks += 1              #az lépések száma 1-el növekszik
                    if self.noMoreMoves():              #ha nincs több lépés
                        msgBox = QMessageBox()
                        msgBox.setText("Döntetlen!")    #döntetlent ír ki
                        msgBox.setWindowTitle("INFO")
                        msgBox.exec()
                        self.gameEndingDialog()         #szeretne-e új játékot játszani?
                elif self.current_turn == -1:           #ha a 2. játékos jön
                    self.positions[x][y] = self.current_turn    #az x és y indexű pushbuttont -1-re írja át
                    self.gombok[index].setText("O")             #a pushbutton text-jét X-re átírja
                    self.label.setStyleSheet("color: black")    #az 2. játékos nevét feketére változtatja
                    self.label_4.setStyleSheet("color: red")    #a 1. játékos nevét pirosra változtatja
                    if self.checkWin(x, y):         #leellenőrzi, hogy nyert-e az 2. játékos
                        msgBox = QMessageBox()
                        msgBox.setText("A nyertes játékos '{}' játékos!".format(self.playerTwo))    #kiírja a 2. játékos nevét
                        msgBox.setWindowTitle("INFO")
                        msgBox.exec()
                        self.gameEnded = True
                        self.gameEndingDialog()                     #szeretnél-e új játékot játszani?
                        self.saveData()                             #elmenti a játékot
                        return
                    self.current_turn *= -1             #ha nem nyert az 2. játékos, akkor -1 állítja a self.current_turn-t, hogy a 2. játékos jöhessen
                    self.currentMarks += 1              #az lépések száma 1-el növekszik
                    if self.noMoreMoves():              #ha nincs több lépés
                        msgBox = QMessageBox()
                        msgBox.setText("Döntetlen!")
                        msgBox.setWindowTitle("INFO")
                        msgBox.exec()
                        self.gameEndingDialog()         #szeretnél-e új játékot játszani?
            else:                               ##ha az x és y indexű pushbutton nem 0 értékű
                msgBox = QMessageBox()
                msgBox.setText("Ide nem rakható elem!")     #nem lehet ide rakni
                msgBox.setWindowTitle("HIBA")
                msgBox.exec()
        else:                           #ha vége a játéknak
            msgBox = QMessageBox()
            msgBox.setText("A játék véget ért!")    #játék vége
            msgBox.setWindowTitle("INFO")
            msgBox.exec()
            self.gameEndingDialog()             #szeretnél-e új játékot játszani?

    def saveData(self):
        file = open("data.txt", "a")                #megnyitja a data.txt-t
        winner = self.playerOne if self.current_turn == 1 else self.playerTwo   #a current_turn alapján megállapítja, hogy ki nyert
        winnersMark = 'X' if winner == self.playerOne else 'O'                  #megállapítja a győztes jelét
        file.write("Winner: {} - {}\n".format(winner, winnersMark))             #kiírja a játék menete fölé, hogy ki nyert és mivel volt
        for i in self.positions:
            for j in i:                                                         #végigmegy az összes pozíción
                if j == 0:                                                      #ha nem rakott senki se oda, akkor ponttal jelzi az eredményben
                    file.write('. ')
                elif j == 1:                                                    #az első játékos léőéseit X-el jelöli
                    file.write('X ')
                elif j == -1:                                                   #a második játékos léőéseit O-el jelöli
                    file.write('O ')
            file.write('\n')                                                    #a mátrix alakohoz kell
        file.write('\n')                                                        #két játék között legyen hely
        file.close()

    def noMoreMoves(self):
        if self.currentMarks >= self.maxMarks:              #ha eléri a max lépések számát a jelenlegi lépések száma
            self.gameEnded = True                           #játék vége
            return True
        return False                                        #ha nem éri el, akkor folytatódik

    def gameEndingDialog(self):                             #létrehoz egy új ablakot és megkérdezi, hogy akarunk-e új játékot játszani
        self.gameEndDialog = QDialog()
        self.gameEndDialog.setWindowTitle("Új játék")
        self.gameEndDialog.setGeometry(QRect(300, 300, 200, 70))
        self.gameEndLabel = QLabel(self.gameEndDialog)
        self.gameEndLabel.setText("A játék véget ért!\nSzeretne új játékot kezdeni?")
        self.gameEndLabel.move(10, 10)
        self.gameEndButtons = QDialogButtonBox(self.gameEndDialog)
        self.gameEndButtons.addButton("Igen", QDialogButtonBox.AcceptRole)
        self.gameEndButtons.accepted.connect(self.clear)
        self.gameEndButtons.addButton("Nem", QDialogButtonBox.RejectRole)
        self.gameEndButtons.rejected.connect(self.gameEndDialog.reject)
        self.gameEndButtons.move(10, 40)
        self.gameEndDialog.setModal(True)
        self.gameEndDialog.show()

    def checkWin(self, x, y):
        if self.checkWin1(x, y) or self.checkWin2(x, y) or self.checkWin3(x, y) or self.checkWin4(x, y) or self.checkWin5(x, y) or \
        self.checkWin6(x, y) or self.checkWin7(x, y) or self.checkWin8(x, y) or self.checkWin9(x, y) or self.checkWin10(x, y) or \
        self.checkWin11(x, y) or self.checkWin12(x, y) or self.checkWin13(x, y) or self.checkWin14(x, y) or self.checkWin15(x, y) or \
        self.checkWin16(x, y) or self.checkWin17(x, y) or self.checkWin18(x, y) or self.checkWin19(x, y) or self.checkWin20(x, y):
            return True
        return False

    def checkWin1(self, x, y):
        if x < 4 or y < 4:
            return False

        for i in range(5):
            if self.positions[x - i][y - i] != self.current_turn:
                return False
        return True

    def checkWin2(self, x, y):
        if x < 4 or y > self.size - 5:
            return False

        for i in range(5):
            if self.positions[x - i][y + i] != self.current_turn:
                return False
        return True

    def checkWin3(self, x, y):
        if x > self.size - 5 or y < 4:
            return False

        for i in range(5):
            if self.positions[x + i][y - i] != self.current_turn:
                return False
        return True

    def checkWin4(self, x, y):
        if x > self.size - 5 or y > self.size - 5:
            return False

        for i in range(5):
            if self.positions[x + i][y + i] != self.current_turn:
                return False
        return True

    def checkWin5(self, x, y):
        if x < 3 or y < 3 or x > self.size - 2 or y > self.size - 2:
            return False

        for i in range(4):
            if self.positions[x - i][y - i] != self.current_turn:
                return False
        if self.positions[x + 1][y + 1] != self.current_turn:
            return False
        return True

    def checkWin6(self, x, y):
        if x < 3 or y > self.size - 4 or x > self.size - 2 or y < 1:
            return False

        for i in range(4):
            if self.positions[x - i][y + i] != self.current_turn:
                return False
        if self.positions[x + 1][y - 1] != self.current_turn:
            return False
        return True

    def checkWin7(self, x, y):
        if x > self.size - 4 or y < 3 or x < 1 or y > self.size - 2:
            return False

        for i in range(4):
            if self.positions[x + i][y - i] != self.current_turn:
                return False
        if self.positions[x - 1][y + 1] != self.current_turn:
            return False
        return True

    def checkWin8(self, x, y):
        if x > self.size - 4 or y > self.size - 4 or x < 1 or y < 1:
            return False

        for i in range(4):
            if self.positions[x + i][y + i] != self.current_turn:
                return False
        if self.positions[x - 1][y - 1] != self.current_turn:
            return False
        return True

    def checkWin9(self, x, y):
        if x < 2 or y < 2 or x > self.size - 3 or y > self.size - 3:
            return False

        for i in range(3):
            if self.positions[x - i][y - i] != self.current_turn or self.positions[x + i][y + i] != self.current_turn:
                return False
        return True

    def checkWin10(self, x, y):
        if x < 2 or y < 2 or x > self.size - 3 or y > self.size - 3:
            return False

        for i in range(3):
            if self.positions[x + i][y - i] != self.current_turn or self.positions[x - i][y + i] != self.current_turn:
                return False
        return True

    def checkWin11(self, x, y):
        if x < 4:
            return False

        for i in range(5):
            if self.positions[x - i][y] != self.current_turn:
                return False
        return True

    def checkWin12(self, x, y):
        if y > self.size - 5:
            return False

        for i in range(5):
            if self.positions[x][y + i] != self.current_turn:
                return False
        return True

    def checkWin13(self, x, y):
        if x > self.size - 5:
            return False

        for i in range(5):
            if self.positions[x + i][y] != self.current_turn:
                return False
        return True

    def checkWin14(self, x, y):
        if y < 4:
            return False

        for i in range(5):
            if self.positions[x][y - i] != self.current_turn:
                return False
        return True

    def checkWin15(self, x, y):
        if x < 3 or x > self.size - 2:
            return False

        for i in range(4):
            if self.positions[x - i][y] != self.current_turn:
                return False
        if self.positions[x + 1][y] != self.current_turn:
            return False
        return True

    def checkWin16(self, x, y):
        if y < 1 or y > self.size - 4:
            return False

        for i in range(4):
            if self.positions[x][y + i] != self.current_turn:
                return False
        if self.positions[x][y - 1] != self.current_turn:
            return False
        return True

    def checkWin17(self, x, y):
        if x < 1 or x > self.size - 4:
            return False

        for i in range(4):
            if self.positions[x + i][y] != self.current_turn:
                return False
        if self.positions[x - 1][y] != self.current_turn:
            return False
        return True

    def checkWin18(self, x, y):
        if y < 3 or y > self.size - 2:
            return False

        for i in range(4):
            if self.positions[x][y - i] != self.current_turn:
                return False
        if self.positions[x][y + 1] != self.current_turn:
            return False
        return True

    def checkWin19(self, x, y):
        if x < 2 or x > self.size - 3:
            return False

        for i in range(3):
            if self.positions[x - i][y] != self.current_turn or self.positions[x + i][y] != self.current_turn:
                return False
        return True

    def checkWin20(self, x, y):
        if y < 2 or y > self.size - 3:
            return False

        for i in range(3):
            if self.positions[x][y - i] != self.current_turn or self.positions[x][y + i] != self.current_turn:
                return False
        return True
