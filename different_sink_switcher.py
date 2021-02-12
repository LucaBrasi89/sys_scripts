#! /usr/bin/python3
#        
#         *************************************
#         *************************************
#         ******   AUDIO PORT SWITCHER  *******
#         *************************************
#         *************************************
#         
#         Switch audio sinks between specified devices.
#         Based on manipulation with Linux PulseAudio server.
#         
#         Start from  
#         "1: Specify devices section"
#             Basicly, you have to specify output sink. You can know more by:
#                 
#                 pactl list sinks short
#                 
#             And desired port for each sink. Here are all active ports:
#                 
#                 pacmd list | grep "active port"
#                 
#             When you know list sinks and ports for them - just create obj of Device type.
#             
#             
#         Maybe you want to preset port for some of device. But maybe you don't.
#         So, this section is optional.
#         "2: Preset default port section"
#
#         ____________________________________________
#
#         Wrote by Andrew Sotnikov
#                 aka Luca Brasi
#                     
#                     andrew.sotnikov@zoho.com
#         
        

import subprocess
import re
import time


class Device():
    
    index = None
    isDefault = None
    
    def __init__(self,name,port):

        
        self.name = name
        self.port = port
        self.initIndex()
        self.initIsDefault()

    @DeprecationWarning
    @property
    def isDefaultDeprecated(self):
        
        #getting default sink
        rawResult = subprocess.check_output("pacmd list-sinks", 
                                      shell=True, universal_newlines=True)
        
        defaultSinkIndex = re.search(r"(\* index:)\s*([0-9])", rawResult).group(2)
        
        if defaultSinkIndex == self.index:
            self._isDefault = True
        else:
            self._isDefault = False
        
        return self._isDefault
    
    
    def initIsDefault(self):
        
              
        #getting sink indexes
        rawResult = subprocess.check_output("pactl list sinks short", 
                                      shell=True, universal_newlines=True)
        defaultSinkIndex = 999
        
        for row in rawResult.split("\n"):
#             print(row)
            if (row.find("RUNNING") != -1):
                defaultSinkIndex = re.search(r'([0-9])\s', row).group(1)
        if defaultSinkIndex == self.index:
            self.isDefault = True
        else:
            self.isDefault = False
            
        
        return self.isDefault
    
    def initIndex(self):
    
        #getting sink indexes
        rawResult = subprocess.check_output("pactl list sinks short", 
                                      shell=True, universal_newlines=True)
        
        for row in rawResult.split("\n"):
            if (row.find(self.name) != -1):
                res = re.search(r"(^[0-9]*)", row).group(1) 
                self.index = res
    
        self.index
    
        
    def __str__(self):
        
        output = self.name + '\n' + self.port + '\n' + str(
            self.isDefault) + '\n' + self.index + '\n' + '*****'
        
        return output
        

if __name__ == "__main__":
    
    
    # 1: Specify devices section
    devices = []
    devices.append(Device("alsa_output.pci-0000_26_00.1.hdmi-stereo-extra1",
                  "analog-output-lineout"))
    
    devices.append(Device("alsa_output.pci-0000_28_00.3.analog-stereo",
                  "analog-output-headphones"))
    
     # 2: Preset default port section
    subprocess.check_output("pactl set-sink-port {} {}".format(devices[1].index, devices[1].port), 
                                          shell=True, universal_newlines=True)
    
    # 3: Getting sink-output section
    sinkInputs = []
    rawResult = subprocess.check_output("pactl list sink-inputs short", 
                                  shell=True, universal_newlines=True)
    
    for row in rawResult.split("\n"):
        sinkInputs.append(re.search(r"(^[0-9]*)", row).group(1))
    
    sinkInputs = list(filter(None, sinkInputs)) #remove empty elements 
    
    
    # 4: Loop switcher
    for i in range(len(devices)):
        print(devices[i])
        if (devices[i].isDefault):
            for sink in sinkInputs:
                subprocess.check_output("pactl move-sink-input  {} {}".format(sink,
                                                                                   devices[i-1].index), 
                                          shell=True, universal_newlines=True)
            
