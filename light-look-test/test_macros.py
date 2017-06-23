import meka_ach as ma
import touch_input as ti
import light_look_test_macros as look
import time

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
    reset(5.0)
  else:
    reset(hold_time)

  if(robot_pre == None):
    robot_pre = -0.2

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
  return (side_robot, side_human, side_light, dt)
     

def log( from_run):
  global the_file_name
  target = open(the_file_name, 'a')

  t = time.time()
  target.write(str(t) + " " + from_run[0] + " " + from_run[1] + " " + from_run[2] + " " + str(from_run[3])+ '\n')  
  target.close() 
