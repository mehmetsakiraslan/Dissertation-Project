from robot import Robot
from time import sleep

robot = Robot()

def ileri():
    robot.set_motors(0.27, 0.25)
    
def sol():
    robot.left(0.14)
    
def sag():
    robot.right(0.14)

def geri():
    robot.set_motors(-0.16, -0.15)
    
def dur():
    robot.stop()
    
def sol_arka():
    robot.set_motors(-0.20, -0.12)
    
def sag_arka():
    robot.set_motors(-0.13, -0.20)
