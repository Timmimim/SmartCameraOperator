#!/usr/bin/python3

import ffmpeg
import PIL
import cv2
import sys
import os
import ntpath

if __name__ == '__main__' :
    print(sys.argv)

    if sys.argv[1]:
        file = sys.argv[1]
        try:
            with open(file, 'r') as fh:
                vid = cv2.VideoCapture(file)

                # Find OpenCV version
                (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

                if int(major_ver)  < 3 :
                    fps = vid.get(cv2.cv.CV_CAP_PROP_FPS)
                    print(f"Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {fps}")
                else :
                    fps = vid.get(cv2.CAP_PROP_FPS)
                    print(f"Frames per second using video.get(cv2.CAP_PROP_FPS) : {fps}")

                filename = os.path.splitext(os.path.basename(file))[0]
                os.makedirs(filename, exist_ok=True)

                input_vid = ffmpeg.input(file)
                audio = input_vid.audio
                video = input_vid.video

                vid.release()

        except FileNotFoundError:
            print("Please pass a valid path to a video file as the first CL parameter.")
    else:
        print("Please pass a valid path to a video file as the first CL parameter.")