#!/bin/sh

# Arguments: root name of files
# Call this with the root names of the files as first argument, e.g.
# > hetg_ciao.sh hetg_plaw
# to process the first example.

root=$1
evtfile="${root}_evt2.fits"
evt1afile="${root}_evt1a.fits"
reg1afile="${root}_reg1a.fits"
asol1file="${root}_asol1.fits"
pha2file="${root}_pha2.fits"

X=4096.5;    # determined by hand in ds9
Y=4096.5;    # determined by hand in ds9

tg_create_mask infile="$evtfile" outfile="$reg1afile" \
  use_user_pars=yes last_source_toread=A \
  sA_id=1 sA_zero_x=$X sA_zero_y=$Y clobber=yes grating_obs=header_value 

tg_resolve_events infile="$evtfile" outfile="$evt1afile" \
  regionfile="$reg1afile" acaofffile="$asol1file" \
  osipfile=CALDB verbose=0 clobber=yes

tgextract infile="$evt1afile" outfile="$pha2file" mode=h clobber=yes tg_order_list="-1,1"

# make response matrices for the MEG +1 and -1 order
mkgrmf grating_arm="MEG" order=-1 outfile="${root}meg-1_rmf.fits" srcid=1 detsubsys=ACIS-S3 \
   threshold=1e-06 obsfile="$pha2file" regionfile="$pha2file" \
   wvgrid_arf="compute" wvgrid_chan="compute"

mkgrmf grating_arm="MEG" order=1 outfile="${root}meg1_rmf.fits" srcid=1 detsubsys=ACIS-S3 \
   threshold=1e-06 obsfile="$pha2file" regionfile="$pha2file" \
   wvgrid_arf="compute" wvgrid_chan="compute"

fullgarf phafile="$pha2file"  pharow=3 evtfile="$evtfile" \
   asol="$asol1file" engrid="grid(${root}meg-1_rmf.fits[cols ENERG_LO,ENERG_HI])" \
   maskfile=NONE dafile=NONE dtffile=NONE badpix=NONE rootname="$root" ardlibqual=";UNIFORM;bpmask=0"

fullgarf phafile="$pha2file"  pharow=4 evtfile="$evtfile" \
   asol="$asol1file" engrid="grid(${root}meg1_rmf.fits[cols ENERG_LO,ENERG_HI])" \
   maskfile=NONE dafile=NONE dtffile=NONE badpix=NONE rootname="$root" ardlibqual=";UNIFORM;bpmask=0"
