import tkinter as tk
import csv
import numpy as np
import os
from PIL import Image,ImageTk

IMG = "img"
LOCATION = "location"
ICON_ID = "icon_id"

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
    current_location = [i/stepscale for i in grid.coords(character_icons[itin[0]][ICON_ID])]
    step_move = [(square[0]-current_location[0]), 
                 (square[1]-current_location[1])]
    # Move the character's icon to the grid square
    grid.move(character_icons[itin[0]][ICON_ID], step_move[0]*stepscale, step_move[1]*stepscale)
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
root.geometry("550x650")
itineraries = openItenerary()
grid = tk.Canvas(root, width=500, height=500, background='gray75')
grid.pack()

stepscale = 75
imscale = 70

# Create a dictionary to store the character icons
character_icons = {"current_time":8}
# def populate():# For each character
for itin in itineraries[1:]:
    
    square = get_square(itin, 8)
    # Load the character's icon based on filename cell
    character_icons[itin[0]] = {
        IMG: ImageTk.PhotoImage(Image.open(itin[1] + '.png').resize((imscale,imscale), Image.LANCZOS)),
        "grid": square}
    
    # print("Image is {}, id is {}".format(type(icon), id(icon)))
    icon_id = grid.create_image(character_icons[itin[0]]["grid"][0]*stepscale,
                             character_icons[itin[0]]["grid"][1]*stepscale,
                             anchor="center", image=character_icons[itin[0]][IMG])

    character_icons[itin[0]][ICON_ID] = icon_id

    print("Added entry {}:{}".format(itin[0], character_icons[itin[0]]))

    # character_icons[itin[0]] = icon


grid.pack()

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

# Start the mainloop
root.mainloop() 