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

import requests
import subprocess as sp

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
            .require("PingKeyword").require("key").build()
        self.register_intent(ping_intent, self.handle_ping_intent)


    def handle_ping_intent(self, message):
        hosts = dict()
        f = open('hosts.txt','r')
        for line in f.readlines():
            if line.startswith("#") or "," not in line:
                continue
            l=line.split(",")
            hosts[l[0].strip()] = [l[1].strip(), l[2].strip()]
        f.close()
        
        k = message.data.get("key").lower()
        if k in hosts:
            if hosts[k][0] == '1':
                response = requests.get(hosts[k][1])
                self.speak_dialog("ServerResponse", response.reason +" "+ \
                    str(response.status_code) )
            else:
                status,result = sp.getstatusoutput("ping -c1 -w2 " \
                    + hosts[k][1][(hosts[k][1]).find("//")+2:])
                if status == 0:
                    self.speak_dialog("PingResponse", result.split('/')[5] )
                else:
                    self.speak_dialog("PingFailure")
        else:
            # way too complex to parse spoken full URLs, 
            # just exit if keyword not found. 
            self.speak_dialog("KeywordFailure")
            
            # Possible TODO: add spoken URL to ping
            # Parse URL? Libraries? Just google it and ping first result?
            #  if any item in array is 'dot', replace with '.'
            #    ... so, slashdot is impossible to parse.
            #  if last, replace: calm, come, cum, etc., with com

    # Ping/ Server responses usually don't take more than a second or two 
    # to register so there isn't much opportunity to stop the operation.
    def stop(self)
        pass

def create_skill():
    return PingSkill()
