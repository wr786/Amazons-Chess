import sys
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton

class GameWindow(QWidget):
    
    def __init__(self):
        super(GameWindow, self).__init__()
        # self.ChessBoard = QGridLayout()
        self.init_chess_board()
        # self.setLayout(self.ChessBoard)
        self.setWindowTitle('Amazons')
        self.setWindowIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'BLACK.png')))
        # self.setFixedSize(760, 440)
        self.resize(880, 880)

    def init_chess_board(self):
        self.ChessBoard_unit = [[0] * 8 for _ in range(8)] # 生成ChessBoard单元
        for i in range(8):
            for j in range(8):
                self.ChessBoard_unit[i][j] = QPushButton(self)
                # self.ChessBoard.addWidget(self.ChessBoard_unit[i][j], i, j)
                # TEST
                self.ChessBoard_unit[i][j].setGeometry(100*(i-1), 100*(j-1), 100, 100)
                self.ChessBoard_unit[i][j].setIconSize(QSize(110,110))
                self.ChessBoard_unit[i][j].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'EMPTY.png')))
                self.ChessBoard_unit[i][j].clicked.connect(self.test)

    def test(self):
        sender = self.sender() # 用sender来获取发送者
        sender.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'BLACK.png')))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gamewindow = GameWindow()
    gamewindow.show()
    sys.exit(app.exec_())
