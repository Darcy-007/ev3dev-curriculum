"""This module is Darcy's project for CSSE120 course. It is designed for human to control the robot to
 go through a maze without human see the maze in front of it. It will use the pixy cam and the auto correct
 from the robot to help the human to make proper decision. Assuming the walls of the maze is all right angled. The command human can in put are the following:
 Go forth: robot go forth til the wall of the maze
 Go back: robot go back to the last place before it go forth
 Left: robot turn left and go forward
 Right: robot turn right and go forward
 stop: robot stop"""

from tkinter import *
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


def main():

    print('\x1b[6;30;43m'+"Are you ready for this maze?"+'\x1b[0m')
    command = input('\x1b[6;30;43m'+"Say Yes If You Are"+'\x1b[0m')
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    if command != "Yes":
        print('\x1b[6;30;42m'+"Guess I will see you next time..."+'\x1b[0m')
        mqtt_client.send_message("ev3.Sound.speak",[str("Guess I will see you next time...")])
        return
    else:
        print()
        print('\x1b[6;30;41m'+"Glad you chosed yes! Let us begin"+'\x1b[0m')

    root = tkinter.Tk()
    root.title("Darcy's Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()
    scale = Scale(root, orient=HORIZONTAL,to=900,length=200,troughcolor="azure")
    scale.orient = HORIZONTAL
    scale.grid(row=1,column=0)
    scale.set(scale.get())
    left_speed_entry=scale.get()
    right_speed_entry=scale.get()


    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=1, column=1)
    forward_button['command'] = lambda: drive_forward(mqtt_client,scale.get(),scale.get())
    root.bind('<Up>',lambda event:drive_forward(mqtt_client,scale.get(),scale.get()))


    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=2, column=0)
    left_button['command'] = lambda: drive_left(mqtt_client, scale.get())
    root.bind('<Left>',lambda event:drive_left(mqtt_client, scale.get()))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=2, column=1)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=2, column=2)
    right_button['command'] = lambda: drive_right(mqtt_client,scale.get())
    root.bind('<Right>', lambda event: drive_right(mqtt_client, scale.get()))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=3, column=1)
    back_button['command']= lambda: drive_backward(mqtt_client,scale.get(),scale.get())
    root.bind('<Down>', lambda event: drive_backward(mqtt_client, scale.get(), scale.get()))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=4, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=5, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=4, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))
    root.bind('<q>', lambda event: drive_left(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=5, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))
    root.bind('<Escape>', lambda event: quit_program(mqtt_client, True))

    root.mainloop()

def drive_backward(mqtt_client,left_speed_entry,right_speed_entry):
    print("drive_back")
    mqtt_client.send_message("back",[int(left_speed_entry), int(right_speed_entry)])


def drive_forward(mqtt_client,left_speed_entry,right_speed_entry):
    print("drive_forward")
    mqtt_client.send_message("forward",[int(left_speed_entry), int(right_speed_entry)])


def drive_left(mqtt_client,right_speed_entry):
    print("drive_left")
    mqtt_client.send_message("left",[ int(right_speed_entry)])


def drive_right(mqtt_client,right_speed_entry):
    print("drive_right")
    mqtt_client.send_message("right", [int(right_speed_entry)])



def stop(mqtt_client):
    print("stop_driving")
    mqtt_client.send_message("stop")


def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")



def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()