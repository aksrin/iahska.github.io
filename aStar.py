import random
import math
from queue import PriorityQueue
import pygame
import time

cols = 160
rows = 120
arr = [[0 for i in range(cols)] for j in range(rows)]

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)
GREEN = (0,255,0)
RED = (255,0,0)
DRED = (149,1,1)
BLUE = (0,0,255)
ORANGE = (255,183,37)
DORANGE = (232,155,1)

MAGENTA = (127,0,255)
MAGENTA2 = (255,0,255)

WIDTH = 8
HEIGHT = 8
MARGIN = 2
    
#Highway
def newHighwayStartingPoint():
    randx = random.randint(0,159)
    randy = random.randint(0,119)
    x_forward = 0
    y_forward = 0

    randb = random.randint(1,4)
    if (randb == 1):
        randx = 0
        x_forward = 1
    if (randb == 2):
        randx = 159
        x_forward = -1
    if (randb == 3):
        randy = 0
        y_forward = 1
    if (randb == 4):
        randy = 119
        y_forward = -1
    return (randx,randy,x_forward,y_forward)    

    
arr = [[0 for i in range(160)] for j in range(120)]

for i in range(0,120):
    for j in range(0,160):
        arr[i][j] = '1'


#Hard to Tranverse centers
for i in range (0,8):
    randx = random.randint(0,159)
    randy = random.randint(0,119)
    #print(randx,randy)
    x_1 = randx - 15
    x_2 = randx + 15
    y_1 = randy - 15
    y_2 = randy + 15
            
    if(randx < 15):
        x_1 = 0
    elif (randx > 144):
        x_2 = 159

    if(randy < 15):
        y_1 = 0
    elif (randy > 104):
        y_2 = 119
               
    for x in range(x_1,x_2):
        for y in range(y_1,y_2):
            chance = random.randint(0,1)
            if chance == 1:
                arr[y][x] = '2'


#Highways
x, y, x_f, y_f = newHighwayStartingPoint()
visited = []
count = 0
steps = 0

while count < 4:

    while(steps < 100):

        if arr[randy][randx] == 'a' or arr[randy][randx] == 'b':
            #intersects a highway
            x, y, x_f, y_f = newHighwayStartingPoint()
            visted = []
            steps = 0
            break
        
        else:
            #does not intersect a highway
            steps = steps + 1
            #adds cords to our list
            cords = tuple([x,y])
            visited.append(cords)

            #calculate change in direction
            chance = random.randint(1,10)

            if ((chance == 7)or(chance == 8)): #Turn left
                if (x_f == 0): #If y_f is moving (up or down)    
                    y_f = 0 #Stop moving up/down
                    x_f = -1 #Turn left instead
                elif (y_f == 0): #If x_f is moving (left or right)
                    x_f = 0 #Stop moving left/right
                    y_f = -1 #Turn up instead

            if ((chance == 9)or(chance == 10)): #Turn right
                if (x_f == 0): #If y_f is moving (up or down)    
                    y_f = 0 #Stop moving up/down
                    x_f = 1 #Turn right instead
                elif (y_f == 0): #If x_f is moving (left or right)
                    x_f = 0 #Stop moving left/right
                    y_f = 1 #Turn down instead        

            #move to next point
            x = x + x_f
            if (x == -1) or (x == 160):
                x = x - x_f
                steps = steps - 1
                
            y = y + y_f
            if (y == -1) or (y == 120):
                y = y - y_f
                steps = steps - 1

    for cord in visited:               
        if arr[cord[1]][cord[0]] == "2": 
            arr[cord[1]][cord[0]] = 'b'
        else:
            arr[cord[1]][cord[0]] = 'a'
                
    x, y, x_f, y_f = newHighwayStartingPoint()
    visited = []
    count = count + 1
    steps = 0
  
#Impassibles
for i in range(0,3840):
    randx = random.randint(0,159)
    randy = random.randint(0,119)

    if ((arr[randy][randx] == 'a') or (arr[randy][randx] == 'b')): #if the cell is a highway redo it
        while ((arr[randy][randx] == 'a') or (arr[randy][randx] == 'b')):
            randx = random.randint(0,159)

    arr[randy][randx] = '0'

#print grid
#for rows in arr:
#    print(rows)


#Initialize pygame
pygame.init()
#Set Height and Width of the screen
WINDOW_SIZE = [1602,1202]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Grid Plane")
#Manange how fast the screen updates
clock = pygame.time.Clock()
screen.fill(BLACK)
for row in range(120):
    for col in range(160):
        color = WHITE
        if arr[row][col] == '0':
            color = BLACK
        if arr[row][col] == '2':
            color = GRAY
        if arr[row][col] == 'a':
            color = (0,255,255)
        if arr[row][col] == 'b':
            color = BLUE
        pygame.draw.rect(screen,
                         color,
                         [(MARGIN + WIDTH)*col+MARGIN,
                          (MARGIN + HEIGHT)* row+MARGIN,
                          WIDTH,
                          HEIGHT])
clock.tick(144)
pygame.display.flip()
#pygame.quit()        

def pickStartAndEndPoints():

    chance = random.randint(1,4)

    if chance == 1: #TL
        randx = random.randint(0,19)
        randy = random.randint(0,19)
        if arr[randy][randx] == '0': 
            while arr[randy][randx] == '0':
                randx = random.randint(0,19)
                randy = random.randint(0,19)
                    
    if chance == 2: #TR
        randx = random.randint(139,159)
        randy = random.randint(0,19)
        if arr[randy][randx] == '0': 
            while arr[randy][randx] == '0':
                randx = random.randint(139,159)
                randy = random.randint(0,19)
        
    if chance == 3: #BL
        randx = random.randint(0,19)
        randy = random.randint(99,119)
        if arr[randy][randx] == '0': 
            while arr[randy][randx] == '0':
                randx = random.randint(0,19)
                randy = random.randint(99,119)
        
    if chance == 4: #BR
        randx = random.randint(139,159)
        randy = random.randint(99,119)
        if arr[randy][randx] == '0': 
            while arr[randy][randx] == '0':
                randx = random.randint(139,159)
                randy = random.randint(99,119)

    startx = randx
    starty = randy

    running = True
    while (running):
        chance = random.randint(1,4)
        if chance == 1: #TL
            randx = random.randint(0,19)
            randy = random.randint(0,19)
            if arr[randy][randx] == '0': 
                while arr[randy][randx] == '0':
                    randx = random.randint(0,19)
                    randy = random.randint(0,19)
                        
        if chance == 2: #TR
            randx = random.randint(139,159)
            randy = random.randint(0,19)
            if arr[randy][randx] == '0': 
                while arr[randy][randx] == '0':
                    randx = random.randint(139,159)
                    randy = random.randint(0,19)
            
        if chance == 3: #BL
            randx = random.randint(0,19)
            randy = random.randint(99,119)
            if arr[randy][randx] == '0': 
                while arr[randy][randx] == '0':
                    randx = random.randint(0,19)
                    randy = random.randint(99,119)
            
        if chance == 4: #BR
            randx = random.randint(139,159)
            randy = random.randint(99,119)
            if arr[randy][randx] == '0': 
                while arr[randy][randx] == '0':
                    randx = random.randint(139,159)
                    randy = random.randint(99,119)
        if(abs(startx-randx)+abs(starty-randy) > 99):
            running = False

    endx = randx
    endy = randy

    return startx, starty, endx, endy
        
        
def heuristicOne(x1,x2,y1,y2): #A*
    return(math.sqrt((x1-x2)**2+(y1-y2)**2))

def heuristicTwo(x1,x2,y1,y2): #Uniform Cost
    return 0

def heuristicThree(x1,x2,y1,y2):
    return (1.25*heuristicOne(x1,x2,y1,y2))



def heuristicFour(x1,x2,y1,y2):
    global w2
    if (w2==0):
        w2=1
        return (1.5*heuristicOne(x1,x2,y1,y2))
    if (w2==1):
        w2=2
        return (5*heuristicOne(x1,x2,y1,y2))
    if (w2==2):
        w2=3
        return (heuristicOne(x1,x2,y1,y2))
    if (w2==3):
        w2=0
        return (0.25*heuristicOne(x1,x2,y1,y2))

def distance(point,point2):
    if (abs(point.x-point2.x)+abs(point.y-point2.y))==1:
        dist=1
    else:
        dist=1.4
    if point.gtype=='1':
        if point2.gtype=='2':
            dist=dist*1.5
        #do highways
    if point.gtype=='2':
        if point2.gtype=='2':
            dist=dist*2
        if point2.gtype=='1':
            dist=dist*1.5
        #do highways
    return(dist)

        
class node:
    def __init__(self,x,y,g,h,gtype,last):
        self.x=x
        self.y=y
        self.g=g
        self.h=h
        self.gtype=gtype
        self.last=last

    def __lt__(self,other):
        return ( (self.g) < (other.g) )

def updateVertex(c,n):
    dist = distance(c,n)
    if (c.g + dist < n.g):
        n.g = c.g + dist
        n.last = c

def exploreNeighbor(current,x,y,closedL,openL,endx,endy,h):
    temp = []
    neighbor = None
    isFringe = False
    xBounded = ((x>=0)and(x<160))
    yBounded = ((y>=0)and(y<120))
    if (xBounded and yBounded):
        openCell = (arr[y][x] != '0')
    else: openCell = False
    
    if (xBounded and yBounded and openCell): #Check if valid neighbor
        isContained = False
        for c in closedL: #Check if neighbor node is in the closed list
            if ((c[1].x == x) and (c[1].y == y)):
                isContained = True

        if not (isContained): #Node is not in the closed list
            #check if not in openlist
            temp = []
            while not openL.empty():
                check = openL.get()
                if ((check[1].x == x) and(check[1].y == y)): #It's already in the open list, take its original g and parent values
                    isFringe = True
                    g = check[1].g
                    parent = check[1].last
                else:
                    temp.append(check)
                    
            for i in temp: #Put the nodes back into the list
                if (i != None):
                    f = i[1].g + i[1].h
                    openL.put((f,i[1]))

            if not (isFringe):
                g = 500000
                parent = None
                    
            neighbor = node(x,y,g,h(x,endx,y,endy),arr[y][x],parent)
            updateVertex(current,neighbor)

    return neighbor

def expandNode(c,closedL,openL,endx,endy,neighbors,h):       
    neighbors.append(exploreNeighbor(c,c.x-1,c.y,closedL,openL,endx,endy,h)) #left  
    neighbors.append(exploreNeighbor(c,c.x+1,c.y,closedL,openL,endx,endy,h)) #right   
    neighbors.append(exploreNeighbor(c,c.x,c.y-1,closedL,openL,endx,endy,h)) #up   
    neighbors.append(exploreNeighbor(c,c.x,c.y+1,closedL,openL,endx,endy,h)) #down    
    neighbors.append(exploreNeighbor(c,c.x-1,c.y-1,closedL,openL,endx,endy,h)) #up-left    
    neighbors.append(exploreNeighbor(c,c.x+1,c.y-1,closedL,openL,endx,endy,h)) #up-right    
    neighbors.append(exploreNeighbor(c,c.x-1,c.y+1,closedL,openL,endx,endy,h)) #down-left    
    neighbors.append(exploreNeighbor(c,c.x+1,c.y+1,closedL,openL,endx,endy,h)) #down-right
    
def aStarSearch(startx, starty, endx, endy, h):
    openlist = PriorityQueue()
    closedlist=[]
    print("Startx: ",startx,"Starty: ",starty)
    print("endx: ",endx,"endy: ",endy)
    start = node(startx,starty,0,h(startx,endx,starty,endy),arr[starty][startx],None)
    print()
    openlist.put((h(startx,endx,starty,endy),start))
    while not openlist.empty():
        #time.sleep(0.1)

        current=openlist.get() #Pop the next node

        if ((current[1].x == endx)and(current[1].y == endy)): #Stop if we reach goal            
            print("Path found")
            return current[1]

        closedlist.append(current) #Add to closed list

        n = []
        expandNode(current[1],closedlist,openlist,endx,endy,n,h) #Expand current node and return list of valid neighbors

        for i in n:
            if i != None:
                openlist.put(( (i.g+i.h),i))
                if (i.gtype == '2'):
                    pygame.draw.rect(screen,DORANGE,[(MARGIN + WIDTH)*i.x +MARGIN,(MARGIN + HEIGHT)*i.y + MARGIN,WIDTH,HEIGHT])
                else: pygame.draw.rect(screen,ORANGE,[(MARGIN + WIDTH)*i.x +MARGIN,(MARGIN + HEIGHT)*i.y + MARGIN,WIDTH,HEIGHT])

        temp = PriorityQueue()
        if (current[1].gtype == '2'):
            pygame.draw.rect(screen,DRED,[(MARGIN + WIDTH)*current[1].x+MARGIN,(MARGIN + HEIGHT)*current[1].y+MARGIN,WIDTH,HEIGHT])
        else: pygame.draw.rect(screen,RED,[(MARGIN + WIDTH)*current[1].x+MARGIN,(MARGIN + HEIGHT)*current[1].y+MARGIN,WIDTH,HEIGHT])
        pygame.draw.rect(screen,GREEN,[(MARGIN + WIDTH)*startx+MARGIN,(MARGIN + HEIGHT)* starty+MARGIN,WIDTH,HEIGHT])
        pygame.draw.rect(screen,MAGENTA2,[(MARGIN + WIDTH)*endx+MARGIN,(MARGIN + HEIGHT)* endy+MARGIN,WIDTH,HEIGHT])

        pygame.display.flip()

    print("Path not found")
    return None


sx,sy,ex,ey = pickStartAndEndPoints()

pygame.draw.rect(screen,GREEN,[(MARGIN + WIDTH)*sx+MARGIN,(MARGIN + HEIGHT)* sy+MARGIN,WIDTH,HEIGHT])
pygame.draw.rect(screen,MAGENTA2,[(MARGIN + WIDTH)*ex+MARGIN,(MARGIN + HEIGHT)* ey+MARGIN,WIDTH,HEIGHT])
pygame.display.flip()

#ready = input("Are you ready?")

w2=0


#e = aStarSearch(sx,sy,ex,ey,heuristicOne)
#e = aStarSearch(sx,sy,ex,ey,heuristicTwo)
#e = aStarSearch(sx,sy,ex,ey,heuristicThree)
e = aStarSearch(sx,sy,ex,ey,heuristicFour)

while (e != None):
    pygame.draw.rect(screen,MAGENTA,[(MARGIN + WIDTH)*e.x+MARGIN,(MARGIN + HEIGHT)* e.y+MARGIN,WIDTH,HEIGHT])
    e = e.last

pygame.draw.rect(screen,GREEN,[(MARGIN + WIDTH)*sx+MARGIN,(MARGIN + HEIGHT)* sy+MARGIN,WIDTH,HEIGHT])
pygame.draw.rect(screen,MAGENTA2,[(MARGIN + WIDTH)*ex+MARGIN,(MARGIN + HEIGHT)* ey+MARGIN,WIDTH,HEIGHT])
pygame.display.flip()
