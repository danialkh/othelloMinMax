import pygame;
import sys, time, math

#------------------------------------ Minimax vs Human ------------------------------------
#Decribe Variable
#These variables for board game gui
BLOCK_SIZE = 50
PADDING_SIZE = 5
BOARD_WIDTH = BLOCK_SIZE * 8
BOARD_HEIGHT = BLOCK_SIZE * 8 + 20
FRAME_PER_SECOND = 40
WINDOWWIDTH = BLOCK_SIZE * 10
WINDOWHEIGHT = BLOCK_SIZE * 10
XMARGIN = int(((8 * BLOCK_SIZE)) / 2)
YMARGIN = int(((8 * BLOCK_SIZE)) / 2)
HINT_TILE = 'HINT_TILE'

#These variables for players
debug = False
player = 1
victory = 0
whiteTiles = 2
blackTiles = 2
useAI = True
changed = True
AIReadyToMove = False
move = (-1, -1)

#These variables for board
board = [[0 for x in range(8)] for x in range(8)]
board[3][3] = 1
board[3][4] = 2
board[4][3] = 2
board[4][4] = 1

#Creating a board
pygame.init()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Othello')
font = pygame.font.SysFont("Helvetica", 48)
icon = pygame.image.load("boardIcon.png")
pygame.display.set_icon(icon)
boardground = pygame.image.load('boardground.png')
black = (pygame.image.load('black.png'))
white = pygame.image.load('white.png')
BGIMAGE = pygame.image.load('background.jpg')
BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
black_color= (0,0,0)
menuFont = pygame.font.SysFont("comicsansms", 15)

#newGame is starting method
def newGame():
    global changed #I said global for variable to access it.
    drawBoard()

    #This loop over until the player exit.
    while True:
        # If AI move is True, go to the AIMove method.
        if AIReadyToMove:
            start = time.time()
            AIMove()
            end = time.time()
            print('Evaluation time: {}s'.format(round(end - start, 7)))
        #Otherwise it is human so I have to control its mouse click.
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    if x >= 120 and x <= 175 and y >= 480: #That means click new game button
                        newGame()
                    elif x >= 220 and x <= 250 + menuFont.size("Exit")[0] and y > 480: #That means click exit button
                        pygame.quit()
                        sys.exit()
                    elif x >= 50 and x <= 450 and y >= 50 and y <= 450: #That means click the board
                        #I control the board x and y coordinates. When you run this game, there will be a board.
                        #The board is actual board and there will be also a board that is game board inside the actual borad
                        chessman_x = int(math.floor(x / (BLOCK_SIZE)) - 1) #convert RealBoard size to GameBoard
                        chessman_y = int(math.floor(y / (BLOCK_SIZE)) - 1) #convert RealBoard size to GameBoard
                        if debug:
                            print("player " + str(player) + " x: " + str(chessman_x) + " y: " + str(
                                chessman_y))
                        try:
                            playerMove(chessman_x, chessman_y)
                        except Exception as e:
                            print("Wrong Place")
                else:
                    pass
        if changed:
            drawBoard()
            changed = False

        if AIReadyToMove:
             AIMove()

        clock.tick(FRAME_PER_SECOND)
    self.quitGame()

#This method for text on the actual board.
def drawText(text, font, screen, x, y, rgb):
    textObj = font.render(text, 1, (rgb[0],rgb[1],rgb[2]))
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    screen.blit(textObj, textRect)

#This method draw the board in every change
def drawBoard():
    global board
    #These are for board background image and menu.
    background = pygame.Rect(0,0,WINDOWWIDTH,WINDOWHEIGHT)
    screen.blit(BGIMAGE, background)
    boardTable = pygame.Rect(BLOCK_SIZE, BLOCK_SIZE, BOARD_WIDTH, BOARD_HEIGHT)
    screen.blit(boardground, boardTable)
    menu = pygame.Rect(0, 480, WINDOWWIDTH, 20)
    pygame.draw.rect(screen, (255, 255, 255), menu)
    drawText("Restart", menuFont, screen, 120, 480 - 1, (0, 0, 0))
    drawText("Exit", menuFont, screen,220, 480 - 1, (0, 0, 0))
    drawText("Hint", menuFont, screen, 320, 480 - 1, (0, 0, 0)) ## However it is not working

    #These line for GameBoard
    for i in range(9):
        startx = (i * 50) + BLOCK_SIZE
        starty = BLOCK_SIZE
        endx = (i * 50) + BLOCK_SIZE
        endy = BLOCK_SIZE + (8 * 50)
        pygame.draw.line(screen, black_color, (startx, starty), (endx, endy))
    for i in range(9):
        startx = BLOCK_SIZE
        starty = (i * 50) + BLOCK_SIZE
        endx = BLOCK_SIZE + (8 * 50)
        endy = (i * 50) + BLOCK_SIZE
        pygame.draw.line(screen, black_color, (startx, starty), (endx, endy))

    #gameBoard(boad) is 2D array.
    # If an element in the array is 1 that means the element is black otherwise white.
    for row in range(0, 8):
        for col in range(0, 8):
            block = board[row][col]
            chessman_size = BLOCK_SIZE - 2 * PADDING_SIZE
            chessman = pygame.Rect(row * BLOCK_SIZE + PADDING_SIZE + BLOCK_SIZE, col * BLOCK_SIZE + PADDING_SIZE + BLOCK_SIZE,chessman_size, chessman_size)
            if block == 1:
                screen.blit(black, chessman)
            elif block == 2:
                screen.blit(white, chessman)
            elif block == 0:
                pass
            else:
                sys.exit('Error occurs - player number incorrect!')

    if victory == -1:
        drawText("Draw! " + str(whiteTiles) + ":" + str(blackTiles), font, screen, 50, 10, (255, 128, 0))
    elif victory == 1:
        if useAI:
            drawText("You Won! " + str(blackTiles) + ":" + str(whiteTiles), font, screen, 50, 10, (255, 128, 0))
    elif victory == 2:
        if useAI:
            drawText("MinMax Won! " + str(whiteTiles) + ":" + str(blackTiles), font, screen, 50, 10, (255, 128, 0))

    pygame.display.update()


#I check the player's move
def playerMove(x, y):
    global AIReadyToMove
    if victory != 0 or (useAI and player != 1):
        return
    performMove(x, y)
    if useAI and player == 2:
        AIReadyToMove = True
        if debug:
            print("AI is ready to move!")


def performMove(x, y):
    global changed
    global player

    if board[x][y] != 0:
        print(" - Block has already been occupied!")
    else:
        numFlipped = isAvaible(board, x, y, player, PLAYMODE=True)
        if debug:
            print("Flipped " + str(numFlipped) + " pieces!")
        changed = True

        # check game ending
        allTiles = [item for sublist in board for item in sublist]
        emptyTiles = sum(1 for tile in allTiles if tile == 0)
        whiteTiles = sum(1 for tile in allTiles if tile == 2)
        blackTiles = sum(1 for tile in allTiles if tile == 1)
        print("Current state - empty: " + str(emptyTiles) + " white: " + str(
            whiteTiles) + " black: " + str(blackTiles))

        if debug:
            for x in range(0, 8):
                for y in range(0, 8):
                    print(str(board[x][y]) + " ", end='')
                print('')

        if whiteTiles < 1 or blackTiles < 1 or emptyTiles < 1:
            endGame(whiteTiles, blackTiles)
            return
        movesFound = moveCanBeMade(board, 3 - player)
        if not movesFound:
            if debug:
                print("Player " + str(3 - player) + " cannot move!")
            movesFound = moveCanBeMade(board, player)
            if not movesFound:
                if debug:
                    print("Player " + str(player) + "cannot move either!")
                endGame(whiteTiles, blackTiles)
                return
            else:
                if debug:
                    print("Player " + str(player) + " can move, then move!")
                if useAI and player == 2:
                    performMoveMinMax()
                changed = True
        else:
            player = 3 - player
            changed = True

#It is check the move can be made with isAvaible method.
def moveCanBeMade(board, playerID):
    movesFound = False
    for row in range(0, 8):
        for col in range(0, 8):
            if movesFound:
                continue
            elif board[row][col] == 0:
                numAvailableMoves = isAvaible(board, row, col, playerID, PLAYMODE=False)
                if numAvailableMoves > 0:
                    movesFound = True
    return movesFound

#This method goes to AI.
def AIMove():
    global AIReadyToMove

    performMoveMinMax()
    AIReadyToMove = False

def endGame(whiteTile, blackTile):
    global victory
    global changed
    global whiteTiles
    global blackTiles

    if whiteTile > blackTile:
        victory = 2
    elif whiteTile < blackTile:
        victory = 1
    else:
        victory = -1
    changed = True
    whiteTiles = whiteTile
    blackTiles = blackTile

#This method checks the game rules.
def isAvaible(board, row, col, playerID, PLAYMODE=True):
    global changed
    global player
    global debug
    global victory
    global whiteTiles
    global blackTiles

    if PLAYMODE:
        board[row][col] = player
    count = 0
    __column = board[row]
    __row = [board[i][col] for i in range(0, 8)]
    if playerID in __column[:col]:
        changes = []
        searchCompleted = False
        for i in range(col - 1, -1, -1):
            if searchCompleted:
                continue
            piece = __column[i]
            if piece == 0:
                changes = []
                searchCompleted = True
            elif piece == playerID:
                searchCompleted = True
            else:
                changes.append(i)
        if searchCompleted:
            count += len(changes)
            if PLAYMODE:
                for i in changes:
                    board[row][i] = player


    if playerID in __column[col:]:
        changes = []
        searchCompleted = False

        for i in range(col + 1, 8, 1):
            if searchCompleted:
                continue
            piece = __column[i]
            if piece == 0:
                changes = []
                searchCompleted = True
            elif piece == playerID:
                searchCompleted = True
            else:
                changes.append(i)
        if searchCompleted:
            count += len(changes)
            if PLAYMODE:
                for i in changes:
                    board[row][i] = player



    if playerID in __row[:row]:
        changes = []
        searchCompleted = False

        for i in range(row - 1, -1, -1):
            if searchCompleted:
                continue
            piece = __row[i]
            if piece == 0:
                changes = []
                searchCompleted = True
            elif piece == playerID:
                searchCompleted = True
            else:
                changes.append(i)
        if searchCompleted:
            count += len(changes)
            if PLAYMODE:
                for i in changes:
                    board[i][col] = player



    if playerID in __row[row:]:
        changes = []
        searchCompleted = False

        for i in range(row + 1, 8, 1):
            if searchCompleted:
                continue
            piece = __row[i]
            if piece == 0:
                changes = []
                searchCompleted = True
            elif piece == playerID:
                searchCompleted = True
            else:
                changes.append(i)
        if searchCompleted:
            count += len(changes)
            if PLAYMODE:
                for i in changes:
                    board[i][col] = player

    i = 1
    ulDiagonal = []
    while row - i >= 0 and col - i >= 0:
        ulDiagonal.append(board[row - i][col - i])
        i += 1
    if playerID in ulDiagonal:
        changes = []
        searchCompleted = False
        for i in range(0, len(ulDiagonal)):
            piece = ulDiagonal[i]
            if searchCompleted:
                continue
            if piece == 0:
                changes = []
                searchCompleted = True
            elif piece == playerID:
                searchCompleted = True
            else:
                changes.append((row - (i + 1), col - (i + 1)))
        if searchCompleted:
            count += len(changes)
            if PLAYMODE:
                for i, j in changes:
                    board[i][j] = player



    i = 1
    urDiagonal = []
    while row + i < 8 and col - i >= 0:
        urDiagonal.append(board[row + i][col - i])
        i += 1
    if playerID in urDiagonal:
        changes = []
        searchCompleted = False
        for i in range(0, len(urDiagonal)):
            piece = urDiagonal[i]
            if searchCompleted:
                continue
            if piece == 0:
                changes = []
                searchCompleted = True
            elif piece == playerID:
                searchCompleted = True
            else:
                changes.append((row + (i + 1), col - (i + 1)))
        if searchCompleted:
            count += len(changes)
            if PLAYMODE:
                for i, j in changes:
                    board[i][j] = player


    i = 1
    llDiagonal = []
    while row - i >= 0 and col + i < 8:
        llDiagonal.append(board[row - i][col + i])
        i += 1
    if playerID in llDiagonal:
        changes = []
        searchCompleted = False

        for i in range(0, len(llDiagonal)):
            piece = llDiagonal[i]
            if searchCompleted:
                continue
            if piece == 0:
                changes = []
                searchCompleted = True
            elif piece == playerID:
                searchCompleted = True
            else:
                changes.append((row - (i + 1), col + (i + 1)))
        if searchCompleted:
            count += len(changes)
            if PLAYMODE:
                for i, j in changes:
                    board[i][j] = player


    i = 1
    lrDiagonal = []
    while row + i < 8 and col + i < 8:
        lrDiagonal.append(board[row + i][col + i])
        i += 1
    if playerID in lrDiagonal:
        changes = []
        searchCompleted = False

        for i in range(0, len(lrDiagonal)):
            piece = lrDiagonal[i]
            if searchCompleted:
                continue
            if piece == 0:
                changes = []
                searchCompleted = True
            elif piece == playerID:
                searchCompleted = True
            else:
                changes.append((row + (i + 1), col + (i + 1)))

        if searchCompleted:
            count += len(changes)
            if PLAYMODE:
                for i, j in changes:
                    board[i][j] = player

    if count == 0 and PLAYMODE:
        board[row][col] = 0

    return count

#This method for Minimax Algorithm.
def performMoveMinMax():
    tmpBoard = [row[:] for row in board]
    startTime = time.time()
    timeElapsed = 0
    depth = 2 #depth is 2.
    optimalMove = (-1, -1)
    optimalBoard = tmpBoard
    stop = False #this value for ending the minmax algorithm. If the successboard is true then stop the minmax algorithm.
    currentLevel =0
    # I did 'timeElapsed < 5' because the minimax algorithm time will be less than 5 in a move.
    while not stop and timeElapsed < 5:
        (stop, optimalBoard) = miniMax(tmpBoard, currentLevel, depth,player , -math.inf, math.inf,stop);
        endTime = time.time()
        timeElapsed += endTime - startTime
        startTime = endTime
        #depth += 1 (actually when you increase depth in every move, the minimax algorithm gives better results.)

    for row in range(0, 8):
        for col in range(0, 8):
            if tmpBoard[row][col] != optimalBoard[row][col]:
                optimalMove = (row, col)

    move = optimalMove
    performMove(move[0], move[1])

#For minimax algorithm
def miniMax(board, currentLevel, maxLevel, player, alpha, beta,stop):
    all = [item for sublist in board for item in sublist]
    white = sum(1 for tile in all if tile == 2)
    black = sum(1 for tile in all if tile == 1)
    successBoards = []

    if (not moveCanBeMade(board, player) or currentLevel == maxLevel ):
        return (stop, board)
    if white > black:
        diff = (white / (black + white)) * 100
    else:
        diff = - (black / (black + white)) * 100
    # Mobility controls how many steps can player move.
    # first player is black
    # second player is white
    if moveCanBeMade(board, 1) + moveCanBeMade(board, 2) == 0:
        mobility = 0
    else:
        mobility = 100 * moveCanBeMade(board, 2) / (moveCanBeMade(board, 2) + moveCanBeMade(board, 1))

    # Update the sucessorBoard
    for row in range(0, 8):
        for col in range(0, 8):
            if board[row][col] == 0:
                numAvailableMoves = isAvaible(board, row, col, player, PLAYMODE=False)
                if numAvailableMoves > 0:
                    successorBoard = [row[:] for row in board]
                    successorBoard[row][col] = player
                    successBoards.append(successorBoard)

    if len(successBoards) == 0:
        stopDigging = True
        return (stopDigging, board)
    bestBoard = None

    #If player is 2 that means white, check the alpha value.
    #If the value is smaller than utility update bestBoard
    if player == 2:
        maxValue = -math.inf #alpha
        for i in range(0, len(successBoards)):
            stop, boardS = miniMax(successBoards[i], currentLevel + 1, maxLevel, 1, alpha,beta,stop)
            best = diff + mobility #utility is heuristics for nonfinal node.
            if best > maxValue:
                maxValue = best
                bestBoard = successBoards[i]
            alpha = max(alpha, best)
            if best >= beta:
                return (stop, boardS)
    # If player is 1 that means white, check the beta value.
    # If the value is greather than utility update bestBoard
    else:
        minValue = math.inf #beta
        for i in range(0, len(successBoards)):
            stop, boardS = miniMax(successBoards[i], currentLevel + 1, maxLevel, 2, alpha,beta,stop)
            utility = diff  + mobility
            if utility < minValue:
                minValue = utility
                bestBoard = successBoards[i]
            beta = min(beta, utility)
            if utility <= alpha:
                return (stop, boardS)

    return (stop, bestBoard)


if __name__ == '__main__':
	newGame()