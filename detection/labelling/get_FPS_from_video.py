#!/usr/bin/python3

import cv2
import sys

if __name__ == '__main__' :
	if len(sys.argv) > 1:
		try:
			with open(sys.argv[1], 'r') as fh:
				video = cv2.VideoCapture(sys.argv[1]);

				# Find OpenCV version
				(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

				if int(major_ver)  < 3 :
					fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
					print(f"Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {fps}")
				else :
					fps = video.get(cv2.CAP_PROP_FPS)
					print(f"Frames per second using video.get(cv2.CAP_PROP_FPS) : {fps}")

				video.release(); 
		except FileNotFoundError:
			print("Please pass a valid path to a video file as the first CL parameter.")
	else:
		print("Please pass a valid path to a video file as the first CL parameter.")