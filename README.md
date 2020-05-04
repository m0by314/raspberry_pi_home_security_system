# Home surveillance With RaspberryPi and Telegram bot 

How to build a home surveillance system with a RaspberryPI, a motion sensor, a camera and a Telegram bot. 

### How it works

When a movement is detected, the application records a video that is sent to your phone by the bot.  
Once installed, the monitoring system is managed from your smartphone with the bot's commands.  
The system is started by a systemd service activated at boot time

### Prerequisites

* Raspberry Pi Camera Module  
* PIR motion sensor module   
* 3 female-to-female jumper wires   
* [Tutorial for create your Telegram Bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot)  

### Connect the PIR sensor

![image](img/pir-diagram.png)

## Setting up the camera hardware
```
sudo raspig-config
```
Use the cursor keys to select and open Interfacing Options, and then select Camera and follow the prompt to enable the camera.  
Upon exiting `raspi-config`, it will ask to reboot.

## Setup
   
 * Open the file `lib/config.pl` and add your token_id   
 ```
     TOKEN_ID = 'Your token_id'
     VIDEO_TIME = 60  # duration of video recording
     REGISTRATION_FOLDER = 'tmp/video'  # video recording folder
```

### Installing 

Before installing set your token_id then:
```
make install
```

### Bot's commands

* /start  : start the home monitoring system 
* /stop   : stop the home monitoring system  
* /status : show the status of the monitoring system 
* /photo  : take a picture 
* /video time=<delay> : records a video, argument time defines the duration of the recording
* /clean  : remove all files in video folder
* /help   : show help 
  
### Details 		

  * By default, the duration of the video is set to 60s. If you want change this, you need to modify the VIDEO_TIME constant in `lib/config.py`    		

  * It's possible to add other commands to the bot in `app.py` with the decorator @bot.handler()		
 ```		
 @bot.handler("/hello")		
 def func_hello():		
     return bot.semd_message("Hello World")		
 ```
 
### Testing
 
```
make test
```

### Uninstall
 
```
make uninstall
```

## Built With

* [gpiozero](https://pypi.org/project/gpiozero/)
* [telepot](https://pypi.org/project/telepot/)  
* [picamera](https://pypi.org/project/picamera/) 
