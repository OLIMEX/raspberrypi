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
    from spi import SPI
    lcd = SPI(0, 0)
    lcd.msh = 1000000
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

print 'Loading GPIO-MODULE.....',   
try:
    import RPi.GPIO as GPIO
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
    

print 'Initializating GPIO-MODULE.....',   
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(0, GPIO.OUT)     #SDA -> LCD_C/#D
    GPIO.setup(1, GPIO.OUT)     #SCL -> #LCD_RESET
    GPIO.output(0, True)
    GPIO.output(1, True)
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
   

 
    
#define some variables
SEND_CMD = 0
SEND_CHR = 1

LCD_X_RES = 84
LCD_Y_RES = 48

PIXEL_OFF = 0
PIXEL_ON = 1
PIXEL_XOR = 2

FONT_1X = 1
FONT_2X = 2

LCD_CACHE_SIZE = ((LCD_X_RES * LCD_Y_RES) / 8)



LcdMemIdx = 0
LcdMemory = [0x00] * LCD_CACHE_SIZE
Temp_BUff = [[0x00 for i in range(LCD_X_RES)] for j in range(LCD_Y_RES)]
LCD_START_LINE_ADDR = 64

FontLookup = []
FontLookup.append ([0x00, 0x00, 0x00, 0x00, 0x00])  # sp
FontLookup.append ([0x00, 0x00, 0x2f, 0x00, 0x00])  # !
FontLookup.append ([0x00, 0x07, 0x00, 0x07, 0x00])  # "
FontLookup.append ([0x14, 0x7f, 0x14, 0x7f, 0x14])  # #
FontLookup.append ([0x24, 0x2a, 0x7f, 0x2a, 0x12])  # $
FontLookup.append ([0xc4, 0xc8, 0x10, 0x26, 0x46])  # %
FontLookup.append ([0x36, 0x49, 0x55, 0x22, 0x50])  #
FontLookup.append ([0x00, 0x05, 0x03, 0x00, 0x00])
FontLookup.append ([0x00, 0x1c, 0x22, 0x41, 0x00])
FontLookup.append ([0x00, 0x41, 0x22, 0x1c, 0x00])
FontLookup.append ([0x14, 0x08, 0x3E, 0x08, 0x14])
FontLookup.append ([0x08, 0x08, 0x3E, 0x08, 0x08])
FontLookup.append ([0x00, 0x00, 0x50, 0x30, 0x00])
FontLookup.append ([0x10, 0x10, 0x10, 0x10, 0x10])
FontLookup.append ([0x00, 0x60, 0x60, 0x00, 0x00])
FontLookup.append ([0x20, 0x10, 0x08, 0x04, 0x02])
FontLookup.append ([0x3E, 0x51, 0x49, 0x45, 0x3E])
FontLookup.append ([0x00, 0x42, 0x7F, 0x40, 0x00])
FontLookup.append ([0x42, 0x61, 0x51, 0x49, 0x46])
FontLookup.append ([0x21, 0x41, 0x45, 0x4B, 0x31])
FontLookup.append ([0x18, 0x14, 0x12, 0x7F, 0x10])
FontLookup.append ([0x27, 0x45, 0x45, 0x45, 0x39])
FontLookup.append ([0x3C, 0x4A, 0x49, 0x49, 0x30])
FontLookup.append ([0x01, 0x71, 0x09, 0x05, 0x03])
FontLookup.append ([0x36, 0x49, 0x49, 0x49, 0x36])
FontLookup.append ([0x06, 0x49, 0x49, 0x29, 0x1E])  # 9
FontLookup.append ([0x00, 0x36, 0x36, 0x00, 0x00])
FontLookup.append ([0x00, 0x56, 0x36, 0x00, 0x00])
FontLookup.append ([0x08, 0x14, 0x22, 0x41, 0x00])
FontLookup.append ([0x14, 0x14, 0x14, 0x14, 0x14])
FontLookup.append ([0x00, 0x41, 0x22, 0x14, 0x08])
FontLookup.append ([0x02, 0x01, 0x51, 0x09, 0x06])
FontLookup.append ([0x32, 0x49, 0x59, 0x51, 0x3E])
FontLookup.append ([0x7E, 0x11, 0x11, 0x11, 0x7E])  #A
FontLookup.append ([0x7F, 0x49, 0x49, 0x49, 0x36])
FontLookup.append ([0x3E, 0x41, 0x41, 0x41, 0x22])
FontLookup.append ([0x7F, 0x41, 0x41, 0x22, 0x1C])
FontLookup.append ([0x7F, 0x49, 0x49, 0x49, 0x41])
FontLookup.append ([0x7F, 0x09, 0x09, 0x09, 0x01])
FontLookup.append ([0x3E, 0x41, 0x49, 0x49, 0x7A])
FontLookup.append ([0x7F, 0x08, 0x08, 0x08, 0x7F])
FontLookup.append ([0x00, 0x41, 0x7F, 0x41, 0x00])
FontLookup.append ([0x20, 0x40, 0x41, 0x3F, 0x01])
FontLookup.append ([0x7F, 0x08, 0x14, 0x22, 0x41])
FontLookup.append ([0x7F, 0x40, 0x40, 0x40, 0x40])
FontLookup.append ([0x7F, 0x02, 0x0C, 0x02, 0x7F])
FontLookup.append ([0x7F, 0x04, 0x08, 0x10, 0x7F])
FontLookup.append ([0x3E, 0x41, 0x41, 0x41, 0x3E])
FontLookup.append ([0x7F, 0x09, 0x09, 0x09, 0x06])
FontLookup.append ([0x3E, 0x41, 0x51, 0x21, 0x5E])
FontLookup.append ([0x7F, 0x09, 0x19, 0x29, 0x46])
FontLookup.append ([0x46, 0x49, 0x49, 0x49, 0x31])
FontLookup.append ([0x01, 0x01, 0x7F, 0x01, 0x01])
FontLookup.append ([0x3F, 0x40, 0x40, 0x40, 0x3F])
FontLookup.append ([0x1F, 0x20, 0x40, 0x20, 0x1F])
FontLookup.append ([0x3F, 0x40, 0x38, 0x40, 0x3F])
FontLookup.append ([0x63, 0x14, 0x08, 0x14, 0x63])
FontLookup.append ([0x07, 0x08, 0x70, 0x08, 0x07])
FontLookup.append ([0x61, 0x51, 0x49, 0x45, 0x43])
FontLookup.append ([0x00, 0x7F, 0x41, 0x41, 0x00])
FontLookup.append ([0x55, 0x2A, 0x55, 0x2A, 0x55])
FontLookup.append ([0x00, 0x41, 0x41, 0x7F, 0x00])
FontLookup.append ([0x04, 0x02, 0x01, 0x02, 0x04])
FontLookup.append ([0x40, 0x40, 0x40, 0x40, 0x40])
FontLookup.append ([0x00, 0x01, 0x02, 0x04, 0x00])
FontLookup.append ([0x20, 0x54, 0x54, 0x54, 0x78])
FontLookup.append ([0x7F, 0x48, 0x44, 0x44, 0x38])
FontLookup.append ([0x38, 0x44, 0x44, 0x44, 0x20])
FontLookup.append ([0x38, 0x44, 0x44, 0x48, 0x7F])
FontLookup.append ([0x38, 0x54, 0x54, 0x54, 0x18])
FontLookup.append ([0x08, 0x7E, 0x09, 0x01, 0x02])
FontLookup.append ([0x0C, 0x52, 0x52, 0x52, 0x3E])
FontLookup.append ([0x7F, 0x08, 0x04, 0x04, 0x78])
FontLookup.append ([0x00, 0x44, 0x7D, 0x40, 0x00])
FontLookup.append ([0x20, 0x40, 0x44, 0x3D, 0x00])
FontLookup.append ([0x7F, 0x10, 0x28, 0x44, 0x00])
FontLookup.append ([0x00, 0x41, 0x7F, 0x40, 0x00])
FontLookup.append ([0x7C, 0x04, 0x18, 0x04, 0x78])
FontLookup.append ([0x7C, 0x08, 0x04, 0x04, 0x78])
FontLookup.append ([0x38, 0x44, 0x44, 0x44, 0x38])
FontLookup.append ([0x7C, 0x14, 0x14, 0x14, 0x08])
FontLookup.append ([0x08, 0x14, 0x14, 0x18, 0x7C])
FontLookup.append ([0x7C, 0x08, 0x04, 0x04, 0x08])
FontLookup.append ([0x48, 0x54, 0x54, 0x54, 0x20])
FontLookup.append ([0x04, 0x3F, 0x44, 0x40, 0x20])
FontLookup.append ([0x3C, 0x40, 0x40, 0x20, 0x7C])
FontLookup.append ([0x1C, 0x20, 0x40, 0x20, 0x1C])
FontLookup.append ([0x3C, 0x40, 0x30, 0x40, 0x3C])
FontLookup.append ([0x44, 0x28, 0x10, 0x28, 0x44])
FontLookup.append ([0x0C, 0x50, 0x50, 0x50, 0x3C])
FontLookup.append ([0x44, 0x64, 0x54, 0x4C, 0x44])
FontLookup.append ([0x08, 0x6C, 0x6A, 0x19, 0x08])
FontLookup.append ([0x0C, 0x12, 0x24, 0x12, 0x0C])
FontLookup.append ([0x7E, 0x7E, 0x7E, 0x7E, 0x7E])

    

def LCD_DC_HIGH():
    GPIO.output(0, True)
    return

def LCD_DC_LOW():
    GPIO.output(0, False)
    return

#function definitions
def LCDReset():
    GPIO.output(1, False)
    time.sleep(0.05)
    GPIO.output(1, True)
    
def LCDInit():
    "Init LCD Controller"
    LCDReset()
    
    LCDSend(0x03, SEND_CMD)
    time.sleep(1)
    LCDSend( 0x21, SEND_CMD)                                        #LCD Extended Commands
    LCDSend( 0xC8, SEND_CMD)                                        #Set KCD Vop (contrast)
    LCDSend( 0x04 | int(not(not(LCD_START_LINE_ADDR & (1 << 6)))), SEND_CMD)   #Set Temp S6 for start line
    LCDSend( 0x40 | (LCD_START_LINE_ADDR & ((1<<6)-1)), SEND_CMD)   #Set Temp S[5:0] for start line
    LCDSend( 0x12, SEND_CMD)                                        #LCD bias mode 1:68
    LCDSend( 0x20, SEND_CMD)                                        #LCD Standard Commands, Horizontal addressing
    LCDSend( 0x08, SEND_CMD)                                        #LCD Blank
    LCDSend( 0x0C, SEND_CMD)                                        #LCD in normal mode
    
    LCDClear()
    LCDUpdate()
    
    return

def LCDSend(data, cd):
    "Send to LCD"
    
    if cd == SEND_CHR:
        LCD_DC_HIGH()
    else:
        LCD_DC_LOW()
        
    lcd.writebytes([data])    
    return

def LCDUpdate():
    "Update LCD memory"
    
    for y in range(6):
        LCDSend(0x80, SEND_CMD)
        LCDSend(0x40 | y, SEND_CMD)
        for x in range(84):
            LCDSend(LcdMemory[(y * 84) +x], SEND_CHR)
    return

def LCDClear():
    "Clear LCD"
    for i in range(LCD_CACHE_SIZE):
        LcdMemory[i] = 0x00
    return

def LCDChrXY(x, y, ch):
    "Write char at x position on y row"
    index = 0
    offset = 0
    i = 0
    
    if x > LCD_X_RES:
        return
    
    index = x*6 + y*84
    
    for i in range(6):
        if i == 5:
            LcdMemory[index] = 0x00
            break
        offset = FontLookup[ch - 32][i]
        LcdMemory[index] = offset
        index = index + 1        
    return

def LCDChrXYInverse(x, y, ch):
    "Wrute char at x position on y row - inverse"
    
    index = 0
    i = 0
    
    if x > LCD_X_RES:
        return
    if y > LCD_Y_RES:
        return
    
    index = x*5 + y*84
    
    for i in range(5):
        LcdMemory[index] = ~(FontLookup[ch-32][i])
        index = index + 1
    return

def LCDContrast(contrast):
    "Set LCD contrast"
    
    LCDSend (0x21, SEND_CMD)                #LCD Extended Commands
    LCDSend (0x80 | contrast, SEND_CMD)     #Set LCD Vop (Contrast)
    LCDSend (0x20, SEND_CMD)
    
    return

def LCDStr(row, string, inv):
    "Send string to LCD"
    x = 0
    for i in range(len(string)):
        if inv:
            LCDChrXYInverse(x, row, ord(string[i]))
        else:
            LCDChrXY(x, row, ord(string[i]))
        x = x + 1
    LCDUpdate()
    
    return
def Draw_4_Ellipse_Points(CX, CY, X, Y):
    Draw_Point (CX+X, CY+Y)
    Draw_Point (CX-X, CY+Y)
    Draw_Point (CX-X, CY-Y)
    Draw_Point (CX+X, CY-Y)
    return
def Draw_Point(x, y):
    
    if x >= 0 and x < LCD_X_RES and y >= 0 and y < LCD_Y_RES:
        row = y / 8
        i = x + row * 84
        LcdMemory[i] |= 1 << (y % 8)
    return

def Draw_Ellipse(CX, CY, XRadius, YRadius):
    
    TwoASquare = 2 * XRadius * XRadius
    TwoBSquare = 2 * YRadius * YRadius
    X = XRadius
    Y = 0
    XChange = YRadius * YRadius * (1 - 2 * XRadius)
    YChange = XRadius * XRadius
    EllipseError = 0
    StoppingX = TwoBSquare * XRadius
    StoppingY = 0
    
    while StoppingX >= StoppingY:
        Draw_4_Ellipse_Points (CX, CY, X, Y)
        Y = Y +1
        StoppingY = StoppingY + TwoASquare
        EllipseError = EllipseError + YChange
        YChange = YChange + TwoASquare
        if (2 * EllipseError + XChange) > 0:
            X = X - 1
            StoppingX = StoppingX - TwoBSquare
            EllipseError = EllipseError + XChange
            XChange = XChange + TwoBSquare
    
    X = 0
    Y = YRadius
    XChange = YRadius * YRadius
    YChange = XRadius * XRadius * (1 - 2 * YRadius)
    EllipseError = 0
    StoppingX = 0
    StoppingY = TwoASquare * YRadius
    
    while StoppingX <= StoppingY:
        Draw_4_Ellipse_Points(CX, CY, X, Y)
        X = X + 1
        StoppingX = StoppingX + TwoBSquare
        EllipseError = EllipseError + XChange
        XChange = XChange + TwoBSquare
        if (2 * EllipseError + YChange) > 0:
            Y = Y - 1
            StoppingY = StoppingY - TwoASquare
            EllipseError = EllipseError + YChange
            YChange = YChange + TwoASquare
    
            
    return

def Draw_Circle(x, y, r):
    Draw_Ellipse(x, y, r, r)
    return

def Draw_Rectangle(x1, y1, x2, y2):
    Draw_Line (x1, y1, x1, y2)
    Draw_Line (x1, y1, x2, y1)
    Draw_Line (x2, y1, x2, y2)
    Draw_Line (x1, y2, x2, y2)
    return

def Draw_Triangle(x1, y1, x2, y2, x3, y3):
    Draw_Line (x1, y1, x2, y2)
    Draw_Line (x2, y2, x3, y3)
    Draw_Line (x3, y3, x1, y1)
    return

def Draw_Line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    if x1 < x2:
        sx = 1
    else:
        sx = -1
    
    if y1 < y2:
        sy = 1
    else:
        sy = -1
        
    err = dx - dy
    
    while True:
        Draw_Point(x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        
        if e2 > -dy:
            err = err - dy
            x1 = x1 + sx
            
        if e2 < dx:
            err = err + dx
            y1 = y1 + sy
    return

def Animate():
    
    j = 20
    while j > 0:
        i = 12
        while i > 0:
            LCDClear()
            Draw_Rectangle(i, i, 83 - i, 47 - i)
            Draw_Rectangle(12 + i, 12 + i, 83 - i - 12, 47 - i - 12)
            LCDUpdate()
            time.sleep(0.05)
            i = i - 1
        
        j = j - 1
        
    LCDClear()
    LCDUpdate()
    return

def main():
    print 'Initializing LCD.....',   
    try:
        LCDInit()
        try:
            print colored('Done', 'green')
        except NameError:
            print 'Done'
    except Exception:
        try:
            print colored('Fail', 'red')
        except NameError:
            print 'Fail'
        sys.exit(0)
    
    print 'Setting contrast.....',   
    try:
        LCDContrast(0xFF)
        try:
            print colored('Done', 'green')
        except NameError:
            print 'Done'
    except Exception:
        try:
            print colored('Fail', 'red')
        except NameError:
            print 'Fail'
        sys.exit(0)
       

    print ''
    print '1. Draw Text'
    print '2. Draw Point'
    print '3. Draw Line'
    print '4. Draw Triangle'
    print '5. Draw Rectangle'
    print '6. Draw Circle'
    print '7. Draw Ellipse'
    print '8. Test'
    print '9. Clear'
    print '0. Exit'
    print ''
    
    while True:
        try:
            x = int(raw_input('Enter choice: '), 10)
            break
        except Exception:
            try:
                print colored('Invalid character!', 'red')
            except Exception:
                print 'Invalid character!'
    
    
    if x == 1:
        while True:
            try:
                x = int(raw_input('Enter row: '), 10)
                if x < 0 or x > 6:
                    raise Exception
                y = raw_input('Text:')
                LCDStr(x, y, 0)
                LCDUpdate()
                break
            except Exception:
                try:
                    print colored('Invalid character!', 'red')
                except Exception:
                    print 'Invalid character'
    elif x == 2:
        while True:
            try:
                x = int(raw_input('X: '), 10)
                y = int(raw_input('Y: '), 10)
                Draw_Point(x, y)
                LCDUpdate()
                break
            except Exception:
                try:
                    print colored('Invalid character!', 'red')
                except Exception:
                    print 'Invalid character'
    elif x == 3:
        while True:
            try:
                x1 = int(raw_input('X1: '), 10)
                y1 = int(raw_input('Y1: '), 10)
                x2 = int(raw_input('X2: '), 10)
                y2 = int(raw_input('Y2: '), 10)
                Draw_Line(x1, y1, x2, y2)
                LCDUpdate()
                break
            except Exception:
                try:
                    print colored('Invalid character!', 'red')
                except Exception:
                    print 'Invalid character'
    
    elif x == 4:
        while True:
            try:
                x1 = int(raw_input('X1: '), 10)
                y1 = int(raw_input('Y1: '), 10)
                x2 = int(raw_input('X2: '), 10)
                y2 = int(raw_input('Y2: '), 10)
                x3 = int(raw_input('X3: '), 10)
                y3 = int(raw_input('Y3: '), 10)
                Draw_Triangle(x1, y1, x2, y2, x3, y3)
                LCDUpdate()
                break
            except Exception:
                try:
                    print colored('Invalid character!', 'red')
                except Exception:
                    print 'Invalid character'
                    
    elif x == 5:
        while True:
            try:
                x1 = int(raw_input('X1: '), 10)
                y1 = int(raw_input('Y1: '), 10)
                x2 = int(raw_input('X2: '), 10)
                y2 = int(raw_input('Y2: '), 10)
                Draw_Rectangle(x1, y1, x2, y2)
                LCDUpdate()
                break
            except Exception:
                try:
                    print colored('Invalid character!', 'red')
                except Exception:
                    print 'Invalid character'
                    
    elif x == 6:
        while True:
            try:
                x = int(raw_input('X: '), 10)
                y = int(raw_input('Y: '), 10)
                r = int(raw_input('R: '), 10)
                Draw_Circle(x, y, r)
                LCDUpdate()
                break
            except Exception:
                try:
                    print colored('Invalid character!', 'red')
                except Exception:
                    print 'Invalid character'
                    
    elif x == 7:
        while True:
            try:
                X = int(raw_input('X: '), 10)
                Y = int(raw_input('Y: '), 10)
                XR = int(raw_input('XR: '), 10)
                YR = int(raw_input('YR: '), 10)
                Draw_Ellipse(X, Y, XR, YR)
                LCDUpdate()
                break
            except Exception:
                try:
                    print colored('Invalid character!', 'red')
                except Exception:
                    print 'Invalid character'
                    
    elif x == 8:
        Animate()
        LCDUpdate()
                    
    elif x == 9:
        Clear()
        LCDUpdate()
                
                    
    elif x == 0:
        sys.exit(0)
                    
    
    
    





if __name__ == '__main__':
    main()
    