
import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    ev3.Sound.speak("Are you ready for this maze?").wait()

    while not robot.touch_sensor.is_pressed:
        mqtt_client.send_message("on_Line_draw",
                                 [int(-robot.left_speed/25), int(robot.right_speed/25)])
        if robot.ir_sensor.proximity<35:
           robot.stop()
           ev3.Sound.speak("there is wall in front of me, dumbass")
        time.sleep(1)

        # if robot.left_speed!=robot.right_speed:
        #     mqtt_client.send_message("on_Line_draw",
        #                              [0, -int(robot.left_speed / 400)])
    robot.loop_forever()

main()