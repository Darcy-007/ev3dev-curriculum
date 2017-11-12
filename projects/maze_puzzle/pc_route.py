import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com

class myDelegate():
    def __init__(self, canvas,coord):
        self.canvas = canvas
        self.coord=coord
    def on_Line_draw(self, x, y):
        c=len(self.coord)
        a=self.coord[c-2]
        b= self.coord[c-1]
        self.coord += [a+x]
        self.coord += [b-y]
        self.canvas.create_line(self.coord)


def main():
    top = tkinter.Tk()
    C = tkinter.Canvas(top, bg="white", height=500, width=500)
    coord = [250,500,250,500]
    my_delegate = myDelegate(C, coord)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()
    C.create_line(coord, fill="red")
    C.pack()
    top.mainloop()

main()