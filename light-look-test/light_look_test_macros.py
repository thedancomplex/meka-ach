import meka_ach as ma
import light_ctrl as light
import light_look_test_macros as look
import numpy as np
import time


def left():
  ma.setX(0.5)
  ma.setY(-0.4)
  ma.setZ(1.0)
  ma.setR(10)
  ma.go()
  return 0

def right():
  ma.setX(-0.5)
  ma.setY(-0.4)
  ma.setZ(1.0)
  ma.setR(-10)
  ma.go()
  return 0

def center():
  ma.setX(0.0)
  ma.setY(0.0)
  ma.setZ(1.0)
  ma.setR(0)
  ma.go()
  return 0

def look_side(side):
  if(side == 'left'):
    left()
  elif(side == 'right'):
    right()
  elif(side == 'center'):
    center()
  else:
    return 1
  return 0

def other_side(side):
  if(side == 'left'):
    return 'right'
  elif(side == 'right'):
    return 'left'
  else:
     return 1

def reset(delay = None):
  look('center')
  light.light('left',False)
  light.light('right',False)
  if(delay == None):
    return 0
  ma.time.sleep(np.abs(delay))

def look(side,correct = None, delay = None, record = None):
  t = -1
  if(correct == None):
    return look_side(side)
    
  if(delay == 0):
    look(side)
    t = time.time()
    light.light(side,correct)
    light.light(other_side(side), not correct)
  elif(delay > 0):
    t = time.time()
    light.light(side,correct)
    light.light(other_side(side), not correct)
    ma.time.sleep(delay)
    look(side)
  elif(delay < 0):
    look(side)
    ma.time.sleep(np.abs(delay))
    t = time.time()
    light.light(side,correct)
    light.light(other_side(side), not correct)
  else:
    return -1
  #ma.time.sleep(np.abs(hold))

  return t

  if(record == None):
    return t

  




    
