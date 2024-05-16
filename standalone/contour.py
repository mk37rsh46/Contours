

import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib.tri import Triangulation, LinearTriInterpolator
from scipy.interpolate import griddata

#Replace with contour or contourf for different graph types
graph_mode = "contour"
#Replace with linear or nearest for different interpolation types
interpolation_type = "nearest"
with open('20240411_Deeper_Sonar_120_min_05.csv', 'r') as csvfile:
    #Extract only rows where latitude and longitude are given
    csvreader = csv.reader(csvfile)
    data = [row for row in csvreader]
    data_array = np.array(data)[1:]
    indices_to_keep = data_array[:, 0] != ''
    data_array = data_array[indices_to_keep][:, :3]
    data_array = data_array.astype(float)
    latitude = data_array[:, 0]
    longitude = data_array[:, 1]
    depth = data_array[:, 2]

    #Interpolate to add missing values
    lon_min, lon_max = np.min(longitude), np.max(longitude)
    lat_min, lat_max = np.min(latitude), np.max(latitude)
    lon_grid, lat_grid = np.linspace(lon_min, lon_max, 100), np.linspace(lat_min, lat_max, 100)
    lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)

    triang = Triangulation(longitude, latitude)

    interpolator = LinearTriInterpolator(triang, depth)
    depth_interp = interpolator(lon_mesh, lat_mesh) if interpolation_type == "linear" else griddata((longitude, latitude), depth, (lon_grid[None,:], lat_grid[:,None]), method='nearest')

    plt.figure()
    if graph_mode == "contourf": 
        plt.contourf(lon_mesh, lat_mesh, depth_interp, cmap='viridis')
    else:
        plt.contourf(lon_mesh, lat_mesh, depth_interp, cmap='viridis')
    plt.colorbar(label='Depth')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Contour Plot of Depth')
    cs = plt.contour(lon_mesh, lat_mesh, depth_interp, colors='k')
    plt.clabel(cs, inline=True, fontsize=8)
    plt.gca().xaxis.set_major_formatter(plt.FormatStrFormatter('%0.4f'))
    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%0.4f'))
    plt.show()
