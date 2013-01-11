#!/usr/bin/env python

import smbus
import sys
import os
import time

def Initialize():
    "Initalize MOD-Wii-UEXT-Nunchuck"
    
    bus = smbus.SMBus(0)
    address = 0x52
    command = 0xF0  
    data = 0x55
    
    bus.write_byte_data(address, command, data)
    return


def main():
    print "MOD-Wii-UEXT-Nunchuck"
    bus = smbus.SMBus(0)
    address = 0x52
    command = 0x00
    Initialize()
    while True:
        time.sleep(0.1)
        os.system('clear')
        buf = bus.read_i2c_block_data(address, command, 6)
        
        data = [0x00]*6
        
        for i in range(len(buf)):
       #     buf[i] ^= 0x17
        #    buf[i] += 0x17
            data[i] = buf[i]
        
        z = data[5] & 0x01
        c = (data[5] >> 1) & 0x01
        
        data[2] <<= 2
        data[2] |= (data[5] >> 2) & 0x03
        
        data[3] <<= 2
        data[3] |= (data[5] >> 6) & 0x03
        
        print "Analog X: %d" %(data[0])
        print "Analog Y: %d" %(data[1])    
        print "X-axis: %d" %(data[2])
        print "Y-axis: %d" %(data[3])
        print "Z-axis: %d " %(data[4])
        
        if z == 1:
            print "Button Z: NOT PRESSED"
        else:
            print "Button Z: PRESSED"
            
        if c == 1:
            print "Button C: NOT PRESSED"
        else:
            print "Button C: PRESSED"
    

if __name__ == '__main__':
    main()


