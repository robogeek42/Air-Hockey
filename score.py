import pygame
from pygame.locals import *
from pygame.color import *

grid=[[0,0],[2,0], # 0 1
      [0,1],[2,1], # 2 3
      [0,2],[2,2], # 4 5
      [0,3],[2,3], # 6 7
      [0,4],[2,4]] # 8 9
MOVE=0
DRAW=1
numidx=[]
for i in range(0,10):
    numidx.append([])
numidx[0]=[[MOVE,0], [DRAW,1], [DRAW,9], [DRAW,8], [DRAW,0]]
numidx[1]=[[MOVE,1], [DRAW,9]]
numidx[2]=[[MOVE,2], [DRAW,0], [DRAW,1], [DRAW,3], [DRAW,8], [DRAW,9]]
numidx[3]=[[MOVE,0], [DRAW,1], [DRAW,9], [DRAW,8], [MOVE,4], [DRAW,5]]
numidx[4]=[[MOVE,0], [DRAW,4], [DRAW,5], [MOVE,1], [DRAW,9]]
numidx[5]=[[MOVE,1], [DRAW,0], [DRAW,4], [DRAW,5], [DRAW,9], [DRAW,8], [DRAW,6]]
numidx[6]=[[MOVE,3], [DRAW,1], [DRAW,0], [DRAW,8], [DRAW,9], [DRAW,5], [DRAW,4]]
numidx[7]=[[MOVE,0], [DRAW,1], [DRAW,3], [DRAW,8]]
numidx[8]=[[MOVE,0], [DRAW,1], [DRAW,9], [DRAW,8], [DRAW,0], [MOVE,4], [DRAW,5]]
numidx[9]=[[MOVE,5], [DRAW,4], [DRAW,0], [DRAW,1], [DRAW,9], [DRAW,8]]

def DrawDigit(N, X,Y, MAG, screen, col, lw):
    cx=0 ; cy=0
    if N < 0 or N > 9:
        print "Digit ",N," out of range"
        return
    for m in numidx[N]:
        if m[0]==MOVE:
            cx=grid[m[1]][0]*MAG+X
            cy=grid[m[1]][1]*MAG+Y
        else:
            pygame.draw.line(screen, col,
                    (cx,cy),
                    (grid[m[1]][0]*MAG+X, grid[m[1]][1]*MAG+Y),
                    lw)
            cx = grid[m[1]][0]*MAG+X
            cy = grid[m[1]][1]*MAG+Y

COLON=0
SPEC_FIRST=0
SPEC_LAST=0
def DrawSpecial(N, X,Y, MAG, screen, col, lw):
    cx=0 ; cy=0
    if N < SPEC_FIRST or N > SPEC_LAST:
        print "Special character ",N," out of range"
        return
    if N==COLON:
        rect=pygame.Rect(1*MAG+X -lw/2, 1*MAG+Y -lw/2, lw, lw)
        pygame.draw.rect(screen, col, rect,0)
        rect=pygame.Rect(1*MAG+X -lw/2, 3*MAG+Y -lw/2, lw, lw)
        pygame.draw.rect(screen, col, rect,0)

## Draw digits X,Y is top left
def DrawNumber(N, X,Y, MAG, GAP, screen, col, lw):
    # count digits
    dc=0 ; n=N
    while n>0:
        dc += 1 ; n /= 10

    if N==0:
        dc=1

    # calc end position of number
    cx=X + (dc-1)*(MAG*2+GAP)

    if N==0:
        DrawDigit(0, cx, Y, MAG, screen, col, lw)
    else:
    # get digits one by one and draw digits backwards
        n=N 
        while n>0:
            digit = n % 10 ; n /= 10
            DrawDigit(digit, cx, Y, MAG, screen, col, lw)
            cx -= MAG*2+GAP

    return X + dc*(MAG*2+GAP)

## Draw digits X,Y is top right
def DrawNumberRJ(N, X,Y, MAG, GAP, screen, col, lw):
    # count digits
    dc=0 ; n=N
    while n>0:
        dc += 1 ; n /= 10

    if N==0:
        dc=1

    # drawing from X backwards
    cx=X - (MAG*2+GAP)

    if N==0:
        DrawDigit(0, cx, Y, MAG, screen, col, lw)
    else:
        # get digits one by one
        n=N 
        while n>0:
            digit = n % 10 ; n /= 10
            DrawDigit(digit, cx, Y, MAG, screen, col, lw)
            cx -= MAG*2+GAP

    return X - dc*(MAG*2+GAP)

def DrawScore(P1, P2, X, Y, MAG, GAP, screen, col, lw):
    DrawSpecial(COLON, X, Y, MAG, screen, col, lw)
    DrawNumberRJ(P1, X-GAP, Y, MAG, GAP, screen, col, lw)
    DrawNumber(P2, X+(MAG*2)+GAP, Y, MAG, GAP, screen, col, lw)


# Test code
if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        size=10 ; gap=8 ; lw=2
        width=size*2+gap
        xpos=10 ; ypos=10
        for digit in range(0,10):
            DrawDigit(digit,xpos,ypos,size,screen,THECOLORS["white"],lw)
            xpos += width

        nextx = DrawNumber(674, 100, 100, 8, 4, screen, THECOLORS["cyan"],lw)
        nextx = DrawNumber(85, nextx, 100, 8, 4, screen, THECOLORS["magenta"],lw)

        DrawNumberRJ(93, 100, 200, 8, 4, screen, THECOLORS["yellow"],lw)

        DrawSpecial(COLON, 120, 200, 8, screen, THECOLORS["red"],lw)

        DrawScore(21386, 983726, 200, 300, 10, 8, screen, THECOLORS["grey"], 2)

        pygame.display.flip()
        clock.tick(50)

