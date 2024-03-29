#!/bin/sh

X=4096.5
Y=4096.5

Verbose=1

# marx2fits generated file
evt2file="letgplaw_evt2.fits"

# These files are generated by this script
evt1afile="letgplaw_evt1a.fits"
reg1afile="letgplaw_reg1a.fits"
asolfile="letgplaw_asol1.fits"
pha2file="letgplaw_pha2.fits"

tg_create_mask infile="$evt2file" outfile="$reg1afile" \
  use_user_pars=yes last_source_toread=A \
  sA_id=1 sA_zero_x=$X sA_zero_y=$Y grating_obs=header_value \
  clobber=yes verbose=$Verbose

tg_resolve_events infile="$evt2file" outfile="$evt1afile" \
     regionfile="$reg1afile" osipfile="CALDB" acaofffile="$asolfile" \
     verbose=$Verbose clobber=yes

tgextract infile="$evt1afile" outfile="$pha2file" tg_order_list="-1,+1" \
  ancrfile=none respfile=NONE inregion_file=none clobber=yes \
  tg_srcid_list=1 outfile_type=pha_typeII tg_part_list='header_value'

mkgrmf grating_arm="LEG" order=-1 outfile="leg-1_rmf.fits" srcid=1 detsubsys="ACIS-S3" \
  threshold=1e-06 obsfile="$pha2file" regionfile="$pha2file" \
  wvgrid_arf="compute" wvgrid_chan="compute" clobber=yes

fullgarf phafile="$pha2file"  pharow=1 evtfile="$evt2file" \
  asol="$asolfile" engrid="grid(leg-1_rmf.fits[cols ENERG_LO,ENERG_HI])" \
  maskfile=NONE dafile=NONE dtffile=NONE badpix=NONE maskfile=NONE rootname="leg" ardlibqual=";UNIFORM;bpmask=0"

mkgrmf grating_arm="LEG" order=+1 outfile="leg+1_rmf.fits" srcid=1 detsubsys="ACIS-S3" \
   threshold=1e-06 obsfile="$pha2file" regionfile="$pha2file" \
   wvgrid_arf="compute" wvgrid_chan="compute" clobber=yes

fullgarf phafile="$pha2file"  pharow=2 evtfile="$evt2file" \
   asol="$asolfile" engrid="grid(leg+1_rmf.fits[cols ENERG_LO,ENERG_HI])" \
   maskfile=NONE dafile=NONE dtffile=NONE badpix=NONE maskfile=NONE rootname="leg" ardlibqual=";UNIFORM;bpmask=0"


