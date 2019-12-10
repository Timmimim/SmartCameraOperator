import os
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import sys


from os.path import join
from PIL import Image
from PIL import ImageDraw
from matplotlib.widgets import Button, CheckButtons

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
print(videos[1])
video_paths = [join(FRAME_SOURCE, d) for d in os.listdir(FRAME_SOURCE) if os.path.isdir(join(FRAME_SOURCE, d))]
print(video_paths[1])

pictures = [[join(video_paths[p], f) for f in os.listdir(video_paths[p]) if f.endswith(".png")] for p in range( len(video_paths))]

print(pictures[1][0])


def show(a, b):
    plt.subplot(111)
    plt.imshow(Image.open(pictures[a][b]), cmap='brg', aspect='equal', extent=(20, 80, 20, 80))
   # for i in range(len(videos)):
    #    im = Image.open(pictures[0][i], "r")
#
   #     im.show()


plt.figure(figsize=(16,9))

plt.title('frame')
plt.axis('off')
show(0,0)
plt.tight_layout()







class Index:
    data = videos
    data_min = 0
    data_max = len(data) - 1
    selected = 0

    def next(self, event):
        if self.selected >= self.data_max:
            self.selected = self.data_max

        else:
            self.selected += 1

            plt.title('frame')

            #plt.imshow(Image.open(pictures[self.selected][0]), cmap = 'brg', aspect= 'equal', extent=(20,80,20,80))
            show(0, self.selected)


    def prev(self, event):
        if self.selected <= self.data_min:
            self.selected = 0

        else:
            self.selected -= 1

            plt.title('frame')

            #plt.imshow(Image.open(pictures[self.selected][0]), cmap = 'brg', aspect= 'equal', extent=(20,80,20,80))
            show(0, self.selected)


callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])

bnext = Button(axnext, '>')
bnext.on_clicked(callback.next)

bprev = Button(axprev, '<')
bprev.on_clicked(callback.prev)

plt.show()