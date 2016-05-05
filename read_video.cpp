#include<iostream>
#include<fstream>
#include<cv.h>
#include<highgui.h>
#include<opencv2/features2d.hpp>


using namespace std;
using namespace cv;


int main(int argc, char *argv[]) {
    if (argc <= 1) {
        printf("Usage: %s video\n", argv[0]);
        return -1;
    }

    VideoCapture capture(argv[1]);

    if(!capture.isOpened()) {
        printf("Failed to open the video\n");
        return -1;
    }

    for(;;) {
        Mat frame;
        capture >> frame; // get a new frame from camera
    }

    return 0;
}


