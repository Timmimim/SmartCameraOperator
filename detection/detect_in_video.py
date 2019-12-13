import os
import sys
import cv2
import pydarknet as pdNet
import time

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

if (not sys.argv[1] == "-i") and (not sys.argv[1] == "-v"):
    raise OSError("Wrong input - must set flag -i for image-, or -v for video classification.")

elif len(sys.argv) < 3:
    raise OSError("Wrong use; put argument -i <path_to_image> or -v <path_to_file>.")

else:
    DARKNET_LOCATION = "/home/timmimim/darknet"

    # Darknet YOLOv3 20000 epochs à 32 frames, racist but stable on test data
    net = pdNet.Detector(bytes(f"{DARKNET_LOCATION}/cfg/horsey-yolov3.cfg", encoding="utf-8"),
                   bytes(f"{DARKNET_LOCATION}/backup/horsey1_yolo3_lr.001/horsey-yolov3_20000.weights", encoding="utf-8"),
                   0,
                   bytes(f"{DARKNET_LOCATION}/data/horsey-obj.data", encoding="utf-8"))    
    """
    # Darknet tiny-YOLOv3
    net = pdNet.Detector(bytes(f"{DARKNET_LOCATION}/cfg/horsey-yolov3-tiny.cfg", encoding="utf-8"),
                   bytes(f"{DARKNET_LOCATION}/backup/horsey_tinyYOLOv3/horsey-yolov3-tiny_1700.weights", encoding="utf-8"),
                   0,
                   bytes(f"{DARKNET_LOCATION}/data/horsey-obj.data", encoding="utf-8"))
    """
    if sys.argv[1] == "-i":
        filepath = sys.argv[2]
        img = cv2.imread(filepath)

        start_time = time.time()

        img_darknet = pdNet.Image(img)

        results = net.detect(img_darknet)

        end_time = time.time()

        print(f"Time to classify frame: {end_time-start_time}")

        for category, score, bounds in results:
            x, y, w, h = bounds
            label = str(category.decode("utf-8"))
            if label == "horse":
                cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0),
                              thickness=2)
            if label == "horse":
                cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 0, 255),
                              thickness=2)
            cv2.putText(img, f"{label} ({score})", (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

        cv2.imwrite("out.jpg", img)

    elif sys.argv[1] == "-v":
        filepath = sys.argv[2]
        vid = cv2.VideoCapture(filepath)

        if vid.isOpened():
            # Find OpenCV version
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

            vid_output = cv2.VideoWriter("out-vid.mp4", cv2.VideoWriter_fourcc(*'DIVX'), fps, (width,height))

            average_time = 0
            total_time = 0
            frame_count = 0

            while True:
                if frame_count == num_total_frames:
                    break

                successfully_read, frame = vid.read()

                if successfully_read:
                    # Measuring Time taken by YOLO and API Call overhead
                    start_time = time.time()

                    dark_frame = pdNet.Image(frame)
                    results = net.detect(dark_frame)
                    del dark_frame

                    frame_count += 1
                    end_time = time.time()

                    classification_time = (end_time - start_time)
                    total_time += classification_time
                    average_time = total_time / frame_count
                    print(f"Time-Cost for current frame: {end_time-start_time}  (avg: {average_time})")

                    if len(sys.argv) == 5 and sys.argv[3] == "-sli":
                        target_dir = sys.argv[4]
                        os.makedirs(target_dir, exist_ok=True)
                        txt_name, img_name = create_filenames_txt_img(target_dir, frame_count-1)
                        txt_file = open(txt_name, "w+")
                        for cat, score, bounds in results:
                            class_found = str(cat.decode("utf-8"))
                            class_code = 2
                            if class_found == "horse":
                                class_code = 0
                            elif class_found == "rider":
                                class_code = 1
                            else:
                                pass
                            x, y, w, h = bounds
                            x_norm = (x - w/2) / width
                            y_norm = (y - h/2) / height
                            w_norm = (x + w/2) / width
                            h_norm = (y + h/2) / height
                            txt_file.write(f"{class_code} {x_norm} {y_norm} {w_norm} {h_norm}\n")
                        txt_file.close()
                        cv2.imwrite(img_name, frame)


                    for cat, score, bounds in results:
                        class_found = str(cat.decode("utf-8"))
                        class_code = (163, 161, 159)
                        if class_found == "horse":
                            class_code = (77, 166, 20)
                        elif class_found == "rider":
                            class_code = (82, 95, 206)
                        else:
                            pass

                        x, y, w, h = bounds
                        x = int((x - w / 2))
                        y = int((y - h / 2))
                        w = int((x + w))
                        h = int((y + h))

                        cv2.rectangle(frame, (x, y), (w, h), class_code, 6)
                        cv2.putText(frame, class_found, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, class_code, 3)

                    vid_output.write(frame)

                else:
                    frame_count += 1
                    print(f"Failed to read frame number {frame_count}.")

                if frame_count%50 == 0:
                    remaining_time = (num_total_frames-frame_count) * average_time
                    hours = int(remaining_time / 3600)
                    minutes = int((remaining_time % 3600) / 60)
                    print(f"\n\nCurrent frame: #{frame_count} of {num_total_frames}.",
                          f"\nApproximate time remaining: {hours}h {minutes}min {remaining_time - 3600*hours - 60*minutes}s\n\n")

            vid.release()
            vid_output.release()
            print("Finished classification.")

    else:
        pass
