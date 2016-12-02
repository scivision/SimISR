#!/usr/bin/env python
"""
Created on Tue Dec 31 10:58:18 2013

@author: JohnSwoboda
"""
import os
import tables

import ISRSpectrum
CONSTPATH = ISRSpectrum.__path__[0]

def getangles(bcodes,radar='risr'):
    """ getangles: This function creates take a set of beam codes and determines
        the angles that are associated with them.
        Inputs
        bcodes - A list of beam codes.
        radar - A string that holds the radar name.
        Outputs
        angles - A list of tuples of the angles.
    """
    constpath = os.path.join(CONSTPATH,'const')
    if radar.lower() == 'risr' or radar.lower()=='risr-n':
        reffile = os.path.join(constpath,'RISR_PARAMS.h5')
    elif radar.lower() == 'pfisr':
        reffile = os.path.join(constpath,'PFISR_PARAMS.h5')
    elif radar.lower() == 'millstone':
        reffile = os.path.join(constpath,'Millstone_PARAMS.h5')
    elif radar.lower() == 'sondrestrom':
        reffile = os.path.join(constpath,'Sondrestrom_PARAMS.h5')

    with tables.open_file(reffile) as f:
        all_ref = f.root.Params.Kmat.read()


    # make a beamcode to angle dictionary
    bco_dict = dict()
    for slin in all_ref:
        bco_num=slin[0].astype(int)
        bco_dict[bco_num] = (float(slin[1]),float(slin[2]))

    # Read in file
    #file_name = 'SelectedBeamCodes.txt'
    if type(bcodes) is str:
        file_name = bcodes
        f = open(file_name)
        bcolines = f.readlines()
        f.close()

        bcolist = [int(float(x.rstrip())) for x in bcolines]
    else:
        bcolist = bcodes
    angles = [bco_dict[x] for x in bcolist]
    return angles