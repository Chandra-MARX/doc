CONFIG=../config.inc
include ${CONFIG}

all: obs1068_chandra.png compare_sims.png

%.par:
	cp ${MARXPREFIX}/share/marx/pfiles/$@ .

1068/primary/acisf01068N003_evt2.fits.gz: ../runciaotool.sh
	../runciaotool.sh download_chandra_obsid 1068

1068/repro/acisf01068_repro_evt2.fits: 1068/primary/acisf01068N003_evt2.fits.gz
	../runciaotool.sh chandra_repro 1068 1068/repro

obs1068_chandra.png obs1068_chandra.eps: 1068/repro/acisf01068_repro_evt2.fits
	../runciaotool.sh ds9 -width 800 -height 500 -log -cmap heat $< -crosshair 5256 6890 physical -pan to 5256 6890 physical -bin about 5256 6890 -regions load all scalebar.reg -saveimage $@ -exit


obs1068.arf: 1068/repro/acisf01068_repro_evt2.fits runmkarf.sh ../runciaotool.sh
	../runciaotool.sh ./runmkarf.sh

obs1068.spec: 1068/repro/acisf01068_repro_evt2.fits extract.sh ../runciaotool.sh
	../runciaotool.sh ./extract.sh

input_spec_marx.tbl: obs1068.arf obs1068.spec spectrum2ascii.sh ../runciaotool.sh
	../runciaotool.sh ./spectrum2ascii.sh

marx_only.fits: marxonly.sh 1068/repro/acisf01068_repro_evt2.fits ../runmarxtool.sh input_spec_marx.tbl marx.par
	../runmarxtool.sh ./$<

saotrace.fits: saotrace.sh input_spec_marx.tbl ../runsaotracetool.sh
	../runsaotracetool.sh ./$<

marx_saotrace.fits: marxsaotrace.sh saotrace.fits ../runmarxtool.sh marx.par
	../runmarxtool.sh ./$<

marx_saotrace-filtered.fits: gtimarxsaotrace.sh marx_saotrace.fits ../runciaotool.sh
	../runciaotool.sh ./$<

compare_sims.png compare_sims.eps: 1068/repro/acisf01068_repro_evt2.fits marx_only.fits marx_saotrace-filtered.fits
	../runciaotool.sh ds9 -width 800 -height 500 -log -cmap heat $^ -pan to 5256 6890 physical -bin about 5256 6890 -match frame wcs -match bin -frame 1 -regions command 'text 5:39:27.987 -69:43:52.31 # text=Observation font="helvetica 24"' -frame 2 -regions command 'text 5:39:27.987 -69:43:52.31 # text="only MARX" font="helvetica 24"' -frame 3 -regions command 'text 5:39:27.987 -69:43:52.31 # text=SAOTrace font="helvetica 24"' -regions load all scalebar.reg -saveimage $@ -exit

clean:
	/bin/rm -f *~ */*~
distclean: clean
	/bin/rm -rf *.tbl *.fits *.par 1068 *.png *.eps *.jpg \
	marx_onlyx_saotrace obs1068* input_spec* *.reg

.PHONY: all clean distclean

