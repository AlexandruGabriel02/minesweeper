import pygame
import sys
import random
import tkinter as tk

pygame.init()

#constants
BOMB_COUNT = 10
CELL_WIDTH = 32
CELL_HEIGHT = 32
CELL_COUNT_X = 10
CELL_COUNT_Y = 8
FRAME_HEIGHT = 64
SCREEN_WIDTH = CELL_WIDTH * CELL_COUNT_X
SCREEN_HEIGHT = CELL_HEIGHT * CELL_COUNT_Y + FRAME_HEIGHT

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minesweeper")

clock = pygame.time.Clock()
time = 0

textures = [pygame.image.load(f"assets/minesweeper_{i}.png") for i in range(16)]
flag = pygame.image.load("assets/frame_flag.png")
timer = pygame.image.load("assets/timer.png")
restart = pygame.image.load("assets/restart_button.png")

flag_count = BOMB_COUNT

class Button():
    def __init__(self, texture, WIDTH, HEIGHT, position):
        self.texture = texture
        self.width = WIDTH
        self.height = HEIGHT
        self.position = position
    def draw(self):
        window.blit(self.texture, self.position)
    def canClick(self):
        (mousePosX, mousePosY) = pygame.mouse.get_pos()
        if mousePosX <= self.position[0] + self.width and mousePosX >= self.position[0]:
            if mousePosY <= self.position[1] + self.height and mousePosY >= self.position[1]:
                return True
        return False

class Cell():
    def __init__(self, texture, WIDTH, HEIGHT):
        self.isRevealed = False
        self.isFlagged = False
        self.type = 0 #empty cell
        self.texture = textures[0]
        self.width = WIDTH
        self.height = HEIGHT
        self.texture = texture
    def Reveal(self):
        self.isRevealed = True
        if self.type == 0: #empty cell
            self.texture = textures[1]
        elif self.type < 9: #digits
            self.texture = textures[self.type + 7]
        elif self.type == 9:
            self.texture = textures[5] #bomb
        else:
            self.texture = textures[6] #exploded bomb
    def Flag(self):
        global flag_count
        if not self.isFlagged:
            self.isFlagged = True
            self.texture = textures[2] #flag
            flag_count -= 1
        else:
            self.isFlagged = False
            self.texture = textures[0] #empty
            flag_count += 1
    def draw(self, position):
        window.blit(self.texture, position)


restartButton = Button(restart, restart.get_width(), restart.get_height(),
                       (SCREEN_WIDTH // 2 - restart.get_width() // 2, FRAME_HEIGHT // 2 - restart.get_height() // 2))
grid = [ [Cell(textures[0], CELL_WIDTH, CELL_HEIGHT) for i in range(CELL_COUNT_X)] for j in range(CELL_COUNT_Y) ]

def drawWindow():
    LIGHT_BLUE = (102, 153, 255)
    window.fill(LIGHT_BLUE)

    font = pygame.font.SysFont("Helvetica", 32)

    window.blit(flag, (20, (FRAME_HEIGHT - flag.get_height()) // 2) )
    window.blit(timer, (SCREEN_WIDTH - 20 - timer.get_width(), (FRAME_HEIGHT - timer.get_height()) // 2) )
    window.blit(font.render(str(time), True, (0, 0, 0)), (SCREEN_WIDTH - 70 - timer.get_width(), (FRAME_HEIGHT - timer.get_height()) // 2))
    window.blit(font.render(str(flag_count), True, (0, 0, 0)), (75 , (FRAME_HEIGHT - flag.get_height()) // 2) )
    restartButton.draw()

    row = 0
    for i in range(FRAME_HEIGHT, SCREEN_HEIGHT, CELL_HEIGHT):
        col = 0
        for j in range(0, SCREEN_WIDTH, CELL_WIDTH):
            grid[row][col].draw((j, i))
            col += 1
        row += 1

    pygame.display.update()

def Extend(row, col, count, maxCount):
    if count <= maxCount:
        grid[row][col].Reveal()
        directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]
        random.shuffle(directions)

        valid = True
        nextRow = 0
        nextCol = 0
        for dir in directions:
            nextRow = row + dir[0]
            nextCol = col + dir[1]
            if nextRow < CELL_COUNT_Y and nextCol < CELL_COUNT_X and nextRow >= 0 and nextCol >= 0:
                if not grid[nextRow][nextCol].isRevealed:
                    valid = False
                    break

        if valid:
            Extend(nextRow, nextCol, count + 1, maxCount)

def firstClick():
    isRunning = True
    while isRunning:
        drawWindow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
                sys.exit()
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if restartButton.canClick():
                    Reset()

        if restartButton.canClick():
            restartButton.texture = pygame.image.load("assets/restart_button_2.png")
        else:
            restartButton.texture = restart

        (mousePosX, mousePosY) = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()[0]

        if mousePressed and mousePosY > FRAME_HEIGHT:
            col = mousePosX // CELL_WIDTH
            row = mousePosY // CELL_HEIGHT - FRAME_HEIGHT // CELL_HEIGHT

            Extend(row, col, 0, random.randint(1, min(6, CELL_COUNT_X * CELL_COUNT_Y - BOMB_COUNT)))
            isRunning = False


def Fill(row, col):
    grid[row][col].Reveal()
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]
    for dir in directions:
        nextRow = row + dir[0]
        nextCol = col + dir[1]
        if nextRow < CELL_COUNT_Y and nextCol < CELL_COUNT_X and nextRow >= 0 and nextCol >= 0:
            if grid[nextRow][nextCol].type == 0 and not grid[nextRow][nextCol].isRevealed:
                Fill(nextRow, nextCol)

def Generate():

    randPos = []
    for row in range(CELL_COUNT_Y):
        for col in range(CELL_COUNT_X):
            valid = 1
            directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]
            for dir in directions:
                nextRow = row + dir[0]
                nextCol = col + dir[1]
                if nextRow < CELL_COUNT_Y and nextCol < CELL_COUNT_X and nextRow >= 0 and nextCol >= 0:
                    if grid[nextRow][nextCol].isRevealed or grid[row][col].isRevealed:
                        valid = 0
            if valid:
                randPos.append((row, col))

    random.shuffle(randPos)

    for i in range(BOMB_COUNT):
        row = randPos[i][0]
        col = randPos[i][1]
        grid[row][col].type = 9 #bomb

    for row in range(CELL_COUNT_Y):
        for col in range(CELL_COUNT_X):
            directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]
            for dir in directions:
                nextRow = row + dir[0]
                nextCol = col + dir[1]
                if nextRow < CELL_COUNT_Y and nextCol < CELL_COUNT_X and nextRow >= 0 and nextCol >= 0:
                    if grid[nextRow][nextCol].type == 9 and grid[row][col].type != 9:
                        grid[row][col].type += 1

    ok = 0
    for row in range(CELL_COUNT_Y):
        for col in range(CELL_COUNT_X):
            if grid[row][col].isRevealed:
                Fill(row, col)
                ok = 1
            if ok:
                break
        if ok:
            break

    for row in range(CELL_COUNT_Y):
        for col in range(CELL_COUNT_X):
            directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]
            for dir in directions:
                nextRow = row + dir[0]
                nextCol = col + dir[1]
                if nextRow < CELL_COUNT_Y and nextCol < CELL_COUNT_X and nextRow >= 0 and nextCol >= 0:
                    if not grid[row][col].isRevealed and grid[nextRow][nextCol].isRevealed and grid[nextRow][nextCol].type == 0:
                        grid[row][col].Reveal()

def getMouseInput(event):
    (mousePosX, mousePosY) = pygame.mouse.get_pos()

    col = mousePosX // CELL_WIDTH
    row = mousePosY // CELL_HEIGHT - FRAME_HEIGHT // CELL_HEIGHT

    if event.button == 1 and mousePosY > FRAME_HEIGHT and grid[row][col].isFlagged == False:
        grid[row][col].Reveal()
        if grid[row][col].type == 0:

            Fill(row, col)
            for row in range(CELL_COUNT_Y):
                for col in range(CELL_COUNT_X):
                    directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]
                    for dir in directions:
                        nextRow = row + dir[0]
                        nextCol = col + dir[1]
                        if nextRow < CELL_COUNT_Y and nextCol < CELL_COUNT_X and nextRow >= 0 and nextCol >= 0:
                            if not grid[row][col].isRevealed and grid[nextRow][nextCol].isRevealed and grid[nextRow][nextCol].type == 0:
                                grid[row][col].Reveal()
    elif event.button == 3 and mousePosY > FRAME_HEIGHT:
        if not grid[row][col].isRevealed:
            grid[row][col].Flag()


def gameOver():
    for row in range(CELL_COUNT_Y):
        for col in range(CELL_COUNT_X):
            if grid[row][col].isRevealed and grid[row][col].type == 9:
                grid[row][col].type = 10 #exploded bomb
                return -1 #has lost

    for row in range(CELL_COUNT_Y):
        for col in range(CELL_COUNT_X):
            if grid[row][col].isRevealed == False and grid[row][col].type != 9:
                return 0 #still going

    return 1 #has won

def gameLoop():
    isRunning = True
    hasWon = False
    hasLost = False

    start_time = pygame.time.get_ticks()
    while isRunning:
        global time
        time = (pygame.time.get_ticks() - start_time) // 1000
        clock.tick(30)

        drawWindow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                getMouseInput(event)
                if restartButton.canClick():
                    return

        gameState = gameOver()
        if gameState == 1:
            hasWon = True
            for row in range(CELL_COUNT_Y):
                for col in range(CELL_COUNT_X):
                    if grid[row][col].isRevealed == False and grid[row][col].isFlagged == False:
                        grid[row][col].Flag()
            isRunning = False
        elif gameState == -1:
            hasLost = True
            for row in range(CELL_COUNT_Y):
                for col in range(CELL_COUNT_X):
                    if grid[row][col].type >= 9:
                        grid[row][col].Reveal()
            isRunning = False
            break

        if restartButton.canClick():
            restartButton.texture = pygame.image.load("assets/restart_button_2.png")
        else:
            restartButton.texture = restart

    if hasWon or hasLost:
        isRunning = True
        while isRunning:
            clock.tick(20)
            drawWindow()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                    sys.exit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if restartButton.canClick():
                        return

            if restartButton.canClick():
                restartButton.texture = pygame.image.load("assets/restart_button_2.png")
            else:
                restartButton.texture = restart


def changeDiff(bomb_count, cell_count_x, cell_count_y, root):
    global BOMB_COUNT, CELL_COUNT_X, CELL_COUNT_Y, SCREEN_WIDTH, SCREEN_HEIGHT, window, CELL_WIDTH, CELL_HEIGHT, FRAME_HEIGHT
    BOMB_COUNT = bomb_count
    CELL_COUNT_X = cell_count_x
    CELL_COUNT_Y = cell_count_y
    SCREEN_WIDTH = CELL_WIDTH * CELL_COUNT_X
    SCREEN_HEIGHT = CELL_HEIGHT * CELL_COUNT_Y + FRAME_HEIGHT

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    root.destroy()

def Reset():
    root = tk.Tk()
    root.geometry("250x150")
    root.title("Difficulty")

    frame = tk.Frame(root)
    label = tk.Label(root, text="Select the difficulty:", height=2)
    button1 = tk.Button(frame, text="Beginner", command=lambda: changeDiff(10, 10, 8, root))
    button2 = tk.Button(frame, text="Intermediate", command=lambda: changeDiff(40, 16, 16, root))
    button3 = tk.Button(frame, text="Expert", command=lambda: changeDiff(99, 30, 16, root))

    frame.place(relx=0.2, rely=0.25, relheight=0.6, relwidth=0.6)
    label.pack()
    button1.pack()
    button2.pack()
    button3.pack()

    root.mainloop()

    global grid, flag_count, time, CELL_COUNT_X, CELL_COUNT_Y, CELL_WIDTH, CELL_HEIGHT, restart, restartButton
    grid = [[Cell(textures[0], CELL_WIDTH, CELL_HEIGHT) for i in range(CELL_COUNT_X)] for j in range(CELL_COUNT_Y)]
    flag_count = BOMB_COUNT
    time = 0
    restartButton = Button(restart, restart.get_width(), restart.get_height(),
                        (SCREEN_WIDTH // 2 - restart.get_width() // 2, FRAME_HEIGHT // 2 - restart.get_height() // 2))


def main():
    isRunning = True
    while isRunning:
        firstClick()
        Generate()
        gameLoop()
        Reset()

main()