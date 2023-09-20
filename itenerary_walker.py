import tkinter as tk
import csv
import numpy as np
import os
from PIL import Image,ImageTk
from moving_character import Character
import yaml

IMG = "imname"
LOCATION = "location"
ICON_ID = "icon_id"
NAME = "name"
PLAN = "plan"

# Load the CSV file containing the character itineraries

def openItenerary():
    f = open('character_itineraries.csv')
    reader = csv.reader(f)
    itineraries = [row for row in reader]
    f.close()
    return itineraries

def get_square(itin, time):
    index = itineraries[0].index(str(time))
    return (int(itin[index]), int(itin[index+1]))
    
# Create a function to move the characters to the appropriate grid squares
def move_characters(time=None):
    # populate()
    # Get the current time of day
    if time is None:
        time = float(time_entry.get())
    for tick in itineraries[0][2:]:
        if time <= int(tick):
            time=int(tick)
            break
        # else:
        #     print("Time " + str(time) + " is later than tick " + str(tick) + "so let's check next tick.")
    if not (str(time) in itineraries[0][2:]):
        raise ValueError("Invalid time entered!")
        quit()
    print("---Selected time tick is " + str(time) + "---")

    # For each character
    for itin in itineraries[1:]:
        move_char(itin, time)

    print("all done")

def move_char(itin, time):
    # Get the grid square that the character should be in at the current time
    square = get_square(itin, time)
    current_location = [i/stepscale for i in grid.coords(character_icons[itin[0]])]
    step_move = [(square[0]-current_location[0]), 
                 (square[1]-current_location[1])]
    # Move the character's icon to the grid square
    grid.move(character_icons[itin[0]], step_move[0]*stepscale, step_move[1]*stepscale)
    print("Placed character {} from {} to {}, moving by {}".format(itin[0], current_location, square, step_move))
    character_icons[itin[0]][LOCATION] = square

def later():
    time = character_icons["current_time"]

    index = itineraries[0][2:].index(str(int(time)))    
    while float(itineraries[0][2:][index]) == time:
        index = index + 1
        if index >= len(itineraries[0][2:]):
            index = 0
            print("Looping back to start")
    character_icons["current_time"] = float(itineraries[0][2:][index])
    move_characters(character_icons["current_time"])
    

    print("---Selected time tick is " + str(time) + "---")
    
def earlier():
    time = character_icons["current_time"]

    index = itineraries[0][2:].index(str(int(time)))    
    while float(itineraries[0][2:][index]) == time:
        index = index - 1
        if index < 0:
            index = len(itineraries[0][2:]) - 1
            print("Looping back to start")
    character_icons["current_time"] = float(itineraries[0][2:][index])
    move_characters(character_icons["current_time"])
    

    print("---Selected time tick is " + str(time) + "---")
  

# Create a window
root = tk.Tk()
basedims = np.array([230, 140])
canvas_scale = 5
canvas_size = basedims * canvas_scale
# root.geometry("1050x950")
root.geometry(str(canvas_size[0]+200)+"x"+str(canvas_size[1]+200))
itineraries = openItenerary()
grid = tk.Canvas(root, width=canvas_size[0], height=canvas_size[1], background='gray75')
grid.pack()

stepscale = 75
imscale = 70


bg_img = ImageTk.PhotoImage(Image.open("assets/The Spit cropped.png").resize(canvas_size, Image.LANCZOS)),
# bg_label = tk.Label(grid, image = bg_img)
# bg_label.place(x=0, y=0)
grid.create_image(0, 0, anchor='nw', image=bg_img)

# Create a dictionary to store the character icons
character_icons = {"current_time":8}
# def populate():# For each character
# for itin in itineraries[1:]:
#     square = get_square(itin, 8)
#     # Load the character's icon based on filename cell
#     character_icons[itin[0]] = {
#         IMG: ImageTk.PhotoImage(Image.open("assets/" + itin[1] + '.png').resize((imscale,imscale), Image.LANCZOS)),
#         "grid": square}
#     # create images from each:
#     icon_id = grid.create_image(character_icons[itin[0]]["grid"][0]*stepscale,
#                              character_icons[itin[0]]["grid"][1]*stepscale,
#                              anchor="center", image=character_icons[itin[0]][IMG])
#     character_icons[itin[0]][ICON_ID] = icon_id
#     print("Added entry {}:{}".format(itin[0], character_icons[itin[0]]))

# Instantiate a bunch of moving_character objects in a list "chars"

def save_characters():
    chardict = dict()
    for a in chars:
        b = {"name": a.name,
             "pic": a.imagename,
             "plan": a.plan}
        chardict[a.name] = b
    with open('assets/start_state.yml', 'w') as outfile:
        yaml.dump(chardict, outfile, default_flow_style=False)
    

def next_offset(thing):
    j=thing[2]
    newThing = [0,0,j]
    distance = (np.floor(j/4)+1.0)/2
    newThing[0] = np.around(np.cos(np.pi * j/4), 2)*distance
    newThing[1] = np.around(np.sin(np.pi * j/4), 2)*distance
    newThing[2] += 1
    print('new thing is {}'.format(newThing))
    return newThing

chars = []
disturb = next_offset([0,0,1])
for itin in itineraries[1:]:
    args = {"imscale": imscale,
            "stepscale":stepscale,
            "disturb": disturb}
    definition = {IMG: "assets/" + itin[1] + '.png',
                                NAME: str(itin[0])
                                }
    # Transform the csv data into a triple-value plan: time, x, y format.
    plan = []
    i = 2    
    while i < len(itin[2:])-3:
        plan.append((itineraries[0][i], itin[i], itin[i+1]))
        i = i + 2

    definition[PLAN] = plan
    a = Character(definition, args)
    disturb = next_offset(disturb)

    chars.append(a)

    # create images from each:
    icon_id = a.create_image(grid, plan[0][0], debug=True)
    # icon_id = grid.create_image(plan[0][1]*stepscale,
    #                          plan[0][2]*stepscale,
    #                          anchor="center", image=a.image)

    character_icons[itin[0]] = icon_id
    print("Added entry {}:{}".format(itin[0], character_icons[itin[0]]))

    # grid.pack(side="top", padx=50, pady=50)

# Create a label for the time of day
time_label = tk.Label(root, text='Time of Day')
# .grid(row=0, column=16, columnspan=4, padx=5, pady=5)
time_label.pack()

# Create an entry box for the time of day
time_entry = tk.Entry(root)
# time_entry.grid(row=1, column=16, columnspan=4, padx=5, pady=5)
time_entry.pack()

# Create a button to move the characters
move_button = tk.Button(root, text='Move Characters', command=move_characters)
# move_button.grid(row=2, column=16, columnspan=4, padx=5, pady=5)
move_button.pack()

# Create a button to move the characters
later_button = tk.Button(root, text='Later', command=later)
# move_button.grid(row=2, column=16, columnspan=4, padx=5, pady=5)
later_button.pack()

# Create a button to move the characters
earlier_button = tk.Button(root, text='Earlier', command=earlier)
# move_button.grid(row=2, column=16, columnspan=4, padx=5, pady=5)
earlier_button.pack()

root.setvar("time_entry", character_icons["current_time"])

save_characters()
# exit()
# Start the mainloop
root.mainloop() 

exit()

# scratchpad
