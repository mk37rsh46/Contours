import numpy as np
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def stats(data):
    values, counts = np.unique(data, return_counts=True)
    mode_index = np.argmax(counts)
    mode = values[mode_index]

    return {
        'Range': np.ptp(data),
        'Median': np.median(data),
        'Mode': mode,
        'Standard Deviation': np.std(data),
        'Average': np.mean(data)
    }
    

with open('20240411_Deeper_Sonar_120_min_05.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    data = [row for row in csvreader]
    data_array = np.array(data)[1:]
    indices_to_keep = data_array[:, 0] != ''
    data_array = data_array[indices_to_keep][:, :3]
    data_array = data_array.astype(float)
    latitude = data_array[:, 0]
    longitude = data_array[:, 1]
    depth = data_array[:, 2]
    latitude_stats = stats(latitude)
    longitude_stats = stats(longitude)
    depth_stats = stats(depth)

    c = canvas.Canvas("rep.pdf", pagesize=letter)
    c.setAuthor("Keshav")
    title = "Statistical Report"
    c.setFont("Helvetica-Bold", 18)
    title_width = c.stringWidth(title)
    x = (letter[0] - title_width) / 2
    c.drawString(x, 750, title)
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, "Latitude Statistics:")
    for i, (key, value) in enumerate(latitude_stats.items()):
        c.drawString(120, 680 - i * 15, f"{key}: {value}")
    c.drawString(100, 580, "Longitude Statistics:")
    for i, (key, value) in enumerate(longitude_stats.items()):
        c.drawString(120, 560 - i * 15, f"{key}: {value}")
    c.drawString(100, 460, "Depth Statistics:")
    for i, (key, value) in enumerate(depth_stats.items()):
        c.drawString(120, 440 - i * 15, f"{key}: {value}")
    c.save()









