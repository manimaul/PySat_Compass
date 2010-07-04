#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>
# Published under the terms of "Simplified BSD License".
# License text available at http://opensource.org/licenses/bsd-license.php

# GGA - essential fix data which provide 3D location and accuracy data.
#                                                                       14
#                                                              11     13|
#        1          2         3 4          5 6 7  8   9     10 |    12| | 15
#        |          |         | |          | | |  |   |     |  |    | | | |
# $--GGA,hhmmss.ss,llll.llll,a,yyyyy.yyyy,a,x,xx,x.x,xxx.x,a,-xx.x,a,x,x*hh<CR><LF>
# 
# 1) UTC Time
# 2) Latitude
# 3) North or South
# 4) Longitude
# 5) East or West
# 6) Fix Quality
#        1 = GPS fix (SPS)
#        2 = DGPS fix
#        3 = PPS fix
#        4 = Real Time Kinematic
#        5 = Float RTK
#        6 = estimated (dead reckoning) (2.3 feature)
#        7 = Manual input mode
#        8 = Simulation mode
# 7) Number of Satellites being tracked
# 8) Horizontal dilution of position
# 9) Altitude above mean sea level
#10) Altitude units
#        M = Meters
#11) Height of geoid (mean sea level) above WGS84 ellipsoid
#12) Height of geoid units
#        M = Meters
#13) Seconds since last DGPS update
#14) DGPS station ID#
#15) Checksum

import string
#import time
#import calendar
from operator import xor

def is_gga(gga): #check that the sentence is gga
    if gga[3:6] == 'GGA':
        return True
    else:
        return False

def checksum(gga): #see if the sentence has a valid checksum
    if is_gga(gga) == True:
        try:
            nmea = map(ord, gga[1:gga.index('*')])
            chksum = reduce(xor, nmea)
            chksum = str(hex(chksum))[2:4]
            chksum = chksum.upper()
            schksum = gga.find("*")
            schksum = gga[schksum+1:schksum+3]
            if schksum[0] == '0':
                schksum = schksum[1]
            if chksum == schksum:
                return 'valid'
            else:
                return 'invalid'
        except ValueError:
            return None

def gga_utc(gga): #utc time derived gga
    if is_gga(gga) == True:
        gga = gga.split(',')
        utc = gga[1]
        return utc
    
def gga_lat(gga): #latitude from gga
    if is_gga(gga) == True:
        try:
            gga = gga.split(',')
            lat = string.atof(gga[2])
            if gga[3] == 'S':
                lat = -lat
            deg = int(lat/100)
            min = lat - deg*100
            lat = deg + (min/60)            
            return round(lat, 6)
        except ValueError:
            return None
        
        
def gga_long(gga): #longitude from gga
    if is_gga(gga) == True:
        try:
            gga = gga.split(',')
            long = string.atof(gga[4])
            if gga[5] == 'W':
                long = -long
            deg = int(long/100)
            min = long - deg*100
            long = deg + (min/60)
            return round(long, 6)
        except ValueError:
            return None
        
def gga_fix(gga):
    if is_gga(gga) == True:
        try:
            gga = gga.split(',')
            fq = string.atof(gga[6])
            return fq
        except ValueError:
            return None
def gga_sat(gga):
    if is_gga(gga) == True:
        try:
            gga = gga.split(',')
            return gga[7]
        except ValueError:
            return None
        
def gga_altM(gga):
    if is_gga(gga) == True:
        try:
            gga = gga.split(',')
            unit = gga[10]
            alt = string.atof(gga[9])
            if unit == 'M' and alt != '':
                return alt
        except ValueError:
            return None
    
#def gga_epochsecs(gga): #seconds since the epoch derived from utc and date in gga
#    isgga = is_gga(gga)
#    utc = gga_utc(gga)
#    #TODO: get dat from OS
#    dat = gga_date(gga)
#    if isgga == True and utc != '' and dat != '':
#        hour = int(utc[0:2])
#        min = int(utc[2:4])
#        sec = int(utc[4:6])
#        day = int(dat[0:2])
#        month = int(dat[2:4])
#        year = dat[4:6]
#        year = int(time.strftime('%Y', time.strptime(year, '%y'))) #convert 2 digit year to 4
#        utc = (year, month, day, hour, min, sec)
#        return calendar.timegm(utc) #convert time to seconds since epoch
#    
#def gga_datetime(gga, fmt): #local time derived from utc and date in gga
#    # example:  gga_datetime(gga, '%I:%M:%S %p') produces 05:03:59 PM
#    # example:  gga_datetime(gga, '%b. %d, %Y') produces Mar. 13, 2010
#    # %a     Locale's abbreviated weekday name.      
#    # %A     Locale's full weekday name.      
#    # %b     Locale's abbreviated month name.      
#    # %B     Locale's full month name.      
#    # %c     Locale's appropriate date and time representation.      
#    # %d     Day of the month as a decimal number [01,31].      
#    # %H     Hour (24-hour clock) as a decimal number [00,23].      
#    # %I     Hour (12-hour clock) as a decimal number [01,12].      
#    # %j     Day of the year as a decimal number [001,366].      
#    # %m     Month as a decimal number [01,12].      
#    # %M     Minute as a decimal number [00,59].      
#    # %p     Locale's equivalent of either AM or PM.     (1)
#    # %S     Second as a decimal number [00,61].     (2)
#    # %U     Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0.     (3)
#    # %w     Weekday as a decimal number [0(Sunday),6].      
#    # %W     Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0.     (3)
#    # %x     Locale's appropriate date representation.      
#    # %X     Locale's appropriate time representation.      
#    # %y     Year without century as a decimal number [00,99].      
#    # %Y     Year with century as a decimal number.      
#    # %Z     Time zone name (no characters if no time zone exists).      
#    # %%     A literal '%' character.
#    sse = gga_epochsecs(gga) #convert time to seconds since epoch
#    if sse != None:
#        stime = time.localtime(sse) #convert to struct_time
#        return time.strftime(fmt, stime)