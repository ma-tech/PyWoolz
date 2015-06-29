#!/usr/bin/python
# Reads a Woolz 2D or 3D domain object and generates a histogram.

from __future__ import print_function
import sys
import ctypes
import Wlz
import matplotlib.pyplot as pt
import numpy as np

libc = ctypes.CDLL("libc.so.6")
fopen = libc.fopen
fclose = libc.fclose

errNum = Wlz.enum__WlzErrorNum(Wlz.WLZ_ERR_NONE)

f = 'test3d.wlz'

print('Read a 3D test object from the file ' +  f);
fp = fopen(f, 'rb')
obj = Wlz.WlzAssignObject(Wlz.WlzReadObj(fp, ctypes.byref(errNum)), None)
fclose(fp)
if(bool(errNum)):
  print('Failed to read object from ' + f + \
        ' (' + Wlz.WlzStringFromErrorNum(errNum, None) + ').')
  exit(1)


if((not bool(obj.contents)) or
   ((obj.contents.type != Wlz.WlzObjectType(Wlz.WLZ_3D_DOMAINOBJ).value) and
    (obj.contents.type != Wlz.WlzObjectType(Wlz.WLZ_2D_DOMAINOBJ).value))): 
  print('Either 2 or 3D domain object with values required.')
  exit(1)

print('Computing histogram')
hobj = Wlz.WlzAssignObject( \
       Wlz.WlzHistogramObj(obj, \
               ctypes.c_int(0), ctypes.c_double(0.0), ctypes.c_double(1.0), \
				       ctypes.byref(errNum)), None)
if(bool(errNum)):
  print('Failed to compute histogram ' + \
        '(' + Wlz.WlzStringFromErrorNum(errNum, None) + ').')
  exit(1)
  
print('Plotting histogram')
hist   = hobj.contents.domain.hist.contents;
n_bins = hist.nBins
center = np.arange(n_bins) + 1.0;
bins = [0] * n_bins
if(hist.type == Wlz.WLZ_HISTOGRAMDOMAIN_INT):
  for i in range(0, n_bins):
    bins[i] = hist.binValues.inp[i]
elif(hist.type == Wlz.WLZ_HISTOGRAMDOMAIN_FLOAT):
  for i in range(0, n_bins):
    bins[i] = hist.binValues.dbp[i]
pt.yscale('log')
pt.bar(center, bins, align='center', width=1)
pt.show()

print('Free the objects')
Wlz.WlzFreeObj(hobj)
Wlz.WlzFreeObj(obj)

