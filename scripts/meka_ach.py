import m3.toolbox_head_s2 as m3h
import m3.rt_proxy as m3p
import m3.toolbox as m3t
import m3.component_factory as m3f
import m3.toolbox_beh as m3b
import m3.head_s2csp_ctrl as m3csp
import time
import math

def init_robot():
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

    return (proxy, bot, beh)

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

    def zero(self):
        target=m3h.spherical_to_cartesian(0,0)
        self.csp.set_target_csp_frame(target)
        self.set_eye_slewrate_proportion(0.06)
        #print 'Zero'
        return m3b.res_continue

    def roll_backforth(self):
        amp=-10.0
        freq=0.2 #Hz
        des=amp*math.sin(time.time()*math.pi*2*freq)
        self.csp.set_theta_j2_deg(des)

    def roll_zero(self):
        self.csp.set_theta_j2_deg(0)

    def random(self):
        if time.time()-self.t_rand>6.0:
            self.t_rand=time.time()
            self.target_rand=[-10.0+(2*random.random()-1)*30.0,(2*random.random()-1)*70.0]
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
            print 'FaceDetectTarget',self.fd_target
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
        print self.csp



if __name__ == '__main__':
    # Init the robot
    proxy, bot, beh = init_robot()
    
    #ini the head
    tbox = m3h.M3HeadToolboxS2(bot.get_chain_component_name('head'),bot)

    #hb = HeadBehaviors()
    #hb.start(proxy,bot,beh)

    csp_name=proxy.get_available_components('m3head_s2csp_ctrl')[0]
    csp=m3csp.M3HeadS2CSPCtrl(csp_name)
    proxy.publish_command(csp)
    proxy.publish_param(csp)

    csp.set_target_csp_frame(m3h.spherical_to_cartesian(0,0))

    #eye_test = LookBehaviors(bot,csp,beh,False)
    #eye_test.roll_backforth()

    csp.enable()
    des = 10
    #csp.set_theta_j2_deg(des)

    #   distance (optical frame)     Left/right     Up/Down
    x = [ 40.1,                         20.0,        -2.0]
    
    print csp.param.origin
    csp.set_target_csp_frame(x)
    csp.set_theta_j2_deg(0)
    print csp.command
    #csp.set_target_head_base_frame(x)
    #csp.command.target[0] = csp.param.origin[0]
    #csp.command.target[1] = csp.param.origin[1]
    #csp.command.target[2] = csp.param.origin[2]
    print csp.command.target

#self.joint_names={'NeckTilt':0,
#                                  'NeckPan':1,
#                                  'HeadRoll':2,
#                                  'HeadTilt':3,
#                                  'EyeTilt':4,
#                                  'EyePanRight':5,
#                                  'EyePanLeft':6}
    # initilize data
    ts = time.time()
    proxy.step()

    try:
        while True:
           # proxy.step()
           # beh.step(verbose=True)
           a = 1
    except (KeyboardInterrupt,EOFError):
        print '---- Exiting ----'
        bot.set_motor_power_off()
        proxy.step()
        time.sleep(0.25)
        proxy.stop()
        pass
    bot.set_motor_power_off()
    proxy.step()
    time.sleep(0.25)
    proxy.stop()
