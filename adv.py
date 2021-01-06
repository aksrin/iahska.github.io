import pygame
import numpy
from numpy import *
from queue import PriorityQueue
from copy import deepcopy

#colors
b = (0, 0, 0) #grid lines
w = (255, 255, 255) #empty grid block
bl=(0,0,255) #mage
re=(255,0,0) #hero
gr=(0,255,0) #wumpus
da=(50,50,50) #pit
si = (150, 150, 150) #empty space legal to move to
ye = (255,255,0) #killable wumpus
pi= (255,0,255) #killable hero
cy =(0,255,255) #killable mage
me=(100,100,100) #pit legal to move to

#window size
H = 900
W = 900

#spaces are (x,y)

class space:
    def __init__(self,x,y,p):
        self.x=x
        self.y=y
        self.p=p

    def __repr__(self):
        return "X: "+str(self.x)+" Y: "+str(self.y)#+" P: "+str(self.p.name)

    def __lt__(self,other):
        return ( (self.x) < (other.x) )
        
class piece:
    killed=False;

    #team 0: player 1 - Player
    #team 1: player 2 - AI
    #team 2: pit
    
    #name 0 wumpus
    #name 1 hero
    #name 2 mage
    #name 3 pit

    def __init__(self,team,name):
        self.team=team
        self.name=name

    def __repr__(self):
        if self.team == 0:
            if self.name == 0:
                return "W"
            if self.name == 1:
                return "H"
            if self.name == 2:
                return "M"
        else:
            if self.name == 0:
                return "w"
            if self.name == 1:
                return "h"
            if self.name == 2:
                return "m"
            else:
                return "*"


class node:
    def __init__(self,board,i,f,parent,child,value):
        self.board = board
        self.i = i
        self.f = f
        self.parent = parent
        self.child = child
        self.value = value

    def __lt__(self,other):
        return ( (self.value) < (other.value))
        
def legal(i,f):
    
    if(i == None):
        return False
    
    if (f.p==None):
        cardinal=(((i.x-f.x)*(i.x-f.x)+(i.y-f.y)*(i.y-f.y))==1)
        diagonal=(((i.x-f.x)*(i.x-f.x)+(i.y-f.y)*(i.y-f.y))==2)   
        if (cardinal or diagonal):
            return True
        return False
    
    if (f.p != None):
        if (f.p.team == i.p.team):
            return False
        
    cardinal=(((i.x-f.x)*(i.x-f.x)+(i.y-f.y)*(i.y-f.y))==1)
    diagonal=(((i.x-f.x)*(i.x-f.x)+(i.y-f.y)*(i.y-f.y))==2)
        
    if (cardinal or diagonal):
        return True
    return False


def printBoard(board,d):
    for row in range(d*3):
        for col in range(d*3):
            if (board[row][col] != None):
                if(board[row][col].p != None):
                    print (board[row][col].p,end=" ")
                else: print("-",end=" ")
        print()
    print()
   
def setUpBoard(dimensions):
    result=[]
    for row in range(dimensions*3):
        result2=[]
        for col in range(dimensions*3):
            #print("Row: ",row, "Col: ",col)
            if (row==0):
                if col%3==0:
                    result2.append(space(col,row,piece(0,0)))
                if col%3==1:
                    result2.append(space(col,row,piece(0,1)))
                if col%3==2:
                    result2.append(space(col,row,piece(0,2)))
            elif(row==dimensions*3-1):
                if col%3==0:
                    result2.append(space(col,row,piece(1,0)))
                if col%3==1:
                    result2.append(space(col,row,piece(1,1)))
                if col%3==2:
                    result2.append(space(col,row,piece(1,2)))
            
        placeOfPits=[]
        if (row != 0) and (row != dimensions*3 - 1):
            for i in range(dimensions-1):
                randomNum=random.randint(dimensions*3)
                while (randomNum in placeOfPits):
                    randomNum=random.randint(dimensions*3)
                #print (row,randomNum)
                placeOfPits.append(randomNum)
            for x in range(dimensions*3):
                if x in placeOfPits:
                    result2.append(space(x,row,piece(2,3)))
                else:
                    result2.append(space(x,row,None))
                
        result.append(result2)
    return result

def drawBoard(board,active,dimensions):
    blockSize=(900/(dimensions*3)) - 1
    for row in range(dimensions*3):
        for col in range(dimensions*3):
            rect = pygame.Rect(col*(blockSize+1), row*(blockSize+1), blockSize, blockSize)
            if active==None:
                if board[row][col].p==None:
                    pygame.draw.rect(SCREEN, w, rect)
                else:
                    if board[row][col].p.name==0:
                        pygame.draw.rect(SCREEN, gr, rect)
                    if board[row][col].p.name==1:
                        pygame.draw.rect(SCREEN, re, rect)
                    if board[row][col].p.name==2:
                        pygame.draw.rect(SCREEN, bl, rect)
                    if board[row][col].p.name==3:
                        pygame.draw.rect(SCREEN, da, rect)
            else:
                if board[row][col].p==None:
                    s=board[row][col]
                    if legal(active,s)==True:
                        pygame.draw.rect(SCREEN, si, rect)
                    else:                    
                        pygame.draw.rect(SCREEN, w, rect)
                else:                
                    if board[row][col].p.name==0:
                        s=board[row][col]
                        if legal(active,s)==True:
                            pygame.draw.rect(SCREEN, ye, rect)
                        else:
                            pygame.draw.rect(SCREEN, gr, rect)
                    if board[row][col].p.name==1:
                        s=board[row][col]
                        if legal(active,s)==True:
                            pygame.draw.rect(SCREEN, pi, rect)
                        else:                    
                            pygame.draw.rect(SCREEN, re, rect)
                    if board[row][col].p.name==2:
                        s=board[row][col]
                        if legal(active,s)==True:
                            pygame.draw.rect(SCREEN, cy, rect)
                        else:                    
                            pygame.draw.rect(SCREEN, bl, rect)
                    if board[row][col].p.name==3:
                        s=board[row][col]
                        if legal(active,s)==True:
                            pygame.draw.rect(SCREEN, me, rect)
                        else:                    
                            pygame.draw.rect(SCREEN, da, rect)


def battle(t1, t2):
    if (t1 == t2): #Same
        return False, False
    if (t2 == 3): #Pit
        return False, True
    if (t1 == 1): #Hero
        if (t2 == 2):
            return False, True
        else: return True, False
    elif (t1 == 2): #Mage
        if (t2 == 0):
            return False, True
        else: return True, False
    else:
        if (t2 == 1):
            return False, True
        else: return True, False


def move(start, end):
    #print()
    #print()
    #if (end.p == None):
    #    print("end.p None")
    #if (start.p == None):
    #    print("start.p None")
    #if (end.p.name == None):
    #    print("end.p.name None")
    #if (start.p.name == None):
    #    print("start.p.name None")
    
    if (end.p != None):
    #    print("bypass")
        results = battle(start.p.name,end.p.name)

        if (results[0]): #Moving Piece won
            end.p = start.p
            start.p = None

        else: #Moving Piece lost
            if(results[1]):
                start.p = None
            else:
                start.p = None
                end.p = None

    else:
        end.p = start.p
        start.p = None


def selectCell(board,blockSize):
    
    pos = pygame.mouse.get_pos() #User clicks the mouse. Get the position
    
    column = int(pos[0] // (blockSize+1)) #Change the x/y screen coordinates to grid coordinates
    row = int(pos[1] // (blockSize+1))
    #print("Click ",pos, "Grid coordinates: ", row, column)
    
    return board[row][column]


def countPieces(b,dimensions,team):
    count = 0
    if (team):
        for row in range(dimensions*3):
            for col in range(dimensions*3):
                if b[row][col].p != None:
                    if b[row][col].p.team != None:
                       if b[row][col].p.team == 0:
                           count = count + 1
    else:
        for row in range(dimensions*3):
            for col in range(dimensions*3):
                if b[row][col].p != None:
                    if b[row][col].p.team != None:
                       if b[row][col].p.team == 1:
                           count = count + 1
    return count


def detectWin(b,d,t):
    p_1 = countPieces(b,d,t)
    p_2 = countPieces(b,d,not(t))

    if (p_1 == 0) and (p_1 == p_2):
        return 3
    elif (p_1 == 0):
        return 2
    elif (p_2 == 0):
        return 1
    else:
        return 0
    

def heuristic(b, d):
    return countPieces(b,d,False) - countPieces(b,d,True)


def phantomBoard(b):
    b2 = deepcopy(b)
    return b2
    

def findLegals(b,r,c,d,neighbors):
    
    if (c - 1 >= 0): #Left
        if legal(b[r][c],b[r][c-1]):
            print("L")
            neighbors.append(b[r][c-1])
    
    if (c + 1 <= d*3-1): #Right
        if legal(b[r][c],b[r][c+1]):
            print("R")
            neighbors.append(b[r][c+1])
    
    if (r - 1 >= 0): #Up
        if legal(b[r][c],b[r-1][c]):
            print("U")
            neighbors.append(b[r-1][c])
    
    if (r + 1 <= d*3-1): #Down
        if legal(b[r][c],b[r+1][c]):
            print("D")
            neighbors.append(b[r+1][c])
    
    if (r - 1 >= 0) and (c - 1 >= 0): #Up-Left
        if legal(b[r][c],b[r-1][c-1]):
            print("UL")
            neighbors.append(b[r-1][c-1])
    
    if (r - 1 >= 0) and (c + 1 <= d*3-1): #Up-Right
        if legal(b[r][c],b[r-1][c+1]):
            print("UR")
            neighbors.append(b[r-1][c+1])
    
    if (r + 1 <= d*3-1) and (c - 1 >= 0): #Down-Left
        if legal(b[r][c],b[r+1][c-1]):
            print("DL")
            neighbors.append(b[r+1][c-1])
    
    if (r + 1 <= d*3-1) and (c + 1 <= d*3-1): #Down-Right
        if legal(b[r][c],b[r+1][c+1]):
            print("DR")
            neighbors.append(b[r+1][c+1])

    return neighbors


def miniMax(root, d, a, beta, maxPlayer, dimension,board):
    b = root.board
    #printBoard(b,dimension)
    #printBoard(board,dimension)
    #print()
    
    if (d == 0) or (detectWin(b,dimension,True) > 0):
        print("Leaf")
        return heuristic(b,dimension), root

    n = []
    if maxPlayer: #Ai's Turn
        value = -1000#numpy.inf
        pQ = PriorityQueue()
        newBoard = []
        for row in range(dimension*3): #Go through rows
            for col in range(dimension*3): #go through columns
                if b[row][col].p != None: #if current piece at space is not none
                    if b[row][col].p.team == 1: #if the team of the piece is the same as the AI
                        n = findLegals(b,row,col,dimension,n) #create an array of all legal spaces
                        count = 0
                        for i in n: #Iterate through all legals spaces
                            print (i)
                            newBoard = []
                            newBoard = phantomBoard(board) #Creates a new board copy
                            print("Phantom Board Copy")
                            printBoard(newBoard,dimension)
                            move(newBoard[row][col],newBoard[i.y][i.x])
                            #count = count + 1
                            #print(count)
                            print("Board Movement")
                            printBoard(newBoard,dimension)
                            print("OG Board")
                            printBoard(board,dimension)
                            nextNode = node(newBoard, newBoard[row][col], newBoard[i.y][i.x], root,None,heuristic(newBoard,dimension))
                            pQ.put(( heuristic(newBoard,dimension), nextNode ))
                            newBoard = []
                            print()
                        n = []
                            

        while not pQ.empty():
            
            current = pQ.get()
            mini, temp = miniMax(current[1], d-1, a, beta, False, dimension,board)
            if mini > a:
                temp.parent.child = temp
            value = max(value,mini)    
            a = max(a,value)
            if a >= beta:
                break

        return value, root

    else: #Player's Turn
        value = 1000#numpy.inf
        pQ = PriorityQueue()
        for row in range(dimension*3):
            for col in range(dimension*3):
                if b[row][col].p != None:
                    if b[row][col].p.team == 0:
                        n = findLegals(b,row,col,dimension,n)
                        
                        for i in n:
                            newBoard = []
                            newBoard = phantomBoard(b)
                            move(newBoard[row][col],newBoard[i.y][i.x])
                            nextNode = node(newBoard, newBoard[row][col], newBoard[i.y][i.x], root,None,heuristic(newBoard,dimension))
                            pQ.put(( heuristic(newBoard,dimension), nextNode ))
                            newBoard = []
                            

        while not pQ.empty():
            
            current = pQ.get()
            mini, temp = miniMax(current[1], d-1, a, beta, True, dimension,board)
            if mini < beta:
                temp.parent.child = temp
            value = min(value,mini)
            beta = min(beta,value)
            if a >= beta:
                break
        
        return value, root            
        


def main():

    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((H,W))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(b)
    state = 0
    dimension = 2
    #unlike the spaces, the board is (y,x)
    board = setUpBoard(dimension)
    pygame.display.flip()
    blockSize=(900/(dimension*3)) - 1
    active = None
    destination = None
    update = True
    nextTurn = True
    newBoard = []
    n = []
    
    #state 0: player 1 turn
    #state 1: player 2 turn
    #state 2: player 1 win
    #state 3: player 2 win
    #state 4: draw

    #for row in board:
        #for col in row:
            #print(col.p)
        #print()

    drawBoard(board,active,dimension)
    
    while state<2:

        update = False
        nextTurn = False
        
        if (state == 0):
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    state = 5

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    s = selectCell(board,blockSize)

                    if active == None: #Nothing Currently Selected
                        if (s.p != None): #Selection is not an empty space
                            if (s.p.team == state): #Selection is on the same team
                                active = s
                                update = True
                                
                                #print("Active: ",active.x,active.y)
                    else:
                        destination = s
                        #print("Destination: ", destination.x,destination.y)

                    if (destination != None):
                        if legal(active,destination) == True:
                            move(active,destination)
                            #print("Moved")
                            active = None
                            destination = None
                            update = True
                            nextTurn = True
                            
                        else:
                            active = None
                            destination = None
                            update = True

        elif (state == 1):
            #printBoard(board,dimension)
            newBoard = phantomBoard(board)
            #printBoard(newBoard,dimension)
            root = node(newBoard,None,None,None,None,None)

            v, best = miniMax(root,1,-numpy.inf,numpy.inf,True,dimension,newBoard)
            
            ##print(v)
            
            while (best != None) and (best.child != None):
                #print("e")
                #print(best.child.i,best.child.f,best.child.value)
                best = best.child

            ##best = best.child
            print(best.i)
            print(best.f)
            move(board[best.i.y][best.i.x],board[best.f.y][best.f.x])
            
            nextTurn = True
            update = True

        ayye = detectWin(board,dimension,True)
        if (ayye > 0):
            if ayye == 1:
                state = 2
            elif ayye == 2:
                state = 3
            else: state = 4
        
        if (nextTurn):         
            if (state == 0):
                state = 1
            elif (state == 1):
                state = 0

        if (update):
            drawBoard(board,active,dimension)
        pygame.display.update()

    print()
    if state == 2:
        print("Player wins!")
    elif state == 3:
        print("AI wins!")
    else: print("Draw!")


main()
