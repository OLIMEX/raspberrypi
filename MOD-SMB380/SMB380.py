#!/usr/bin/env python

import sys
import time

try:    
    from termcolor import colored
except ImportError:
    print "Termcolor module is not installed."
 
print ''
print 'Loading SPI-MODULE.....',   
try:
    import spidev
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.mode = 3
    spi.max_speed_hz = 1000000
    
    try:
        print colored('Done', 'green')
    except NameError:
        print 'Done'
except ImportError:
    try:
        print colored('Fail', 'red')
    except NameError:
        print 'Fail'
    sys.exit(0)
    
    

def main():
        
    sys.stdout.write("\n")
    
    while True:
        
        r = spi.xfer([0x80, 0, 0, 0, 0, 0, 0, 0, 0, 0])
       
        #calculate temperature   
        temp = (r[9] * 0.5) - 30     
                
        x = (r[3] & 0xC0) >> 6
        x = x | ( r[4] << 2 )
        
        y = (r[5] & 0xC0) >> 6
        y = y | ( r[6] << 2 )
        
        z = (r[7] & 0xC0) >> 6
        z = z | ( r[8] << 2 )
        
        if x & 0x0200 == 0:
            x = (x & 0x1FF) * 0.008
        else:
            x = -4.096 + (x & 0x1FF) * 0.008
        
        if y & 0x0200 == 0:
            y = (y & 0x1FF) * 0.008
        else:
            y = -4.096 + (y & 0x1FF) * 0.008
        
        if z & 0x0200 == 0:
            z = (z & 0x1FF) * 0.008
        else:
            z = -4.096 + (z & 0x1FF) * 0.008
            
        print '\f'
        print 'Temperature: %.1f' % temp
        print 'ACC_X: %.3f' % x
        print 'ACC_Y: %.3f' % y
        print 'ACC_Z: %.3f' % z
            
        
        time.sleep(0.1)
        

    
if __name__ == '__main__':
    main()



