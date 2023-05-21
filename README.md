# Smart-Air-Conditioning-System
This project aims to design a smart air conditioning system that can detect human presence and adjust its power consumption accordingly. Additionally, the system will provide users with remote control capabilities, adding to its convenience and flexibility


Instruction & Steps of How to set up the environment for ESP8266 Node MCU in Arduino IDE:
1. Download the Arduino IDE, the latest version.
2. Install the IDE
3. Set up your Arduino IDE as: Go to File->Preferences and copy the URL below to get the ESP board manager extensions: http://arduino.esp8266.com/stable/package_esp8266com_index.json Placing the http:// before the URL lets the Arduino IDE use it...otherwise it gives you a protocol error.
4. Go to Tools > Board > Board Manager> Type "esp8266" and download the Community esp8266 and install.
5. Set up your chip as:
Tools -> Board -> NodeMCU 1.0 (ESP-12E Module)
Tools -> Flash Size -> 4M (3M SPIFFS)
Tools -> CPU Frequency -> 80 Mhz
Tools -> Upload Speed -> 921600
Tools-->Port--> (whatever it is)
6. Download and run the 32 bit flasher exe at Github(Search for nodemcu/nodemcu-flasher/tree/master/ at Github) github.com/nodemcu/nodemcu-flasher/tree/master/Win32/Release Or download and run the 64 bit flasher exe at: github.com/nodemcu/nodemcu-flasher/tree/master/Win64/Release
7. In Arduino IDE, look for the old fashioned Blink program. Load, compile and upload.
8. Go to FILE> EXAMPLES> ESP8266> BLINK, it will start blinking.

After you finished, open the program "air_con.ino". Set the ssid and password to be your own Wi-Fi name and password. Upload the program to the ESP8266 Node MCU. Open the serial monitor. You will see the following messages if the program runs successfully:

	WiFi Connected!
	
	MQTT Server Connected.
	Server Address:   broker.hivemq.com
	ClientId:   "your clientid"
	Subscribe Topic:   room/air_con
	
	temperature.txt FOUND.
	Current Temperature: 25

Download the Mobile App "MQTTool", set the host to be the same as in "air_con.ino". The initial value should be "broker.hivemq.com". The port should be 1883. You can set the client id to anything you like, but make sure the id is unique. Then, press the connect button. After connecting your phone to the server, try to publish some messages. The topic should be "room/air_con". Type down any message and press publish. The MCU should receive your message. The received message is shown in the serial monitor. 

To turn on the air conditioner, send message "1". To turn off the air conditioner, send message "0". To modify the setting temperature, send message "t" followed by the temperature you want. For example, if you send message "t22", it means setting the air conditioner to be 22 degrees Celsius. 
