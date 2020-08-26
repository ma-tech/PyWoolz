#PyWoolz#

A Python binding to Woolz (https://github.com/ma-tech/Woolz). Woolz is an
efficient image processing system developed mainly for atlas informatics
which has is particularly compute and storage efficient for morphological
and set operations in 2D and 3D.

The binding relies on Python, ctypes ctypesgen and the Woolz libraries which
should be build with position independent code.

To build the binding edit the Makefile so that the Woolz include and library
files can be found, then type make. Once built copy the Python file (Wlz.py)
and shared library file (libPyWlz.so) to somewhere in your Python path and
shared library path.

It is possible to generate a binding which is Python 3 compatible, but
python 2 must be used to do this and a modified version of ctypesgen
must be used. A suitable vesion of ctypesgen can be found at
https://github.com/ma-tech/ctypesgen .

Simple example:

    import sys
    from ctypes import *
    from Wlz import *

    libc = ctypes.CDLL('libc.so.6')
    fopen = libc.fopen
    fclose = libc.fclose
    fopen.restype = POINTER(FILE)

    errNum = enum__WlzErrorNum(WLZ_ERR_NONE)

    print('WlzVersion() = ' + str(WlzVersion()))

    fp = fopen(b'test.wlz', 'rb')
    obj = WlzReadObj(fp, byref(errNum))
    fclose(fp)

    v = WlzVolume(obj, byref(errNum))
    print('The volume of obj = ' + str(v) + \
	  ' (errNum = ' +  str(WlzStringFromErrorNum(errNum, None)) + ')')

    WlzFreeObj(obj)


