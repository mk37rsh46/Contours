import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from numpy.random import randn


# Replace .csv file and rename the file here
with open('20240411_Deeper_Sonar_120_min_05.csv', 'r') as csvfile:
    #Extract only rows where latitude and longitude are given
    csvreader = csv.reader(csvfile)
    data = [row for row in csvreader]
    data_array = np.array(data)[1:]
    indices_to_keep = data_array[:, 0] != ''
    data_array = data_array[indices_to_keep][:, :3]
    data_array = data_array.astype(float)
    Xs = data_array[:, 0]
    Ys = data_array[:, 1]
    Zs = data_array[:, 2]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_trisurf(Xs-Xs.mean(), Ys-Ys.mean(), Zs, cmap=cm.jet, linewidth=0)
    fig.colorbar(surf)
    

    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(6))
    ax.zaxis.set_major_locator(MaxNLocator(5))

    fig.tight_layout()
    plt.show()