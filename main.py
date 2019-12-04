import sys
import os
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap
from PyQt5.QtCore import pyqtSignal, QSize, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout

def inBoard(x, y):
    if(x < 0 or x >= 8 or y < 0 or y >= 8):
        return False
    return True

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
        
        self.showChess()
        # self.readLog()

    def init_chess_board(self):
        self.ChessBoard_unit = [[0] * 8 for _ in range(8)] # 生成ChessBoard单元 8×8
        self.ChessBoard_unit_content = [[0] * 8 for _ in range(8)]
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
                self.ChessBoard_unit[i][j].clicked.connect(self.selectChess)
                # self.ChessBoard_unit[i][j].clicked.connect(self.test)
        # init初始坐标
        # 这里的坐标都是转置过的，后续坐标也要记得转置……
        self.ChessBoard_unit_content[0][2] = 1
        self.ChessBoard_unit_content[2][0] = 1
        self.ChessBoard_unit_content[5][0] = 1
        self.ChessBoard_unit_content[7][2] = 1
        self.ChessBoard_unit_content[0][5] = 2
        self.ChessBoard_unit_content[2][7] = 2
        self.ChessBoard_unit_content[5][7] = 2
        self.ChessBoard_unit_content[7][5] = 2
        self.dx = [0, 1, 1, 1, 0, -1, -1, -1]
        self.dy = [1, 1, 0, -1, -1, -1, 0, 1]
        self.selectChessFlag = False
        self.selectBlockFlag = False
        self.turn_player = 1


    def init_buttons(self):
        self.Redo_button = QPushButton(self)
        self.Hint_button = QPushButton(self)
        self.Save_button = QPushButton(self)
        self.Read_button = QPushButton(self)
        self.Skin_button = QPushButton(self)

        self.Redo_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'REDO.png')))
        self.Redo_button.setIconSize(QSize(80,80))
        self.Hint_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'HINT.png')))
        self.Hint_button.setIconSize(QSize(80,80))
        self.Save_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'SAVE.png')))
        self.Save_button.setIconSize(QSize(80,80))
        self.Read_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'READ.png')))
        self.Read_button.setIconSize(QSize(80,80))
        self.Skin_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'SKIN.png')))
        self.Skin_button.setIconSize(QSize(80,80))

        self.Redo_button.setText("悔棋")
        self.Hint_button.setText("提示")
        self.Save_button.setText("存档")
        self.Read_button.setText("读档")
        self.Skin_button.setText("换肤")

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
        self.Skin_button.setStyleSheet( "QPushButton{color:black}"
                              "QPushButton{background-color:white}"
                              "QPushButton{border:2px}"
                              "QPushButton{padding:20px 40px}"
                              "QPushButton{font-size: 48px}"
                              "QPushButton{font-family:'Microsoft YaHei'}")

        self.Redo_button.setGeometry(1260, 150, 280, 100)
        self.Hint_button.setGeometry(1260, 300, 280, 100)
        self.Save_button.setGeometry(1260, 450, 280, 100)
        self.Read_button.setGeometry(1260, 600, 280, 100)
        self.Skin_button.setGeometry(1260, 750, 280, 100)

        self.Redo_button.clicked.connect(self.regret)
        self.Hint_button.clicked.connect(self.hint)
        self.Save_button.clicked.connect(self.saveLog)
        self.Read_button.clicked.connect(self.readLog)
        self.Skin_button.clicked.connect(self.changeSkin)

    def showChess(self):
        for i in range(8):
            for j in range(8):
                chesstype = self.ChessBoard_unit_content[i][j]
                if chesstype == 0: # EMPTY
                    self.ChessBoard_unit[i][j].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'EMPTY.png')))
                elif chesstype == 1: # BLACK
                    self.ChessBoard_unit[i][j].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'BLACK.png')))
                elif chesstype == 2: # WHITE
                    self.ChessBoard_unit[i][j].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'WHITE.png')))
                elif chesstype == -1: # BLOCK
                    self.ChessBoard_unit[i][j].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'BLOCK.png')))
        # sender = self.sender() # 用sender来获取发送者
        # sender.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'WHITE.png')))

    # <----------------------------------------测试区------------------------------------>

    def selectChess(self):
        # 此处应有判断是否为自己的棋子
        if self.selectChessFlag: # 此处应有弹出提示框
            pass
        self.selectChessFlag = True
        sender = self.sender()
        x = -1
        y = -1
        for i in range(8):
            for j in range(8):
                if self.ChessBoard_unit[i][j] == sender:
                    x = i
                    y = j
                    break        
            if x != -1:
                break
        self.ox = x
        self.oy = y
        for dir in range(8):
            nx = x + self.dx[dir]
            ny = y + self.dy[dir]
            while(inBoard(nx, ny) and self.ChessBoard_unit_content[nx][ny] == 0):
                self.ChessBoard_unit[nx][ny].clicked.disconnect(self.selectChess)
                self.ChessBoard_unit[nx][ny].clicked.connect(self.selectBlock)
                self.ChessBoard_unit_content[nx][ny] = 19260817 # 被标记为黄色的可以去往的格子
                self.ChessBoard_unit[nx][ny].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'CANGO.png')))
                nx += self.dx[dir]
                ny += self.dy[dir]

    def selectBlock(self):
        if self.selectBlockFlag: # 此处应有弹出提示框
            pass
        self.selectBlockFlag = True
        sender = self.sender()
        x = -1
        y = -1
        for i in range(8):
            for j in range(8):
                if self.ChessBoard_unit[i][j] == sender:
                    x = i
                    y = j
                if self.ChessBoard_unit_content[i][j] == 19260817: # 恢复
                    self.ChessBoard_unit_content[i][j] = 0
                    self.ChessBoard_unit[i][j].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'EMPTY.png')))
                    self.ChessBoard_unit[i][j].clicked.disconnect(self.selectBlock)
                    self.ChessBoard_unit[i][j].clicked.connect(self.selectChess)
        self.ChessBoard_unit[self.ox][self.oy].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'EMPTY.png')))
        if self.turn_player == 1:
            self.ChessBoard_unit[x][y].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'BLACK.png')))
        else:
            self.ChessBoard_unit[x][y].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'BLACK.png')))
        for dir in range(8):
            nx = x + self.dx[dir]
            ny = y + self.dy[dir]
            while(inBoard(nx, ny) and (self.ChessBoard_unit_content[nx][ny] == 0 or (nx == self.ox and ny == self.oy))):
                self.ChessBoard_unit[nx][ny].clicked.disconnect(self.selectChess)
                self.ChessBoard_unit[nx][ny].clicked.connect(self.procMove)
                self.ex = x
                self.ey = y
                self.bx = nx
                self.by = ny
                self.ChessBoard_unit_content[nx][ny] = -19260817 # 被标记为红色的可以放障碍物的格子
                self.ChessBoard_unit[nx][ny].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'CANBLOCK.png')))
                nx += self.dx[dir]
                ny += self.dy[dir]

    def procMove(self):
        pass

    def calc(self):
        os.system('bot.exe')

    def initLog(self): # 从零开始游戏
        f = open(os.path.join(os.path.abspath('.'), 'data', 'moves.amazons'), 'w')
        f.write("1 -1 -1 -1 -1 -1 -1")
        f.close()

    def readLog(self): # 读档 
        f = open(os.path.join(os.path.abspath('.'), 'data', 'chessboard.amazons'), "r")
        rownum = 0
        for line in f:
            items = line.split() # 以空格分割
            colnum = 0
            for item in items:
                chesstype = int(item)
                self.showChess(self, rownum, colnum, chesstype)
                colnum += 1
            rownum += 1
        f.close()
    # <----------------------------------------待施工------------------------------------>

    def saveLog(self): # 存档
        f = open(os.path.join(os.path.abspath('.'), 'data', 'moves.amazons'), 'w')
        f.close()

    def regret(self): # 悔棋
        pass

    def hint(self): # 提示
        pass

    def changeSkin(self): # 换肤
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gamewindow = GameWindow()
    gamewindow.show()
    sys.exit(app.exec_())
