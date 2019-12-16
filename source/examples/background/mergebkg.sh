#! /bin/bash

# Pick how many background photons we want to add to our simulation.

n=`dmlist acis7sbkg.fits header,raw | grep NAXIS2 | awk '{ print $6 }'`
dmtcalc acis7sbkg.fits temp.fits expression="randnum=$n/3e4*#trand" clobber=yes
dmcopy "temp.fits[randnum=0:1]" temp2.fits clobber=yes

# Assign some random time during the observation to each photon.
t0=`dmkeypar diffuse_evt2.fits TSTART echo+`
t1=`dmkeypar diffuse_evt2.fits TSTOP echo+`

dmtcalc temp2.fits temp3.fits expression="time=$t0+($t1-$t0)*#trand" clobber=yes
dmsort temp3.fits temp4.fits keys=TIME clobber=yes

# Reproject the blank sky fields to the same position on the sky as the marx simulation.
punlearn reproject_events 
reproject_events infile=temp4.fits outfile=acis7s_bkg_reproj.fits aspect=diffuse_asol1.fits match=diffuse_evt2.fits clobber=yes

# Merge marx simulation and blank sky fields into a single fits table.
punlearn dmmerge
dmmerge "diffuse_evt2.fits[cols ccd_id,node_id,chip,det,sky,pha,energy,pi,fltgrade,grade,status,time]","acis7s_bkg_reproj.fits[cols ccd_id,node_id,chip,det,sky,pha,energy,pi,fltgrade,grade,status,time]" merged.fits clobber=yes

