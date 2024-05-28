import csv
import numpy as np
def csv_file():
    with open('20240411_Deeper_Sonar_120_min_05.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            data = [row for row in csvreader]
            data_array = np.array(data)[1:]
            indices_to_keep = data_array[:, 0] != ''
            data_array = data_array[indices_to_keep][:, :2]
            data_array = data_array.astype(float)
            lat_sort  = np.argsort(data_array[:, 0])
            small_lat = data_array[lat_sort[0]]
            big_lat = data_array[lat_sort[-1]]
            long_sort  = np.argsort(data_array[:, 1])
            small_long = data_array[long_sort[0]]
            big_long = data_array[long_sort[-1]]
            with open("sample.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Latitude", "Longitude"])  # Write header
                writer.writerow(small_lat)
                writer.writerow(big_lat)
                writer.writerow(small_long)
                writer.writerow(big_long)



csv_file()