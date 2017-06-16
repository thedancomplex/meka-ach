import meka_ach as ma

if __name__ == '__main__':

    # Start System
    ma.start()

    # Sets X location of gaze in image frame
    ma.setX(0.0)

    # Sets Y location of gaze in image frame
    ma.setY(-2.0)

    # Sets Z location (distance) of image frame
    ma.setZ(40.1)

    # Sets the roll of the head
    ma.setR(0)

    # Sends above values to the robot
    ma.go()

    # Sleeps 10 seconds
    ma.time.sleep(10.0)

    # Stops system
    ma.stop()

