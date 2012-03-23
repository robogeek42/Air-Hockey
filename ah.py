import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
from pymunk import Vec2d
import math, sys, random
from score import *

WINW=800
WINH=600
PI=3.14247

## Balls
balls = []
   
## players
players = []

# Wall thickness
wt=20.0
# Goal width
gw=WINW/4.0

score = {'p1':0, 'p2':0}

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+WINH)

def from_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+WINH)
    
def addball():
    radius=10
    mass=1
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    ball_body = pymunk.Body(mass, inertia)
    ball_body.position=(WINW/2,WINH/2)

    mainball = pymunk.Circle(ball_body, radius, (0,0))
    mainball.elasticity = 0.95
    space.add(ball_body, mainball)
    balls.append(mainball)
    #ball_body.apply_impulse((40.0,0.0), (0,0))

def draw_table():
    pygame.draw.rect(screen, THECOLORS["brown"], [[0.0, 0.0], [WINW, wt]], 0)
    pygame.draw.rect(screen, THECOLORS["brown"], [[0.0, WINH-wt], [WINW, WINH]], 0)
    pygame.draw.rect(screen, THECOLORS["brown"], [[0.0, 0.0], [wt, (WINH-gw)/2]], 0)
    pygame.draw.rect(screen, THECOLORS["brown"], [[0.0, (WINH+gw)/2], [wt,WINH]], 0)
    pygame.draw.rect(screen, THECOLORS["brown"], [[WINW-wt, 0.0], [WINW, (WINH-gw)/2]], 0)
    pygame.draw.rect(screen, THECOLORS["brown"], [[WINW-wt, (WINH+gw)/2], [WINW,WINH]], 0)

    pygame.draw.line(screen, THECOLORS["grey"], (WINW/2, wt), (WINW/2, WINH-wt), 2)
    circrad=1.2*gw/2
    pygame.draw.circle(screen, THECOLORS["grey"], (WINW/2, WINH/2), circrad, 2)
    pygame.draw.arc(screen, THECOLORS["grey"], [[-circrad, WINH/2-circrad], [+circrad,WINH/2+circrad]], 270, 90, 2)

    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, THECOLORS["black"], False, [p1,p2])
    
def draw_score():
    DrawScore(score['p1'], score['p2'], 100,50, 8, 6, screen, THECOLORS["grey"], 2)

pygame.init()

screen = pygame.display.set_mode((WINW, WINH))
clock = pygame.time.Clock()
running = True

### Physics stuff
space = pymunk.Space(50)
space.gravity = (0.0,0.0)

### walls
static_body = pymunk.Body()
static_lines = [pymunk.Segment(static_body, (wt, wt), (WINW-wt, wt), 1.0),
                pymunk.Segment(static_body, (wt, WINH-wt), (WINW-wt, WINH-wt), 1.0),
                pymunk.Segment(static_body, (wt, wt), (wt, (WINH-gw)/2), 1.0),
                pymunk.Segment(static_body, (wt, (WINH+gw)/2), (wt, WINH-wt), 1.0),
                pymunk.Segment(static_body, (WINW-wt, wt), ((WINW-wt), (WINH-gw)/2), 1.0),
                pymunk.Segment(static_body, (WINW-wt, (WINH+gw)/2), (WINW-wt, WINH-wt), 1.0)
                ]  
for line in static_lines:
    line.elasticity = 0.7
    line.group = 1
space.add(static_lines)

# Setup Player 1
pmass=3
pradius=20
p1inertia = pymunk.moment_for_circle(pmass, 0, pradius, (0,0))
p1_body = pymunk.Body(pmass, p1inertia)
p1_body.position=(WINW-WINW/8, WINH/2)

p1_shape = pymunk.Circle(p1_body, pradius, (0,0))
p1_shape.elasticity = 0.95
space.add(p1_body, p1_shape)
players.append(p1_shape)

mouse_body = pymunk.Body()
joint1=None
selected = None


# Add the ball
addball()

draw_score()

while running:
    mpos = pygame.mouse.get_pos()
    mouse_body.position = from_pygame( Vec2d(mpos) )
    mouse_body.angle = 0
    mouse_body.angular_velocity = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1: # LMB
            #selected = space.point_query_first(from_pygame(Vec2d(mpos)))
            #if selected != None:
            p1_body.position = mouse_body.position
            joint1 = pymunk.PivotJoint(mouse_body, p1_body, (0,0), (0,0) )
            space.add(joint1)

        elif event.type == MOUSEBUTTONUP:
            if joint1 != None:
                space.remove(joint1)
            joint1 = None
    
    p1_body.angular_velocity=0
  
    ### Clear screen
    screen.fill(THECOLORS["white"])
    
    ### Draw 
    draw_table()

    for ball in balls:
        p = to_pygame(ball.body.position)
        if p[0] < 0:
            score['p1'] += 1
        if p[0] >WINW:
            score['p2'] += 1

        if p[0] < 0 or p[0]>WINW:
            addball()
            space.remove(ball)
            balls.remove(ball)

        pygame.draw.circle(screen, THECOLORS["purple"], p, int(ball.radius), 0)

    p = to_pygame(p1_body.position)
    pygame.draw.circle(screen, THECOLORS["darkgreen"], p, int(p1_shape.radius), 0)
    pygame.draw.circle(screen, THECOLORS["black"], p, int(p1_shape.radius+1), 2)
    pygame.draw.circle(screen, THECOLORS["black"], p, int(p1_shape.radius/2), 1)

    draw_score()

    ### Update physics
    dt = 1.0/60.0/5.
    for x in range(5):
        space.step(dt)
    
    ### Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
        
