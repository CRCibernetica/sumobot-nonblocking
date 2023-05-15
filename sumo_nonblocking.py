import board
import time
from ideaboard import IdeaBoard

ib = IdeaBoard()

ir = ib.DigitalIn(board.IO27)

GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (150,255,0)
BLACK = (0,0,0)

# Robot modes
FORWARD = 0
AVOID = 1

class Robot:
    
    def __init__(self, initial_mode, initial_speed = 1.0):
        self.mode = initial_mode
        self.speed = initial_speed

def checkIR():
    if ir.value == True:
        return False
    elif ir.value == False:
        return True

def stop(robot):
    ib.pixel = RED
    ib.motor_1.throttle = 0
    ib.motor_2.throttle = 0

def forward(robot):
    ib.pixel = GREEN
    ib.motor_1.throttle = robot.speed
    ib.motor_2.throttle = robot.speed
    
def reverse(robot):
    ib.pixel = RED
    ib.motor_1.throttle = -robot.speed
    ib.motor_2.throttle = -robot.speed
    
def turn(robot):
    ib.pixel = BLUE
    ib.motor_1.throttle = robot.speed
    ib.motor_2.throttle = -robot.speed

def avoid(robot):
    stop(robot)
    time.sleep(0.1)
    reverse(robot)
    time.sleep(1.0)
    turn(robot)
    time.sleep(0.5)   
    
def update_move(robot):
    if robot.mode == FORWARD:
        forward(robot)
    elif robot.mode == AVOID:
        avoid(robot)
    

robot = Robot(FORWARD, 1.0)
while True:
    hitBorder = checkIR()
    if hitBorder:
        robot.mode = AVOID
    else:
        robot.mode = FORWARD
    update_move(robot)