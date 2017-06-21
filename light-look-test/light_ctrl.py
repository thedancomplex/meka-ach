import os

ip_left = "192.168.1.191"
ip_right = "192.168.1.196"

def onOff(light, onoff):
  the_ip = " "
  if (light == 'left'):
    the_ip = ip_left
  elif (light == 'right'):
    the_ip = ip_right
  else:
    return 1

  if(onoff == 'on'):
    os.system("tplight on " + the_ip + " &")
  elif(onoff == 'off'):
    os.system("tplight off " + the_ip + " &")
  else:
    return 1
  return 0

def light(side, state):
  theState = 'off'
  if(state == True):
    theState = 'on'
  elif(state == False):
    theState = 'off'
  else:
    return 1
  return onOff(side, theState)
