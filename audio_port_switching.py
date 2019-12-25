#! /usr/bin/python3
import subprocess
import re
import time


class Device():
    
    _index = None
    _isDefault = None
    
    def __init__(self,name,port):

        
        self.name = name
        self.port = port

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
    
    
    
    @property
    def isDefault(self):
        
              
        #getting sink indexes
        rawResult = subprocess.check_output("pactl list sinks short", 
                                      shell=True, universal_newlines=True)
        defaultSinkIndex = 999
        
        for row in rawResult.split("\n"):
            print(row)
            if (row.find("RUNNING") != -1):
                defaultSinkIndex = re.search(r'([0-9])\s', row).group(1)
                
        
        print(defaultSinkIndex, self.index)
        
        if defaultSinkIndex == self.index:
            self.isDefault = True
        else:
            self.isDefault = False
            
        
        return self._isDefault
    
    
    
    @isDefault.setter
    def isDefault(self, state):
        
        self._isDefault = state
        
        
    @property
    def index(self):
        
        #getting sink indexes
        rawResult = subprocess.check_output("pactl list sinks short", 
                                      shell=True, universal_newlines=True)
        
        for row in rawResult.split("\n"):
            if (row.find(self.name) != -1):
                res = re.search(r"(^[0-9]*)", row).group(1) 
                self._index = res

        return self._index
    
    @index.setter
    def index(self, i):
        
        self._index = i
        
    def __str__(self):
        
        output = self.name + '\n' + self.port + '\n' + str(
            self.isDefault) + '\n' + self.index + '\n' + '*****'
        
        return output
        


#getting sink inputs
sinkInputs = []
rawResult = subprocess.check_output("pactl list sink-inputs short", 
                              shell=True, universal_newlines=True)

for row in rawResult.split("\n"):
    sinkInputs.append(re.search(r"(^[0-9]*)", row).group(1))

sinkInputs = list(filter(None, sinkInputs)) #remove empty elements 

print(sinkInputs)



devices = []
devices.append(Device("alsa_output.pci-0000_26_00.1.hdmi-stereo-extra1",
              "analog-output-lineout"))

devices.append(Device("alsa_output.pci-0000_28_00.3.analog-stereo",
              "analog-output-headphones"))

for i in range(len(devices)):
    print(devices[i])
    if (devices[i].isDefault):
         
#         print(subprocess.check_output("pacmd set-sink-port {} {}".format(devices[i-1].index,
#                                                                                devices[i-1].port), 
#                                       shell=True, universal_newlines=True))
          
# #         print(subprocess.check_output("pacmd set-default-sink {}".format(devices[i-1].index, 
# #                                       shell=True, universal_newlines=True)))

        for sink in sinkInputs:
            subprocess.check_output("pactl move-sink-input  {} {}".format(sink,
                                                                               devices[i-1].index), 
                                      shell=True, universal_newlines=True)
        
        
        
        
#                                                                          