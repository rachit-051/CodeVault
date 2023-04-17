// 2 sides for each conveyor, L_16, R_16_error
#define totalStationsNum 9 // 10 stations on each side
#define laneNum 2 // 2 lanes for package collection

double conveyor_Speed = 800 / 13.3; // 80mm in 13.3sec

double servoDistance  = 80;  //80 mm from the center of the camera to the swing Arm
double RGB_strip_distance  = 420 + 15; //420 mm from the camera to the RGB strips

double RGB_module_distance = 100 / 3; // 33.3mm distance between each RGB module (mm)

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#define RGB_left_PIN        32
#define RGB_right_PIN       33
#define NUMPIXELS totalStationsNum

Adafruit_NeoPixel left_RGB_Lane(NUMPIXELS, RGB_left_PIN , NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel right_RGB_Lane(NUMPIXELS, RGB_right_PIN, NEO_GRB + NEO_KHZ800);


byte package_RGB_output[4][3] = {
  {0, 10, 10} //green for pickup
  , {0, 0, 0} //blue for package location
  , {0, 0, 0} //red for error package location
  , {0, 0, 0} //black for empty
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#include <Servo.h>
Servo swingArm;  // create servo object to control a servo
# define servoPin  18


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
int pos_light[totalStationsNum][laneNum]; // hold box position info       {-1 for empty space, 0-9 for positions, from 1-10 (station number) }

int incoming_package_destination[10];       // 0 is the latest, higher number are older records
unsigned long incoming_package_time[10];

unsigned long last_RGB_delay = 0;

unsigned long lastSwingArmTime = 0;
bool SwingArmBlock = 0;

void DisplayRGB()
{
  int j = 0;
  for (int station = 0; station < totalStationsNum; station++)
  {
    int pos_equal_station = (station == pos_light[station][j]);

    if (pos_equal_station)
    {
      left_RGB_Lane.setPixelColor(station, left_RGB_Lane.Color(200, 100 , 0 ));  //green for pickup
    }
    else if (pos_light[station][j] != -1)
    {
      left_RGB_Lane.setPixelColor(station, left_RGB_Lane.Color(0, 0 , 0 ));  //blue for package location
    }
    //    else if (pos_light[station][j] != -1)
    //    {
    //      left_RGB_Lane.setPixelColor(station, left_RGB_Lane.Color(10, 0 , 0 ));  //red for error package location
    //    }
    else
    {
      left_RGB_Lane.setPixelColor(station, left_RGB_Lane.Color(0, 0 , 0 ));  //black for empty
    }
  }

  j = 1;
  for (int station = 0; station < totalStationsNum; station++)
  {
    int pos_equal_station = (station == pos_light[station][j]);

    if (pos_equal_station)
    {
      right_RGB_Lane.setPixelColor(station, right_RGB_Lane.Color(200, 100 , 0 ));  //green for pickup
    }
    else if (pos_light[station][j] != -1)
    {
      right_RGB_Lane.setPixelColor(station, right_RGB_Lane.Color(0, 0 , 0 ));  //blue for package location
    }
    //    else if (pos_light[station][j] != -1)
    //    {
    //      right_RGB_Lane.setPixelColor(station, right_RGB_Lane.Color(10, 0 , 0 ));  //red for error package location
    //    }
    else
    {
      right_RGB_Lane.setPixelColor(station, right_RGB_Lane.Color(0, 0 , 0 ));  //black for empty
    }
  }
  left_RGB_Lane.show();
  right_RGB_Lane.show();
}
