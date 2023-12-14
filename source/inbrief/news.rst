.. _highlights:

*************************************
Highlights for each version of |marx|
*************************************

Marx 5.5.3 (Dec 2023)
=====================
Version 5.5.3 is identical to the previous version 5.5.2 except to a small tweak in the installation scripts that help when compiling marx on Apple’s ARM chips. 


Marx 5.5.2 (Dec 2022)
=====================
This release just upgrades the `CalDB`_ files that are shipped with |marx|.
There are no code changes.


Marx 5.5.1 (Dec 2020)
=====================
This release just upgrades the `CalDB`_ files that are shipped with |marx|.
There are no code changes.

Marx 5.5 (Dec 2019)
===================

Update `CalDB`_ files that are shipped with |marx| to `CalDB`_ version 4.9.0.

Change column type of PHA and PI columns written by :marxtool:`marx2fits` to float32
to match the files that CIAO writes.

User-compiled sources (:par:`SourceType="USER"`) have a function called
``user_create_ray`` which is called with a pointer to ray properties
(direction, time, and energy). All ray properties used to be undefined before
calling this function and the user function could return ``-1`` for energy and
time to have |marx| assign energy and time. Now, ``energy`` is initialized
*before* ``user_create_ray`` is called, to allow user code that assigns
locations based on the ray energy.  With this change, marx.par must contain a
valid specification for the source spectrum, since an energy will be drawn,
even if the user source later assigns a different value. For
backwards-compatibility, if ``user_create_ray`` sets the energy to a negative
value, |marx| will assign the energy drawn before to the variable again.



Marx 5.4 (Dec 2018)
===================
Update `CalDB`_ files that are shipped with |marx| to `CalDB`_ version 4.8.2.

HRC PSF
-------
The HRC detector PSF has some blur in it. See
https://cxc.cfa.harvard.edu/twiki/bin/view/HrcCal/DetectorPSF for how the
parameters used in previous versions of |marx| are determined. However, we
recently found that the PSFs are wider than observed. Thus, in this version we
change the values of the default `marx.par` file to use a single Gaussian
instead. This change is most important for the profile of the wings in very
bright HRC sources.  We continue to investigate this and expect another change
in the next |marx| release.


Marx 5.3.3 (Dec 2017)
=====================
Small bug fix to the source code to allow compilation with clang
(which is the default compiler on Macs).

Marx 5.3.2 (Dec 2016)
=====================
Update `CalDB`_ files that are shipped with |marx|. No changes to the source
code.


Marx 5.3.1 (Aug 2016)
=====================
This fixes two bugs for users of SIMPUT sources; all other
runs are unaffected.


Marx 5.3 (Apr 2016)
===================

Important bug-fix for off-axis sources: Please upgrade!
-------------------------------------------------------
MARX 5.0, 5.1, and 5.2 contain a bug that affects the PSF for 
simulations of off-axis sources; this is fixed in 5.3.
The root cause for this bug was that the entrance aperture of the Chandra
mirrors was chosen to match the size of the mirror opening as seen an on-axis
source exactly. For an off-axis source that means that the generated photons
hit only part of the mirror, leading to gaps in the simulated PSF. Now, the
entrance aperture has been increased to allow sources anywhere in the
field-of-view to fill the detector. This necessarily increases the run time of
all |marx| simulations, because more photons need to be generated.
See https://github.com/Chandra-MARX/marx/issues/21 for a detailed
description of the issue.


New source type: SIMPUT
-----------------------
|marx| now supports the new `SIMPUT standard`_, which is a fits based
description of sources, which allows a large number of source with different
spectra, light curves, and shapes on the sky. This file format is supported by a
number of other simulators (e.g. for ATHENA), so integrating it in |marx|
allows users to use the same source specification for different X-ray missions.
The support in |marx| is through the `SIMPUT code`_ which needs to be installed
separately and is linked dynamically at runtime if :par:`SourceType="SIMPUT"`.

Marx 5.2 (Dec 2015)
===================

There are only minor enhancements, calibration updates, and bug fixes 
in this version.

Change in default parameters
----------------------------
Set the :par:`PointingOffsetY` and :par:`PointingOffsetZ` to 0 to match the
values in current Chandra observations (was ``-21`` and ``12`` before).
This defines the difference between RA/DEC_NOM and RA/DEC_PNT in the 
fits headers of event files; it is not used in the code except to output 
the RA/DEC_PNT values by :marxtool:`marx2fits`.

Bug Fixes
---------
- Match use of long and double types in fits output to standard CIAO products.
- Previously an ASOL file name > 63 characters would crash :marxtool:`marx2fits`.
  Now, it cuts the pathname to shorten the string.

Marx 5.1 (Apr 2015)
===================

|marx| version 5.1 is a maintenance release. Since more than
two years have gone by since release 5.0, there are major changes in the
Chandra calibration data that |marx| uses, particularly in the soft energy
response of ACIS. In addition there are several minor changes, some of which are
listed below (see the commit log of the `git repository
<https://github.com/Chandra-MARX/marx>`_ for complete details):

- |marx| now compiles with ``clang``, the compiler that is shipped with Max OS X-code.
  (Apple sets an alias called ``gcc``, but this really points to ``clang``.)
- Enhanced support for dithered `SAOTrace`_ rays on input. In particular, that
  means that the parameter :par:`SAOSAC_Color_Rays` is no longer
  needed. Setting it currently has no effect and this parameter will be removed
  in the next version.
- :marxtool:`marx2fits` writes more header keywords in the output fits files,
  which enables more `CIAO`_ tools to work with those files.
- The HRC blur model has been improved. Simulations with HRC-I and HRC-S will
  give slightly different PSF shapes. In order to describe the HRC blur
  properly, new parameters have been added to ``marx.par``. These parameters
  should not be changed by the user; instead we strongly recommend to just copy
  and modify the version of ``marx.par`` that comes with the installation
  which includes those new parameters.
- |marx| now includes the LEG misalignment compared to the ACIS chips. Handling
  this required changes to the default values of the :par:`hegTheta`,
  :par:`megTheta`, and :par:`legTheta`. These parameters
  should not be changed by the user; instead we strongly recommend to just copy
  and modify the version of ``marx.par`` that comes with the installation
  which includes those updated values.

Marx 5.0
========
|marx| 5.0 is a major new release.  This page is devoted to the new
features.


Subpixel Randomization
----------------------
The EDSER subpixel algorithm was incorporated into CIAO 4.3.  When
computing Sky coordinates, :ciao:`acis_process_events` first converts the
integer-valued chip coordinate to a floating point value.  There are
several ways in which this may be done.  One way is to simply cast the
integer to a float, e.g,, the integer 2 becomes 2.0.  The problem with
this approach is that it can cause aliasing artifacts in the resulting
Sky image.  For this reason, the default up until CIAO 4.3 was to
simply add a uniform random deviate from -0.5 to 0.5 to the integer
value so that 2 would become a random real number in the semi-open
interval [1.5, 2.5).  The default was changed in CIAO 4.3 to use a
discrete probability distribution based upon flight grade and energy, known as
the EDSER method.

The |marx| 5 version of :marxtool:`marx2fits` introduces a ``--pixadj`` command
line parameter that allows the user to select one of several pixel
randomization methods.  Simply running :marxtool:`marx2fits` without any command
line arguments will display its usage message::

    marx2fits v5.0.0:
    Usage: marx2fits [options] marxdir outfile
    Options:
      --pileup             Process a marxpileup simulation
      --pixadj=EDSER       Use a subpixel algorithm (default)
      --pixadj=RANDOMIZE   Randomize within a detector pixel
      --pixadj=NONE        Do not randomize within a detector pixel
      --pixadj=EXACT       Use exact chip coordinates

The effect of these randomization methods may be seen in the following
plot, which shows that the EDSER distribution approaches the
exact limit.

.. figure:: marxsubpix.*
   :alt: Image of PSF with different pixadj values
   :align: center

   Image of PSF with different pixadj values


If using `SAOTrace`_ rays with |marx|, see :ref:`caveats` regarding the use of
the EDSER method with such rays. **Note: Caveat removed in 2015. SAOTrace now
supports dither.**

New dither model
----------------
The EDSER subpixel algorithm necessitated numerous changes to the
\marx aspect code.  In particular, aspect reconstruction blur
had to be cleanly separated into its independently contributing
pieces, namely the telescope pointing uncertainty, the blur introduced
by pixel quantization/truncation, and the blur associated with pixel
randomization.  Previous versions of |marx| incorporated these blurs
under the guise of a single parameter, :par:`DitherBlur`, whose value
was the RSS sum of the contributing blurs.  This was the source of a
lot of confusion among users resulting in numerous help desk inquiries
about how this value was obtained and why it was so large.
For these reasons, the :par:`DitherBlur` parameter was removed from |marx|
and replaced by one called :par:`AspectBlur` whose value represents
just the telescope pointing uncertainty,
`0.07 arc-seconds <http://cxc.harvard.edu/cal/ASPECT/img_recon/report.html>`_.  One consequence of this change is that |marx| 4.x
parameter files cannot be used with marx 5.0.

It was also necessary to remove the blur parameters from :marxtool:`marxasp`,
which computes an aspect solution file for use in reprocessing a
:marxtool:`marx2fits` generated event file.  Hence any scripts that pass blur
parameter values to :marxtool:`marxasp` will need to be modified.

Calibration Updates
-------------------
As mentioned above, the :par:`DitherBlur` parameter's value reflected
more that just that associated with the aspect uncertainty.  It was
also tweaked to get the marx PSF to better match Chandra grating line
profiles.  With this parameter gone, the |marx| HRMA blur parameters
had to be re-calibrated to get the widths of the |marx| simulated
grating line profiles to match those in the Chandra CALDB.

There was a long standing issue of a relative rotation between the
LETG and the ACIS detector.  The root of this problem was tracked down
(with the help of |marx|) to a rotation offset between the aspect
coordinate system and the focal plane detector system.  This offset
was masked by compensating rotations of the detectors from astrometric
analysis, and manifested itself as a small rotation of the LEG
dispersion arm on the ACIS detector.  Changes were added to CIAO 4.3
that effectively adds an additional rotation to the LETG when used
with ACIS.  The corresponding change in |marx| 5.0 is implemented via a
new parameter called :par:`LETG_ACIS_dTheta`.

The |marx| calibration data have been brought up to date with the
Chandra CALDB 4.4.7.

Marx Parameter File Updates
---------------------------
The parameter files for earlier versions of marx (e.g., the marx.par
file for version 4.5) cannot be used with marx 5.0.  The recalibrations
that were necessary for subpixel support resulted in changes to all of
the HRMA blur parameters, as well as the introduction of the new
:par:`AspectBlur` parameter discussed above.

The following marx.par parameter values have changed since marx 4.5::

 P1Blur: 0.18129215 --> 0.303427
 H1Blur: 0.13995037 --> 0.0051428
 P3Blur: 0.11527828 --> 0.0951899
 H3Blur: 0.16360829 --> 0.0713614
 P4Blur: 0.1289134 --> 0.178899
 H4Blur: 0.098093014 --> 0.0101367
 P6Blur: 0.076202759 --> 0.151085
 H6Blur: 0.079767401 --> 0.0239287
 MEGRowlandDiameter: 8632.65 --> 8632.48
 HEGRowlandDiameter: 8632.65 --> 8632.48
 HETG_Shell1_Period: 0.400141 --> 0.400195
 HETG_Shell3_Period: 0.400141 --> 0.400195
 LETG_Shell1_Theta: -0.07 --> 0.07
 LETG_Shell3_Theta: -0.07 --> 0.07
 LETG_Shell4_Theta: -0.07 --> 0.07
 LETG_Shell6_Theta: -0.07 --> 0.07
 legCoarseNumOrders: 11 --> 121

The following parameters have been removed::

   DitherBlur

The following parameters have been added::

 AspectBlur: 0.07
 LETG_ACIS_dTheta: -0.0867
 Use_This_Order: 0
 DetExtendFlag: no

The latter two parameters were added for the purposes of calibration.

MARX 4.0
========

MARX 4.0 represents a major upgrade since the previous release.
Where possible, MARX now uses CIAO CALDB data files directly for
detector responses and quantum efficiencies thus providing the ability
to transparently analyze simulations using standard CIAO tools. In
addition to calibration changes, a number of improvements and
enhancements to MARX’s functionality have been made. These include:

-  Simplified source position specification

-  Direct CALDB interface for calibration information

-  Direct use of FEF files for ACIS spectral response

-  New ACIS photon pileup tool

-  Enhancements to support processing CHART rayfiles

-  Improved compatibility with CIAO data analysis tools

-  Miscellaneous bug fixes

As with previous updates, most of these changes should be completely
transparent to the returning user.

