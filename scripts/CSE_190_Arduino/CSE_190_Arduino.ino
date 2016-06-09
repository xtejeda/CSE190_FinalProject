#include <ros.h>
#include <std_msgs/String.h>

ros::NodeHandle nh;

std_msgs::String str_msg;
std_msgs::String startS;
std_msgs::String rightS;
std_msgs::String leftS;
std_msgs::String downS;
std_msgs::String upS;
std_msgs::String completeS;


// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int red1 = 8;    // down
int green1 = 9;  // up
int red2 = 10;   // left
int green2 = 11; // right

void messageHandler( const std_msgs::String& move_msg){
  
  str_msg.data = move_msg.data;
  //int char_msgS = str_msg.data.indexOf('S');
  //int char_msgR = str_msg.data.indexOf('S');
  //int char_msgL = str_msg.data.indexOf('S');
  //int char_msgD = str_msg.data.indexOf('S');
  //int char_msg = str_msg.data.indexOf('S');
  //int char_msg = str_msg.data.indexOf('S');
  
  startS.data = "S";
  rightS.data = "R";
  leftS.data = "L";
  downS.data = "D";
  upS.data = "U";
  completeS.data = "C";
  
  if(str_msg.data == startS.data)
  {
    digitalWrite(red1, HIGH);   // turn the LED on
    digitalWrite(green1, HIGH);   // turn the LED on
    digitalWrite(red2, HIGH);   // turn the LED on
    digitalWrite(green2, HIGH);   // turn the LED on
    delay(1000);                // wait for a second
    digitalWrite(red1, LOW);    // turn the LED off
    digitalWrite(green1, LOW);    // turn the LED off
    digitalWrite(red2, LOW);    // turn the LED off
    digitalWrite(green2, LOW);    // turn the LED off
    delay(1000);                // wait for a second
  }
  else if(str_msg.data == downS.data)
  {
    digitalWrite(red1, HIGH);   // turn the LED on 
    delay(1000);                // wait for a second
    digitalWrite(red1, LOW);    // turn the LED off
    delay(1000);                // wait for a second
  }
  else if(str_msg.data == upS.data)
  {
    digitalWrite(green1, HIGH); // turn the LED on
    delay(1000);                // wait for a second
    digitalWrite(green1, LOW);  // turn the LED off
    delay(1000);                // wait for a second
  }
  else if(str_msg.data == leftS.data)
  {
    digitalWrite(red2, HIGH);   // turn the LED on 
    delay(1000);                // wait for a second
    digitalWrite(red2, LOW);    // turn the LED off
    delay(1000);                // wait for a second
  }
  else if(str_msg.data == rightS.data)
  {
    digitalWrite(green2, HIGH); // turn the LED on 
    delay(1000);                // wait for a second
    digitalWrite(green2, LOW);  // turn the LED off 
    delay(1000);                // wait for a second
  }
  else if(str_msg.data == completeS.data)
  {
    digitalWrite(red1, HIGH);   // turn the LED on
    digitalWrite(green1, HIGH);   // turn the LED on
    digitalWrite(red2, HIGH);   // turn the LED on
    digitalWrite(green2, HIGH);   // turn the LED on
    delay(1000);                // wait for a second
    digitalWrite(red1, LOW);    // turn the LED off
    digitalWrite(green1, LOW);    // turn the LED off
    digitalWrite(red2, LOW);    // turn the LED off
    digitalWrite(green2, LOW);    // turn the LED off
    delay(1000);  
    
    digitalWrite(red1, HIGH);   // turn the LED on
    digitalWrite(green1, HIGH);   // turn the LED on
    digitalWrite(red2, HIGH);   // turn the LED on
    digitalWrite(green2, HIGH);   // turn the LED on
    delay(1000);                // wait for a second
    digitalWrite(red1, LOW);    // turn the LED off
    digitalWrite(green1, LOW);    // turn the LED off
    digitalWrite(red2, LOW);    // turn the LED off
    digitalWrite(green2, LOW);    // turn the LED off
    delay(1000);  
    
    digitalWrite(red1, HIGH);   // turn the LED on
    delay(1000);                // wait for a second
    digitalWrite(green1, HIGH);   // turn the LED on
    delay(1000);                // wait for a second
    digitalWrite(red2, HIGH);   // turn the LED on
    delay(1000);                // wait for a second
    digitalWrite(green2, HIGH);   // turn the LED on
    delay(1000);                // wait for a second
    digitalWrite(red1, LOW);    // turn the LED off
    delay(1000);                // wait for a second
    digitalWrite(green1, LOW);    // turn the LED off
    delay(1000);                // wait for a second
    digitalWrite(red2, LOW);    // turn the LED off
    delay(1000);                // wait for a second
    digitalWrite(green2, LOW);    // turn the LED off
    delay(1000);  
  }
  else
  {
    digitalWrite(green2, HIGH);    // turn the LED off
    delay(1000);
    digitalWrite(green2, LOW);    // turn the LED off
    delay(1000);
  }
}

ros::Subscriber<std_msgs::String> sub("/results/arduino", messageHandler);
 

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pins as outputs.
  pinMode(red1, OUTPUT);
  pinMode(green1, OUTPUT);
  pinMode(red2, OUTPUT);
  pinMode(green2, OUTPUT); 
 
  nh.initNode();
  nh.subscribe(sub); 
}

// the loop routine runs over and over again forever:
void loop() {
  
  nh.spinOnce();
  delay(1000);
  
}
