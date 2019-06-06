#! /usr/bin/python3

### Fonction for using Telegram bot

import telepot
import subprocess
import camera

class Telepot:
    def __init__(self,bot_id) :
        self.camera = None
        self.bot = telepot.Bot(bot_id)
        self.chat_listen = {}
        self.bot.message_loop(self.handle)
       
    def camera(self):
        if self.camera is None:
            self.camera = camera.Camera()
            
        return self.camera
 
    def __islisten(self):
        if self.chat_id in self.chat_listen:
            return True

    def handle(self,msg):
        self.chat_id = msg['chat']['id']
        self.command = msg['text']
        
        if self.command == '/start':
            if self.__islisten() : 
                self.bot.sendMessage(self.chat_id, "Listen Motion is already use")
            else :
                self.bot.sendMessage(self.chat_id, "Listen Motion start")     
                self.chat_listen[self.chat_id] = True
                
        elif self.command == '/stop':
            if self.__islisten():
                self.bot.sendMessage(self.chat_id, "Listening Motion stop")
                self.chat_listen[self.chat_id] = None
            else:
                self.bot.sendMessage(self.chat_id, "Listen Motion doesn't run")
                                   
        elif self.command == '/status':
            if self.__islisten():
                self.bot.sendMessage(self.chat_id, "Bot is running")
            else:
                self.bot.sendMessage(self.chat_id, "Bot doesn't run")
         
        elif self.command == '/help':
            return self.help()
        
        elif self.command == '/snap':
            if self.__islisten() : 
                self.bot.sendMessage(self.chat_id, "Take a photo")
                self.bot.sendPhoto(self.chat_id, photo=open(self.camera.selfie(), 'rb'), caption='photo')
            else :
                self.bot.sendMessage(self.chat_id, "Listen Motion not start")     
        
        elif self.command == '/clean':
            bot.sendMessage(chat_id, self._remove())              
        
    @staticmethod
    def usage():
        str =  "command usage:\n"
        str += "\t/start launch the dectection\n"
        str += "\t/stop stop the detection\n"
        str += "\t/snap take a photo\n"
        str += "\t/status show status of the movement detection\n"
        str += "\t/help show help\n"
        str += "\t/clean remove all files in video folder\n"
        print(str)
        
    def _remove(self):
        command ="cd "+ self.tmp_path + " && rm *"
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            status = 'FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output)
            return status
        else :
            status = 'files removed'
            return status      
    
    @staticmethod    
    def send_video(vid):
        for key, val in vid.items():
            if key == 0:
                bot.sendVideo(chat_id, video=open(val, 'rb'), caption='Motion Detected')
            else:
                bot.sendMessage(chat_id, val)
        

