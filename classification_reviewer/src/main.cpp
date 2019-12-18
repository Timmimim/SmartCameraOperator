#include <opencv2/opencv.hpp>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <vector>
#include <string>
#include <cstdio>



//Put the directory with the images and the corresponding files here!
const char* directory = "/home/timmimim/Documents/WWU/Info_MSc/CV/SmartCameraOperator/data/data_and_labels";


namespace fs = std::filesystem;
using namespace std;

static vector<fs::path>pictures_path;



int main() {

	// iterate over given folder to catch all images and save the path in a vector
	// for iteration over subfolders, use recursive_directory_iterator
	for (const auto& p : fs::directory_iterator(directory)) {
		if (p.path().has_extension() && (p.path().extension() == ".png" || p.path().extension() == ".jpg")) {
			pictures_path.push_back(p.path());
		}
	}

    //Create a static window to load the different images into
    cv::namedWindow("Image", cv::WINDOW_NORMAL);
    cv::resizeWindow("Image", 960, 540);

	//definition of a temporary space to save the received rectangle data
	//not necessary but adds to the readability of the code 
	class rectangle {
	public:
		float index, x, y, height, width;
		rectangle(float index, float x, float y, float width, float height):
			index(index), x(x), y(y), width(width), height(height){}
	};


	//iterate over the vector we created at the top
	// basically the program will automatically skip to the next image, but on each iteration it waits for a key to be pressed 
	for (fs::path path : pictures_path) {
		cv::Mat image;
		image = cv::imread(path.string(), 1);
		cv::Vec2i size(image.size().width, image.size().height);
		std::vector<float> rectangle_data;


		//grab the image path and change it into .../xxx.txt
		string file_s = path.string();
		std::ifstream file(file_s.replace(file_s.end() - 3, file_s.end(), "txt"));
		std::string temp;
		
		
		//read the .txt line by line and then word by word to store it in another vector
		while (std::getline(file, temp)) {
			stringstream ss(temp);
			string item;

			while (getline(ss, item, ' ')) {
				rectangle_data.push_back(stof(item));
			}
		}
	
		//Iterate over the rectangle data and split it into rectangles
		for (int i = 0; i < rectangle_data.size() / 5; i++) {
			rectangle rect = rectangle(rectangle_data.at(i*5+0), rectangle_data.at(i*5+1), rectangle_data.at(i*5+2), rectangle_data.at(i*5+3), rectangle_data.at(i*5+4));

			cv::Scalar color;
			string Index;

			//
			if (rect.index == 0) {
				color = cv::Scalar(0, 0, 170);
				Index = "Horse";
			}
			else {
				color = cv::Scalar(0, 170, 0);
				Index = "Rider";
			}

			//create two points in order to draw the rectangle -> draw the rectangle
			cv::Point2f p1((rect.x - rect.width/2)*size(0), (rect.y - rect.height/2)*size(1));
			cv::Point2f p2((rect.x + rect.width/2)*size(0), (rect.y + rect.height/2)*size(1));
			cv::rectangle(image, p1, p2, color, 2);

			//create a small label  at the top
			cv::rectangle(image, p1, cv::Point2f(p1.x + 70, p1.y - 20), color, -10);
			cv::putText(image, Index, p1, 1, 1.5, cv::Scalar(255,255,255), 2);
		}


        cv::imshow("Image", image);
		cv::resizeWindow("Image", 960, 540);


        bool waiting = true;
		int secKey;
		while(waiting)
        {
            int key = (int)cv::waitKey(0);
            switch (key) {
                case 27: // "Esc"
                    cout << "Terminating" << endl;
                    return 0;
                case 43: // "+"
                    cout << "Good Yolo :)" << endl;
                    waiting = false;
                    break;
                case 45: // "-"
                    cout << "Bad Yolo!" << endl;

                    // FILE REMOVAL SECTION EDIT HERE:

                    fs::remove(path);
                    fs::remove(&file_s[0]);

                    waiting = false;
                    break;
                case 233:
                    secKey = int(cv::waitKey(0));
                    if (secKey == -1)
                    {
                        cv::destroyWindow("Image");
                        return 0;
                    }
                    break;
                case -1:
                    return 0;
                default:
                    cout << "Unknown Key: " << key << endl;
            }
        }
	}
    cv::destroyWindow("Image");
	return 0;
}