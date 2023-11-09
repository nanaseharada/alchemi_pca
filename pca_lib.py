import os, sys, glob, copy, inspect
from astropy.io import fits
import numpy as np
from astropy.coordinates import SkyCoord
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import time
import matplotlib.animation as animation
from matplotlib import pyplot as plt, colors
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import csv

#function to calculate observed frequency from rest freq and vel
def obsfreq(restf,vel):
    spl = 2.998e5 #speed of light in km/s
    obsf = restf * (1. - vel/spl)
    return obsf # in the unit of restf

#function to convert Jy/beam to K---------------------------------                                                                                                                     
def JytoK(jyint,freq,beam):
    """                                                                     
    parameters                                                                                                              
    jyint [Jy/beam]: observed intensity                                                                                                            
    freq [GHz] : observed frequency                                                                                                                                  
    beam [arcsec] : beam size                                                                                                                              
    """
    return  1.224e6*jyint/(beam*beam*freq*freq)
#end of function JytoK ------------------------------------------- 
#read the 2dimentional fits image -------------------
def read_data(fitsimage):
    #function to read the data from fits image                   
    #fitsfile  :  fits file names to read                

    #open the fits file and read                                                                                                                                                                                                                      
    with fits.open(fitsimage) as hdul:
        hdul.verify('fix')
        header = hdul[0].header
        data = hdul[0].data
        hdul.close()

    raref = header['CRVAL1'] # reference ra in deg
    decref = header['CRVAL2'] # reference dec in deg
    rarfpix = header['CRPIX1'] # reference pix of ra
    decrfpix = header['CRPIX2'] # reference pix of dec
    raincr = header['CDELT1'] # increment ra in deg
    decincr = header['CDELT2'] # increment dec in deg
    xsize = header['NAXIS1'] # number of pixels in x
    ysize = header['NAXIS2'] # number of pixels in y

    raincras = raincr*3600. # ra increment in arcsec
    decincras = decincr*3600. # dec increment in arcsec

    x = [(i-rarfpix)*raincras for i in range(xsize)]
    y = [(i-decrfpix)*decincras for i in range(ysize)]

    return x,y,data
#end of a function read_2Ddata ------------------
#Obtain the hexagonally binned data pixel by pixel in images
def get_hexbin(
        x,
        y,
        data,
        beam=1.6,
        gridsize=(40,20),
        fill = 0.,
):
    """
    Parameters 
    x : 1D array of x coordinates
    y : 1D array of y coordinates
    data : 2D data of intensity in the data
    beam : float [arcsec] beam size
    gridsize :integer number of hexagon in one direction
    fill: value to fill nan with
    """

    #change the x array into 2D that can be fed to hexbin
    nx = len(x)
    ny = len(y)

    x2d = []
    y2d=[]
    
    for ye in y:
        y2d.append([ye]*nx)

    x2d = x*ny

    X = np.array(x2d).reshape(-1)
    Y = np.array(y2d).reshape(-1)
    print('Length of x, y',nx,ny,len(X),len(Y))
    # determine sampling grid                                                                                                                                                       
    sizex   = 0.5 * gridsize[0] * beam
    sizey   = 0.5 * np.sqrt(3.) * gridsize[1] * beam
    extent = [sizex, -sizex, -sizey, sizey]

    # hex sampling                                                                                           
    #fig = plt.figure(figsize=(9,9))
    #gs  = GridSpec(nrows=1,ncols=1)
    #ax  = plt.subplot(gs[0:1,0:1],aspect='equal')

    dataall =[]
    ims =[]

    fig = plt.figure(figsize=(9,9))
    gs  = GridSpec(nrows=1,ncols=1)
    ax  = plt.subplot(gs[0:1,0:1],aspect='equal')
    c     = np.nan_to_num(data,nan=fill) # K.km/s
    C = np.array(c).reshape(-1)

    hexdata = ax.hexbin(X, Y, C=C, gridsize=gridsize, extent=extent)
    hexc    = np.array(hexdata.get_array())
    print('shape of hexbinned data',np.shape(hexc))
    """
    if idx == 50:
    ax.invert_xaxis()
    fig.colorbar(hexdata)
    plt.axis('scaled')
    plt.show()
    """
    #print(hexc[0])
    dataall.append(hexc)
    #print(hexc)
    
    hexdata = ax.hexbin(X, Y, C=X, gridsize=gridsize, extent=extent)
    hexx    = np.array(hexdata.get_array())
    print('shape of hexbinned x',np.size(hexx))
    hexdata = ax.hexbin(X, Y, C=Y, gridsize=gridsize, extent=extent)
    hexy    = np.array(hexdata.get_array())
    plt.close()
    return hexx,hexy,np.c_[dataall]
#------------------------------------------------------------
