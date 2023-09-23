import numpy as np
import yaml, sys
from matplotlib import pyplot as plt

PEAKS       = "Craggy Peaks"
SOURCE      = "River Source"
RIVER       = "River Bend"
RIVERMOUTH  = "River Mouth"
LOOKOUTS    = "Lookout Trees"
LAKE        = "Lake"
TRAILHEAD   = "Trailhead"
FORT        = "Ruined Fort"
HOLDOUT     = "Piper Tunnel Holdout"
REDOUBT     = "Mysties' Redoubt"
DEAD        = "Dead"
FAR         = "Far Away"

# MILK = 0
# AARFIELD = 1
# BOBFIELD = 2
# MYSTIES = 3
# COORS = 4
# ARROGATRIX = 5
# TDH = 6
# SPOHRLOR = 7

MILK = "Milk Walker, Tick Boy"          
AARFIELD = "Aarfield Singer, Plant Pal"     
BOBFIELD = "Bobfield Dogwalker, the Prophet"
MYSTIES = "Mystietown"                     
HUMANS = "Melgol Granitegrater's outpost" 
ARROGATRIX = "Arrogatrix the Astounding"      
TDH = "Tall Dark and Handsome"         
SPOHRLOR = "The Nartogardic Spohrlor"        
PLAYERS = "The Player Characters"

with open('assets/start_state.yml', 'r') as outfile:
    char_dict = yaml.full_load(outfile)

# print(char_dict)

# Day starts at start time:
start_time = 7
# Day ends at nightfall, 8pm:
end_time = 20
# Name waypoints on the map
locations = {
            PEAKS       : [2, 4],
            SOURCE      : [1, 3],
            RIVER       : [2, 3],
            LOOKOUTS    : [4, 3],
            LAKE        : [4, 2],
            TRAILHEAD   : [4, 1],
            RIVERMOUTH  : [5, 1],
            FORT        : [5, 4],
            HOLDOUT     : [6, 2],
            REDOUBT     : [2, 2],
            DEAD        : [-1, -1],
            FAR         : [50, 50]
            }

# parties = [
#             "Milk Walker, Tick Boy",                
#             # "Aarfield Singer, Plant Pal",           
#             "Bobfield Dogwalker, the Prophet",      
#             "Mystietown",                           
#             "Coors Limestonebiter's outpost",       
#             "Arrogatrix the Astounding",        
#             "Tall Dark and Handsome",           
#             "The Nartogardic Spohrlor"              
#             ]

parties = [
            BOBFIELD,
            MILK,
            # AARFIELD,
            MYSTIES,
            HUMANS,
            ARROGATRIX,
            TDH,
            SPOHRLOR
            # PLAYERS
            ]

colors = {
    MILK            : (.55, .5, .2),
    # AARFIELD        : (.2, .6, 0),
    BOBFIELD        : (.8, .4, .4),
    MYSTIES         : (.4, 0, .50),
    HUMANS          : (.6, .4, 0),
    ARROGATRIX      : (0, 0, 1.0),
    TDH             : (.2, .2, .2),
    SPOHRLOR        : (.5, .4, .2),
    PLAYERS         : (0.1, .7, 0.1)
}

# branch = {}
# for person in parties:
#     branch[person] = []

# # Each line has format: [integer_hour_time, location_tag, string_description]
# branch[SPOHRLOR].append([17, HOLDOUT, "Eats humans"])
# branch[SPOHRLOR].append([10, LAKE, "Dead for trying to go to the lake"])
# branch[SPOHRLOR].append([14, LOOKOUTS, "Eating humans"])
# # branch[SPOHRLOR].append
# # branch[SPOHRLOR].append

with open("branch0.yaml", "r") as file:
    branch = yaml.safe_load(file)


fig = plt.figure(figsize = (7, 10), facecolor = (.7,.65,.5))
# Graphing functions I definitely want

def format_plot(ax):
     # Format graph
        # Make legend, set axes limits and labels
        
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                  ncols=2, mode="expand", borderaxespad=0.)
        ax.set_xlim(0, 7)
        ax.set_ylim(0, 7)
        ax.set_zlim(7, 20)
        ax.set_xlabel('East')
        ax.set_ylabel('North')
        ax.set_zlabel('Hour')
        ax.set_box_aspect([1,1,3])
        plt.tight_layout()


def plot_all(times=None):
    if times is None:
        times = np.linspace(start_time, end_time, 14)
    fig.clear()
    ax = fig.add_subplot(111, projection = '3d', )
    pos = []
    # Plot a line for each party:
    for p in parties:
        points = None
        for place in branch[p]:
            if DEAD in place[1]:
                # If the character died, just mark the location with a big X
                pos = [pos[0], pos[1], place[0]]
                ax.scatter(*pos, marker='X', s=80, color=colors[p])
                print("Adding Death marker at position {}".format([*pos[1:], place[0]]))
            else:
                pos = [*locations[place[1]], place[0]]
            if points is not None: 
                points = np.vstack([points, pos])
            else:
                points = np.array(pos)
        points = points.T
        ax.plot(points[0][:], points[1][:], points[2][:], zdir='z', label=p, color=colors[p], marker='*')
    format_plot(ax)


def whereYall(time):
    if time > 24:
        raise IndexError("That's too late.")
    fig.clear()
    latest_report = []
    reports = []
    for p in parties:
        latest_report = branch[p][0][:]
        # find latest Time before or equal to desired time
        for line in branch[p]:
            if line[0] <= time:
                if line[0] > latest_report[0]:
                    # This is the latest time we've found so far.
                    latest_report = line
        # Add the name of the party to the end of the report to keep things clear
        
        reports.append(latest_report)
        reports[-1].append(p)
    return reports

def island_state(time):
    reports = []
    reports = whereYall(time)
    string_output = ''
    for entry in reports:
        if string_output != '':
            string_output = string_output + ' \n> '
        
        string_output = string_output + entry[-1]
        string_output = string_output + ' is at '
        string_output = string_output + entry[1]
        string_output = string_output + ': '
        string_output = string_output + entry[2]

    return string_output

def whos_here(time, location):
    reports = whereYall(time)
    string_output = ''
    for entry in reports:
        if entry[1] == location:
            if string_output != '':
                string_output = string_output + ' \n '
            string_output = string_output + '> '    
            string_output = string_output + entry[-1]
            # string_output = string_output + ' is at '
            # string_output = string_output + entry[1]
            string_output = string_output + ': '
            string_output = string_output + entry[2]
    if string_output == '':
        string_output = "Nobody's here right now!"
    return string_output



killing_locations = [
    [RIVER,     .5],
    [RIVERMOUTH,.5],
    [SOURCE,    .3],
    [HOLDOUT,   .2],
    [REDOUBT,   .2],
    [TRAILHEAD, .2],
    [LAKE,      .6],
    [LOOKOUTS,  .3],
    [FORT,      .1],
    [PEAKS,     .1]]
killing_locs_total_weight = 0
for pair in killing_locations:
    killing_locs_total_weight += pair[1]    
rng = np.random.default_rng(seed=12347)

def rand_location():
    # Returns the name of a weighted-random location
    number =  killing_locs_total_weight * rng.random()
    # print("Number is {}".format(number))
    index = -1
    while number > 0.0:
        index += 1
        # Go down the weighted list of locations, decrement by weight,
        # and select the location where we run out of number.
        number = number - killing_locations[index][1]
        
    return killing_locations[index][0]


def spohrlor_sequence(duration):
    t = np.linspace(1,duration,duration)
    killdays = np.array([0,0,0,0])
    killcount = 0
    delay = 0
    last_feed = 0
    belly = 4
    for i in t:
        if i > last_feed + delay:
            killcount += belly
            killdays = np.vstack((killdays, np.array([i, belly, delay, rand_location()])))
            delay = 2 * np.log2(belly/2+1)
            belly = belly * 1 + (20 / (belly+5))
            last_feed = i
    return killdays[1:], killcount


array, total = spohrlor_sequence(15*12)

    
def ready_today(month):
    readies = np.array([0,0,0,0])
    for item in array[:]:
        if float(item[0]) % month == 0:
            readies = np.vstack((readies, item))
    return readies[1:]

def spohrlor_manifest(month):
    readies = ready_today(month)
    sleeping = np.array([a for a in array if not(a[0] in readies[:,0])])
    for item in set(list(array[:,3])):
        print("At {}: \t\t {} spohrlors hybernating and \t\t {} that woke up this morning.".format(\
            item, list(sleeping[:,3]).count(item), list(readies[:,3]).count(item)))



print(ready_today(6))


"""
for item in set(list(array[:,3])):
    print("At {}: {} spohrlors hybernating.".format(item, list(array[:,3]).count(item)))

# print(island_state(4))
# plot_all()
# plt.show()


"""

print("Ready!")
# exit()


def plot_slice(time, branch=None):
    """
    Plot a map with labeled points for all parties at their current locations at a given time.
    """
    fig.clear()
    ax = fig.add_axes(projection = '3d')

    # Then run the full 3d plot function, but only with the single time value.
    plot_all(time=time)

        
# exit()
# Not sure if gonna use:

class branch4d:
    """
    A matrix interpreter which pulls individual times, characters, and places from a big list
    to help against index headaches.
    Axes: 
        0: (right) Set list of characters
        1: (down) location at each timestamp (1 per hour for 13 hours) as strings 
        from the locations list
    """
    def __init__(self, parties):
        """
        Setup ofc
        """
        self.graph = parties


    
    def path_of(character):
        return 
    

# scratchpad
    

