import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib.tri import Triangulation
from pykrige.ok import OrdinaryKriging

#WORK IN PROGRESS

# Replace with contour or contourf for different graph types
graph_mode = "contour"
# Replace with linear or nearest for different interpolation types
interpolation_type = "nearest"

with open('20240411_Deeper_Sonar_120_min_05.csv', 'r') as csvfile:
    # Extract only rows where latitude and longitude are given
    csvreader = csv.reader(csvfile)
    data = [row for row in csvreader]
    data_array = np.array(data)[1:]
    indices_to_keep = data_array[:, 0] != ''
    data_array = data_array[indices_to_keep][:, :3]
    data_array = data_array.astype(float)
    latitude = data_array[:, 0]
    longitude = data_array[:, 1]
    depth = data_array[:, 2]


    OK = OrdinaryKriging(latitude,longitude,depth,
        variogram_model='',
        verbose=True,
        enable_plotting=False,
        nlags=10,
    )
    # Set up kriging interpolation with min_points parameter
    gridx = np.arange(0, 50, 10, dtype='float64')
    gridy = np.arange(0, 30, 6, dtype='float64')
    zstar, ss = OK.execute("grid", gridx, gridy)

    cax = plt.imshow(zstar, extent=(0, 50, 0, 50), origin='lower')
    plt.scatter(latitude, longitude, c='k', marker='.')
    cbar=plt.colorbar(cax)
    plt.title('Porosity estimate')
    plt.show()
    