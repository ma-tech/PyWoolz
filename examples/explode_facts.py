#!/usr/bin/python
# Reads a Woolz 3D domain object, prints it's facts. If the object is
# a 3D domain object, then prints the facts for each plane.

from __future__ import print_function
import sys
from ctypes import *
from Wlz import *

libc = ctypes.CDLL("libc.so.6")
fopen = libc.fopen
fclose = libc.fclose

errNum = enum__WlzErrorNum(WLZ_ERR_NONE)

fopen.restype = POINTER(FILE)

f = 'test3d.wlz'

print('Read a 3D test object from the file ' +  f);
fp = fopen(f, 'rb')
obj3 = WlzAssignObject(WlzReadObj(fp, byref(errNum)), None)
fclose(fp)
print('errNum = ' + WlzStringFromErrorNum(errNum, None))
print()


print('Run WlzFacts on the 3D object')
facts = ctypes.cast(0, ctypes.c_char_p)
errNum = WlzObjectFacts(obj3, None,  ctypes.byref(facts), 0);
print('Facts = \n' + facts.value)
print()

if(obj3.contents.type == WlzObjectType(WLZ_3D_DOMAINOBJ).value):
  print('It\'s 3D')
  n_objs = ctypes.c_int()
  objs = ctypes.POINTER(ctypes.POINTER(WlzObject))()
  errNum = WlzExplode3D(ctypes.byref(n_objs), ctypes.byref(objs), obj3);
  print('n_objs ' + str(n_objs.value))
  for i in range(0, n_objs.value):
    print('objs[' + str(i) + ']')
    errNum = WlzObjectFacts(objs[i], None,  ctypes.byref(facts), 0);
    print('Facts = \n' + facts.value)
    print()

print()

print('Free the object')
WlzFreeObj(obj3)
