import sys
import os
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton

class GameWindow(QWidget):
    
    def __init__(self):
        super(GameWindow, self).__init__()
        self.init_chess_board()
        self.setWindowTitle('Amazons ~ 再生産！ © wr786')
        self.setWindowIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'BLACK_t.png')))
        # self.setFixedSize(760, 440)
        self.resize(1440, 1080)
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


    # <----------------------------------------测试区------------------------------------>
    def test(self):
        sender = self.sender() # 用sender来获取发送者
        sender.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'WHITE.png')))

    # <----------------------------------------待施工------------------------------------>
    def readLog(self): # 存档 
        f = open(os.path.join(os.path.abspath('.'), 'data', 'log.amazons'), "r")    
        f.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gamewindow = GameWindow()
    gamewindow.show()
    sys.exit(app.exec_())
