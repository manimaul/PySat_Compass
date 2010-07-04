#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>
# Converted to python from georef.c (Copyright (C) 2010 by David S. Register)
# Published under the terms of "Simplified BSD License".
# License text available at http:#opensource.org/licenses/bsd-license.php

import math

WGSinvf = 298.257223563
mercator_k0 = 0.9996;
WGS84_semimajor_axis_meters = 6378137.0;
PI = math.pi
DEGREE = PI/180

def BearingMercator(lat0, lon0, lat1, lon1):
    lon0x = lon0
    lon1x = lon1
    ##Calculate bearing by conversion to SM (Mercator) coordinates, then simple trigonometry

    #Make lon points the same phase
    if((lon0x * lon1x) < 0.):
        if(lon0x < 0.):
            lon0x += 360.
        else:
            lon1x += 360.
            #Choose the shortest distance
            if(math.fabs(lon0x - lon1x) > 180.):
                if(lon0x > lon1x):
                    lon0x -= 360.
                else:
                    lon1x -= 360.
            #Make always positive
            lon1x += 360.
            lon0x += 360.
    #Calculate the bearing using the un-adjusted original latitudes and Mercator Sailing
    east, north = toSM_ECC(lat1, lon1x, lat0, lon0x)
    C = math.atan2(east, north)
    brgt = 180. + (C * 180. / PI)
    if (brgt < 0):
        brgt += 360.
    if (brgt > 360.):
        brgt -= 360

    return brgt
        

def toSM_ECC(lat, lon, lat0, lon0):
    f = 1.0 / WGSinvf   # WGS84 ellipsoid flattening parameter
    e2 = 2 * f - f * f  # eccentricity^2  .006700
    e = math.sqrt(e2)
    
    xlon = lon
    
    z = WGS84_semimajor_axis_meters * mercator_k0
    
    x1 = (xlon - lon0) * DEGREE * z
    east = x1
    
    s = math.sin(lat * DEGREE)
    y3 = (.5 * math.log((1 + s) / (1 - s))) * z
    
    s0 = math.sin(lat0 * DEGREE)
    y30 = (.5 * math.log((1 + s0) / (1 - s0))) * z
    y4 = y3 - y30;
    
    falsen = z * math.log(math.tan(PI/4 + lat0 * DEGREE / 2) * math.pow((1. - e * s0)/(1. + e * s0), e/2.))
    test = z * math.log(math.tan(PI/4 + lat  * DEGREE / 2) * math.pow((1. - e * s )/(1. + e * s), e/2.))
    ypy = test - falsen
    
    north = ypy
    
    return east, north