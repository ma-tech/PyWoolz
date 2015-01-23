#!/usr/bin/python

import sys
from ctypes import *
from Wlz import *

libc = ctypes.CDLL("libc.so.6")
fopen = libc.fopen
fclose = libc.fclose

errNum = enum__WlzErrorNum(WLZ_ERR_NONE)

print "Get the version of Woolz"
print "WlzVersion() = ", WlzVersion()
print

f = 'test.wlz'

print "Read a test object from the file", f
fp = fopen(f, 'rb')
obj = WlzReadObj(fp, byref(errNum))
fclose(fp)
print "obj = ", obj
print "(errNum = ", WlzStringFromErrorNum(errNum, None) + ")"
print

print "Print fields of the object structure directly"
print "Object   type    = ", obj.contents.type
print "Object linkcount = ", obj.contents.linkcount
print "Object domain    = ", obj.contents.domain
print "Object values    = ", obj.contents.values
print "Object  plist    = ", obj.contents.plist
print "Object  assoc    = ", obj.contents.assoc
print

print "Compute the object's volume"
v = WlzVolume(obj, byref(errNum))
print "The volume of obj =", v, \
      " (errNum =", WlzStringFromErrorNum(errNum, None) + ")"
print

print "Find simple object statistics"
n = c_int(0)
g_type = WlzGreyType(WLZ_GREY_ERROR)
g_min  = c_double(0)
g_max  = c_double(0)
g_sum  = c_double(0)
g_ssq  = c_double(0)
g_mean = c_double(0)
g_sdv  = c_double(0)
n = WlzGreyStats(obj, byref(g_type), byref(g_min), byref(g_max),
                 byref(g_sum), byref(g_ssq), byref(g_mean), byref(g_sdv),
		 byref(errNum))
print "g_type = ", WlzStringFromGreyType(g_type, None)
print "g_min  = ", g_min.value
print "g_max  = ", g_max.value
print "g_sum  = ", g_sum.value
print "g_ssq  = ", g_ssq.value
print "g_mean = ", g_mean.value
print "g_sdv  = ", g_sdv.value
print "(errNum =", WlzStringFromErrorNum(errNum, None) + ")"
print

print "Free the object"
WlzFreeObj(obj)
