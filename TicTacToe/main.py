import string

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon


class Ui_MainWindow(object):
    global current_player
    current_player = "x"

    global buttonFlags
    buttonFlags = ["-", "-", "-",
                   "-", "-", "-",
                   "-", "-", "-"]

    global winner
    winner = None

    global game_on
    game_on = True

    # Main Game logic
    def play_game(self, pos):
        _translate = QtCore.QCoreApplication.translate

        if game_on:
            self.handle_turn(pos)

            self.check_game_end()
            self.check_tie()

        # The game has ended
        if not game_on and winner is not None:
            self.message.setText(_translate("MainWindow", "Congratulations " + winner + "!"))
        elif not game_on and winner is None:
            self.message.setText(_translate("MainWindow", "It's a tie!"))

        self.flip_player(current_player)

    # Handle turns
    def handle_turn(self, pos):
        global current_player, buttonFlags

        buttons = [self.button_0, self.button_1, self.button_2, self.button_3,
                   self.button_4, self.button_5, self.button_6, self.button_7, self.button_8]

        _translate = QtCore.QCoreApplication.translate

        next_player = "o" if current_player == "x" else "x"

        self.message.setText(_translate("MainWindow", "It's " + next_player + "'s turn."))

        # Based on the current player, put the right icon on the board
        if current_player == "x" and buttonFlags[pos] == "-":
            buttons[pos].setIcon(QIcon("assets/x.png"))
            buttons[pos].setIconSize(QSize(55, 55))
            buttonFlags[pos] = current_player
        elif current_player == "o" and buttonFlags[pos] == "-":
            buttons[pos].setIcon(QIcon("assets/o.png"))
            buttons[pos].setIconSize(QSize(55, 55))
            buttonFlags[pos] = current_player
        else:
            self.message.setText(_translate("MainWindow", "Choose a free spot."))

    # Check if the game is over
    def check_game_end(self):
        global winner
        # check columns
        row_winner = self.check_rows()
        # check rows
        column_winner = self.check_columns()
        # check diagonals
        diagonal_winner = self.check_diagonals()
        if row_winner or column_winner or diagonal_winner:
            winner = current_player
        else:
            self.check_tie()
        return

    def check_rows(self):
        global game_on, current_player, buttonFlags

        # Check if we have 3 equal elements in a row
        row_1 = buttonFlags[0] == buttonFlags[1] == buttonFlags[2] != "-"
        row_2 = buttonFlags[3] == buttonFlags[4] == buttonFlags[5] != "-"
        row_3 = buttonFlags[6] == buttonFlags[7] == buttonFlags[8] != "-"

        if row_1 or row_2 or row_3:
            game_on = False

        if row_1:
            return buttonFlags[0]
        elif row_2:
            return buttonFlags[3]
        elif row_3:
            return buttonFlags[6]
        return

    def check_columns(self):
        global game_on, current_player, buttonFlags

        # Check if we have 3 equal elements in a column
        column_1 = buttonFlags[0] == buttonFlags[3] == buttonFlags[6] != "-"
        column_2 = buttonFlags[1] == buttonFlags[4] == buttonFlags[7] != "-"
        column_3 = buttonFlags[2] == buttonFlags[5] == buttonFlags[8] != "-"

        if column_1 or column_2 or column_3:
            game_on = False

        if column_1:
            return buttonFlags[0]
        elif column_2:
            return buttonFlags[1]
        elif column_3:
            return buttonFlags[2]
        return

    def check_diagonals(self):
        global game_on, current_player, buttonFlags

        # Check if we have 3 equal elements in a diagonal
        diagonal_1 = buttonFlags[0] == buttonFlags[4] == buttonFlags[8] != "-"
        diagonal_2 = buttonFlags[2] == buttonFlags[4] == buttonFlags[6] != "-"

        if diagonal_1 or diagonal_2:
            game_on = False

        if diagonal_1:
            return buttonFlags[0]
        elif diagonal_2:
            return buttonFlags[2]
        return

    # Check if it's a tie
    def check_tie(self):
        global game_on, buttonFlags
        if "-" not in buttonFlags:
            game_on = False
        return

    # Flip player
    def flip_player(self, player: string):
        global current_player
        current_player = "x" if player == "o" else "o"

    # Reset the game
    def clear_board(self):
        global buttonFlags, current_player, winner, game_on

        buttons = [self.button_0, self.button_1, self.button_2, self.button_3,
                   self.button_4, self.button_5, self.button_6, self.button_7, self.button_8]

        current_player = "x"
        buttonFlags = ["-", "-", "-",
                       "-", "-", "-",
                       "-", "-", "-"]

        winner = None
        game_on = True

        for button in buttons:
            button.setIcon(QIcon(None))

        _translate = QtCore.QCoreApplication.translate
        self.message.setText(_translate("MainWindow", "Make the first move."))

    # Setup the GUI
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(312, 380)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(35, 10, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Ink Free")
        font.setPointSize(23)
        self.title.setFont(font)
        self.title.setAutoFillBackground(False)
        self.title.setStyleSheet("color: white")
        self.title.setObjectName("title")
        self.message = QtWidgets.QLabel(self.centralwidget)
        self.message.setGeometry(QtCore.QRect(40, 320, 171, 21))
        self.message.setObjectName("message")
        font2 = QtGui.QFont()
        font2.setPointSize(14)
        self.message.setFont(font2)
        self.message.setStyleSheet("color: white")

        # Restart game
        self.clear = QtWidgets.QPushButton(self.centralwidget)
        self.clear.setGeometry(QtCore.QRect(220, 310, 61, 41))
        self.clear.setObjectName("clear")
        self.clear.setIcon(QIcon("assets/reset.png"))
        self.clear.setIconSize(QSize(40, 40))
        self.clear.clicked.connect(lambda: self.clear_board())

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 60, 251, 239))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        # Button 1
        self.button_0 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.button_0.setMinimumSize(QtCore.QSize(55, 75))
        self.button_0.setObjectName("button_0")
        self.button_0.clicked.connect(lambda: self.play_game(0))
        self.gridLayout.addWidget(self.button_0, 0, 0, 1, 1)

        # Button 2
        self.button_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.button_1.setMinimumSize(QtCore.QSize(55, 75))
        self.button_1.setObjectName("button_1")
        self.button_1.clicked.connect(lambda: self.play_game(1))
        self.gridLayout.addWidget(self.button_1, 0, 1, 1, 1)

        # Button 3
        self.button_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.button_2.setMinimumSize(QtCore.QSize(55, 75))
        self.button_2.setObjectName("button_2")
        self.button_2.clicked.connect(lambda: self.play_game(2))
        self.gridLayout.addWidget(self.button_2, 0, 2, 1, 1)

        # Button 4
        self.button_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.button_3.setMinimumSize(QtCore.QSize(55, 75))
        self.button_3.setObjectName("button_3")
        self.button_3.clicked.connect(lambda: self.play_game(3))
        self.gridLayout.addWidget(self.button_3, 1, 0, 1, 1)

        # Button 5
        self.button_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.button_4.setMinimumSize(QtCore.QSize(55, 75))
        self.button_4.setObjectName("button_4")
        self.button_4.clicked.connect(lambda: self.play_game(4))
        self.gridLayout.addWidget(self.button_4, 1, 1, 1, 1)

        # Button 6
        self.button_5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.button_5.setMinimumSize(QtCore.QSize(55, 75))
        self.button_5.setObjectName("button_5")
        self.button_5.clicked.connect(lambda: self.play_game(5))
        self.gridLayout.addWidget(self.button_5, 1, 2, 1, 1)

        # Button 7
        self.button_6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.button_6.setMinimumSize(QtCore.QSize(55, 75))
        self.button_6.setObjectName("button_6")
        self.button_6.clicked.connect(lambda: self.play_game(6))
        self.gridLayout.addWidget(self.button_6, 2, 0, 1, 1)

        # Button 8
        self.button_7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.button_7.setMinimumSize(QtCore.QSize(55, 75))
        self.button_7.setObjectName("button_7")
        self.button_7.clicked.connect(lambda: self.play_game(7))
        self.gridLayout.addWidget(self.button_7, 2, 1, 1, 1)

        # Button 9
        self.button_8 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.button_8.setMinimumSize(QtCore.QSize(55, 75))
        self.button_8.setObjectName("button_8")
        self.button_8.clicked.connect(lambda: self.play_game(8))
        self.gridLayout.addWidget(self.button_8, 2, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Initial setup
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tic Tac Toe by Jasmine"))
        MainWindow.setWindowIcon(QIcon("assets/ico.png"))
        MainWindow.setMinimumSize(310, 380)
        MainWindow.setMaximumSize(310, 380)
        MainWindow.setStyleSheet("#centralwidget{background-image: url(assets/bg.png);}")
        self.title.setText(_translate("MainWindow", "Tic Tac Toe [x][o]"))
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setText(_translate("MainWindow", "Make the first move."))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
