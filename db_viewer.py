# this is a small example how to read the labels for the rimondo dataset using pandas
# and identifying the corresponding rectangles
# author: soeren.klemm@uni-muenster.de
# date: 19. Nov. 2019
import os
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import sys


from os.path import join
from PIL import Image
from PIL import ImageDraw
from matplotlib.widgets import Button, CheckButtons

import random  # not needed for productive use

# where to find the frames, must contain subfolders 'GOPR*' and 'GP0*'
#FRAME_SOURCE = ´"/rimondo_frames"
FRAME_SOURCE = "C:/Users/Maximilian Loch/Desktop/Uni/datareader/rimondo_frames"
# where to find the labels
#DATABASE = "/database/rimondo_filtered.csv"
DATABASE = "C:/Users/Maximilian Loch/Desktop/Uni/datareader/database/rimondo_filtered.csv"
# colors used for drawing rectangels
colors = {1: "red", 2: "lightgreen"}

label_data = pd.read_csv(DATABASE)

# names of all videos
videos = [d for d in os.listdir(FRAME_SOURCE) if os.path.isdir(join(FRAME_SOURCE, d))]


fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)


plt.figure(figsize=(8,3))

for vid in videos:
    video_path = join(FRAME_SOURCE, vid)
    frames = [f for f in os.listdir(video_path) if f.endswith(".png")]
    # this is just to get different frames displayed in every run
    random.shuffle(frames)
    print(videos.index(vid))

    for frame in frames:
        # images were stored as jpg on the server but are (lossless) png now
        id = vid + "/" + frame.replace("png", "jpg")

        image_file = join(video_path, frame)
        im = Image.open(image_file, "r")
        for item in [1, 2]:
            # select rows for the given image and current item (horse or rider)
            all_rects = label_data.loc[  (label_data["image"] == id) & (label_data["label"] == item) ]
            draw = ImageDraw.Draw(im)
            for _, entry in all_rects.iterrows():
                # x and y define the center of the bounding box
                # all values are relative to image height/width
                x = entry["x"] * im.width
                y = entry["y"] * im.height
                w = entry["width"] * im.width
                h = entry["height"] * im.height
                draw.rectangle(
                    ((x - w // 2, y - h // 2), (x + w // 2, y + h // 2)),
                    outline=colors[item],
                )

        plt.subplot(131+videos.index(vid))
        plt.title('frame' + str(videos.index(vid)))
        plt.axis('off')
        plt.imshow(im, cmap='brg')
        plt.tight_layout()
        plt.show()
        plt.imshow(frames[0], cmap='brg')
       #im.show()
        # only show one frame


       # callback = Index()

        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])

        bnext = Button(axnext, '>')
        bnext.on_clicked(callback.next)

        bprev = Button(axprev, '<')
        bprev.on_clicked(callback.prev)
        break
