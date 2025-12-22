.. _spacecraftpars:


Further |marx| parameters
==========================

|marx| accepts a large number of parameters. Only a small fraction of those is
needed by the average |marx| user and those parameters are explained in detail
in this manual. For each parameter, :ref:`genindex` links to the section that
explains its use.

However, many parameters are only required for calibration purposes.  These
parameters are listed here with a short (or longer) explanation.  Their
defaults point to a file with calibration information that is shipped with
|marx| or they set a parameter of the the Chandra geometry.  Those parameters
typically should not be changed from their default value.  Other parameters are
only of historical interest (e.g. :par:`dNumRays` optimizes |marx| for
computers with less then 50 MB of memory).

Parameters can be set on the command line. All parameters not set in this way
will be read from a parameter file. These files are plain text files and it
should be easy to edit them in any text editor. If required, there is a
`detailed description of the format
<http://cxc.harvard.edu/ciao/ahelp/parameter.html#Contents_of_a_Parameter_File>`_.
See the description of :marxtool:`marx` for different ways to select a
parameter file.


Parameter file
~~~~~~~~~~~~~~
.. parameter:: mode

.. parameter:: DataDirectory


Simulation control
~~~~~~~~~~~~~~~~~~
.. parameter:: dNumRays

   This parameter determines the number of rays per iteration which will be used.
   This parameter is only of historical interest. It was used for computers
   with less than about 50 MB of memory.

.. parameter:: DumpToRayFile

.. parameter:: SourceDistance

   Source distance in meters (`0` means infinite).
   |marx| can also simulate photons from a source at a finite
   distance. This functionality is useful for XRCF simulations
   where the X-ray source was not at infinity.
   Non-astronomical sources can be specified using the
   ``SourceDistance`` parameter which sets the distance
   between the source and the front aperture of the HRMA in meters.


Output Vectors
~~~~~~~~~~~~~~

Although users are encouraged to use the default settings for the |marx|
output, the available options are listed below for completeness:

.. parameter:: OutputVectors
   
   This parameter specifies a list of output files that |marx| writes.
   Each |marx| output file contains information on a given photon property
   (arrival time, energy, etc.) and each is :math:`N` elements long where
   :math:`N` is the number of *detected* photons.
   
   This parameter is set to a string where each desired output
   file is represented as a string.

   +--------------+------+------------------------------------------------+
   | Filename     | Code | Description                                    |
   +==============+======+================================================+
   |b_energy.dat  | B    |Detected energy of event [keV]                  |
   +--------------+------+------------------------------------------------+
   |detector.dat  | D    |Chip ID (CCD for ACIS or MCP for HRC)           |
   +--------------+------+------------------------------------------------+
   |energy.dat    | E    |The true photon energy [keV]                    |
   +--------------+------+------------------------------------------------+
   |marx.par      | --   |Updated parameter file                          |
   +--------------+------+------------------------------------------------+
   |mirror.dat    | M    |Reflection shell of the HRMA                    |
   +--------------+------+------------------------------------------------+
   |obs.par       | --   |Information summary for FITS header             |
   +--------------+------+------------------------------------------------+
   |pha.dat       | P    |The pulse height of the detected photon [PHA]   |
   +--------------+------+------------------------------------------------+
   |time.dat      | T    |Photon arrival time [sec]                       |
   +--------------+------+------------------------------------------------+
   |xcos.dat      | 1    |The X–axis direction cosine of the photon       |
   +--------------+------+------------------------------------------------+
   |xpixel.dat    | x    |The X–axis detection pixel                      |
   +--------------+------+------------------------------------------------+
   |xpos.dat      | X    |The X–axis position of the photon [mm]          |
   +--------------+------+------------------------------------------------+
   |ycos.dat      | 2    |The Y–axis direction cosine of the photon       |
   +--------------+------+------------------------------------------------+
   |ypixel.dat    | y    |The Y–axis detection pixel                      |
   +--------------+------+------------------------------------------------+
   |ypos.dat      | Y    |The Y–axis position of the photon [mm]          |
   +--------------+------+------------------------------------------------+
   |zcos.dat      | 3    |The Z–axis direction cosine of the photon       |
   +--------------+------+------------------------------------------------+
   |zpos.dat      | Z    |The Z–axis position of the photon [mm]          |
   +--------------+------+------------------------------------------------+
   | **Additional HRC specific files**                                    |
   +--------------+------+------------------------------------------------+
   |region.dat    | r    | Detection region on the HRC detector           |
   +--------------+------+------------------------------------------------+
   |hrc_u.dat     | --   | The raw HRC U coordinate of the detected event |
   +--------------+------+------------------------------------------------+
   | hrc_v.dat    | --   | The raw HRC V coordinate of the detected event |
   +--------------+------+------------------------------------------------+
   | **Additional HETG specific files**                                   |
   +--------------+------+------------------------------------------------+
   | order.dat    | O    | The diffraction order of the photon            |
   +--------------+------+------------------------------------------------+
   | **Additional LETG specific files**                                   |
   +--------------+------+------------------------------------------------+
   | ocoarse1.dat | d    | The order of a photon diffracted by the coarse |
   |              |      | wire support structure of the LETG             |
   +--------------+------+------------------------------------------------+
   | ocoarse2.dat | c    | The order of a photon diffracted by the coarse |
   |              |      | wire support structure of the LETG             |
   +--------------+------+------------------------------------------------+
   | ocoarse3.dat | b    | The order of a photon diffracted by the coarse |
   |              |      | wire support structure of the LETG             |
   +--------------+------+------------------------------------------------+
   | ofine.dat    | a    | The order of a photon diffracted by the fine   |
   |              |      | wire support structure of the LETG             |
   +--------------+------+------------------------------------------------+
   | order.dat    | O    | The primary diffraction order of the photon    |
   +--------------+------+------------------------------------------------+
   | **Additional Aspect specific files**                                 |
   +--------------+------+------------------------------------------------+
   | sky_ra.dat   | S    | The Sky X pixel value                          |
   +--------------+------+------------------------------------------------+
   | sky_dec.dat  | S    | The Sky Y pixel value                          |
   +--------------+------+------------------------------------------------+
   | sky_roll.dat | S    | The sky roll angle                             |
   +--------------+------+------------------------------------------------+

   The following table describes the format of the binary output files (Length
   and Offset are given in bytes):

   +--------+--------+-------------------------------------------------------+
   | Offset | Length | Interpretation                                        |
   +========+========+=======================================================+
   | 0      | 4      | Magic number: 0x83 0x13 0x89 0x8D                     |
   +--------+--------+-------------------------------------------------------+
   | 4      | 1      | Data type:                                            |
   |        |        | - "A" : 8 bit signed integer (character)              |
   |        |        | - "I" : 16 bit signed integer                         |
   |        |        | - "J" : 32 bit signed integer                         |
   |        |        | - "E" : 32 bit float                                  |
   |        |        | - "D" : 64 bit float                                  |
   +--------+--------+-------------------------------------------------------+
   | 5      | 15     | Data column name. If the length of the name is less   |
   |        |        | than 15 characters, it will be padded with 0. If the  |
   |        |        | name is 15 characters, there will be no padding.      |
   +--------+--------+-------------------------------------------------------+
   | 20     | 4      | Number of Rows                                        |
   +--------+--------+-------------------------------------------------------+
   | 24     | 4      | Number of Columns, if 0 it is a vector                |
   +--------+--------+-------------------------------------------------------+
   | 28     | 4      | Reserved                                              |
   +--------+--------+-------------------------------------------------------+
   | 32     | N      | Data                                                  |
   +--------+--------+-------------------------------------------------------+

For example, the command::

    unix% marx OutputVectors="ETXYZP"

would run a marx simulation but only print out vectors containing the
energy, time, focal plane position, and detector pulse height for the
detected photons. 

These native binary vectors provide convenient access to the individual
properties of detected photons. For example, to create an ASCII file
containing only the times and pulse heights for a set of detected
photons, we can use::

    unix% marx --dump point/time.dat point/pha.dat > list.txt
    unix% more list.txt
    #            TIME             PHA
        3.199424e+00             241
        3.702556e+00             302
        3.722314e+00             256
        4.840378e+00             257
        5.336663e+00             284
        6.659723e+00             345
        7.989861e+00             255
        1.041432e+01             260
        1.131393e+01             279
        1.195770e+01             270
        1.259386e+01             332
        1.346374e+01             237
        1.532549e+01             322

In this example, the marx simulation directory was assumed to be named
point.



XRCF Shutter Control
~~~~~~~~~~~~~~~~~~~~

.. parameter:: Shutters1

.. parameter:: Shutters3 

.. parameter:: Shutters4 

.. parameter:: Shutters6 


HRMA Setup
~~~~~~~~~~
.. parameter:: FocalLength      

.. parameter:: HRMA_Use_WFold

.. parameter:: HRMA_Use_Blur

.. parameter:: HRMA_Use_Scale_Factors

.. parameter:: HRMA_Use_Struts

.. parameter:: HRMA_Ideal

.. parameter:: WFold_P1_File

.. parameter:: WFold_H1_File

.. parameter:: WFold_P3_File

.. parameter:: WFold_H3_File

.. parameter:: WFold_P4_File

.. parameter:: WFold_H4_File

.. parameter:: WFold_P6_File

.. parameter:: WFold_H6_File

.. parameter:: HRMAOptConst

.. parameter:: HRMAOptConstScale

.. parameter:: HRMAVig

.. parameter:: HRMA_Yaw

.. parameter:: HRMA_Pitch

.. parameter:: HRMA_Geometry_File

.. parameter:: P1Blur

.. parameter:: H1Blur

.. parameter:: P3Blur

.. parameter:: H3Blur

.. parameter:: P4Blur

.. parameter:: H4Blur

.. parameter:: P6Blur

.. parameter:: H6Blur

.. parameter:: H1ScatFactor

.. parameter:: P1ScatFactor

.. parameter:: H3ScatFactor

.. parameter:: P3ScatFactor

.. parameter:: H4ScatFactor

.. parameter:: P4ScatFactor

.. parameter:: H6ScatFactor

.. parameter:: P6ScatFactor

.. parameter:: HRMA_Cap_X

.. parameter:: HRMA_P1H1_XOffset

.. parameter:: HRMA_P3H3_XOffset

.. parameter:: HRMA_P4H4_XOffset

.. parameter:: HRMA_P6H6_XOffset

.. parameter:: PointingOffsetY

.. parameter:: PointingOffsetZ


Grating Setup and Control
~~~~~~~~~~~~~~~~~~~~~~~~~
Further parameters for the grating setup and control are discussed in detail in :ref:`Gratingefficiency` and
in :ref:`misalignments`.

.. parameter:: HEGRowlandDiameter

.. parameter:: MEGRowlandDiameter

.. parameter:: LEGRowlandDiameter

.. parameter:: GratingOptConsts

.. parameter:: Use_This_Order


HETG Efficiency Table Model Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. parameter:: HETG_Sector1_File

.. parameter:: HETG_Sector3_File

.. parameter:: HETG_Sector4_File

.. parameter:: HETG_Sector6_File

.. parameter:: HETG_Shell1_File

.. parameter:: HETG_Shell3_File

.. parameter:: HETG_Shell4_File

.. parameter:: HETG_Shell6_File

.. parameter:: HETG_Shell1_Vig

.. parameter:: HETG_Shell3_Vig

.. parameter:: HETG_Shell4_Vig

.. parameter:: HETG_Shell6_Vig

.. parameter:: HETG_Shell1_Theta

.. parameter:: HETG_Shell3_Theta

.. parameter:: HETG_Shell4_Theta

.. parameter:: HETG_Shell6_Theta

.. parameter:: HETG_Shell1_dTheta

.. parameter:: HETG_Shell3_dTheta

.. parameter:: HETG_Shell4_dTheta

.. parameter:: HETG_Shell6_dTheta

.. parameter:: HETG_Shell1_Period

.. parameter:: HETG_Shell3_Period

.. parameter:: HETG_Shell4_Period

.. parameter:: HETG_Shell6_Period

.. parameter:: HETG_Shell1_dPoverP

.. parameter:: HETG_Shell3_dPoverP

.. parameter:: HETG_Shell4_dPoverP

.. parameter:: HETG_Shell6_dPoverP


LETG Efficiency Table Model Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. parameter:: LETG_Eff_Scale_Factor

.. parameter:: LETG_Sector1_File

.. parameter:: LETG_Sector3_File

.. parameter:: LETG_Sector4_File

.. parameter:: LETG_Sector6_File

.. parameter:: LETG_Shell1_File

.. parameter:: LETG_Shell3_File

.. parameter:: LETG_Shell4_File

.. parameter:: LETG_Shell6_File

.. parameter:: LETG_Shell1_Vig

.. parameter:: LETG_Shell3_Vig

.. parameter:: LETG_Shell4_Vig

.. parameter:: LETG_Shell6_Vig

.. parameter:: LETG_Shell1_Theta

.. parameter:: LETG_Shell3_Theta

.. parameter:: LETG_Shell4_Theta

.. parameter:: LETG_Shell6_Theta

.. parameter:: LETG_Shell1_dTheta

.. parameter:: LETG_Shell3_dTheta

.. parameter:: LETG_Shell4_dTheta

.. parameter:: LETG_Shell6_dTheta

.. parameter:: LETG_Shell1_Period

.. parameter:: LETG_Shell3_Period

.. parameter:: LETG_Shell4_Period

.. parameter:: LETG_Shell6_Period

.. parameter:: LETG_Shell1_dPoverP

.. parameter:: LETG_Shell3_dPoverP

.. parameter:: LETG_Shell4_dPoverP

.. parameter:: LETG_Shell6_dPoverP


HEG Rectangular Grating Bar Model Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. parameter:: HEGVig                     

.. parameter:: hegGold

.. parameter:: hegChromium

.. parameter:: hegNickel

.. parameter:: hegPolyimide

.. parameter:: hegPeriod

.. parameter:: hegdPoverP

.. parameter:: hegBarHeight

.. parameter:: hegBarWidth

.. parameter:: hegNumOrders

.. parameter:: hegTheta

.. parameter:: hegdTheta


MEG Rectangular Grating Bar Model Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. parameter:: MEGVig                     

.. parameter:: megGold

.. parameter:: megChromium

.. parameter:: megNickel

.. parameter:: megPolyimide

.. parameter:: megPeriod

.. parameter:: megdPoverP

.. parameter:: megBarHeight

.. parameter:: megBarWidth

.. parameter:: megNumOrders

.. parameter:: megTheta

.. parameter:: megdTheta


LEG Rectangular Grating Bar Model Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. parameter:: DetExtendFlag

.. parameter:: LEGVig

.. parameter:: legGold

.. parameter:: legChromium

.. parameter:: legNickel

.. parameter:: legPolyimide

.. parameter:: legPeriod

.. parameter:: legdPoverP

.. parameter:: legBarHeight

.. parameter:: legBarWidth

.. parameter:: legTheta

.. parameter:: legdTheta

.. parameter:: legNumOrders

.. parameter:: legFineNumOrders

.. parameter:: legFinePeriod

.. parameter:: legFineBarWidth

.. parameter:: legFineBarHeight

.. parameter:: legCoarseNumOrders

.. parameter:: legCoarsePeriod

.. parameter:: legCoarseBarHeight

.. parameter:: legCoarseBarWidth


ACIS Model Parameters
~~~~~~~~~~~~~~~~~~~~~
.. parameter:: ACIS_Exposure_Time

.. parameter:: ACIS_Frame_Transfer_Time

.. parameter:: ACIS_Gain_Map_File
	     
   This parameter is currently not used; its value will be ignored.
	       
.. parameter:: ACIS_eV_Per_PI


ACIS-S Model Parameters
~~~~~~~~~~~~~~~~~~~~~~~

.. parameter:: ACIS-S0-QEFile

.. parameter:: ACIS-S0-FilterFile

.. parameter:: ACIS-S1-QEFile

.. parameter:: ACIS-S1-FilterFile

.. parameter:: ACIS-S2-QEFile

.. parameter:: ACIS-S2-FilterFile

.. parameter:: ACIS-S3-QEFile

.. parameter:: ACIS-S3-FilterFile

.. parameter:: ACIS-S4-QEFile

.. parameter:: ACIS-S4-FilterFile

.. parameter:: ACIS-S5-QEFile

.. parameter:: ACIS-S5-FilterFile



ACIS-I Model Parameters
~~~~~~~~~~~~~~~~~~~~~~~

.. parameter:: ACIS-I0-QEFile

.. parameter:: ACIS-I0-FilterFile

.. parameter:: ACIS-I1-QEFile

.. parameter:: ACIS-I1-FilterFile

.. parameter:: ACIS-I2-QEFile

.. parameter:: ACIS-I2-FilterFile

.. parameter:: ACIS-I3-QEFile

.. parameter:: ACIS-I3-FilterFile

.. _HRCIparameters:

HRC-I Model Parameters
~~~~~~~~~~~~~~~~~~~~~~

The blur parameters were extracted from
http://cxc.harvard.edu/twiki/bin/view/HrcCal/DetectorPSF .
The (Xctr,Yctr) are offset at runtime such that (G1Xctr,G1Yctr)=(0,0).

.. parameter:: HRC-I-BlurG1FWHM

.. parameter:: HRC-I-BlurG1Xctr

.. parameter:: HRC-I-BlurG1Yctr

.. parameter:: HRC-I-BlurG1Amp

.. parameter:: HRC-I-BlurG2FWHM

.. parameter:: HRC-I-BlurG2Xctr

.. parameter:: HRC-I-BlurG2Yctr

.. parameter:: HRC-I-BlurG2Amp

.. parameter:: HRC-I-BlurL1FWHM

.. parameter:: HRC-I-BlurL1Xctr

.. parameter:: HRC-I-BlurL1Yctr

.. parameter:: HRC-I-BlurL1Amp

.. parameter:: HRC-I-BlurL1Rmax

.. parameter:: HRC-I-QEFile

.. parameter:: HRC-I-UVISFile

.. _HRCSparameters:

HRC-S Model Parameters
~~~~~~~~~~~~~~~~~~~~~~

The blur parameters were extracted from
http://cxc.harvard.edu/twiki/bin/view/HrcCal/DetectorPSF .
The (Xctr,Yctr) are offset at runtime such that (G1Xctr,G1Yctr)=(0,0).

.. parameter:: HRC-S-BlurG1FWHM

.. parameter:: HRC-S-BlurG1Xctr

.. parameter:: HRC-S-BlurG1Yctr

.. parameter:: HRC-S-BlurG1Amp

.. parameter:: HRC-S-BlurG2FWHM

.. parameter:: HRC-S-BlurG2Xctr

.. parameter:: HRC-S-BlurG2Yctr

.. parameter:: HRC-S-BlurG2Amp

.. parameter:: HRC-S-BlurL1FWHM

.. parameter:: HRC-S-BlurL1Xctr

.. parameter:: HRC-S-BlurL1Amp

.. parameter:: HRC-S-BlurL1Yctr

.. parameter:: HRC-S-BlurL1Rmax

.. parameter:: HRC-S-QEFile0

.. parameter:: HRC-S-QEFile1

.. parameter:: HRC-S-QEFile2

.. parameter:: HRC-S-UVISFile0

.. parameter:: HRC-S-UVISFile1

.. parameter:: HRC-S-UVISFile2

.. parameter:: HRC-S-UVISFile3


HESF Model Parameters
~~~~~~~~~~~~~~~~~~~~~
.. parameter:: HESFOffsetX

.. parameter:: HESFOffsetZ

.. parameter:: HESFGapY1

.. parameter:: HESFGapY2

.. parameter:: HESFN

.. parameter:: HESFLength

.. parameter:: HESFCrWidth

.. parameter:: HESFOptConstCr

.. parameter:: HESFOptConstC

.. parameter:: HESFHeight1

.. parameter:: HESFTheta1

.. parameter:: HESFHeight2

.. parameter:: HESFTheta2

.. parameter:: HESFHeight3

.. parameter:: HESFTheta3

.. parameter:: HESFHeight4

.. parameter:: HESFTheta4

.. _sect-flatfieldparameters:

Flat Field Model Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. parameter:: FF_MinY

.. parameter:: FF_MaxY

.. parameter:: FF_MinZ

.. parameter:: FF_MaxZ

.. parameter:: FF_XPos


.. _sect-internalditherpars:

Dither/Aspect Parameters
~~~~~~~~~~~~~~~~~~~~~~~~
The most important parameters that control the dither model are described in
:ref:`simulatingaspect`. In the following we list parameters that control the internal
|marx| dither model, if selected by :par:`DitherModel`. All default values are chosen for ACIS
observations. See `Table 5.4 in the Observatory Guide <http://cxc.cfa.harvard.edu/proposer/POG/html/chap5.html#tb:dither>`_ for the values that are appropriate for HRC observations.
|marx| also offers the possiblity to dither the roll angle, but this is not done in normal Chandra
operations.
(Note that |marx| calls the directions "RA" and "Dec", while the linked table calls it "pitch" and "yaw". The difference is historic, the |marx| implementation correctly applies the values as pitch and yaw angle despite the name.)


.. parameter:: DitherAmp_RA

.. parameter:: DitherAmp_Dec

.. parameter:: DitherAmp_Roll

.. parameter:: DitherPeriod_RA

.. parameter:: DitherPeriod_Dec

.. parameter:: DitherPeriod_Roll

.. parameter:: DitherPhase_RA

.. parameter:: DitherPhase_Dec

.. parameter:: DitherPhase_Roll
