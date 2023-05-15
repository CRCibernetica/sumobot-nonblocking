import asyncio
import time
import board
import keypad
from ideaboard import IdeaBoard

ib = IdeaBoard()

# Robot modes
FORWARD = 0
AVOID = 1

class Robot:
    
    def __init__(self, initial_mode, initial_speed = 1.0):
        self.mode = initial_mode
        self.speed = initial_speed
    
def forward(robot):
    ib.pixel = (0,255,0)
    ib.motor_1.throttle = robot.speed
    ib.motor_2.throttle = robot.speed


async def move(robot):
    while True:
        if robot.mode == FORWARD:
            forward(robot)
        elif robot.mode == AVOID:
            await avoid(robot)
        await asyncio.sleep(0)
        
    
async def avoid(robot):  
    ib.pixel = (150,255,0)
    ib.motor_1.throttle = -robot.speed
    ib.motor_2.throttle = -robot.speed
    ib.pixel = (255,0,0)
    await asyncio.sleep(1.0)
    ib.pixel = (0,0,255)
    ib.motor_1.throttle = robot.speed
    ib.motor_2.throttle = -robot.speed
    await asyncio.sleep(0.5)
    

async def handle_sensor(pin, robot):
    with keypad.Keys((pin,), value_when_pressed=False) as keys:
        while True:
            event = keys.events.get()
            if event:
                if event.pressed:
                    print("pressed")
                    robot.mode = AVOID
                elif event.released:
                    print("released")
                    robot.mode = FORWARD
            await asyncio.sleep(0)
            

async def main():
    
    robot = Robot(FORWARD, initial_speed = 1.0)
    
    move_task = asyncio.create_task(move(robot))
    interrupt_task = asyncio.create_task(handle_sensor(board.IO27, robot))
    
    await asyncio.gather(move_task,interrupt_task)

asyncio.run(main())

