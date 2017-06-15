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
# import m3.toolbox_ros as m3tr
import numpy as nu
import m3.pwr
import math
import random
import os
import roslib; roslib.load_manifest('shm_humanoid_controller')
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from m3ctrl_msgs.msg import *
from PyKDL import *
#import m3.joint_mode_ros_pb2 as mab
import m3.smoothing_mode_pb2 as mas
from threading import Thread
import m3.unit_conversion as m3u
import string


# ######################################################	

class LookBehaviors:
    def __init__(self,bot,csp,beh,use_fd):
        self.joints=range(7)
        self.beh=beh
        self.bot=bot 
        self.csp=csp
	self.use_fd=use_fd
	self.csp.enable()
	self.t_rand=time.time()
	self.t_slew=[m3t.M3Slew(),m3t.M3Slew(),m3t.M3Slew()]
	self.tbox=m3h.M3HeadToolboxS2(self.bot.get_chain_component_name('head'),bot)
	self.target_rand=[0,0]

	if use_fd:
	    self.fd=m3tr.M3FaceDetectThread('right',verbose=False)
	    #self.fd=m3tr.M3FaceTrackThread('middle',verbose=True)
	    self.fd.start()
	    self.fd_last=time.time()
	    self.fd_target=None
	    self.fd_rects=None
	   
	
    def stop(self):
	self.csp.set_target_csp_frame(m3h.spherical_to_cartesian(0,0))
	if self.use_fd:
	    self.fd.stop()
	
    def set_eye_slewrate_proportion(self,val):
	self.csp.set_slew_rate_proportion(4,val)
	self.csp.set_slew_rate_proportion(5,val)
	self.csp.set_slew_rate_proportion(6,val)
	
    def zero(self): #looks around (left and right)
	target=m3h.spherical_to_cartesian(0,0)
	self.csp.set_target_csp_frame(target)
	self.set_eye_slewrate_proportion(0.06)
	#print 'Zero MOFS'   
	self.joints[0]=20*3.14/180
	print "#####$$$$$$"	
	return m3b.res_continue
    
    def roll_backforth(self):
	amp=10.0
	freq=0.2 #Hz
        des=amp*math.sin(time.time()*math.pi*2*freq)
	self.csp.set_theta_j2_deg(des)
	
    def roll_zero(self):
	self.csp.set_theta_j2_deg(0)
    
    def random(self): #twix
	if time.time()-self.t_rand>6.0:
	    self.t_rand=time.time()
	    self.target_rand=[-10.0+(2*random.random()-1)*30.0,(2*random.random()-1)*70.0]
            print self.target_rand	
	self.csp.set_target_csp_frame(m3h.spherical_to_cartesian(self.target_rand[0],self.target_rand[1]))
	self.set_eye_slewrate_proportion(0.10)
        return m3b.res_continue
    
    def leftright(self):
	self.set_eye_slewrate_proportion(0.5)
        self.csp.enable()
	freq=0.3
	des=25.0*math.sin(freq*2*math.pi*time.time())
	target=m3h.spherical_to_cartesian(0,des)
	self.csp.set_target_csp_frame(target)
        return m3b.res_continue

    def face_detected(self):
	#print 'face_detected?'
	#if x>cx, increment x pos, else decr x pos, etc...
	self.fd_rects,dt=self.fd.get_detection()
	if self.fd_rects!=None and dt-self.fd_last>2.0:
	    xi=[self.fd_rects[0].x,self.fd_rects[0].y]
	    #xi=[457.698, 297.003]
	    self.fd_target=self.tbox.image_2_world('right',xi,r=1.0)
	    	 #Target is in the head-base frame
	    #print '-----------'
	    #print 'Pixel',xi
	    print 'FaceDettwixectTarget',self.fd_target
	    #self.fd_target=[1.125,.5,.260]
	    #print 'VirtualTarget',self.fd_target
	    #self.fd_target-self.bot.eye_2_world(eye,xe)
	    #print 'Xw',self.fd_target
	    self.fd_last=dt
	    return True
	return False
    
    def facetrack(self):
	#print 'LookFacetrack'
	
	#self.fd_rects,dt=self.fd.get_detection()
	#if self.fd_rects!=None:
	    #xi=[self.fd_rects[0].x,self.fd_rects[0].y]
	    ##cx=self.tbox.camera_calib['middle']['cx']
	    ##cy=self.tbox.camera_calib['middle']['cy']
	    ##bbox=10
	    ##xi=[max(-bbox,min(bbox,self.fd_rects[0].x-cx))+cx,max(-bbox,min(bbox,self.fd_rects[0].y-cy))+cy]
	    
	    #self.fd_target=self.tbox.image_2_world('middle',xi,r=1.0)
	    #print '-----------'
	    #print 'Pixel',xi
	    #print 'Target',self.fd_target

	if self.fd_target is not None:
	  
	    t=[self.t_slew[0].step(self.fd_target[0],0.05),
	       self.t_slew[1].step(self.fd_target[1],0.05),
	       self.t_slew[2].step(self.fd_target[2],0.05)]
	       
	    self.set_eye_slewrate_proportion(0.08)
	    self.csp.set_target_head_base_frame(self.tbox.world_2_head_base(t))
	    
	    
	    #target=m3h.spherical_to_cartesian(0,0)
	    #self.csp.set_target_csp_frame(target)
	    print 'Facetrack: ',t#World',t,'HeadBase',self.tbox.world_2_head_base(t)
	    return m3b.res_continue
	return m3b.res_finished
	   

# ######################################################   
#Glue class
class HeadBehaviors:
    def __init__(self):
	pass
    def start(self,proxy,bot,beh):
	
    
	csp_name=proxy.get_available_components('m3head_s2csp_ctrl')[0]
	self.csp=m3csp.M3HeadS2CSPCtrl(csp_name)
	proxy.publish_command(self.csp)
	proxy.publish_param(self.csp)
		
	    
	#print 'Use facetracking (Ros services must be started in advance) [n]?'
	#use_fd=m3t.get_yes_no('n')
	use_fd=False
	self.beh_look=LookBehaviors(bot,self.csp,beh,use_fd)
	beh.define_resource('look')
	beh.define_resource('look_roll')
        #twix
	#Higher priority is more likely to run
	beh.always('look','zero',priority=0,action=self.beh_look.zero) #looks left and right only (head)
	#beh.always('look','leftright',priority=0,action=self.beh_look.zero) #looks left and right only (head)
	#beh.random('look','leftright',priority=2,action=self.beh_look.leftright,chance=0.2,timeout=2.5, inhibit=6.0) #head and eyes right and left
	#beh.random('look','random',priority=1,action=self.beh_look.random,chance=.1,timeout=4.0, inhibit=8.0)	
	#beh.always('look_roll','roll_zero',priority=0,action=self.beh_look.roll_zero)
	#beh.random('look_roll','roll_backforth',priority=1,action=self.beh_look.roll_backforth,chance=0.1,timeout=2.5, inhibit=3.0)
    
    def stop(self):
	self.beh_look.stop()
	
# ###################################################### 	
if __name__ == '__main__':
    #Main creates bot and proxy, otherwise can be nested with other behavior script
    
    print "*********************************"
    print m3t.get_config_hostname()
    print "*********************************"

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
    hb=HeadBehaviors()
    hb.start(proxy,bot,beh)
    ts=time.time()
    proxy.step() #Initialize data.
    try:
	while True:
	    proxy.step() 
	    beh.step(verbose=True)
    except (KeyboardInterrupt,EOFError):
	pass
    
    proxy.step()
    print 'Exiting...'
    hb.stop()
    bot.set_motor_power_off()
    proxy.step()
    time.sleep(0.25)
    proxy.stop()
