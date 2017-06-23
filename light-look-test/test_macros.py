import meka_ach as ma
import touch_input as ti
import light_look_test_macros as look
import time
import random

the_file_name = 'look_light_test.log'

def init(port, timeout = None):
  if(timeout == None):
    ti.init(port)
  else:
    ti.init(port,timeout)
  
  #Start Meka Ach
  ma.start()

def stop():
  # Close the serial port
  ti.close()

  # stop the robot
  ma.stop()

def reset(t = None):
  if(t == None):
    look.reset(5.0)
  else:
    look.reset(t)


def run(side_robot, side_light,robot_pre = None, hold_time = None ):
  if(hold_time == None):
    hold_time = 5.0
  reset(hold_time)

  if(robot_pre == None):
    robot_pre = -0.2
  else:
    robot_pre = -1.0 * robot_pre

  human = 'F'
  robot = 'F'
  bulb  = 'F'
  a = []
  if( (side_robot == 'right') | (side_robot == 'left') ):
    bulb_state = False
    if(side_robot == side_light):
      bulb_state = True
    a = look.look(side_robot, bulb_state, robot_pre)

  # Get Touch Input
  # Return: ( side ['L','R','F'], time [sec]) 
  # L = Left, R = Right, F = Fail/Timeout
  b = ti.get()
  side_human = 'fail'
  #move touch input to robot frame
  if(b[0] == 'L'):
    side_human = 'right'
  elif(b[0] == 'R'):
    side_human = 'left'

  dt = b[1] - a
  return (side_robot, side_human, side_light, robot_pre, hold_time, dt)
     

def log( from_run):
  # Log format:
  # Time of log sing "beginning of time" in seconds
  # Side Robot Looked
  # Side Human Touched
  # Side Light Lit
  # When robot started to move it's head in reference to when light turned on in seconds
  # time robot pauses during reset in seconds
  # Difference in time between when the light turned on and the human touched the input in seconds
  # NEW LINE
  global the_file_name
  target = open(the_file_name, 'a')

  t = time.time()
  target.write(str(t) + " " + from_run[0] + " " + from_run[1] + " " + from_run[2] + " " + str(from_run[3])+ " " +str(from_run[4]) + " " + str(from_run[5]) + '\n')  
  target.close()

def random_delay(t0, t1):
  a = random.uniform(t0, t1)
  return a

def random_right_left():
  a = random.random()
  if(a < 0.5): 
    return 'left'
  return 'right' 



def log_name(log_name = None):
  global the_file_name
  if(log_name == None):
    return the_file_name
  the_file_name = log_name
  return the_file_name
