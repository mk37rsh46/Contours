import io
import base64
import numpy as np
import csv
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.tri import Triangulation, LinearTriInterpolator
from scipy.interpolate import griddata
from matplotlib.ticker import MaxNLocator
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def create_3d_graph(csv_data):
    csvreader = csv.reader(csv_data)
    data = [row for row in csvreader]
    data_array = np.array(data)[1:]
    indices_to_keep = data_array[:, 0] != ''
    data_array = data_array[indices_to_keep][:, :3]
    data_array = data_array.astype(float)

    Xs = data_array[:, 0]
    Ys = data_array[:, 1]
    Zs = data_array[:, 2]
    fig = Figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_trisurf(Xs-Xs.mean(), Ys-Ys.mean(), Zs, cmap=cm.jet, linewidth=0)
    fig.colorbar(surf)

    fig.tight_layout()
    buf = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buf)

    data = base64.b64encode(buf.getvalue()).decode()

    return f"<img src='data:image/png;base64,{data}'/>"

def create_contour_graph(csv_data, graph_type, interpolation_type):
    csvreader = csv.reader(csv_data)
    data = [row for row in csvreader]
    data_array = np.array(data)[1:]
    indices_to_keep = data_array[:, 0] != ''
    data_array = data_array[indices_to_keep][:, :3]
    data_array = data_array.astype(float)

    # Extract longitude, latitude, and depth arrays
    longitude = data_array[:, 0]
    latitude = data_array[:, 1]
    depth = data_array[:, 2]

    # Interpolate to add missing values 
    lon_min, lon_max = np.min(longitude), np.max(longitude)
    lat_min, lat_max = np.min(latitude), np.max(latitude)
    lon_grid, lat_grid = np.linspace(lon_min, lon_max, 100), np.linspace(lat_min, lat_max, 100)
    lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)

    triang = Triangulation(longitude, latitude)
    interpolator = LinearTriInterpolator(triang, depth)
    depth_interp = interpolator(lon_mesh, lat_mesh) if interpolation_type == "linear" else griddata((longitude, latitude), depth, (lon_grid[None,:], lat_grid[:,None]), method='nearest')


    fig = Figure()
    ax = fig.add_subplot(111)


    contour = ax.contourf(lon_mesh, lat_mesh, depth_interp, cmap='viridis') if graph_type == "contourf" else  ax.contour(lon_mesh, lat_mesh, depth_interp, cmap='viridis') 
    fig.colorbar(contour, ax=ax, label='Depth')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Contour Plot of Depth')

    buf = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buf)

    data = base64.b64encode(buf.getvalue()).decode()

    return f"<img src='data:image/png;base64,{data}'/>"
