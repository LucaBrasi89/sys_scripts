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
#         All you need is to specify devices in list of section 1.

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

    def __init__(self,name,port):

        
        self.name = name
        self.port = port    
        
    def __str__(self):
        
        output = self.name + '\n' + self.port + '\n'
        return output
        

if __name__ == "__main__":
    
    
    # 1: Specify devices
    devices = []
    devices.append(Device("alsa_output.pci-0000_28_00.3.analog-stereo",
                  "analog-output-lineout"))
    
    devices.append(Device("alsa_output.pci-0000_28_00.3.analog-stereo",
                  "analog-output-headphones"))
    
    
    # 2: Find active port
    sinkInputs = []
    rawResult = subprocess.check_output("pacmd list-sinks short | grep \"active port\"", 
                                  shell=True, universal_newlines=True)
    
    # 3: Set port opposite to active
    for row in rawResult.split("\n"):
        if (devices[0].port in row):
            subprocess.run("pactl set-sink-port {} {}".format(devices[1].name, devices[1].port), shell=True)
        elif (devices[1].port in row):
            subprocess.run("pactl set-sink-port {} {}".format(devices[0].name, devices[0].port), shell=True)
