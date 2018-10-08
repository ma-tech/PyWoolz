
CTG		= ctypesgen.py
#WLZDIR		= /opt/MouseAtlas/
#WLZDIR		= $$HOME/MouseAtlas/Build
WLZDIR		= $$HOME/MouseAtlas/Build/debug
CFLAGS		= -shared -g

Wlz.py:		libPyWlz.so
		$(CTG) -o Wlz.py \
		       -I$(WLZDIR)/include \
		       -L. -L$(WLZDIR)/lib \
		       -l libPyWlz.so \
		       $(WLZDIR)/include/Wlz.h \
		       $(WLZDIR)/include/AlcType.h \
		       $(WLZDIR)/include/AlcProto.h \
		       $(WLZDIR)/include/AlgType.h \
		       $(WLZDIR)/include/AlgProto.h \
		       $(WLZDIR)/include/Wlz.h \
		       $(WLZDIR)/include/WlzType.h \
		       $(WLZDIR)/include/WlzProto.h \
		       $(WLZDIR)/include/WlzError.h \
		       $(WLZDIR)/include/WlzBnd.h \
		       $(WLZDIR)/include/WlzBndType.h \
		       $(WLZDIR)/include/WlzBndProto.h  

libPyWlz.so:
		$(CC) $(CFLAGS) -o $@ \
		      -Wl,--whole-archive \
		      -L$(WLZDIR)/lib -lWlzBnd -lWlz -lAlg -lAlc \
		      -Wl,--no-whole-archive \
		      -lgomp


clean:
		$(RM) Wlz.py Wlz.pyc libPyWlz.so
