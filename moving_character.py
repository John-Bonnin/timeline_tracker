import numpy as np
import tkinter as tk
from PIL import Image,ImageTk
from transitions import Machine

NAME = "name"
IMG = "img"
PLAN = "plan"

class Character(Machine):
    def __init__(self, definition, args) -> None:
        imscale = args["imscale"]
        self.imagename = definition["imname"]
        self.name = definition[NAME]
        self.image = ImageTk.PhotoImage(
            Image.open(definition["imname"]).resize((imscale,imscale), Image.LANCZOS))
        itinerary = definition[PLAN]
        self.plan = definition[PLAN]
        self.index = 0
        self.imscale = args["imscale"]
        self.stepscale = args["stepscale"]
        self.disturb = args["disturb"]

        # Machine.__init__(self, states=states, transitions=transitions, initial=START_STATE)

    def get_position(self, time):
        if time is None:
            time=self.index
        return self.plan[self.index][1:]
    
    def create_image(self, grid, time, debug=False):
        """
        :param grid: canvas object on which to create image
        :param time: time in itinerary to use for position
        """
        if time is None:
            time=self.plan[0][0]
        if str(time) in self.plan[:][0]:
            index = self.plan[:][0].index(str(time))
        else:
            raise ValueError("That time doesn't have a \
                             registered position in plan of {}!".format(self.name))
        if debug:
            print("Placing {} at location ({},{})".format(self.name, self.plan[index][1], self.plan[index][1]))
        # grid.create_line()
        # return grid.create_image((int(self.plan[index][1])+self.disturb)*self.stepscale,
        #                          (int(self.plan[index][2])+self.disturb)*self.stepscale,
        #                         anchor="center", image=self.image)
        x = (float(self.plan[index][1])+self.disturb[0])*self.stepscale
        y = (float(self.plan[index][2])+self.disturb[1])*self.stepscale
        print("X and Y are ({},{})".format(x, y))
        return grid.create_image(int(x),
                                 int(y),
                                 anchor="center",
                                 image=self.image)
    
        
    
    def step(self):
        self.index += 1 
        return self.get_position()

