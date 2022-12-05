#!/bin/sh

X=4068.3;    # determined by hand in ds9
Y=4112.7;    # determined by hand in ds9

# We'll use the same mask for both extractions, because we want the same region.
tg_create_mask infile="EQPegB.fits" outfile="EQPegB_reg1a.fits" \
  use_user_pars=yes last_source_toread=A \
  sA_id=1 sA_zero_x=$X sA_zero_y=$Y clobber=yes grating_obs=header_value \
  width_factor_hetg=10


### Extract EQ Peg B from the EQ PEg B - only simulation ###

tg_resolve_events infile="EQPegB.fits" outfile="EQPegB_evt1a.fits" \
  regionfile="EQPegB_reg1a.fits" acaofffile="EQPeg_asol1.fits" \
  osipfile=CALDB verbose=0 clobber=yes

tgextract infile="EQPegB_evt1a.fits" outfile="EQPegB_pha2.fits" mode=h clobber=yes


### Extract EQ Peg B from the combined simulation ###

tg_resolve_events infile="EQPeg_both.fits" outfile="EQPegB_both_evt1a.fits" \
  regionfile="EQPegB_reg1a.fits" acaofffile="EQPeg_asol1.fits" \
  osipfile=CALDB verbose=0 clobber=yes

tgextract infile="EQPegB_both_evt1a.fits" outfile="EQPegB_both_pha2.fits" mode=h clobber=yes


# make response matrices for the MEG +1 and -1 order
# We are extracting the exact same region in both cases above for EXACTLY the same
# observational parameters (aimpoint, exposure time, ...).
# Thus the arf and rmf files will be identical, so we have to run this only once.
mkgrmf grating_arm="MEG" order=1 outfile="eqpeg_meg1_rmf.fits" srcid=1 detsubsys=ACIS-S3 \
   threshold=1e-06 obsfile="EQPegB_pha2.fits" regionfile="EQPegB_pha2.fits" \
   wvgrid_arf="compute" wvgrid_chan="compute"

mkgrmf grating_arm="MEG" order=-1 outfile="eqpegmeg-1_rmf.fits" srcid=1 detsubsys=ACIS-S3 \
   threshold=1e-06 obsfile="EQPegB_pha2.fits" regionfile="EQPegB_pha2.fits" \
   wvgrid_arf="compute" wvgrid_chan="compute"

fullgarf phafile="EQPegB_pha2.fits"  pharow=3 evtfile="EQPegB.fits" \
   asol="EQPeg_asol1.fits" engrid="grid(eqpeg_meg1_rmf.fits[cols ENERG_LO,ENERG_HI])" \
   maskfile=NONE dafile=NONE dtffile=NONE badpix=NONE rootname="eqpeg" ardlibqual=";UNIFORM;bpmask=0"

fullgarf phafile="EQPegB_pha2.fits"  pharow=4 evtfile="EQPegB.fits" \
   asol="EQPeg_asol1.fits" engrid="grid(eqpeg_meg1_rmf.fits[cols ENERG_LO,ENERG_HI])" \
   maskfile=NONE dafile=NONE dtffile=NONE badpix=NONE rootname="eqpeg" ardlibqual=";UNIFORM;bpmask=0"
