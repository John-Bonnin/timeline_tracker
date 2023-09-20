import numpy as np
import yaml
from matplotlib import pyplot as plt

# Initialize figure
fig = plt.figure()

# Hacky way to add just one subplot, probably go back to plot later
ax = fig.add_subplot(1, 1, 1, projection='3d')

def subplot(self, alg, ax, max = None):
        """ Plot alg with average times above clustered time bars.
        :param alg: (dict) Dictionary of lists of per-test data addressed by keys 'samples', 
         'n_waypoints', and 'Graph Search Time'.
        :param ax: (mpl_toolkits.mplot3d.axes3d) 3d plot axes object onto which to plot data.
        :param max: (float) Optional maximum z-axis value; by default max is greater than
         maximum z value of plotted data.
        """ 

        num_tests = len(self.dict[alg][list(self.dict[alg])[0]])
        #print("count of tests = " + str(num_tests))
        test_color_tuples = [ (self.capped_interp(self.dict[alg]['samples'][x], 150, 1),
            self.capped_interp(self.dict[alg]['n_waypoints'][x], 150, 1),
            self.capped_interp(self.dict[alg]['Graph Search Time'][x], 2, 1))
            for x in range(0, num_tests) ]

        y_vals = [self.dict[alg]['n_waypoints'][x]+(.25*x)  for x in range(0, num_tests)  ]
        
        # Generate plot, amazingly just a single command thanks to matplotlib:
        ax.bar(self.dict[alg]['samples'], self.dict[alg]['Graph Search Time'], y_vals, 
             zdir='y', width=12, color=test_color_tuples, alpha=0.75 )

        a = list(set(tuple(zip(self.dict[alg]["samples"], self.dict[alg]["n_waypoints"]))))
        b = zip(self.dict[alg]["samples"], self.dict[alg]["n_waypoints"], self.dict[alg]["Graph Search Time"])
        zs = [0]*len(a)
        count = [0]*len(a)

        #Print the average time in seconds for each cluster of data
        for x, y, z in b:
            if (x,y) in a:
                n = a.index((x,y))
                # if(n==3):
                #     print('Index of cluster ' + str(x) + " " + str(y) + " is " + str(n) + " and we're adding " + str(z) + "+"+ str(zs[n]) +"=") 
                zs[n] = (zs[n] + z)
                # if(n==3):
                #     print("Running sum: " + str(zs[n]))
                count[n] += 1.0
            else:
                print("Index Error! Can't find cluster!")
        avg_z = [zs[i]/count[i] for i in range(len(zs))]

        b = zip(a, avg_z)
        for (x, y), z in b:
            if (x,y) in a:
                ax.text(x, y, z+.1, str(np.round(z, 3)), color=(0,0,.8), fontsize=8, zdir='y')
            else:
                print("Index Error! Can't find cluster!")

        # Format graph
        ax.set_xlabel('Samples')
        ax.set_ylabel('# of Waypoints')
        ax.set_zlabel('Search Time (s)')
        # On the axes let's only label the discrete values that we have data for.
        ax.set_yticks(self.dict[alg]['n_waypoints'])
        ax.set_xticks(self.dict[alg]['samples'])
        if(max != None):
            ax.set_zlim(top = max+.1)
        ax.set_title(alg, fontsize=8)

    def capped_interp(self, input, max, cap):
        return min(input/max, cap)