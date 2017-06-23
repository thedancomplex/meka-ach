import serial
import time
ser = []

def init(port, timeout_def = None):
  global ser
  if(timeout_def == None):
    ser = serial.Serial(port, 9600)
  else:  
    ser = serial.Serial(port, 9600,timeout=timeout_def)

def get():
  global ser
  out = -1
  ser.flushInput()
  out = ser.readline()
  t = time.time()
  if(out == -1):
    return ('F', t)
  if(out == []):
    return ('F', t)
  if(out == NULL):
    return ('F', t)
  if(out[0] == 'L'):
    return ('L', t)
  elif(out[0] == 'R'):
    return ('R', t)
  return('F',t)
 
