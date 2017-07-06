#import meka_ach as ma
#import light_ctrl as light
#import light_look_test_macros as look
#import touch_input as ti
import test_macros as test
import time
import random

to_list = []
to_max = 1
to =     [('left', 'left'),
	  ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('left', 'left'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('right', 'right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('left','right'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left'),
          ('right','left')]



def getNext():
    global to
    global to_list
    global to_max

    inList = True
    num = -1
    while(inList):   
      num = random.randint(0,to_max-1)
      if num in to_list:
        inList = True
      else:
        to_list.extend([num])
        inList = False
    print '------------------------------'
    print '------------------------------'
    print '------------------------------'
    print 'The Order List: ', to_list
    print '------------------------------'
    print '------------------------------'
    print '------------------------------'
    return num

def doTest():
    global to
    global to_list
    global to_max

    # Start Touch Input
    # ti.init( port, timeout)
    # Return: Null
    test.init('/dev/ttyACM0',5)

    #test.init('/dev/ttyACM0',5)

    to_i = 0;
    to_max = len(to)
    print 'Trial length = ', to_max


    # Set log filename (optional, default = look_light_test.log)
    log_name = 'log_' + time.strftime("%Y-%m-%d") + '_' + time.strftime("%H%M")  
    print test.log_name(log_name)    
    while (to_i < to_max):

      test.reset()
      # Get random right left values
      # Return: 'right' or 'left'
      robot_look = test.random_right_left()
      bulb_light = test.random_right_left()

      # get random delay from head
      robot_head_delay  = 0.25

      # reset delay time in seconds
      robot_reset_delay = 2.0

      # input:   Side Robot Looks ['left', 'right'],
      #          Side Bulb Lights ['left', 'right'],
      #          Time robot looks before light turns on (in sec) ** Optional **
      #          Time robot pauses during reset (in sec) ** Optional **
      #
      # return ( Side Robot Looked ['left', 'right'],
      #          Side Human Picked ['left', 'right'],
      #          Side Bulb Lit On  ['left', 'right'],
      #          Time robot looks before light turns on (in sec) 
      #          Time robot pauses during reset (in sec) 
      #          Change in time between light going on and human touch (sec)
      #         )
      print '------------------------------'
      print '------------------------------'
      print '------------------------------'
      raw_input("Press ENTER For Next Run")
      the_i = getNext()
      tto = to[the_i]
      robot_look = tto[0]
      bulb_light = tto[1]
      out = test.run(robot_look, bulb_light, robot_head_delay, robot_reset_delay)



      print '------------------------------'
      print '------------------------------'
      print '------------------------------'
      print 'Test Number = ', to_i, " - robot = ", robot_look, ' - bulb = ', bulb_light
      print '------------------------------'
      print '------------------------------'
      print '------------------------------'
      to_i += 1
      

      # Log the output
      # Log format:
      # Time of log sing "beginning of time" in seconds
      # Side Robot Looked
      # Side Human Touched
      # Side Light Lit
      # When robot started to move it's head in reference to when light turned on in seconds
      # Difference in time between when the light turned on and the human touched the input in seconds
      # NEW LINE
      test.log(out)

#      test.reset()

    # Stops system

    test.stop()

if __name__ == '__main__':
    doTest()
