# SmartCameraOperator
Practical Assignment complementing the Computer Vision lecture held by Prof. Dr. Risse at WWU Münster during the Winter Semester of 2019/20. 
The Practical is further supervised by Dr. Sören Klemm.

[<img src=./data/example_result_phase_3_multiple_horses_trajectory.png
/>](https://pjreddie.com/media/image/yologo_2.png)

### Goals
This project aims to create a smart detector for horse-rider-pairs in videos.
The detector must find all rider pairs in a scene, and extract the accompanying Regions of Interest (RoI).
RoIs are used to zoom in on the riders.

### Our approach
Our team decided to tackle the assignment using the Python, C and C++ programming languages, 
as well as the [Darknet](https://github.com/pjreddie/darknet "You only click once. ;-)") framework for Convolutional Neural Networks (CNNs)
and the YOLOv3 and tinyYOLOv3 network architectures.

For multiple data management tasks we created a number of Python3 scripts.  
We also compiled the Darknet framework on a Ubuntu Linux computer with a relatively low-end CUDA-able nVidia Graphics Card.

### Project Structure
The Project is split into different stages ('Iterations'), and a number of different but related problems.
The status of our project at any given stage is marked by a tagged commit.
Underlying data is not supplied here, as it would not be exactly reasonable, and also the volume far surpasses GitHub size limitations.
Data was supplied in the form of videos, as well as images extracted from them.


#### Iteration 1
Iteration 1 has no tag, as there was no code generated at that stage. It consisted of labelling only.
The labels were generated by hand by the participants of this practical, and arranged into a database by the supervisors.
Labelled images and the labels assigned to them were supplied later, the latter as a `.csv` file, as well as the original videos.

#### Iteration 2
At the basis of this step lies a self-trained Darknet-based YOLOv3 detector. 
Training was initialised from weights pre-trained on the [COCO](https://cocodataset.org/ "COCO") dataset, provided by [Joseph Chet Redmon](https://pjreddie.com/darknet/yolo/ "pjreddie").

*Iteration 2* was solved in multiple steps:

The `code/` directory contains two Python3 scripts. They manage our training data for the detector
`readCSVAndYolofy.py` reads the hard-coded target `'rimondo_filtered.csv'`, which contains the aforementioned labels.
The script creates objects for each user generating labels, each image they labelled, and each label set. 
Labels are then saved to uniquely named `.txt` files, and a copy of the corresponding image is saved alongside each file by the same name.
This forms the database used to train a *Machine Learning* based detector later. 
Our database spanned 105558 (highly redundant) images plus one label file each, amounting to 101.5GiB.    
`createYoloLearnList.py` creates two `.txt` files listing labelled images. 
The database created above is split into 90% training, and 10% validation data.   

Using this database, we trained the afforementioned YOLOv3 detector, which we then used via the `detect_in_video.py` script, 
located in the `detection/` directory.
This script is written around the [YOLO3-4-Py][yolo34py-gpu] Python-wrapper for Darknet, as a simple command line tool.   
There are different settings available for the tool via flags:

- *-i <path/to/frame>* &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; classify single image

- *-v <path/to/video>* &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; classify entire video

- *-v <path/to/video>* -z &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; classify video and zoom in on RoIs

- *-v <path/to/video>* -sli <out/dir/> &nbsp;&nbsp;&nbsp;&nbsp; **s**ave **l**abelled **i**mages as new YOLO training data

For more details, see the code and corresponding comments.

Finally, to speed up quality checks for newly generated labels and training data, we created a very simplistic Classification Reviewer tool.
The tool is written in C++ (ISO Standard C++17 necessary), uses OpenCV (Version 3.4 or higher), and can be found in the `classification_reviewer/` directory.
We also supply a `CMakeLists.txt` file to make compilation and usage easier on systems that have the `CMake` and `Make` tools installed.    
Our review tool only works on label data in the YOLO training data format.
The target directory holding the label data to be checked must be set in the source code before compilation.
The `+` key accepts the currently displayed labels, the `-` key automatically deletes labels file and corresponding image.


#### Iteration 3
In the final phase of the project, we introduced object tracking to speed up the runtime of our camera operator software. Using tracking, we no longer fully rely on our YOLO detector to find horse-rider pairs in every single frame. Instead, we only use detection in fixed intervals, and track all objects found between intervals. 

After doing some research, we decided to use the [Multitarget-Tracker](https://github.com/Smorodov/Multitarget-tracker) by Andrey Smorodov. Multitarget-Tracker is a very performant C++-implementation of tracking algorithms, including the Hungarian algorithm, and smoothing algorithms such as the Kalman filter. The tracker also integrates YOLO directly, supplying an object tracking pipeline. 

We modified this pipeline and added our own configurations, a full example script (added to the files in [examples](https://github.com/Timmimim/Multitarget-tracker/tree/master/example)), plus a camera-motion-simulation, cropping out the full area of interest (AOI) (which must include all horse-rider-pairs) and resizing the image section, calculating a weighted mean over a fixed interval of past AOIs to simulate a smoothed camera motion and zoom. The tool comes with CMake support. After compilation, this iteration of the _SmartCameraOperator_, inserted as example #7, can be used from the chosen _build_ directory:

- ./MultitargetTracker \<path_to_video> --example=7 [--start_frame]=\<start video from this position> [--end_frame]=\<play video to this position> [--out]=\<name of result video file> 

By using C++ and thus bypassing the added overhead of using a Python wrapper around YOLO, and by utilising the Tracker implementation provided by [Smorodov](https://github.com/Smorodov), we achieve real-time performance on the video material provided.

This prototype does NOT include a camera motion controller, but instead simulates camera motion in the output video.

A written report (in German :-/ ) can be found [here](./written_report/Ausarbeitung_Praktikum_CV_Kühnel_Krause_Loch.pdf).


### Software and Technology used
[<img src=https://pjreddie.com/media/image/yologo_2.png width="482" height="256"/>](https://pjreddie.com/media/image/yologo_2.png)
![Darknet][darknet]
![OpenCV][opencv]

[Darknet](https://github.com/pjreddie/darknet "Really super dark!"),
[YOLOv3](https://pjreddie.com/darknet/yolo/ "You only click once. ;-)"),
[Python 3.6^](https://www.python.org/ "Ni!!!"),
[YOLO3-4-Py][yolo34py-gpu]

##

##### Created by
Max Loch, Jacomo Krause und Timm Kühnel

##### Licence
GNU GPL v3

[yolo]: https://pjreddie.com/media/image/yologo_2.png "You only look once."
[darknet]: https://camo.githubusercontent.com/e69d4118b20a42de4e23b9549f9a6ec6dbbb0814/687474703a2f2f706a7265646469652e636f6d2f6d656469612f66696c65732f6461726b6e65742d626c61636b2d736d616c6c2e706e67 "So dark!!"
[opencv]: https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/OpenCV_Logo_with_text.png/195px-OpenCV_Logo_with_text.png "CV, but Open."
[yolo34py-gpu]: https://github.com/madhawav/YOLO3-4-Py "You only Python-wrap once. ;-)"