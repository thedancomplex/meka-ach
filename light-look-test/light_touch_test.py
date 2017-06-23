import meka_ach as ma
import light_ctrl as light
import light_look_test_macros as look
import touch_input as ti

if __name__ == '__main__':

    # Start System
    ma.start()

    # Start Touch Input
    # ti.init( port, timeout)
    # Return: Null
    ti.init('/dev/ttyACM0',5)


    #look.reset(5.0)




    a = look.look('right', True, -0.2, 5.0)



    # Get Touch Input
    # Return: ( side ['L','R','F'], time [sec]) 
    # L = Left, R = Right, F = Fail/Timeout
    b = ti.get()
    print b



    #look.reset(5.0)

    #look.look('left', True, -1.0, 5.0)

    #look.reset(5.0)



    # Stops system
    ma.stop()

