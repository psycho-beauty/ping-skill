# The MIT License (MIT)	
# 
# Copyright (c) 2017 Noah Greenstein
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os.path import dirname, join
from os import listdir
import re

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'noahgreenstein'

LOGGER = getLogger(__name__)


class PingSkill(MycroftSkill):

    def __init__(self):
        super(PingSkill, self).__init__(name="PingSkill")
        self.process = None

    def initialize(self):
        self.load_data_files(dirname(__file__))

        ping_intent = IntentBuilder("PingIntent")\
            .require("PingKeyword").require("URL").build()
        self.register_intent(ping_intent, self.handle_ping_intent)


    def handle_ping_intent(self, message):
        
        f = open('hosts.txt','r')
        for line in f.readlines():
            l=line.split(",")
            hosts[l[0].strip()] = [l[1].strip(), l[2].strip()]
        f.close()
        
        # TODO check for errors
        if message.metadata.get("URL") in hosts:
            if hosts[message.metadata.get("URL")][1] == "True":
                # XXX import requests
                response = requests.get(hosts[message.metadata.get("URL")][0])
                SPEAK response.reason
            else:
            # XXX import subprocess as sp
                status,result = sp.getstatusoutput("ping -c1 -w2 " + hosts[message.metadata.get("URL")][0])
                #result = os.system("ping -c1 -w2 " + hosts[message.metadata.get("URL")][0])
                SPEAK "Pinged in " + result.split('\n')[-1].split('/')[5] +" milliseconds."
        else:
            # try to parse the URL
            #if any item in array is 'dot', replace with '.'
            # join the string and ping
            url = message.metadata.get("URL").replace("dot", ".")
            
            
        # Ping the URL requested
        title = message.metadata.get("SongTitle")
        # No need to speak the title...
        # self.speak_dialog("play.song", {'title': title})
        title += ".mp3"
        title = re.sub(" ", "_", title)
        self.process = play_mp3(join(dirname(__file__), "mp3", title))





def create_skill():
return PingSkill()
