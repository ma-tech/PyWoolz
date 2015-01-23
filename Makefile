
CTG		= ctypesgen.py
MA		= /home/bill/MouseAtlas/Build
CFLAGS		= -shared

Wlz.py:		libPyWlz.so
		$(CTG) -o Wlz.py \
		       -I$(MA)/debug/include -L . -L$(MA)/debug/lib \
		       -l libPyWlz.so \
		       $(MA)/include/Wlz.h \
		       $(MA)/include/WlzType.h \
		       $(MA)/include/WlzProto.h \
		       $(MA)/include/WlzError.h

libPyWlz.so:
		$(CC) $(CFLAGS) -o $@ \
		      -Wl,--whole-archive \
		      -L$(MA)/lib -lWlz -lAlg -lAlc \
		      -Wl,--no-whole-archive \
		      -lgomp


clean:
		$(RM) Wlz.py Wlz.pyc libPyWlz.so
