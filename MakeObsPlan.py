#!/usr/local/bin/python3
#
# MakeObsPlan.py
#
# Elisa Antolini
# Jeremy Heyl
# UBC Southern Observatory
#
# This script takes the LIGO-Virgo Skymap (P(d|m)) and optionally a
# galaxy-density map (P(m)) and finds the most likely fields to
# observe (P(m|d)).  The fields are assumed to be healpix regions from a
# tesselation with a given value of nside (the value of nside
# depends of the field of view of the telescope).
#
#   P(position|data) = P(position) P(data|position) / P(data)
#
#   P(position) is the galaxy density map ( P(m) )
#   P(data|position) is the skymap from LIGO-Virgo ( P(d|m) )
#   P(data) is constant with position so we neglect it.
#
#
# Usage:
#
#    python3 MakeObsPlan.py _nside_ _SkyMap_ [_GalMap_] 
#
#
#    nside = ceil ( sqrt (3/Pi) 60 / s ) 
#
#    where s is the length of one side of the square field of view in degrees.
#
#
# Questions: heyl@phas.ubc.ca
#


import math as mt
import numpy as np
import healpy as hp

#
# 1) Load the skymap
# 2) Load the optional galaxy density map
#    a) If one map has nside greater than the other, resample the map
#       with the larger value of nside to that of the smaller.
#    b) Multiply the resulting maps together
# 3) Resample the probability map to the value of nside parameter (if different)
# 4) Sort the array by the probability 
# 5) Output the top N regions with healpix number, RA, Dec and probability
#
#    or 
#
#    Output the regions that add to a given fraction of the total probability.
#
#    By default it would output the top ten regions, but you could set a
#    parameter less than one to do the fraction of the total or greater than
#    one to output N regions.
#
#