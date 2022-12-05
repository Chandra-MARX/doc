#!/bin/sh
evtfile="aped_evt2.fits"
evt1afile="aped_evt1a.fits"
reg1afile="aped_reg1a.fits"
asol1file="aped_asol1.fits"
pha2file="aped_pha2.fits"

X=4017.88;    # determined by findzo
Y=4141.43;    # determined by findzo

tg_create_mask infile="$evtfile" outfile="$reg1afile" \
  use_user_pars=yes last_source_toread=A \
  sA_id=1 sA_zero_x=$X sA_zero_y=$Y clobber=yes grating_obs=header_value 

tg_resolve_events infile="$evtfile" outfile="$evt1afile" \
  regionfile="$reg1afile" acaofffile="$asol1file" \
  osipfile=CALDB verbose=0 clobber=yes

tgextract infile="$evt1afile" outfile="$pha2file" mode=h clobber=yes
