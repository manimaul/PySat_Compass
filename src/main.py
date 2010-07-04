#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>
# Published under the terms of "Simplified BSD License".
# License text available at http://opensource.org/licenses/bsd-license.php

import serial
import librmc
import libgga
import libhdt
import time
import threading
import georef

gps1dev = ('/dev/ttyUSB0', 4800)
gps2dev = ('/dev/ttyUSB1', 4800)

dataLst1 = [0] #ostime, lat, long from gps1
dataLst2 = [0] #ostime, lat, long from gps2

brg = 0

offset = 0
#offset = -212

def rxNmea():
    gps1conn = serial.Serial(gps1dev[0], gps1dev[1], timeout=0.5)
    gps2conn = serial.Serial(gps2dev[0], gps2dev[1], timeout=0.5)
    
    while 1:
        gps1Line = gps1conn.readline()
        gps2Line = gps2conn.readline()
        processLines(gps1Line, 1)
        processLines(gps2Line, 2)
        
def processLines(line, gpsnum):
    global dataLst1
    global dataLst2
    if librmc.checksum(line) == 'valid':
        if librmc.is_rmc(line) == True:
            lat = librmc.rmc_lat(line)
            long = librmc.rmc_long(line)
            lst = [time.time(), lat, long]
            if gpsnum == 1:
                dataLst1 = lst
            else:
                dataLst2 = lst
            #print 'got rmc from gps' + str(gpsnum) + ' ' + str(lst)
            
        if libgga.is_gga(line) == True:
            lat = libgga.gga_lat(line)
            long = libgga.gga_long(line)
            lst = [time.time(), lat, long]
            if gpsnum == 1:
                dataLst1 = lst
            else:
                dataLst2 = lst
            #print 'got gga from gps' + str(gpsnum) + ' ' + str(lst)

#receive data and push/pop lists
threading.Thread(target=rxNmea).start()

def calcHdt():
    global brg
    since = time.time() - dataLst1[0] #seconds since fresh data
    freq = dataLst1[0] - dataLst2[0] #seconds between gps1 and gps2 data
    if freq <= 1 and since <= 1 :
        brg = georef.BearingMercator(dataLst1[1], dataLst1[2], dataLst2[1], dataLst2[2])
        brg = round(brg, 2)
        hdt = '$GPHDT,' + str(brg) + ',T'
        print libhdt.addchecksum(hdt)
    tc = threading.Timer(.5, calcHdt)
    tc.start()
    
def offset(brg):
    if brg < offset:
        brg = brg + 360 + offset
    else:
        brg = brg + offset
        

#start timer to calculate heading every .5 seconds
calcHdt()





            