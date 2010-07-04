#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>
# Published under the terms of "Simplified BSD License".
# License text available at http://opensource.org/licenses/bsd-license.php

# RMC - Recommended Minimum Navigation Information
#
#  Version 2.0 Format
#                                                            12
#        1         2 3       4 5        6 7   8   9    10  11|
#        |         | |       | |        | |   |   |    |   | |
# $--RMC,hhmmss.ss,A,llll.ll,a,yyyyy.yy,a,x.x,x.x,xxxx,x.x,a*hh<CR><LF>
#
# Field Number:
#  1) UTC Time
#  2) Status, V = Navigation receiver warning
#  3) Latitude
#  4) N or S
#  5) Longitude
#  6) E or W
#  7) Speed over ground, knots
#  8) Course over ground, degrees true
#  9) Date, ddmmyy
# 10) Magnetic Declination, degrees
# 11) E or W

# Version 2.0
# 12) Checksum

# Version 2.3
# 12) Mode (D or A), optional, may be NULL
# 13) Checksum

import string
import time
import calendar
from operator import xor

def is_rmc(rmc): #check that the sentence is rmc
    if rmc[3:6] == 'RMC':
        return True
    else:
        return False

def checksum(rmc): #see if the sentence has a valid checksum
    #if is_rmc(rmc) == True:
    try:
        nmea = map(ord, rmc[1:rmc.index('*')])
        chksum = reduce(xor, nmea)
        chksum = str(hex(chksum))[2:4]
        chksum = chksum.upper()
        schksum = rmc.find("*")
        schksum = rmc[schksum+1:schksum+3]
        if schksum[0] == '0':
            schksum = schksum[1]
        if chksum == schksum:
            return 'valid'
        else:
            return 'invalid'
    except ValueError:
        return None

def rmc_utc(rmc): #utc time derived rmc
    if is_rmc(rmc) == True:
        rmc = rmc.split(',')
        utc = rmc[1]
        return utc
    
def rmc_epochsecs(rmc): #seconds since the epoch derived from utc and date in rmc
    isrmc = is_rmc(rmc)
    utc = rmc_utc(rmc)
    dat = rmc_date(rmc)
    if isrmc == True and utc != '' and dat != '':
        hour = int(utc[0:2])
        min = int(utc[2:4])
        sec = int(utc[4:6])
        day = int(dat[0:2])
        month = int(dat[2:4])
        year = dat[4:6]
        year = int(time.strftime('%Y', time.strptime(year, '%y'))) #convert 2 digit year to 4
        utc = (year, month, day, hour, min, sec)
        return calendar.timegm(utc) #convert time to seconds since epoch
    
def rmc_datetime(rmc, fmt): #local time derived from utc and date in rmc
    # example:  rmc_datetime(rmc, '%I:%M:%S %p') produces 05:03:59 PM
    # example:  rmc_datetime(rmc, '%b. %d, %Y') produces Mar. 13, 2010
    # %a     Locale's abbreviated weekday name.      
    # %A     Locale's full weekday name.      
    # %b     Locale's abbreviated month name.      
    # %B     Locale's full month name.      
    # %c     Locale's appropriate date and time representation.      
    # %d     Day of the month as a decimal number [01,31].      
    # %H     Hour (24-hour clock) as a decimal number [00,23].      
    # %I     Hour (12-hour clock) as a decimal number [01,12].      
    # %j     Day of the year as a decimal number [001,366].      
    # %m     Month as a decimal number [01,12].      
    # %M     Minute as a decimal number [00,59].      
    # %p     Locale's equivalent of either AM or PM.     (1)
    # %S     Second as a decimal number [00,61].     (2)
    # %U     Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0.     (3)
    # %w     Weekday as a decimal number [0(Sunday),6].      
    # %W     Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0.     (3)
    # %x     Locale's appropriate date representation.      
    # %X     Locale's appropriate time representation.      
    # %y     Year without century as a decimal number [00,99].      
    # %Y     Year with century as a decimal number.      
    # %Z     Time zone name (no characters if no time zone exists).      
    # %%     A literal '%' character.
    sse = rmc_epochsecs(rmc) #convert time to seconds since epoch
    if sse != None:
        stime = time.localtime(sse) #convert to struct_time
        return time.strftime(fmt, stime)

def rmc_status(rmc): #nav status from rmc
    if is_rmc(rmc) == True:
        rmc = rmc.split(',')
        try:
            status = rmc[2]
            if status == 'A':
                return 'active'
            if status == 'V':
                return 'void'
        except ValueError:
            return None

def rmc_lat(rmc): #latitude from rmc
    if is_rmc(rmc) == True:
        try:
            rmc = rmc.split(',')
            lat = string.atof(rmc[3])
            if rmc[4] == 'S':
                lat = -lat
            deg = int(lat/100)
            min = lat - deg*100
            lat = deg + (min/60)            
            return round(lat, 6)
        except ValueError:
            return None
    else:
        return None
        
        
def rmc_long(rmc): #longitude from rmc
    if is_rmc(rmc) == True:
        try:
            rmc = rmc.split(',')
            long = string.atof(rmc[5])
            if rmc[6] == 'W':
                long = -long
            deg = int(long/100)
            min = long - deg*100
            long = deg + (min/60)
            return round(long, 6)
        except ValueError:
            return None
    else:
        return None

def rmc_sog(rmc): #speed over ground from rmc
    if is_rmc(rmc) == True:
        try:
            rmc = rmc.split(',')
            sog = string.atof(rmc[7])
            return sog
        except ValueError:
            return None
    else:
        return None

def rmc_cog(rmc): #course over ground (track made good) from rmc
    if is_rmc(rmc) == True:
        rmc = rmc.split(',')
        if rmc[8] == '':
            cog = '--'
        else:
            cog = string.atof(rmc[8])
            cog = round(cog, 2)
        return cog
    else:
        return None

def rmc_date(rmc): #date from rmc
    if is_rmc(rmc) == True:
        rmc= rmc.split(',')
        date = rmc[9]
        return date

def rmc_decl(rmc): #magnetic declination from rmc
    if is_rmc(rmc) == True:
        rmc = rmc.split(',')
        decl = rmc[10]
        if rmc[11] == '':
            decl = '--'
        if rmc[11] == 'W':
            decl = -decl
        return decl