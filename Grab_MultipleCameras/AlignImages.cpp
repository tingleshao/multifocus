// Grab_MultipleCameras.cpp
/*
    Note: Before getting started, Basler recommends reading the Programmer's Guide topic
    in the pylon C++ API documentation that gets installed with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the Migration topic in the pylon C++ API documentation.

    This sample illustrates how to grab and process images from multiple cameras
    using the CInstantCameraArray class. The CInstantCameraArray class represents
    an array of instant camera objects. It provides almost the same interface
    as the instant camera for grabbing.
    The main purpose of the CInstantCameraArray is to simplify waiting for images and
    camera events of multiple cameras in one thread. This is done by providing a single
    RetrieveResult method for all cameras in the array.
    Alternatively, the grabbing can be started using the internal grab loop threads
    of all cameras in the CInstantCameraArray. The grabbed images can then be processed by one or more
    image event handlers. Please note that this is not shown in this example.
*/

// Include files to use the PYLON API.
#include <pylon/PylonIncludes.h>
#ifdef PYLON_WIN_BUILD
#    include <pylon/PylonGUI.h>
#endif


#include <stdio.h>
#include <iostream>
#include "opencv2/highgui.hpp"
#include "opencv2/features2d.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/core.hpp"

#include "opencv2/xfeatures2d.hpp"
#include "opencv2/calib3d/calib3d.hpp"
 
using namespace cv;

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using cout.
using namespace std;
//using namespace xfeatures2d;
using namespace cv::xfeatures2d;

// Number of images to be grabbed.
static const uint32_t c_countOfImagesToGrab = 10;

// Limits the amount of cameras used for grabbing.
// It is important to manage the available bandwidth when grabbing with multiple cameras.
// This applies, for instance, if two GigE cameras are connected to the same network adapter via a switch.
// To manage the bandwidth, the GevSCPD interpacket delay parameter and the GevSCFTD transmission delay
// parameter can be set for each GigE camera device.
// The "Controlling Packet Transmission Timing with the Interpacket and Frame Transmission Delays on Basler GigE Vision Cameras"
// Application Notes (AW000649xx000)
// provide more information about this topic.
// The bandwidth used by a FireWire camera device can be limited by adjusting the packet size.

// TODO: fix the "vector not found" problem, or making a python version of align program and import the transformation parameters 
static const size_t c_maxCamerasToUse = 2;

int registerImg(Mat img1, Mat img2) {
    Mat gray_img1;
    Mat gray_img2;
    cvtColor(img1, gray_img1, CV_RGB2GRAY);
    cvtColor(img2, gray_img2, CV_RGB2GRAY);
    if (!gray_img1.data || !gray_img2.data) {
        cout << "error getting images" << endl; 
        return -1;
    }
    int minHessian = 400;
    
    Ptr<SURF> detector = SURF::create(minHessian); 
    std::vector< KeyPoint > keypoints_object, keypoints_scene;

    
    detector->detect(gray_img1, keypoints_object);
    detector->detect(gray_img2, keypoints_scene);
    
    //SurfDescriptorExtractor extractor;

    Mat descriptors_object, descriptors_scene; 
    detector->compute(gray_img1, keypoints_object, descriptors_object); 
    detector->compute(gray_img2, keypoints_scene, descriptors_scene);
   
    BFMatcher matcher(NORM_L2);
    
    //FlannBasedMatcher matcher;
    std::vector< DMatch > matches;
    matcher.match(descriptors_object, descriptors_scene, matches); 
 
    double max_dist = 0; 
    double min_dist = 100;
    
    for (int i = 0; i < descriptors_object.rows; i++) {
        double dist = matches[i].distance; 
        if (dist < min_dist) 
             min_dist = dist;
        if (dist > max_dist) 
             max_dist = dist;  
    }  
    
    printf("--Max dist: %f \n", max_dist);
    printf("--Min dist: %f \n", min_dist); 
   
    std::vector< DMatch > good_matches; 
   
    for (int i = 0; i < descriptors_object.rows; i++) {
        if (matches[i].distance < 3 * min_dist) {
            good_matches.push_back(matches[i]);     
        }
    }
    std::vector<Point2f> obj;
    std::vector<Point2f> scene;
   
    for (int i = 0; i< good_matches.size(); i++) {
        obj.push_back(keypoints_object[good_matches[i].queryIdx].pt); 
        scene.push_back(keypoints_scene[good_matches[i].trainIdx].pt);
    }
 
    Mat H = findHomography(obj, scene, CV_RANSAC);
    Mat result, small_result;
    warpPerspective(gray_img1, result, H, cv::Size(gray_img1.cols + gray_img2.cols, gray_img1.rows));
    Mat half(result, cv::Rect(0, 0, img2.cols, img2.rows));
    gray_img2.copyTo(half);   
    Size size(500, 358);
    resize(result, small_result, size);
    imshow("Result", small_result); 
     
    waitKey(0);
    return 0;
}


void function(int event, int x, int y, int flags, void* param) {

     if  ( event == EVENT_LBUTTONDOWN )
     {     
          if (*(double*)param < (double)50) { 
              *(double*)param = *(double*)param + 0.1;
          } 
          cout << "Left button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;
          cout << "param: " << *(double*)param << endl;
     }
     else if  ( event == EVENT_RBUTTONDOWN )
     {
          if (*(double*)param >= (double)1) { 
              *(double*)param = *(double*)param - 0.1;
          }
          cout << "Right button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;
          cout << "param: " << *(double*)param << endl;
     }
     else if  ( event == EVENT_MBUTTONDOWN )
     {
          cout << "Middle button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;
     }
     else if (event == EVENT_MOUSEHWHEEL) {
          cout << "mouse wheel scrolled - position (" << x << ", " << y << ")" << endl;
     }
     else if ( event == EVENT_MOUSEMOVE )
     {
          cout << "Mouse move over the window - position (" << x << ", " << y << ")" << endl;
     }

}


int main(int argc, char* argv[])
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized. 
    PylonInitialize();

    try
    {
        // Get the transport layer factory.
        CTlFactory& tlFactory = CTlFactory::GetInstance();

        // Get all attached devices and exit application if no device is found.
        DeviceInfoList_t devices;
        if ( tlFactory.EnumerateDevices(devices) == 0 )
        {
            throw RUNTIME_EXCEPTION( "No camera present.");
        }

        // Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices.
        CInstantCameraArray cameras( min( devices.size(), c_maxCamerasToUse));

        // Create and attach all Pylon Devices.
        for ( size_t i = 0; i < cameras.GetSize(); ++i) {
            cameras[ i ].Attach( tlFactory.CreateDevice( devices[ i ]));

            // Print the model name of the camera.
            cout << "Using device " << cameras[ i ].GetDeviceInfo().GetModelName() << endl;
        }

        // Starts grabbing for all cameras starting with index 0. The grabbing
        // is started for one camera after the other. That's why the images of all
        // cameras are not taken at the same time.
        // However, a hardware trigger setup can be used to cause all cameras to grab images synchronously.
        // According to their default configuration, the cameras are
        // set up for free-running continuous acquisition.
        cameras.StartGrabbing();

        // This smart pointer will receive the grab result data.
        CGrabResultPtr ptrGrabResult;
        CImageFormatConverter fc;
        fc.OutputPixelFormat = PixelType_RGB8packed;
        CPylonImage image;
        Mat cv_img(3840, 2748, CV_8UC3);
        Mat cv_img0(3840, 2748, CV_8UC3);
        Mat cv_img1(3840, 2748, CV_8UC3);


        int xoffset0 = 380;
        int yoffset0 = 150;
        int xoffset = 600;
        int yoffset = 0;
        int curr_x_lim0 = 3840 - xoffset0; 
        int curr_y_lim0 = 2748 - yoffset0;
        int curr_x_lim1 = 3840 - xoffset; 
        int curr_y_lim1 = 2748 - yoffset;
        Mat cv_img2(curr_x_lim0, curr_y_lim0, CV_8UC3);
        double parameter0 = 1.0;
        double parameter1 = 1.0;	
        double scale = 1; 
        Size size(500, 358);
        Mat dst;
        int is_grabbed0 = 0;
        int is_grabbed1 = 0;

        // Grab c_countOfImagesToGrab from the cameras.
        //for( int i = 0; i < c_countOfImagesToGrab && cameras.IsGrabbing(); ++i)
        while (cameras.IsGrabbing() && (!is_grabbed0 || !is_grabbed1)) {
            cameras.RetrieveResult( 5000, ptrGrabResult, TimeoutHandling_ThrowException);

            // When the cameras in the array are created the camera context value
            // is set to the index of the camera in the array.
            // The camera context is a user settable value.
            // This value is attached to each grab result and can be used
            // to determine the camera that produced the grab result.
            intptr_t cameraContextValue = ptrGrabResult->GetCameraContext();

#ifdef PYLON_WIN_BUILD
            // Show the image acquired by each camera in the window related to each camera.
            Pylon::DisplayImage(cameraContextValue, ptrGrabResult);
#endif

           const uint8_t *pImageBuffer = (uint8_t *) ptrGrabResult->GetBuffer();
            
           if (ptrGrabResult->GrabSucceeded()) {
               fc.Convert(image, ptrGrabResult);
               cv_img = cv::Mat(ptrGrabResult->GetHeight(),  ptrGrabResult->GetWidth(), CV_8UC3, (uint8_t*)image.GetBuffer());
  //              curr_x_lim0 = (int)((double)curr_x_lim0 / parameter0); 
 //               curr_y_lim0 = (int)((double)curr_y_lim0 / parameter0);
   //             curr_x_lim1 = (int)((double)curr_x_lim1 / parameter1); 
   //             curr_y_lim1 = (int)((double)curr_y_lim1 / parameter1);
             
    //            parameter0 = 1;
    //            parameter1 = 1;
	       if (cameraContextValue == 1) {
       //         cv_img2 = cv_img(Rect(xoffset0, yoffset0, curr_x_lim0, curr_y_lim0));
                   cv_img1 = cv_img.clone();
                   resize(cv_img, dst, size);
      //          if (curr_x_lim0 > 2000) 
      //          { 
                   imshow("CV_Image1", dst);
         //       } 	
       //         cvSetMouseCallback("CV_Image", function, &parameter0);	
                   is_grabbed1 = 1;
	       } else {
                 
        //        cv_img0 = cv_img(Rect(xoffset, yoffset, curr_x_lim1, curr_y_lim1));
                   cv_img0 = cv_img.clone();
                   resize(cv_img0, dst, size);
   //             if (curr_x_lim0 <= 2000) {
                   imshow("CV_Image0", dst);
    //                cvSetMouseCallback("CV_Image", function, &parameter1);	
    //            }		
      //          imshow("CV_Image2", dst);
       //         cvSetMouseCallback("CV_Image", function, &parameter1);
                   is_grabbed0 = 1;	
	       }                
	       waitKey(1);
               if (waitKey(30)==27) {
                   cameras.StopGrabbing();
               }
	   }
       }

   cout << "register img..." << endl;
   registerImg(cv_img0, cv_img1);
   }
   catch (const GenericException &e)  {
        // Error handling
       cerr << "An exception occurred." << endl
       << e.GetDescription() << endl;
       exitCode = 1;
   }
    
   
    // Comment the following two lines to disable waiting on exit.
   cerr << endl << "Press Enter to exit." << endl;
   while( cin.get() != '\n');
    // Releases all pylon resources. 
   PylonTerminate(); 
   return exitCode;
}
