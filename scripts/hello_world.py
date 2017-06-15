#! /usr/bin/python

#Copyright  2010, Meka Robotics
#All rights reserved.
#http://mekabot.com

#Redistribution and use in source and binary forms, with or without
#modification, are permitted.


#THIS SOFTWARE IS PROVIDED BY THE Copyright HOLDERS AND CONTRIBUTORS
#"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#Copyright OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES INCLUDING,
#BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#POSSIBILITY OF SUCH DAMAGE.

import time
import m3.rt_proxy as m3p
import m3.toolbox as m3t
import m3.toolbox_beh as m3b
import m3.toolbox_head_s2 as m3h
import m3.component_factory as m3f
import m3.head_s2csp_ctrl as m3csp
import m3.unit_conversion as m3u
#import m3.toolbox_ros as m3tr
import numpy as nu
import m3.pwr
import math
import random

############################################################
# Replace this with your own logic

#Here is where you would include any external modules you might want
#import GMU_AWESOME_FACE_DETECTION_LIBRARY
#import GMU_AWESOME_EYE_TRACKING_LIBRARY

def decide_where_to_look():
    x = int(input("Enter x look value: [-40 to 20]"))
    y = int(input("Enter y look value: [-35 to 35]"))
    return (x,y)
############################################################


class LookBehaviors:
    def __init__(self,bot,csp):
        self.joints=range(7)
        self.bot=bot
        self.csp=csp
        self.csp.enable()
        self.t_rand=time.time()
        self.t_slew=[m3t.M3Slew(),m3t.M3Slew(),m3t.M3Slew()]
        self.tbox=m3h.M3HeadToolboxS2(self.bot.get_chain_component_name('head'),bot)

    def stop(self):
        self.csp.set_target_csp_frame(m3h.spherical_to_cartesian(0,0))

    def set_eye_slewrate_proportion(self,val):
        self.csp.set_slew_rate_proportion(4,val)
        self.csp.set_slew_rate_proportion(5,val)
        self.csp.set_slew_rate_proportion(6,val)

    def zero(self):
        target=m3h.spherical_to_cartesian(0,0)
        self.csp.set_target_csp_frame(target)
        self.set_eye_slewrate_proportion(0.06)
        print 'Zero'
        return m3b.res_continue

    # x from -40 to 20
    # y from -35 to 35
    def look_at(self, x, y):
        self.csp.set_target_csp_frame(
            m3h.spherical_to_cartesian(x, y))
        self.set_eye_slewrate_proportion(0.10)
        return m3b.res_continue


def init_robot():
    proxy = m3p.M3RtProxy()
    proxy.start()
    bot_name=m3t.get_robot_name()
    bot=m3f.create_component(bot_name)
    proxy.publish_param(bot)
    proxy.subscribe_status(bot)
    proxy.publish_command(bot)
    proxy.make_operational_all()
    bot.set_motor_power_on()

    humanoid_shm_names=proxy.get_available_components('m3humanoid_shm')
    if len(humanoid_shm_names) > 0:
      proxy.make_safe_operational(humanoid_shm_names[0])

    beh=m3b.M3BehaviorEngine(rate=.03)

    #get the eye-follow module
    csp_name=proxy.get_available_components('m3head_s2csp_ctrl')[0]
    csp=m3csp.M3HeadS2CSPCtrl(csp_name)
    proxy.publish_command(csp)
    proxy.publish_param(csp)

    look_behaviors = LookBehaviors(bot, csp)
    return (proxy, bot, look_behaviors)

if __name__ == '__main__':
    proxy, bot, look_behaviors = init_robot()
    ts=time.time()
    proxy.step() #Initialize data
    try:
        while True:
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            print 'here'
            x,y = decide_where_to_look()
            look_behaviors.look_at(x,y)
            proxy.step()
    except (KeyboardInterrupt,EOFError):
        pass
    proxy.step()
    print 'Exiting...'
    bot.set_motor_power_off()
    proxy.step()
    time.sleep(0.25)
    proxy.stop()
