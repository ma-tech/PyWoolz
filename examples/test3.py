#!/usr/bin/python3
# Tests of basic access to Woolz objects from python3.

import sys
from ctypes import *
from Wlz import *

libc = ctypes.CDLL("libc.so.6")
fopen = libc.fopen
fclose = libc.fclose

errNum = enum__WlzErrorNum(WLZ_ERR_NONE)

fopen.restype = POINTER(FILE)

print("Get the version of Woolz")
print("WlzVersion() = " + WlzVersion().decode())
print()

f = b'test.wlz'

print("Read a test object from the file" + f.decode())
fp = fopen(f, b'rb')
obj = WlzReadObj(fp, byref(errNum))
fclose(fp)
print("obj = " + str(obj))
print("(errNum = " + WlzStringFromErrorNum(errNum, None).decode() + ")")
print()

print("Print fields of the object structure directly")
print("Object   type    = " + str(obj.contents.type))
print("Object linkcount = " + str(obj.contents.linkcount))
print("Object domain    = " + str(obj.contents.domain))
print("Object values    = " + str(obj.contents.values))
print("Object  plist    = " + str(obj.contents.plist))
print("Object  assoc    = " + str(obj.contents.assoc))
print()

print("Compute the object's volume")
v = WlzVolume(obj, byref(errNum))
print("The volume of obj = " + str(v) + " (errNum = " +
      str(WlzStringFromErrorNum(errNum, None).decode()) + ")")
print()

print("Find simple object statistics")
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
print("g_type = " + WlzStringFromGreyType(g_type, None).decode())
print("g_min  = " + str(g_min.value))
print("g_max  = " + str(g_max.value))
print("g_sum  = " + str(g_sum.value))
print("g_ssq  = " + str(g_ssq.value))
print("g_mean = " + str(g_mean.value))
print("g_sdv  = " + str(g_sdv.value))
print("(errNum = " + str(WlzStringFromErrorNum(errNum, None).decode()) + ")")
print()

print("Free the object")
WlzFreeObj(obj)
