import random, os, time, threading
import tkinter as tk
from PIL import Image, ImageTk

def CreateBoard():
    board = list()
    for i in range(5):
        board.append([0, 0, 0, 0, 0])

    monsterX = random.randint(0, 4)
    monsterY = random.randint(0, 4)
    board[monsterX][monsterY] = 2

    playerX = random.randint(0, 4)
    playerY = random.randint(0, 4)
    if board[playerX][playerY] == 2:
        while board[playerX][playerY] == 2:
            playerX = random.randint(0, 4)
            playerY = random.randint(0, 4)
    board[playerX][playerY] = 1
    
    exitX = random.randint(0, 4)
    exitY = random.randint(0, 4)
    if board[exitX][exitY] == 2 or board[exitX][exitY] == 1:
        while board[exitX][exitY] == 2 or board[exitX][exitY] == 1:
            exitX = random.randint(0, 4)
            exitY = random.randint(0, 4)
    board[exitX][exitY] = 3
    return board

def GetCharacter(board, index):
    for i in range(5):
        for j in range(5):
            if board[i][j] == index:
                return i, j
    return -1, -1

def VisibilitySettings(board, moveCount):
    visibleBoard = list()

    for i in range(5):
        visibleBoard.append([-1, -1, -1, -1, -1])
    for i in range(5):
        for j in range(5):
            if board[i][j] == 1:
                visibleBoard[i][j] = 1
                if moveCount > 0:
                    if i > 0:
                        visibleBoard[i-1][j] = 1

                    if i < 4:
                        visibleBoard[i+1][j] = 1
                    
                    if j > 0:
                        visibleBoard[i][j-1] = 1
                    if j < 4:
                        visibleBoard[i][j+1] = 1
                    
    return visibleBoard

def PrintBoard(board, moveCount, allVisible = False):
    visibleBoard = VisibilitySettings(board, moveCount)
    for i in range(5):
        for j in range(5):
            if allVisible:
                print(board[i][j], end=" ")
            else:
                if visibleBoard[i][j] == 1:
                    print(board[i][j], end=" ")
                else:
                    print("-1", end=" ")
        print()

def MoveMonster (board, monsterPosition):
    verif = False
    while verif == False:
        monsterX = random.randrange(-1, 2)
        if monsterX == 0:
            monsterY = random.randrange(-1, 2, 2)
            if monsterPosition[1] + monsterY > 0 and monsterPosition[1] + monsterY < 4:
                if board[monsterPosition[0]][monsterPosition[1] + monsterY] != 3:
                    board[monsterPosition[0]][monsterPosition[1] + monsterY] = 2
                    verif = True
        elif monsterPosition[0] + monsterX > 0 and monsterPosition[0] + monsterX < 4:
            monsterY = 0
            if board[monsterPosition[0] + monsterX][monsterPosition[1]] != 3:
                board[monsterPosition[0] + monsterX][monsterPosition[1]] = 2
                verif = True
        else:
            continue
    board[monsterPosition[0]][monsterPosition[1]] = 0

def CloseLabel (label):
    print ("Deletando a label de nome {}".format(label.cget("text")))
    time.sleep(5)
    label.destroy()
    print ("Label deletada")

class Application():
    def __init__(self):
        self.inGame = False
        self.window = tk.Tk()
        self.MainScreen()

        self.window.mainloop()

    def StartGame(self):
        self.board = CreateBoard()
        self.moveCount = 0
        self.inGame = True
        self.win = 0

        self.ScreenFrames()

    def ExecuteMove (self):
        print (f"Executou o movimento com o win {self.win}")
        if self.win == 0:
            self.moveCount += 1
            self.ShowBoard()
            time.sleep(0.15)
        else:
            self.ShowBoard(allvisible=True)
            self.ScreenFrames(gameOver=self.win)

    def Interact(self, board, newPlayerCords):
        if board[newPlayerCords[0]][newPlayerCords[1]] == 2:
            print("Você morreu :/")
            return -1
        elif board[newPlayerCords[0]][newPlayerCords[1]] == 3:
            print("Você venceu! Parabens :D")
            return 1
        elif board[newPlayerCords[0]][newPlayerCords[1]] == 0:
            board[newPlayerCords[0]][newPlayerCords[1]] = 1
            return 0
        else:
            print("Invalid interaction")

    def MovePlayer (self, board, moveType):
        #moveType: 0 - up, 1 - down, 2 - left, 3 - right
        playerPosition = GetCharacter(board, 1)
        MoveMonster(board, GetCharacter(board, 2))
        if moveType == 0:
            if playerPosition[0] > 0:
                result = self.Interact(board, [playerPosition[0]-1, playerPosition[1]])
                if result == 0:
                    board[playerPosition[0]][playerPosition[1]] = 0
                    board[playerPosition[0]-1][playerPosition[1]] = 1
                    return 0
                else:
                    return result

        elif moveType == 1:
            if playerPosition[0] < 4:
                result = self.Interact(board, [playerPosition[0]+1, playerPosition[1]])
                if result == 0:
                    board[playerPosition[0]][playerPosition[1]] = 0
                    board[playerPosition[0]+1][playerPosition[1]] = 1
                    return 0
                else:
                    return result

        elif moveType == 2:
            if playerPosition[1] > 0:
                result = self.Interact(board, [playerPosition[0], playerPosition[1]-1])
                if result == 0:
                    board[playerPosition[0]][playerPosition[1]] = 0
                    board[playerPosition[0]][playerPosition[1]-1] = 1
                    return 0
                else:
                    return result
        elif moveType == 3:
            if playerPosition[1] < 4:
                result = self.Interact(board, [playerPosition[0], playerPosition[1]+1])
                if result == 0:
                    board[playerPosition[0]][playerPosition[1]] = 0
                    board[playerPosition[0]][playerPosition[1]+1] = 1
                    return 0
                else:
                    return result

        print("Movimento inválido")
        return -1

    def MoveUp(self):
        if GetCharacter(self.board, 1)[0] > 0:
            self.win = self.MovePlayer(self.board, 0)
            self.currentPlayer = 0
            self.ExecuteMove()

    def MoveDown(self):
        if GetCharacter(self.board, 1)[0] < 4:
            self.win = self.MovePlayer(self.board, 1)
            self.currentPlayer = 1
            self.ExecuteMove()

    def MoveLeft(self):
        if GetCharacter(self.board, 1)[1] > 0:
            self.win = self.MovePlayer(self.board, 2)
            self.currentPlayer = 2
            self.ExecuteMove()

    def MoveRight(self):
        if GetCharacter(self.board, 1)[1] < 4:
            self.win = self.MovePlayer(self.board, 3)
            self.currentPlayer = 3
            self.ExecuteMove()
    
    def ShowBoard(self, allvisible = False):
        self.labels.clear()
        size = 64
        self.BoardFrame2 = tk.Frame(self.BoardFrame, bg = "#B2B2B2")
        self.BoardFrame2.place(relx=0.5, rely=0.5, anchor="center")

        for row in range(5):
            self.labels.append(list())
            for columns in range (5):
                label = tk.Label(self.BoardFrame2, width=size, height=size, bg="#01001f", relief="ridge", borderwidth=2)
                label.grid(row=row + 10, column=columns + 10, padx=10, pady=5)
                self.labels[row].append(label)

        self.visibleBoard = VisibilitySettings(self.board, self.moveCount)
        PrintBoard(self.board, 1, allVisible=True)
        print ("\n-----------------------------\n")

        for row in range (5):
            for column in range (5):
                if self.board[row][column] == 1:
                    self.labels[row][column].configure(image=self.player[self.currentPlayer])
                else:
                    if allvisible:
                        self.labels[row][column].configure(image=self.images[self.indexImages.index(self.board[row][column])])
                    else:
                        if self.visibleBoard[row][column] == 1:
                            self.labels[row][column].configure(image=self.images[self.indexImages.index(self.board[row][column])])
                        else:
                            self.labels[row][column].configure(image=self.images[0])

    def Sla(self):
        self.ShowBoard(allvisible=True)
    
    def ScreenFrames (self, gameOver = 0):
        self.MainFrame = tk.Frame(self.window, bg = "lightblue")
        self.MainFrame.place(relwidth = 0.95, relheight = 0.95, relx=0.025, rely=0.025)

        self.Title = tk.Button(self.MainFrame, text = "Dungeon Runner", bg = "#000028", fg = "white", font = ("Arial", 24, "bold"), command=self.Sla)
        self.Title.place(relwidth = 0.9, relheight = 0.1, rely=0.01, relx=0.05)

        self.StartButton = tk.Button(self.MainFrame, text = "Start", bg = "black", fg = "white", font = ("Arial", 16), command=self.StartGame)
        self.StartButton.place(relwidth=0.2, relheight=0.05, relx=0.4, rely=0.125)

        if self.inGame:
            self.BoardFrame = tk.Frame(self.MainFrame, bg = "#B2B2B2")
            self.BoardFrame.place(relwidth = 0.6, relheight = 0.75, relx=0.05, rely=0.2)

            self.Board = tk.Label(self.BoardFrame, text = "Dungeon", bg = "black", fg = "white", font = ("Arial", 16))
            self.Board.place(relwidth = 1, relheight = 0.05)
            self.GameButtons()
            
            if gameOver == 1:
                self.WinLabel = tk.Label(self.MainFrame, text = "Você venceu! :D", bg = "green", fg = "black", font = ("Arial", 16))
                self.WinLabel.place(relwidth=0.2, relheight=0.05, relx=0.4, rely=0.125)
                threading.Thread(target=CloseLabel, args=(self.WinLabel,)).start()
                self.ShowBoard(True)
            elif gameOver == -1:
                self.LoseLabel = tk.Label(self.MainFrame, text= "Você perdeu :/", bg="red", fg="black", font=("Arial", 16))
                self.LoseLabel.place(relwidth=0.2, relheight=0.05, relx=0.4, rely=0.125)
                threading.Thread(target=CloseLabel, args=(self.LoseLabel,)).start()
                self.ShowBoard(True)         

    def GameButtons(self):
        self.MoveButtonsFrame = tk.Frame(self.MainFrame, bg = "white")
        self.MoveButtonsFrame.place(relwidth = 0.25, relheight = 0.75, relx=0.7, rely=0.2)

        self.Up_Button = tk.Button(self.MoveButtonsFrame, text = "Up", bg = "#650000", fg = "white", font = ("Arial", 15), command=self.MoveUp)
        self.Up_Button.place(relwidth = 0.3, relheight = 0.1, relx=0.35, rely=0.03)

        self.Down_Button = tk.Button(self.MoveButtonsFrame, text = "Down", bg = "#650000", fg = "white", font = ("Arial", 15), command=self.MoveDown)
        self.Down_Button.place(relwidth = 0.3, relheight = 0.1, relx=0.35, rely=0.17)

        self.Left_Button = tk.Button(self.MoveButtonsFrame, text = "Left", bg = "#650000", fg = "white", font = ("Arial", 15), command=self.MoveLeft)
        self.Left_Button.place(relwidth = 0.3, relheight = 0.1, relx=0.03, rely=0.12)

        self.Right_Button = tk.Button(self.MoveButtonsFrame, text = "Right", bg = "#650000", fg = "white", font = ("Arial", 15), command=self.MoveRight)
        self.Right_Button.place(relwidth = 0.3, relheight = 0.1, relx=0.67, rely=0.12)

        self.ShowBoard()

    def MainScreen (self):
        self.window.title("Dungeon Runner")
        self.window.geometry("1024x768")
        self.window.resizable(False, False)
        self.window.configure(bg = "black")
        self.LoadImages()
        self.labels = list()
        self.ScreenFrames()

    def LoadImages(self):
        self.images = list()
        self.indexImages = list()
        self.player = list()
        for i in range(-1, 4):
            if i == 1:
                for i in range (4):
                    img_pil = Image.open(f"Learning/Graphic_Interfaces/DungeonRunner/Images/Player/{i}.png")
                    #img_pil = img_pil.resize((64, 64), Image.LANCZOS)
                    img_tk  = ImageTk.PhotoImage(img_pil)
                    self.player.append(img_tk)
                    #0 = cima, 1 = baixo, 2 = esquerda, 3 = direita
            else:
                img_pil = Image.open(f"Learning/Graphic_Interfaces/DungeonRunner/Images/{i}.png")
                img_tk  = ImageTk.PhotoImage(img_pil)
                self.images.append(img_tk)
                self.indexImages.append(i)
                #0 = vazio, 2 = monstro, 3 = saida, -1 = invisivel
        
        self.currentPlayer = 0

os.system("cls")
Application()
