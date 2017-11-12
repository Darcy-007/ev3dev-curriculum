"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    # DONE: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)
    def __init__(self):
        print('robot init')
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.left_speed = 0
        self.right_speed = 0
        self.t=0
        self.touch_sensor = ev3.TouchSensor()
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor.connected
        self.running = True
        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor.connected
        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor.connected
        self.pixy=ev3.Sensor(driver_name="pixy-lego")
        assert self.pixy.connected

    def drive_inches(self, inches_target, speed_deg_per_second):
        degrees_per_inch = 90
        motor_turns_needed_in_degrees = inches_target * degrees_per_inch#
        self.left_motor.run_to_rel_pos(position_sp=motor_turns_needed_in_degrees, speed_sp=speed_deg_per_second,
                                  stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=motor_turns_needed_in_degrees, speed_sp=speed_deg_per_second,
                                   stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self,degrees_to_turn,turn_speed_sp):
        if degrees_to_turn > 0:
            self.right_motor.run_to_rel_pos(position_sp=degrees_to_turn*5,speed_sp=turn_speed_sp, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.left_motor.run_to_rel_pos(position_sp=-degrees_to_turn*5, speed_sp=-turn_speed_sp, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        if degrees_to_turn < 0:
            self.right_motor.run_to_rel_pos(position_sp=degrees_to_turn*5,speed_sp=-turn_speed_sp, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.left_motor.run_to_rel_pos(position_sp=-degrees_to_turn*5, speed_sp=turn_speed_sp, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
    def trun_polygon(self,number_of_sides,edge_length_in,speed_deg_per_second):
        for k in range(number_of_sides):
            self.drive_inches(edge_length_in,speed_deg_per_second)
            self.turn_degrees(360/number_of_sides,speed_deg_per_second)

    def left(self, left_speed):

        self.turn_degrees(90,left_speed)
        self.forward(left_speed,left_speed)
        if self.t%4==0:
            self.right_speed = 0
            self.left_speed = left_speed
        if self.t%4==1:
            self.right_speed = -left_speed
            self.left_speed = 0
        if self.t%4==2:
            self.right_speed=0
            self.left_speed =-left_speed
        if self.t%4==3:
            self.right_speed=left_speed
            self.left_speed =0
        self.t+=1
        self.t = self.t % 4

    def right(self, left_speed):

        self.turn_degrees(-90, left_speed)
        self.forward(left_speed, left_speed)
        if self.t % 4 == 0:
            self.right_speed = 0
            self.left_speed = 1*left_speed
        if self.t % 4 == 1:
            self.right_speed = left_speed
            self.left_speed = 0
        if self.t % 4 == 2:
            self.right_speed = 0
            self.left_speed = -1*left_speed
        if self.t % 4 == 3:
            self.right_speed = -left_speed
            self.left_speed = 0
        self.t += 1
        self.t = self.t % 4

    def back(self, left_speed, right_speed):
        assert self.left_motor.connected
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)
        self.right_speed = -left_speed
        self.left_speed = 0

    def forward(self, left_speed, right_speed):
        assert self.left_motor.connected
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)
        self.right_speed = left_speed
        self.left_speed = 0

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()
        self.left_speed = 0
        self.right_speed = 0

    def arm_calibration(self):
        """
        Runs the arm up until the touch sensor is hit then back to the bottom again, beeping at both locations.
        Once back at in the bottom position, gripper open, set the absolute encoder position to 0.  You are calibrated!
        The Snatch3r arm needs to move 14.2 revolutions to travel from the touch sensor to the open position.

        Type hints:
          :type arm_motor: ev3.MediumMotor
          :type touch_sensor: ev3.TouchSensor
        """
        # DONE: 3. Implement the arm calibration movement by fixing the code below (it has many bugs).  It should to this:
        #   Command the arm_motor to run forever in the positive direction at max speed.
        #   Create an infinite while loop that will block code execution until the touch sensor's is_pressed value is True.
        #     Within that loop sleep for 0.01 to avoid running code too fast.
        #   Once past the loop the touch sensor must be pressed. So stop the arm motor quickly using the brake stop action.
        #   Make a beep sound
        #   Now move the arm_motor 14.2 revolutions in the negative direction relative to the current location
        #     Note the stop action and speed are already set correctly so we don't need to specify them again
        #   Block code execution by waiting for the arm to finish running
        #   Make a beep sound
        #   Set the arm encoder position to 0 (the last line below is correct to do that, it's new so no bug there)

        # Code that attempts to do this task but has MANY bugs (nearly 1 on every line).  Fix them!
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep().wait()
        # time.sleep(2)
        # arm_motor.stop(stop_action='brake')

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()
        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):
        """
        Moves the Snatch3r arm to the up position.

        Type hints:
          :type arm_motor: ev3.MediumMotor
          :type touch_sensor: ev3.TouchSensor
        """
        # DONE: 4. Implement the arm up movement by fixing the code below
        # Command the arm_motor to run forever in the positive direction at max speed.
        # Create a while loop that will block code execution until the touch sensor is pressed.
        #   Within the loop sleep for 0.01 to avoid running code too fast.
        # Once past the loop the touch sensor must be pressed. Stop the arm motor using the brake stop action.
        # Make a beep sound

        # Code that attempts to do this task but has many bugs.  Fix them!
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep()

    def arm_down(self):
        """
        Moves the Snatch3r arm to the down position.

        Type hints:
          :type arm_motor: ev3.MediumMotor
        """
        # DONE: 5. Implement the arm up movement by fixing the code below
        # Move the arm to the absolute position_sp of 0 at max speed.
        # Wait until the move completes
        # Make a beep sound

        # Code that attempts to do this task but has bugs.  Fix them.
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep()

        # DONE: 6. After you fix the bugs in the three arm movement commands demo your code to a TA or instructor.
        #
        # Observations you should make, the TouchSensor is easy to use, but the motor commands are still a little bit
        #   tricky.  It is neat that the same motor API works for both the wheels and the arm.

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def shutdown(self):
        # Modify a variable that will allow the loop_forever method to end. Additionally stop motors and set LEDs green.
        # The most important part of this method is given here, but you should add a bit more to stop motors, etc.
        self.running = False
        self.right_motor.stop()
        self.left_motor.stop()
        self.arm_motor.stop()

    def seek_beacon(robot):
        beacon_seeker = ev3.BeaconSeeker(channel=1)
        forward_speed = 300
        turn_speed = 100
        while not robot.touch_sensor.is_pressed:
            current_heading = beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = beacon_seeker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                robot.stop()
            else:
                if math.fabs(current_heading) < 2:
                    print("On the right heading. Distance: ", current_distance)
                    while True:
                        current_heading = beacon_seeker.heading  # use the beacon_seeker heading
                        current_distance = beacon_seeker.distance  # use the beacon_seeker distance
                        if math.fabs(current_heading) > 2:
                            break
                        if current_distance > 0:
                            robot.forward(300, 300)
                        if current_distance == 0:
                            time.sleep(0.5)
                            robot.stop()
                            return True
                        time.sleep(0.01)
                elif math.fabs(current_heading) > 10:
                    robot.stop()
                    print('Heading too far off')
                elif current_heading < 0:
                    print('turning left')
                    robot.left(200, 200)
                elif current_heading > 0:
                    print('turning right')
                    robot.right(200, 200)

            time.sleep(0.1)
        print("Abandon ship!")
        robot.stop()
        return False



