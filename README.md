# Home security system with Raspberry Pi and sending notifications with a Telegram bot 
[![Linter](https://github.com/m0by314/Raspberry_Pi_home_security_system/workflows/CI/badge.svg?event=push)](https://github.com/m0by314/Raspberry_Pi_home_security_system/actions?query=workflow%3ACI)

Tutorial to build a home security system with Raspberry Pi and sending notifications with a Telegram bot.

### How it works

- When a movement is detected, the application records a video that is sent to your phone by the Telegram bot.  
- Once installed, the surveillance system is managed from your smartphone with [bot commands](#Bots-commands) from the Telegram app.  
- The system is started by a systemd service activated at boot time

### Prerequisites.

* Raspberry Pi Camera Module  
* PIR motion sensor module   
* 3 female-to-female jumper wires   
* [Tutorial for create your Telegram Bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot)  
* After starting the bot on your smartphone, you must retrieve your chat_id at the following address:   
    * https://api.telegram.org/bot<token_id>/getUpdates

### Connect the PIR sensor

![image](img/pir-diagram.png)

## Setup
 * Open the `config.py` file and configure the TOKEN_ID and CHAT_ID variables with your token_id and your chat_id  
 ```
     # Variable to configure
     TOKEN_ID = 'Your token_id'
     CHAT_ID = 'Your chat_id'
```

### Installing 

The installation requires root rights:

**A reboot will be done at the end of the installation to activate the camera hardware**
```
sudo make install
```

### Bot's commands

* /start  : start the home surveillance  
* /stop   : stop the home surveillance  
* /status : show the status of home surveillance  
* /photo  : take a picture 
* /video time=<duration> :  records a video, by default delay is 60s 
* /clean  : remove all files in video folder
* /help   : show help 
  
### Details 		

  * By default, the duration of the video is set to 60s. If you want change this, you need to modify the VIDEO_TIME constant in `config.py`    		

  * It's possible to add other commands to the bot in `app.py`
 
### Testing
 
```
make test
```

### Uninstall
 
```
sudo make uninstall
```
**A reboot will be done at the end to deactivate the camera hardware**

## Built With
### Hardware:
* Raspberry Pi Zero WH
* Infrared Camera v2 8MP
* HC-SR501 PIR Motion Sensor Module

### Libraries:
* [gpiozero](https://pypi.org/project/gpiozero/)
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)  
* [picamera](https://pypi.org/project/picamera/) 
