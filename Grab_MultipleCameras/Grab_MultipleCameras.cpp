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

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/core/core.hpp"

using namespace cv;

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using cout.
using namespace std;

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


// TODO: tree implementation 
// TODO: map onto disk 
// TODO: test the disk

static const size_t c_maxCamerasToUse = 2;


class CameraNode {
    
    Mat data;
    vector<CameraNode> children;
    int upper_x;
    int upper_y;
    int w;
    int h;
    int xlim;
    int ylim;
    int name;
  //  CameraNode mom;
  
   public:
    void setData(); 
    Mat getData(void);
};

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


int main(int argc, char* argv[]) {
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
        for ( size_t i = 0; i < cameras.GetSize(); ++i)
        {
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

        		
        // Grab c_countOfImagesToGrab from the cameras.
        //for( int i = 0; i < c_countOfImagesToGrab && cameras.IsGrabbing(); ++i)
        while (cameras.IsGrabbing()) {
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
            // Print the index and the model name of the camera.
     //       cout << "Camera " <<  cameraContextValue << ": " << cameras[ cameraContextValue ].GetDeviceInfo().GetModelName() << endl;

            // Now, the image data can be processed.
     //       cout << "GrabSucceeded: " << ptrGrabResult->GrabSucceeded() << endl;
     //       cout << "SizeX: " << ptrGrabResult->GetWidth() << endl;
     //       cout << "SizeY: " << ptrGrabResult->GetHeight() << endl;
           const uint8_t *pImageBuffer = (uint8_t *) ptrGrabResult->GetBuffer();
     //       cout << "Gray value of first pixel: " << (uint32_t) pImageBuffer[0] << endl << endl;
            
           if (ptrGrabResult->GrabSucceeded()) {
                fc.Convert(image, ptrGrabResult);
                cv_img = cv::Mat(ptrGrabResult->GetHeight(),  ptrGrabResult->GetWidth(), CV_8UC3,(uint8_t*)image.GetBuffer());
                curr_x_lim0 = (int)((double)curr_x_lim0 / parameter0); 
                curr_y_lim0 = (int)((double)curr_y_lim0 / parameter0);
                curr_x_lim1 = (int)((double)curr_x_lim1 / parameter1); 
                curr_y_lim1 = (int)((double)curr_y_lim1 / parameter1);
             
                parameter0 = 1;
                parameter1 = 1;
	      if (cameraContextValue == 1) {
                cv_img2 = cv_img(Rect(xoffset0, yoffset0, curr_x_lim0, curr_y_lim0));
                resize(cv_img2, dst, size);
                if (curr_x_lim0 > 2000) 
                { 
                    imshow("CV_Image", dst);
                } 	
                cvSetMouseCallback("CV_Image", function, &parameter0);	
	    }  else {
                cv_img2 = cv_img(Rect(xoffset, yoffset, curr_x_lim1, curr_y_lim1));
                resize(cv_img2, dst, size);
                if (curr_x_lim0 <= 2000) {
                    imshow("CV_Image", dst);
                    cvSetMouseCallback("CV_Image", function, &parameter1);	
                }		
      //          imshow("CV_Image2", dst);
       //         cvSetMouseCallback("CV_Image", function, &parameter1);	
	    }                
	    waitKey(1);
            if(waitKey(30)==27) {
                cameras.StopGrabbing();
		        }
	       }
      }
    }
    catch (const GenericException &e) {
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
