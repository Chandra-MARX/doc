# -*- sh -*-
CONFIG=../config.inc
include ${CONFIG}

# marxflux below requires isis in path, so export that here for all
# subcommands. It does not harm those where isis is not required.
export PATH := $(ISISPATH):$(PATH)

all: aped_evt2.fits apedflux.png apedmeg1.png #MEG_drywet_osort.png
# apedfit.png

# convert pictures
%.png: %.ps
	convert -rotate 90 $< $@


apedflux.tbl: apedfun.sl
	$(MARXFLUX) -s apedfun.sl -l '[1:30:#16384]' aped.p apedflux.tbl
aped_evt2.fits: apedflux.tbl run_marx.sh
	sh ./run_marx.sh
aped_pha2.fits: aped_evt2.fits aped_ciao.sh ../runciaotool.sh
	../runciaotool.sh ./aped_ciao.sh
apedmeg1.ps: aped_pha2.fits isismeg1.sl
	$(ISISSCRIPT) ./isismeg1.sl
apedflux.png: apedflux.tbl makeplots.sl
	slsh ./makeplots.sl
clean:
	/bin/rm -f *~
distclean: clean
	/bin/rm -f *.png *.fits apedflux.tbl meg1.rmg
	/bin/rm -rf aped
