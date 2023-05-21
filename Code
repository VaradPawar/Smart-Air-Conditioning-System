#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>
#include <FS.h>
 
// Setting WiFi information(Modify this part with your WiFi information)
const char* ssid = "myiphone"; // wifi name
const char* password = "12345678"; // password
const char* mqttServer = "broker.hivemq.com";
 
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

#define IR_PIN 4
IRsend irsend(IR_PIN);  // An IR LED is controlled by GPIO pin 4 (D2)

// Define the IR codes for power on/off, and temperature
// Replace these with the actual IR codes for your air conditioner
#define IR_POWER_ON 0xA90
#define IR_POWER_OFF 0xF609
#define IR_TEMPERATURE_UP 0xE817
#define IR_TEMPERATURE_DOWN 0xE01F

String file_name = "temperature.txt";
int current_temp;
bool aircon_on = false;
 
void setup() {
  pinMode(IR_PIN, OUTPUT);     
  Serial.begin(9600);  
  
  WiFi.mode(WIFI_STA);
  
  // Connect to wifi
  Serial.println("Trying to connect WiFi");
  connectWifi();
  
  // Set MQTT server and broker port
  mqttClient.setServer(mqttServer, 1883);
  // Set MQTT callback function
  mqttClient.setCallback(receiveCallback);
 
  // Connect to MQTT server
  connectMQTTserver();

  // Load current temperature
  if (SPIFFS.begin()){ 
    Serial.println("");
  } else {
    Serial.println("SPIFFS Failed to Start.");
  }
  
  if (SPIFFS.exists(file_name)){
    Serial.print(file_name);
    Serial.println(" FOUND.");
    File dataFile = SPIFFS.open(file_name, "r"); 
    Serial.print("Current Temperature: ");
    current_temp = (dataFile.read() - 48) * 10;
    current_temp += dataFile.read() - 48;
    Serial.println(current_temp);       
    dataFile.close(); 
  } else {
    Serial.print(file_name);
    Serial.println(" NOT FOUND.");
    Serial.print("Current Temperature: ");
    current_temp = 24;
    Serial.println(current_temp);
    File dataFile = SPIFFS.open(file_name, "w");
    dataFile.println(current_temp);
    dataFile.close(); 
  }
}
 
void loop() {
  if (mqttClient.connected()) {
    mqttClient.loop();          
  } else {                      
    connectMQTTserver();        
  }
}
 
// Connect to MQTT server and subscribe to the topic
void connectMQTTserver(){
  String clientId = "esp8266-" + WiFi.macAddress();
 
  // Connect to MQTT server
  if (mqttClient.connect(clientId.c_str())) { 
    Serial.println("MQTT Server Connected.");
    Serial.print("Server Address:   ");
    Serial.println(mqttServer);
    Serial.print("ClientId:   ");
    Serial.println(clientId);
    subscribeTopic(); // Subscribe to a certain topic
  } else {
    Serial.print("MQTT Server Connect Failed. Client State:");
    Serial.println(mqttClient.state());
    delay(5000);
  }   
}
 
// Callback function after receiving the message
void receiveCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message Received [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println("");
  if ((char)payload[0] == '1') {     
    irsend.sendNEC(IR_POWER_ON, 32);
    Serial.println("Air conditioner ON");
    aircon_on = true;
  } 
  else if ((char)payload[0] == '0') {                           
    irsend.sendNEC(IR_POWER_OFF, 32);
    Serial.println("Air conditioner OFF");  
    aircon_on = false;
  }
  else if ((char)payload[0] == 't' && aircon_on) {
    
    int temp = (payload[1] - 48)*10 + (payload[2] - 48);
    Serial.print("Setting temperature to ");
    Serial.println(temp);
    if (current_temp < temp) {
      int diff = temp - current_temp;
      for (int i=0; i<diff; ++i) {
        irsend.sendNEC(IR_TEMPERATURE_UP, 32);
        delay(200);
      }
    }
    else if (current_temp < temp) {
      int diff = current_temp - temp;
      for (int i=0; i<diff; ++i) {
        irsend.sendNEC(IR_TEMPERATURE_DOWN, 32);
        delay(200);
      }
    }
    current_temp = temp;
    if(SPIFFS.begin()){
      Serial.println("");
    } else {
      Serial.println("SPIFFS Failed to Start.");
    }
    File dataFile = SPIFFS.open(file_name, "w");
    dataFile.println(current_temp);
    dataFile.close();  
  }
}
 
// Subscribe to a topic
void subscribeTopic(){
  String topicString = "room/air_con";
  char subTopic[topicString.length() + 1];  
  strcpy(subTopic, topicString.c_str());
  
  if(mqttClient.subscribe(subTopic)){
    Serial.print("Subscribe Topic:   ");
    Serial.println(subTopic);
  } else {
    Serial.print("Subscribe Fail...");
  }  
}
 
// ESP8266 connect to wifi
void connectWifi(){
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi Connected!");  
  Serial.println(""); 
}
