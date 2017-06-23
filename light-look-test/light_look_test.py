import meka_ach as ma
import light_ctrl as light
import light_look_test_macros as look

if __name__ == '__main__':

    # Start System
    ma.start()

    look.reset(5.0)

    look.look('right', True, -1.0, 5.0)

    look.reset(5.0)

    look.look('left', True, -1.0, 5.0)

    look.reset(5.0)



    # Stops system
    ma.stop()

