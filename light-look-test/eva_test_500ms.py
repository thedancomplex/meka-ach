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

    # Set log filename (optional, default = look_light_test.log)
    print test.log_name('look_light_test3.log')    
    while (True):

      # Get random right left values
      # Return: 'right' or 'left'
      robot_look = test.random_right_left()
      bulb_light = test.random_right_left()

      # get random delay from head
      robot_head_delay  = 0.8

      # reset delay time in seconds
      robot_reset_delay = 5.0

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

      raw_input("Press ENTER For Next Run")
      out = test.run(robot_look, bulb_light, robot_head_delay, robot_reset_delay)


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

      test.reset()

    # Stops system
    test.stop()

