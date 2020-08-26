#!/usr/bin/python
# Tests of basic access to Woolz objects.

from __future__ import print_function
import sys
from ctypes import *
from Wlz import *

libc = ctypes.CDLL("libc.so.6")
fopen = libc.fopen
fclose = libc.fclose

fopen.restype = POINTER(FILE)

errNum = enum__WlzErrorNum(WLZ_ERR_NONE)

def isPython3():
  return (sys.version_info[0] == 3)

def readObject(f):
  f = f.encode('ascii') if (isPython3) else f
  print('Reading test object from the file ' + str(f))
  fp = fopen(f, 'rb')
  print('fp = ' + str(fp))
  obj = WlzReadObj(fp, byref(errNum))
  fclose(fp)
  print('obj = ' + str(obj))
  print('(errNum = ' + str(WlzStringFromErrorNum(errNum, None)) + ')')
  print()
  return obj


def printCoreObject(obj):
  print('Print fields of the object structure directly')
  print('Object   type    = ' + str(obj.contents.type))
  print('Object linkcount = ' + str(obj.contents.linkcount))
  print('Object domain    = ' + str(obj.contents.domain))
  print('Object values    = ' + str(obj.contents.values))
  print('Object  plist    = ' + str(obj.contents.plist))
  print('Object  assoc    = ' + str(obj.contents.assoc))
  print()

def printObjectFacts(obj):
  print('Print object facts')
  facts = ctypes.cast(0, POINTER(c_char))
  errNum = WlzObjectFacts(obj, None,  ctypes.byref(facts), 0);
  facts = ctypes.cast(facts, c_char_p)
  print('Facts = \n' + bytes.decode(facts.value))
  print()

print('*** Woolz Version ***')

print('WlzVersion() = ' + str(WlzVersion()))
print()

print('*** Domain Object Tests ***')

obj = readObject('test.wlz')

printCoreObject(obj)

printObjectFacts(obj)

print('Compute the object\'s volume')
v = WlzVolume(obj, byref(errNum))
print('The volume of obj = ' + str(v) +
      ' (errNum = ' + str(WlzStringFromErrorNum(errNum, None)) + ')')
print()

print('Find simple object statistics')
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
print('g_type = ' + str(WlzStringFromGreyType(g_type, None)))
print('g_min  = ' + str(g_min.value))
print('g_max  = ' + str(g_max.value))
print('g_sum  = ' + str(g_sum.value))
print('g_ssq  = ' + str(g_ssq.value))
print('g_mean = ' + str(g_mean.value))
print('g_sdv  = ' + str(g_sdv.value))
print('(errNum = ' + str(WlzStringFromErrorNum(errNum, None)) + ')')
print()

print('Free the object')
WlzFreeObj(obj)
print()


print('*** B-Spline Tests ***')

obj = readObject('test-bs.wlz')

printCoreObject(obj)

printObjectFacts(obj)

print('Compute B-spline length')
l = WlzBSplineLength(obj.contents.domain.bs, 0.0, 1.0, byref(errNum))
print('The length of obj = ' + str(l) + 
      ' (errNum = ' + str(WlzStringFromErrorNum(errNum, None)) + ')')
print()

print('Free the object')
WlzFreeObj(obj)
print()
