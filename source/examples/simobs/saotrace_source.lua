ra_pnt = 85.368613
dec_pnt = -70.12585
roll_pnt = 116.86955

dither_asol_chandra{ file = "1068/primary/pcadf01068_000N001_asol1.fits",
                     ra = ra_pnt, dec = dec_pnt, roll = roll_pnt }

point{ position = { ra = 84.91093,
          dec = -69.74348,
          ra_aimpt = ra_pnt,
          dec_aimpt = dec_pnt,
       },
       spectrum = { { file = "input_spec_saotrace.rdb", 
                      units = "photons/s/cm2", 
                      scale = 1, 
                      format = "rdb",
                      emin = "ENERG_LO",
                      emax = "ENERG_HI",
                      flux = "FLUX"} }
    }
