#import meka_ach as ma
#import light_ctrl as light
#import light_look_test_macros as look
#import touch_input as ti
import test_macros as test


if __name__ == '__main__':

    # Start Touch Input
    # ti.init( port, timeout)
    # Return: Null
    test.init('/dev/ttyACM0',5)
    
    while (True):
      # input:   Side Robot Looks ['left', 'right'],
      #          Side Bulb Lights ['left', 'right'],
      #          Delay of robot look (in sec) (Negative values only 
      #
      # return ( Side Robot Looked ['left', 'right'],
      #          Side Human Picked ['left', 'right'],
      #          Side Bulb Lit On  ['left', 'right'],
      #          Change in time between light going on and human touch (sec)
      #         )
      out = test.run('right', 'left')
      test.log(out)
      print out


    # Stops system
    test.stop()

