#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>
# Published under the terms of "Simplified BSD License".
# License text available at http://opensource.org/licenses/bsd-license.php

# HDT - Heading - True
#
#        1   2 3
#        |   | |
# $--HDT,x.x,T*hh<CR><LF>
#
#Field Number: 
#
# 1) Heading Degrees, true
# 2) T = True
# 3) Checksum

import string
import time
import calendar
from operator import xor

def is_hdt(HDT): #check that the sentence is hdt
    if hdt[3:6] == 'HDT':
        return True
    else:
        return False

def checksum(hdt): #see if the sentence has a valid checksum
    try:
        nmea = map(ord, hdt[1:hdt.index('*')])
        chksum = reduce(xor, nmea)
        chksum = str(hex(chksum))[2:4]
        chksum = chksum.upper()
        schksum = hdt.find("*")
        schksum = hdt[schksum+1:schksum+3]
        if schksum[0] == '0':
            schksum = schksum[1]
        if chksum == schksum:
            return 'valid'
        else:
            return 'invalid'
    except ValueError:
        return None
    
def addchecksum(hdt): #create a checksum for a sentence
    nmea = map(ord, hdt)
    chksum = reduce(xor, nmea)
    chksum = str(hex(chksum))[2:4]
    chksum = chksum.upper()
    return hdt + '*' + chksum + '\r\n'
    

