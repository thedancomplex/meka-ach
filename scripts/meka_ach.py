import m3.toolbox_head_s2 as m3h
import m3.rt_proxy as m3p
import m3.toolbox as m3t
import m3.component_factory as m3f
import m3.toolbox_beh as m3b


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

if __name__ == '__main__':
    # Init the robot
    proxy, bot, beh = init_robot()
