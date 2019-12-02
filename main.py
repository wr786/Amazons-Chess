import sys
import os
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap
from PyQt5.QtCore import pyqtSignal, QSize, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout

class GameWindow(QWidget):
    
    def __init__(self):
        super(GameWindow, self).__init__()
        self.init_chess_board()
        self.init_game_window()
        self.init_buttons()

    def init_game_window(self):
        self.setWindowTitle('Amazons ~ 再生産！ © wr786')
        self.setWindowIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'ICON.ico')))
        self.setFixedSize(1600, 1080)
        # self.resize(1440, 1080)
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap(os.path.join(os.path.abspath('.'), 'source', 'background.jpg'))))
        self.setPalette(palette1)
        
        self.readLog()

    def init_chess_board(self):
        self.ChessBoard_unit = [[0] * 8 for _ in range(8)] # 生成ChessBoard单元 8×8
        for i in range(8):
            for j in range(8):
                self.ChessBoard_unit[i][j] = QPushButton(self)
                # TEST
                self.ChessBoard_unit[i][j].setStyleSheet("QPushButton{color:white}"
                                  "QPushButton{background-color:white}"
                                  "QPushButton{border:2px}"
                                  "QPushButton{padding:0px 0px}")
                self.ChessBoard_unit[i][j].setGeometry(250 + 100*(i-1), 250 + 100*(j-1), 100, 100)
                self.ChessBoard_unit[i][j].setIconSize(QSize(110,110))
                self.ChessBoard_unit[i][j].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'EMPTY.png')))
                self.ChessBoard_unit[i][j].clicked.connect(self.test)

    def init_buttons(self):
        self.Redo_button = QPushButton(self)
        self.Hint_button = QPushButton(self)
        self.Save_button = QPushButton(self)
        self.Read_button = QPushButton(self)

        self.Redo_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'REDO.png')))
        self.Redo_button.setIconSize(QSize(80,80))
        self.Hint_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'HINT.png')))
        self.Hint_button.setIconSize(QSize(80,80))
        self.Save_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'SAVE.png')))
        self.Save_button.setIconSize(QSize(80,80))
        self.Read_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'READ.png')))
        self.Read_button.setIconSize(QSize(80,80))

        self.Redo_button.setText("悔棋")
        self.Hint_button.setText("提示")
        self.Save_button.setText("读档")
        self.Read_button.setText("存档")

        self.Redo_button.setStyleSheet( "QPushButton{color:black}"
                              "QPushButton{background-color:white}"
                              "QPushButton{border:2px}"
                              "QPushButton{padding:20px 40px}"
                              "QPushButton{font-size: 48px}"
                              "QPushButton{font-family:'Microsoft YaHei'}")
        self.Hint_button.setStyleSheet( "QPushButton{color:black}"
                              "QPushButton{background-color:white}"
                              "QPushButton{border:2px}"
                              "QPushButton{padding:20px 40px}"
                              "QPushButton{font-size: 48px}"
                              "QPushButton{font-family:'Microsoft YaHei'}")
        self.Save_button.setStyleSheet( "QPushButton{color:black}"
                              "QPushButton{background-color:white}"
                              "QPushButton{border:2px}"
                              "QPushButton{padding:20px 40px}"
                              "QPushButton{font-size: 48px}"
                              "QPushButton{font-family:'Microsoft YaHei'}")
        self.Read_button.setStyleSheet( "QPushButton{color:black}"
                              "QPushButton{background-color:white}"
                              "QPushButton{border:2px}"
                              "QPushButton{padding:20px 40px}"
                              "QPushButton{font-size: 48px}"
                              "QPushButton{font-family:'Microsoft YaHei'}")

        self.Redo_button.setGeometry(1260, 150, 280, 100)
        self.Hint_button.setGeometry(1260, 300, 280, 100)
        self.Save_button.setGeometry(1260, 450, 280, 100)
        self.Read_button.setGeometry(1260, 600, 280, 100)

        self.Redo_button.clicked.connect(self.regret)
        self.Hint_button.clicked.connect(self.hint)
        self.Save_button.clicked.connect(self.saveLog)
        self.Read_button.clicked.connect(self.readLog)


    # <----------------------------------------测试区------------------------------------>
    def test(self):
        sender = self.sender() # 用sender来获取发送者
        sender.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'WHITE.png')))

    # <----------------------------------------待施工------------------------------------>
    def readLog(self): # 读档 
        f = open(os.path.join(os.path.abspath('.'), 'data', 'chessboard.amazons'), "r")    
        f.close()

    def saveLog(self): # 存档
        f = open(os.path.join(os.path.abspath('.'), 'data', 'moves.amazons'), 'w')
        f.close()

    def regret(self): # 悔棋
        pass

    def hint(self): # 提示
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gamewindow = GameWindow()
    gamewindow.show()
    sys.exit(app.exec_())
