import os
import sys
import cv2
import pydarknet
import time

# creates an individual file name by the scheme <outpath>/000000<.mime> for up to a million frames
# outpath must be a String, frame_count must be an Integer
def create_filenames_txt_img(outpath, frame_count):
    numPrefix = ""
    if frame_count < 10:
        numPrefix = "00000"
    elif frame_count < 100:
        numPrefix = "0000"
    elif frame_count < 1000:
        numPrefix = "000"
    elif frame_count < 10000:
        numPrefix = "00"
    elif frame_count < 100000:
        numPrefix = "0"
    elif frame_count > 1000000:
        raise IndexError("Too many frames for current settings (max 1,000,000 frames get individual name).")
    else:
        pass
    img_name = f"{outpath}/frame_{numPrefix}{frame_count}.png"
    txt_name = f"{outpath}/frame_{numPrefix}{frame_count}.txt"

    return txt_name, img_name

"""
    Calculate weighted mean of coordinate 4-tuples.
    A number of coordinates from the nearest past (i.e. closest to current frame) is weighted 
    to ensure keeping the current RoI near the center of the current frame. The remaining frames
    from the coordinate tuple array are included by a weight factor of 1 to compensate missing 
    frames/labels from unstable detection (mostly to compensate tinyYOLO's fickleness).
    
    params:
        array_of_four_tuples    Array;  holds a number of coordinate 4-tuples; organised as circular buffer
        frame_count             int;    index of current image in order of processing; 
                                        needed to locate coordinates to be weighted in the underlying ring memory  
        weight                  int;    
"""
def weighted_mean_coordinates(array_of_four_tuples, frame_count, weight):
    # x and y coordinates of a bounding boxes center
    # w and h are width and height of the BB
    x, y, w, h = 0.0, 0.0, 0.0, 0.0
    i = 0
    num_weighted_near_past_elements = 15
    while i < len(array_of_four_tuples):
        tuple = array_of_four_tuples[(frame_count-i) % len(array_of_four_tuples)]
        if i < num_weighted_near_past_elements:
            x += weight * tuple[0] / (len(array_of_four_tuples) + (weight-1) * num_weighted_near_past_elements)
            y += weight * tuple[1] / (len(array_of_four_tuples) + (weight-1) * num_weighted_near_past_elements)
            w += weight * tuple[2] / (len(array_of_four_tuples) + (weight-1) * num_weighted_near_past_elements)
            h += weight * tuple[3] / (len(array_of_four_tuples) + (weight-1) * num_weighted_near_past_elements)
        else:
            x += tuple[0] / (len(array_of_four_tuples) + (weight - 1) * num_weighted_near_past_elements)
            y += tuple[1] / (len(array_of_four_tuples) + (weight - 1) * num_weighted_near_past_elements)
            w += tuple[2] / (len(array_of_four_tuples) + (weight - 1) * num_weighted_near_past_elements)
            h += tuple[3] / (len(array_of_four_tuples) + (weight - 1) * num_weighted_near_past_elements)
        i += 1

    return int(x), int(y), int(w), int(h)

"""
    Calculate the mean of an array of coordinate 4-tuples
"""
def mean_coordinates(array_of_four_tuples):
    # x and y coordinates of a bounding boxes center
    # w and h are width and height of the BB
    x, y, w, h = 0.0, 0.0, 0.0, 0.0
    for idx, tuple in enumerate(array_of_four_tuples):
        x += tuple[0] / len(array_of_four_tuples)
        y += tuple[1] / len(array_of_four_tuples)
        w += tuple[2] / len(array_of_four_tuples)
        h += tuple[3] / len(array_of_four_tuples)
    return int(x), int(y), int(w), int(h)

if (not sys.argv[1] == "-i") and (not sys.argv[1] == "-v"):
    raise OSError("Wrong input - must set flag -i for image-, or -v for video classification.")

elif len(sys.argv) < 3:
    raise OSError("Wrong use; put argument -i <path_to_image> or -v <path_to_file>.")

else:
    DARKNET_LOCATION = "/home/timmimim/darknet"

    # Initialise neural network using YOLO architecture
    # TODO: Use your own weights and configs! If you would like to try ours, feel free to write us a friendly message.

    # Darknet YOLOv3 20000 epochs à 32 frames, racist but stable on test data
    net = pydarknet.Detector(bytes(f"{DARKNET_LOCATION}/cfg/horsey-yolov3.cfg", encoding="utf-8"),
                   bytes(f"{DARKNET_LOCATION}/backup/horsey1_yolo3_lr.001/horsey-yolov3_20000.weights", encoding="utf-8"),
                   0,
                   bytes(f"{DARKNET_LOCATION}/data/horsey-obj.data", encoding="utf-8"))    
    """
    # Darknet tiny-YOLOv3
    net = pydarknet.Detector(bytes(f"{DARKNET_LOCATION}/cfg/horsey-yolov3-tiny2.cfg", encoding="utf-8"),
                             bytes(f"{DARKNET_LOCATION}/backup/horsey-yolov3-tiny2_5500.weights", encoding="utf-8"),
                             0,
                             bytes(f"{DARKNET_LOCATION}/data/horsey-obj.data", encoding="utf-8"))
    """

    # label a single image
    if sys.argv[1] == "-i":
        filepath = sys.argv[2]
        img = cv2.imread(filepath)

        # time the classification
        start_time = time.time()

        # Use YOLO Darknet to classify the image and store the results
        img_darknet = pydarknet.Image(img)
        results = net.detect(img_darknet)

        end_time = time.time()

        print(f"Time to classify frame: {end_time-start_time}")

        for category, score, bounds in results:
            # Bounds are BoundingBox coordinates, with x,y the centre, and w,h as width and height
            x, y, w, h = bounds
            # Label as found be YOLO CNN
            label = str(category.decode("utf-8"))

            # Draw Bounding Boxes around found RoIs, with different colours depending on found label/class
            if label == "horse":
                cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0),
                              thickness=2)
            if label == "horse":
                cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 0, 255),
                              thickness=2)

            # Write label and confidence score above each BoundingBox
            cv2.putText(img, f"{label} ({score})", (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

        # Save image
        cv2.imwrite("out.jpg", img)

    # flag to label an entire video set (-v)
    elif sys.argv[1] == "-v":
        # video passed as path in arguments (argv[2])
        filepath = sys.argv[2]
        # read video
        vid = cv2.VideoCapture(filepath)

        try:
            # Check if video could be opened; if yes, process it
            if vid.isOpened():
                # Find OpenCV version, to determine parameters that have been changed between versions
                (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

                if int(major_ver) < 3:
                    fps = vid.get(cv2.cv.CV_CAP_PROP_FPS)
                    print(f"Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {fps}")
                    # get vid property
                    width = int(vid.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
                    height = int(vid.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
                    # number frames in video
                    num_total_frames = int(vid.get(cv2.cv.CV_CAP_PROP_POS_FRAME_COUNT))
                else:
                    fps = vid.get(cv2.CAP_PROP_FPS)
                    print(f"Frames per second using video.get(cv2.CAP_PROP_FPS) : {fps}")
                    # get vid property
                    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    # number frames in video
                    num_total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

                # Open an output stream to write the labelled video to
                vid_output = cv2.VideoWriter("out-vid.mp4", cv2.VideoWriter_fourcc(*'DIVX'), fps, (width,height))

                try:
                    # variables to time classification, which will be updated and logged for convenience
                    average_time = 0
                    total_time = 0

                    # numbers of frames processed so far
                    frame_count = 0

                    # initialise a circular buffer (or ring memory) as an Array of size 80, holding 4-tuples of coordinates
                    past_frames_roi = [(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),
                                       (0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height),(0,0,width,height)]

                    while True:
                        # if all frames have been read, end loop and finish classification
                        if frame_count == num_total_frames:
                            break

                        # read next frame
                        successfully_read, frame = vid.read()

                        if successfully_read:
                            # Measuring Time taken by YOLO and API Call overhead
                            start_time = time.time()

                            # Use YOLO Darknet to classify the image and store the results
                            dark_frame = pydarknet.Image(frame)
                            results = net.detect(dark_frame)
                            del dark_frame

                            frame_count += 1
                            end_time = time.time()

                            # get time used for classification and update the average time consumption; then log
                            classification_time = (end_time - start_time)
                            total_time += classification_time
                            average_time = total_time / frame_count
                            print(f"Time-Cost for current frame: {end_time-start_time}  (avg: {average_time})")

                            # if save labelled images flag (-sli) is set in argv[3], do that; output directory must be passed in argv[4]
                            if len(sys.argv) == 5 and sys.argv[3] == "-sli":
                                target_dir = sys.argv[4]
                                os.makedirs(target_dir, exist_ok=True)

                                # use filename creation function to get individual but matching names for frames' txt and img files
                                txt_name, img_name = create_filenames_txt_img(target_dir, frame_count-1)

                                # open txt file stream
                                txt_file = open(txt_name, "w+")
                                for cat, score, bounds in results:
                                    # Label as found be YOLO CNN
                                    class_found = str(cat.decode("utf-8"))
                                    class_code = 2
                                    # translate label back to numeric representation used in YOLO (we used 0 for horse, 1 for rider)
                                    if class_found == "horse":
                                        class_code = 0
                                    elif class_found == "rider":
                                        class_code = 1
                                    else:
                                        pass
                                    # bounds are BoundingBox coordinates, with x,y the centre, and w,h as width and height
                                    x, y, w, h = bounds

                                    # normalise coordinates to fit YOLO training format requirements
                                    x_norm = x / width
                                    y_norm = y / height
                                    w_norm = w / width
                                    h_norm = h / height
                                    txt_file.write(f"{class_code} {x_norm} {y_norm} {w_norm} {h_norm}\n")
                                txt_file.close()
                                cv2.imwrite(img_name, frame)

                            # if zoom flag (-z) is set
                            elif len(sys.argv) == 4 and sys.argv[3] == "-z":
                                # get the position (index) the current frames RoI will be saved at in the frame ring memory
                                array_position = frame_count % len(past_frames_roi)

                                frame_min_x = width
                                frame_min_y = height
                                frame_max_x = 0
                                frame_max_y = 0

                                # in case of no RoIs found, copy the last RoI coordinates found (i.e. pause camera motion and zoom)
                                if len(results) == 0:
                                    past_frames_roi[array_position] = past_frames_roi[(frame_count -1) % len(past_frames_roi)]

                                else:
                                    for cat, score, bounds in results:
                                        # Label as found be YOLO CNN
                                        class_found = str(cat.decode("utf-8"))

                                        # use certain colour codes, depending on class found by detector
                                        class_code = (163, 161, 159)
                                        if class_found == "horse":
                                            class_code = (77, 166, 20)
                                        elif class_found == "rider":
                                            class_code = (82, 95, 206)
                                        else:
                                            pass

                                        # Bounds are BoundingBox coordinates, with x,y the centre, and w,h as width and height
                                        x, y, w, h = bounds
                                        # Change coordinates, so x,y are top left corner, w,h mark bottom right
                                        x = int((x - w / 2))
                                        y = int((y - h / 2))
                                        w = int((x + w))
                                        h = int((y + h))

                                        # draw and label the BoundingBox for the current RoI
                                        cv2.rectangle(frame, (x, y), (w, h), class_code, 6)
                                        cv2.putText(frame, class_found, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, class_code, 6)

                                        # Join Regions of Interest of current frame, to include them all in the Zoom Region
                                        if x < frame_min_x:
                                            frame_min_x = x
                                        if y < frame_min_y:
                                            frame_min_y = y
                                        if w > frame_max_x:
                                            frame_max_x = w
                                        if h > frame_max_y:
                                            frame_max_y = h

                                        #print(f"frame curr: {x},{y}, {w}, {h}")
                                        #print(f"min // max: {frame_min_x}, {frame_min_y}, {frame_max_x}, {frame_max_y}")

                                    # extend frames min and max RoI coordinates by 10% of the frame size in each direction (if possible, else extend to border)
                                    if frame_min_x - int(width*.1) < 0:
                                        frame_min_x = 0
                                    else:
                                        frame_min_x -= int(width*.1)

                                    if frame_min_y - int(height*.1) < 0:
                                        frame_min_y = 0
                                    else:
                                        frame_min_y -= int(height*.1)

                                    if frame_max_x + int(width*.1) > width:
                                        frame_max_x = width
                                    else:
                                        frame_max_x += int(width*.1)

                                    if frame_max_y + int(height*.1) > height:
                                        frame_max_y = height
                                    else:
                                        frame_max_y += int(height*.1)

                                    # Add RoI to ring memory array
                                    past_frames_roi[array_position] = (frame_min_x, frame_min_y, frame_max_x, frame_max_y)

                                #print(f"frame total:{past_frames_roi[array_position]}")

                                # Calculate weighted mean of RoI coordinates
                                curr_min_x, curr_min_y, curr_max_x, curr_max_y = weighted_mean_coordinates(past_frames_roi, frame_count, 6)

                                #print(f"\nglobal: {curr_min_x}, {curr_min_y}, {curr_max_x}, {curr_max_y}\n")

                                # extract mean RoI from frame
                                frame = frame[curr_min_y:curr_max_y, curr_min_x:curr_max_x]

                                # resize RoI to original frame size, i.e. Zoom in on it
                                try:
                                    frame = cv2.resize(frame, (width,height))
                                except cv2.error:
                                    print(f"\n\nWARNING: OpenCV Error during resizing:\n Frame size: {frame.size}, (newH,newW): ({height}, {width})\n\n")

                            # no extra flag set, so only label video
                            else:
                                for cat, score, bounds in results:
                                    # Label as found be YOLO CNN
                                    class_found = str(cat.decode("utf-8"))

                                    # use certain colour codes, depending on class found by detector
                                    class_code = (163, 161, 159)
                                    if class_found == "horse":
                                        class_code = (77, 166, 20)
                                    elif class_found == "rider":
                                        class_code = (82, 95, 206)
                                    else:
                                        pass

                                    # Bounds are BoundingBox coordinates, with x,y the centre, and w,h as width and height
                                    x, y, w, h = bounds

                                    # Change coordinates, so x,y are top left corner, w,h mark bottom right
                                    x = int((x - w / 2))
                                    y = int((y - h / 2))
                                    w = int((x + w))
                                    h = int((y + h))

                                    # draw and label the BoundingBox for the current RoI
                                    cv2.rectangle(frame, (x, y), (w, h), class_code, 6)
                                    cv2.putText(frame, class_found, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, class_code, 3)

                            # Write the current frame to the output video stream
                            vid_output.write(frame)

                        # if the current frame could (for any reason) not be read, skip it, but bump frame_count
                        else:
                            frame_count += 1
                            print(f"Failed to read frame number {frame_count}.")

                        # Every 50 frames, log state and average time consumption
                        if frame_count%50 == 0:
                            remaining_time = (num_total_frames-frame_count) * average_time
                            hours = int(remaining_time / 3600)
                            minutes = int((remaining_time % 3600) / 60)
                            print(f"\n\nCurrent frame: #{frame_count} of {num_total_frames}.",
                                  f"\nApproximate time remaining: {hours}h {minutes}min {remaining_time - 3600*hours - 60*minutes}s\n\n")

                    # Job done, close streams
                    vid.release()
                    vid_output.release()
                    print("Finished classification.")

                except KeyboardInterrupt:
                    vid_output.release()
                    print("Video Output Stream closed upon KeyboardInterrupt.")
                    raise KeyboardInterrupt

        except KeyboardInterrupt:
            vid.release()
            print("Video Read Stream closed upon KeyboardInterrupt.")
    else:
        pass
