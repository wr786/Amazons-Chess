# -*- coding: utf-8 -*-
# author: wr786
import sys
import os
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap
from PyQt5.QtCore import pyqtSignal, QSize, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout, QMessageBox
from base64 import *
from memory_pic import *

def get_pic(pic_code, pic_name):
    image = open(pic_name, 'wb')
    image.write(b64decode(pic_code))
    image.close()

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
        # self.setWindowIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'ICON.ico')))
        self.setWindowIcon(QIcon('ICON.ico'))
        self.setFixedSize(1600, 1080)
        # self.resize(1440, 1080)
        palette1 = QPalette()
        # palette1.setBrush(self.backgroundRole(), QBrush(QPixmap(os.path.join(os.path.abspath('.'), 'source', 'background.jpg'))))
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('background.jpg')))
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
                # self.ChessBoard_unit[i][j].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'EMPTY.png')))
                self.ChessBoard_unit[i][j].setIcon(QIcon('EMPTY.png'))
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
        self.turn_player = 1
        self.chess = [[0, 0, 0, 0], [2, 20, 50, 72], [5, 27, 57, 75]] # 记录棋子的位置
        self.canRegret = False

    def init_buttons(self):
        self.Redo_button = QPushButton(self)
        self.Hint_button = QPushButton(self)
        self.Save_button = QPushButton(self)
        self.Read_button = QPushButton(self)
        self.Skin_button = QPushButton(self)
        self.NewGame_button = QPushButton(self)

        # self.Redo_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'REDO.png')))
        self.Redo_button.setIcon(QIcon('REDO.png'))
        self.Redo_button.setIconSize(QSize(80,80))
        # self.Hint_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'HINT.png')))
        self.Hint_button.setIcon(QIcon('HINT.png'))
        self.Hint_button.setIconSize(QSize(80,80))
        # self.Save_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'SAVE.png')))
        self.Save_button.setIcon(QIcon('SAVE.png'))
        self.Save_button.setIconSize(QSize(80,80))
        # self.Read_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'READ.png')))
        self.Read_button.setIcon(QIcon('READ.png'))
        self.Read_button.setIconSize(QSize(80,80))
        # self.Skin_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'SKIN.png')))
        self.Skin_button.setIcon(QIcon('SKIN.png'))
        self.Skin_button.setIconSize(QSize(80,80))
        # self.NewGame_button.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'NEWGAME.png')))
        self.NewGame_button.setIcon(QIcon('NEWGAME.png'))
        self.NewGame_button.setIconSize(QSize(80,80))

        self.Redo_button.setText("悔棋")
        self.Hint_button.setText("提示")
        self.Save_button.setText("存档")
        self.Read_button.setText("读档")
        self.Skin_button.setText("换肤")
        self.NewGame_button.setText("新游戏")

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
        self.NewGame_button.setStyleSheet( "QPushButton{color:black}"
                              "QPushButton{background-color:white}"
                              "QPushButton{border:2px}"
                              "QPushButton{padding:20px 40px}"
                              "QPushButton{font-size: 36px}"
                              "QPushButton{font-family:'Microsoft YaHei'}")

        self.Redo_button.setGeometry(1260, 130, 280, 100)
        self.Hint_button.setGeometry(1260, 280, 280, 100)
        self.Save_button.setGeometry(1260, 430, 280, 100)
        self.Read_button.setGeometry(1260, 580, 280, 100)
        self.Skin_button.setGeometry(1260, 730, 280, 100)
        self.NewGame_button.setGeometry(1260, 880, 280, 100)

        self.Redo_button.clicked.connect(self.regret)
        self.Hint_button.clicked.connect(self.hint)
        self.Save_button.clicked.connect(self.saveLog)
        self.Read_button.clicked.connect(self.readLog)
        self.Skin_button.clicked.connect(self.changeSkin)
        self.NewGame_button.clicked.connect(self.newGame)

    def showChess(self):
        for i in range(8):
            for j in range(8):
                chesstype = self.ChessBoard_unit_content[i][j]
                if chesstype == 0: # EMPTY
                    # self.ChessBoard_unit[i][j].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'EMPTY.png')))
                    self.ChessBoard_unit[i][j].setIcon(QIcon('EMPTY.png'))
                elif chesstype == 1: # BLACK
                    # self.ChessBoard_unit[i][j].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'BLACK.png')))
                    self.ChessBoard_unit[i][j].setIcon(QIcon('BLACK.png'))
                elif chesstype == 2: # WHITE
                    # self.ChessBoard_unit[i][j].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'WHITE.png')))
                    self.ChessBoard_unit[i][j].setIcon(QIcon('WHITE.png'))
                elif chesstype == -1: # BLOCK
                    # self.ChessBoard_unit[i][j].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'BLOCK.png')))
                    self.ChessBoard_unit[i][j].setIcon(QIcon('BLOCK.png'))
        # sender = self.sender() # 用sender来获取发送者
        # sender.setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'WHITE.png')))

    def selectChess(self):
        # 此处应有判断是否为自己的棋子
        if self.selectChessFlag: # 此处应有弹出提示框
            QMessageBox.critical(self,"请先把这步走完！","恁已经选择了一个棋子，请先把这步走完！",QMessageBox.Ok)
            return
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
        if self.ChessBoard_unit_content[x][y] != self.turn_player:
            QMessageBox.critical(self,"这不是恁的棋子！","这不是恁的棋子，请选择恁的棋子！",QMessageBox.Ok)
            return
        self.ox = x
        self.oy = y
        self.selectChessFlag = True
        for dir in range(8):
            nx = x + self.dx[dir]
            ny = y + self.dy[dir]
            while(inBoard(nx, ny) and self.ChessBoard_unit_content[nx][ny] == 0):
                self.ChessBoard_unit[nx][ny].clicked.disconnect(self.selectChess)
                self.ChessBoard_unit[nx][ny].clicked.connect(self.selectBlock)
                self.ChessBoard_unit_content[nx][ny] = 19260817 # 被标记为黄色的可以去往的格子
                # self.ChessBoard_unit[nx][ny].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'CANGO.png')))
                self.ChessBoard_unit[nx][ny].setIcon(QIcon('CANGO.png'))
                nx += self.dx[dir]
                ny += self.dy[dir]

    def selectBlock(self):
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
                    # self.ChessBoard_unit[i][j].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'EMPTY.png')))
                    self.ChessBoard_unit[i][j].setIcon(QIcon('EMPTY.png'))
                    self.ChessBoard_unit[i][j].clicked.disconnect(self.selectBlock)
                    self.ChessBoard_unit[i][j].clicked.connect(self.selectChess)
        # self.ChessBoard_unit[self.ox][self.oy].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'EMPTY.png')))
        self.ChessBoard_unit[self.ox][self.oy].setIcon(QIcon('EMPTY.png'))
        if self.turn_player == 1:
            # self.ChessBoard_unit[x][y].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'BLACK.png')))
            self.ChessBoard_unit[x][y].setIcon(QIcon('BLACK.png'))
        else:
            # self.ChessBoard_unit[x][y].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'WHITE.png')))
            self.ChessBoard_unit[x][y].setIcon(QIcon('WHITE.png'))
        self.ex = x
        self.ey = y
        for dir in range(8):
            nx = x + self.dx[dir]
            ny = y + self.dy[dir]
            while(inBoard(nx, ny) and (self.ChessBoard_unit_content[nx][ny] == 0 or (nx == self.ox and ny == self.oy))):
                self.ChessBoard_unit[nx][ny].clicked.disconnect(self.selectChess)
                self.ChessBoard_unit[nx][ny].clicked.connect(self.procMove)
                self.ChessBoard_unit_content[nx][ny] = -19260817 # 被标记为红色的可以放障碍物的格子
                # self.ChessBoard_unit[nx][ny].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'CANBLOCK.png')))
                self.ChessBoard_unit[nx][ny].setIcon(QIcon('CANBLOCK.png'))
                nx += self.dx[dir]
                ny += self.dy[dir]

    def procMove(self):
        sender = self.sender()
        x = -1
        y = -1
        for i in range(8):
            for j in range(8):
                if self.ChessBoard_unit[i][j] == sender:
                    x = i
                    y = j
                if self.ChessBoard_unit_content[i][j] == -19260817: # 恢复
                    self.ChessBoard_unit_content[i][j] = 0
                    # self.ChessBoard_unit[i][j].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'EMPTY.png')))
                    self.ChessBoard_unit[i][j].setIcon(QIcon('EMPTY.png'))
                    self.ChessBoard_unit[i][j].clicked.disconnect(self.procMove)
                    self.ChessBoard_unit[i][j].clicked.connect(self.selectChess)
        self.bx = x
        self.by = y
        self.ChessBoard_unit_content[self.ox][self.oy] = 0
        # self.ChessBoard_unit[self.ox][self.oy].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'EMPTY.png')))
        self.ChessBoard_unit[self.ox][self.oy].setIcon(QIcon('EMPTY.png'))
        self.ChessBoard_unit_content[self.ex][self.ey] = self.turn_player
        if self.turn_player == 1:
            # self.ChessBoard_unit[self.ex][self.ey].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'BLACK.png')))
            self.ChessBoard_unit[self.ex][self.ey].setIcon(QIcon('BLACK.png'))
        else:
            # self.ChessBoard_unit[self.ex][self.ey].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'WHITE.png')))
            self.ChessBoard_unit[self.ex][self.ey].setIcon(QIcon('WHITE.png'))
        self.ChessBoard_unit_content[self.bx][self.by] = -1
        # self.ChessBoard_unit[self.bx][self.by].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'BLOCK.png')))
        self.ChessBoard_unit[self.bx][self.by].setIcon(QIcon('BLOCK.png'))
        self.selectChessFlag = False
        for i in range(4):
            if self.chess[self.turn_player][i] == self.ox * 10 + self.oy: # 找到被移动的棋
                self.chess[self.turn_player][i] = self.ex * 10 + self.ey
                break
        self.turn_player = 3 - self.turn_player
        self.judgeWin()
        self.canRegret = True

    def canMove(self, x, y):
        for dir in range(8):
            nx = x + self.dx[dir]
            ny = y + self.dy[dir]
            if(not inBoard(nx, ny)):
                continue
            if(self.ChessBoard_unit_content[nx][ny] == 0): # 如果有一个方向可以动那就没有被锁死
                return True
        return False

    def judgeWin(self):
        locked = [[False] * 5 for _ in range(3)] # 记录[某颜色]的第[i]个棋子是否被锁死，其中第5项存储是否全部被锁死
        # for i in range(8):
        #     for j in range(8):
        #         print((self.ChessBoard_unit_content[i][j]), end = " ")
        #     print("\n")
        for i in range(4):
            locked[1][i] = not self.canMove(self.chess[1][i]//10, self.chess[1][i]%10) # // 是整除
            locked[2][i] = not self.canMove(self.chess[2][i]//10, self.chess[2][i]%10)
            # print("{} {}: {} {}\n".format(self.chess[1][i], self.chess[2][i], locked[1][i], locked[2][i]))
        locked[1][4] = locked[1][0] & locked[1][1] & locked[1][2] & locked[1][3]
        locked[2][4] = locked[2][0] & locked[2][1] & locked[2][2] & locked[2][3]
        # print("sum:{} {}\n".format(locked[1][4], locked[2][4]))
        if(locked[1][4]):
            QMessageBox.information(self,"游戏结束","白方获胜！",QMessageBox.Ok)
        elif(locked[2][4]):
            QMessageBox.information(self,"游戏结束","黑方获胜！",QMessageBox.Ok)

    def newGame(self): # 是新游戏
        if self.selectChessFlag:
            QMessageBox.critical(self,"不要脚踏两条船！","请先完成移动操作！",QMessageBox.Ok)
            return
        # 此处应有询问是否需要人机对战
        for i in range(8):
            for j in range(8):
                self.ChessBoard_unit_content[i][j] = 0 # 归 零
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
        self.selectChessFlag = False
        self.turn_player = 1
        self.chess = [[0, 0, 0, 0], [2, 20, 50, 72], [5, 27, 57, 75]] # 记录棋子的位置
        self.canRegret = False

        self.showChess()

    def regret(self): # 悔棋     
        if self.selectChessFlag:
            QMessageBox.critical(self,"不要脚踏两条船！","请先完成移动操作！",QMessageBox.Ok)
            return
        if not self.canRegret:
            QMessageBox.critical(self,"约束！","恁现在不能悔棋！",QMessageBox.Ok)
            return
        self.canRegret = False
        self.turn_player = 3 - self.turn_player
        self.selectChessFlag = False
        self.ChessBoard_unit_content[self.ex][self.ey] = 0
        # self.ChessBoard_unit[self.ex][self.ey].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'EMPTY.png')))
        self.ChessBoard_unit[self.ex][self.ey].setIcon(QIcon('EMPTY.png'))
        self.ChessBoard_unit_content[self.bx][self.by] = 0
        # self.ChessBoard_unit[self.bx][self.by].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'EMPTY.png')))
        self.ChessBoard_unit[self.bx][self.by].setIcon(QIcon('EMPTY.png'))
        self.ChessBoard_unit_content[self.ox][self.oy] = self.turn_player
        if self.turn_player == 1:
            # self.ChessBoard_unit[self.ox][self.oy].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'BLACK.png')))
            self.ChessBoard_unit[self.ox][self.oy].setIcon(QIcon('BLACK.png'))
        else:
            # self.ChessBoard_unit[self.ox][self.oy].setIcon(QIcon(os.path.join(os.path.abspath('.'), 'source', 'WHITE.png')))
            self.ChessBoard_unit[self.ox][self.oy].setIcon(QIcon('WHITE.png'))
        for i in range(4):
            if self.chess[self.turn_player][i] == self.ex * 10 + self.ey: # 找到被移动的棋
                self.chess[self.turn_player][i] = self.ox * 10 + self.oy
                break
    # <----------------------------------------待施工------------------------------------>
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

    def saveLog(self): # 存档
        f = open(os.path.join(os.path.abspath('.'), 'data', 'moves.amazons'), 'w')
        f.close()

    def hint(self): # 提示
        pass

    def changeSkin(self): # 换肤
        pass

if __name__ == '__main__':
    get_pic(background_jpg, 'background.jpg')
    get_pic(ICON_ico, 'ICON.ico')
    get_pic(EMPTY_png, 'EMPTY.png')
    get_pic(BLACK_png, 'BLACK.png')
    get_pic(WHITE_png, 'WHITE.png')
    get_pic(BLOCK_png, 'BLOCK.png')
    get_pic(CANGO_png, 'CANGO.png')
    get_pic(CANBLOCK_png, 'CANBLOCK.png')
    get_pic(HINT_png, 'HINT.png')
    get_pic(REDO_png, 'REDO.png')
    get_pic(READ_png, 'READ.png')
    get_pic(SAVE_png, 'SAVE.png')
    get_pic(SKIN_png, 'SKIN.png')
    get_pic(NEWGAME_png, 'NEWGAME.png')
    app = QApplication(sys.argv)
    gamewindow = GameWindow()
    gamewindow.show()
    app.exec_()
    os.remove('background.jpg')
    os.remove('ICON.ico')
    os.remove('EMPTY.png')
    os.remove('BLACK.png')
    os.remove('WHITE.png')
    os.remove('BLOCK.png')
    os.remove('CANGO.png')
    os.remove('CANBLOCK.png')
    os.remove('HINT.png')
    os.remove('REDO.png')
    os.remove('READ.png')
    os.remove('SAVE.png')
    os.remove('SKIN.png')
    os.remove('NEWGAME.png')
    sys.exit()