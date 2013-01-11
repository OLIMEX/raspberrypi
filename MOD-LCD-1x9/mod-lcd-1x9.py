#!/usr/bin/env python

import smbus
import time
import sys


class CHAR_TypeDef:
    def __init__(self):
        self.com = []
        self.bit = []
        
text = []
for i in range(9):
    text.append(CHAR_TypeDef());

for i in range(9):
    text[i].com = [3, 3, 0, 0, 2, 1, 1, 3, 1, 3, 1, 2, 2, 2, 0, 0]
    text[i].bit = [34 - i*4, 32 - i*4, 32 - i*4, 34 - i*4, 35 - i*4, 35 - i*4, 34 - i*4, 35 - i*4, 33 - i*4, 33 - i*4, 32 - i*4, 32 - i*4, 33 - i*4, 34 - i*4, 33 - i*4, 35 - i*4]



LCDAlphabet = [0x0000,      # space
               0x1100,      # !
               0x0280,      # "
               0x0000,      # #
               0x0000,      # $
               0x0000,      # %
               0x0000,      # &
               0x0000,      # J
               0x0039,      # (
               0x000F,      # )
               0x0463,      # *
               0x1540,      # +
               0x0000,      # ,
               0x0440,      # -
               0x1000,      # .
               0x2200,      # /
               0x003F,      # 0
               0x0006,      # 1
               0x045B,      # 2
               0x044F,      # 3
               0x0466,      # 4
               0x046D,      # 5
               0x047D,      # 6
               0x0007,      # 7
               0x047F,      # 8
               0x046F,      # 9
               0x0000,      # :
               0x0000,      # ;
               0x0A00,      # <
               0x0000,      # =
               0x2080,      # >
               0x0000,      # ?
               0xFFFF,      # @
               0x0477,      # A
               0x0A79,      # B
               0x0039,      # C
               0x20B0,      # D
               0x0079,      # E
               0x0071,      # F
               0x047D,      # G
               0x0476,      # H
               0x0030,      # I
               0x000E,      # J
               0x0A70,      # K
               0x0038,      # L
               0x02B6,      # M
               0x08B6,      # N
               0x003F,      # O
               0x0473,      # P
               0x083F,      # Q
               0x0C73,      # R
               0x046D,      # S
               0x1101,      # T
               0x003E,      # U
               0x2230,      # V
               0x2836,      # W
               0x2A80,      # X
               0x046E,      # Y
               0x2209,      # Z
               0x0039,      # [
               0x0880,      # BACKSLASH
               0x000F,      # ]
               0x0001,      # ^
               0x0008,      # 
               0x0100,      # `
               0x1058,      # a
               0x047C,      # b
               0x0058,      # c
               0x045E,      # d
               0x2058,      # e
               0x0471,      # f
               0x0C0C,      # g
               0x0474,      # h
               0x0004,      # i
               0x000E,      # j
               0x0C70,      # k
               0x0038,      # l
               0x1454,      # m
               0x0454,      # n
               0x045C,      # o
               0x0473,      # p
               0x0467,      # q
               0x0450,      # r
               0x0078,      # s
               0x001C,      # t
               0x2010,      # u
               0x2814,      # v
               0x2A80,      # w
               0x080C,      # x
               0x2048,      # y
               0x0000       
               ]

               
lcdBitmap = [0x00]*20

def Initialize_LCD():
    "Initialize MOD-LCD-1x9"
    print "Initialization..."
    
    address = 0x38
    command = 0xC8
    bus = smbus.SMBus(0)
    buf = [0xF0, 0xE0, 0x00]
    
    for i in range(20):
        buf.append(0xFF)
        
    bus.write_i2c_block_data(address, command, buf)
    
    print "Done"
    return
def LCD1x9_enableSegment(comIndex, bitIndex):
    "Enables a segment in the display buffer"
    
    if bitIndex >= 40:
        return
    
    comIndex &= 0x3
    
    if bitIndex & 0x1:
        comIndex |= 0x4
        
    bitIndex >>= 1
    
    lcdBitmap[bitIndex] |= 0x80 >> comIndex
    return
def LCD1x9_disableSegment(comIndex, bitIndex):
    "Disables a segment in the display buffer"
    
    if bitIndex >= 40:
        return
    
    comIndex &= 0x3
    
    if bitIndex & 0x1:
        comIndex |= 0x4
        
    bitIndex >>= 1
    
    lcdBitmap[bitIndex] &= ~(0x80 >> comIndex)
    return
def LCD1x9_Update():
    "Updates the display buffer"
    
    address = 0x38
    command = 0xE0
    bus = smbus.SMBus(0)
    buf = [0x00]
    
    for i in range(20):
        buf.append(lcdBitmap[i])
        

        
    bus.write_i2c_block_data(address, command, buf)
def LCD1x9_Write(string):
    "Writes a string to the display"
    
    l = len(string)
    
    if l > 9:
        return
    
    index = 0
    
    for index in range(9):
        if index < l:
            data = ord(string[index])
        else:
            data = 0x20
            
        data -= 0x20
        bitfield = LCDAlphabet[data]
    
        for i in range(16):
            bit = text[index].bit[i]
            com = text[index].com[i]
            a = int(1<<i)
            if bitfield & a:
                LCD1x9_enableSegment(com, bit)
            else:
                LCD1x9_disableSegment(com, bit)
        
    LCD1x9_Update()
    return
    
    

print "\nMOD-LCD-1x9"
print "-----------------------------------"
print "1. Init LCD"
print "2. Write text"
print "3. Dispaly clock"
print ""

x = raw_input('Enter: ')
if x ==  '1':
    Initialize_LCD()

elif x == '2':
    print ""
    ch = raw_input('Enter text: ')
    LCD1x9_Write(ch)

elif x == '3':
    while True:
        a = int(time.strftime("%S", time.gmtime()))
        if a%2 == 0:
            LCD1x9_Write(time.strftime("%H %M %S", time.gmtime()))
        else:
            LCD1x9_Write(time.strftime("%H-%M-%S", time.gmtime()))
    
else:
    print "Error"

    

