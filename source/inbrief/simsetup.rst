.. _sect-runningmarx:

--------------------------
Running |marx| simulations
--------------------------

The |marx| Parameter File
=========================

The details of a given simulation are controlled by the |marx| parameter
file ``marx.par``.  This file currently contains about 270 different
parameters which determine everything from the exposure time to the
level of scattering off the HRMA surface.
Fortunately, only about 30 of these parameters need ever be (or in fact
should ever be) modified under most conceivable circumstances.
In practice, most typical science simulations can be defined and
controlled with less than 10.
Template |marx| parameter files are included as part of the distribution
and can be found in the top level of the source directory.
The tool :marxtool:`plist` can be used to print the contents
of ``marx.par`` in a more readable format while :marxtool:`pset` can
be used to set the values of specific parameters.

|marx| utilizes an PROS/IRAF--style parameter interface.  By default, |marx|
will search for ``marx.par`` in the directories specified by the
:envvar:`PFILES` and :envvar:`UPARM` environment variables. The first version of
``marx.par`` found will be used. If a valid parameter file is not
found in either of these locations, the current directory will be
searched. The tool :marxtool:`pwhich` can be used to check the current
parameter file search path.

|marx| will also assume that the relevant parameter file is named
``marx.par``.  An alternative parameter file may be specified by
prefixing the file name with ``@@`` and using the resulting expression
as argument on the command line, e.g.,
::

    unix% marx  @@/home/user/simulations/marx_cluster.par

The path to the desired parameter file need not be absolute.

Any |marx| parameters may be set on the command line via the syntax::

    unix% marx PARAMETER-NAME=VALUE PARAMETER-NAME=VALUE ...

The program will prompt for a parameter's value if VALUE is not
specified, e.g.,
::

    unix% marx DetectorType=
    Reading HRMA optical constants:
            /usr/local/src/marx_5.1.0-dist/marx/data/iridium.dat
    Range error occurred while looking at parameter DetectorType.
    Select detector type (HRC-S|ACIS-S|HRC-I|ACIS-I|NONE)[]:

Note that there must be **no** whitespace surrounding the ``=`` sign
and |marx| parameters are case sensitive.
In the next few sections, we will discuss the various essential
parameters the user must adjust to produce a |marx| simulation.

Simulation Control
==================

By "simulation control", we specifically refer to any necessary
parameter choices which define the execution of the simulation and
are not instrument or source related. These include such things
as length of exposure, timed versus ray generation execution,
and output location and format.

.. parameter:: RandomSeed

   |marx| is a Monte-Carlo simulation program, where all parameters (e.g. the
    energy or position of a photon, the scattering of a mirror or the
    diffraction in a grating) are drawn from a distribution of possible
    outcomes by means of a random number. This means that two |marx| simulations with the same input
    parameters will give different results, unless they use the same sequence of
    random numbers. Set this parameter to a positive number to
    obtain the same sequence of random numbers. The default is ``-1``, which
    sets the starting number of the random number generator to the current time
    when the simulation is run.


Exposure Time
-------------

|marx| simulations can be run either in *ray generation mode* or in
*timed exposure mode*. Timed exposure mode is probably the simulation
method most users will employ most of the time. 

.. parameter:: ExposureTime

   This parameter is used to specify the total integration time in seconds.

       unix% marx ExposureTime=10000 ...

   would generate a 10 ksec simulation. |marx| will accumulate photons
   until the indicated integration time is reached.
   **This mode takes precedence over ray generation mode.
   If ``ExposureTime`` parameter is set to any positive,
   non-zero value, the simulation will be run in timed exposure mode.**
   Users wishing to run simulations in ray generation mode, should set
   ``ExposureTime=0``.

.. parameter:: NumRays

   This parameter sets the exact number of rays to run through the simulator
   in *ray generation mode*. Note, that this value is *not* the
   number of detected rays which will be produced (some rays maybe absorbed or
   scattered outside of the detector). This parameter
   specifies the number of input rays. 

.. parameter:: TStart

   The sets the year of the observation, e.g. ``2014.5`` would be the first of
   July 2014. Some of the calibration files contain a time dependence, e.g. the
   ACIS detector contamination increases with time. Set this parameter to the
   time of the observation to reproduce a specific dataset or to the current
   year for proposal planning.

Output Directory
----------------
Depending on the particular instrument configuration chosen,
|marx| will produce different sets of binary output data files. 
By default all available information is saved.
:par:`OutputVectors` can modify this, but we recommend not to change this.

In addition to the binary vectors containing the detected event
properties, |marx| also creates an ``obs.par`` file in the output
directory. The file contains header information about the simulation
which :marxtool:`marx2fits` uses in the creation of the FITS Level 1 event
file. This file should *not* be modified.


.. parameter:: OutputDir

   (*default*: ``point``)
   This parameter specifies the directory where |marx| output is written.
   If the directory specified does not exist, |marx| will create it.
   Alternatively, if the specified directory does exist, its
   contents will be overwritten. In addition to the output photon
   vectors, |marx| also copies the current version of the ``marx.par``
   parameter file to the output directory.
   Note, if the value of ``OutputDir`` corresponds to the current
   directory and the ``marx.par`` controlling the simulation resides
   in this directory, |marx| will abort with an error message.
   Output from a |marx| run can be directed to the current directory,
   but only if the ``marx.par`` file is in another location.
   This behavior prevents corruption of the ``marx.par`` file.


Instrument Configuration
========================

These parameters control the science instruments which are
to be used in the simulation as well as which of |marx| mirror models to use.

.. parameter:: MirrorType

   (*default*: ``HRMA``)
   This parameter can be one of three values: ``HRMA``, ``EA-MIRROR``, or ``FLATFIELD``.
   The ``HRMA`` model is a full raytrace using an accurate physical model of the
   HRMA's parabolic and hyperbolic components. Mode details can be found in
   :ref:`sect-HRMA`. ``EA-MIRROR`` model is a simpler
   model based on a thin--lens approximation and using tabulated
   effective area and point spread function data. This simple model is of historical interest only
   and is no longer accurate or supported. This option should *not*
   be selected. 

   If ``MirrorType=FLATFIELD``, |marx| will propagate rays to a specified
   rectangular region in the focal plane parallel to the optical axis.
   No HRMA vignetting or scattering is applied.
   The size of the rectangular region which is illuminated is controlled
   by the parameters listed in :ref:`sect-flatfieldparameters`.
   Although useful for simulating detector instrumental backgrounds
   as well as debugging focal plane geometries, simulations
   created with the ``FLATFIELD`` model can *not* be combined
   with standard |marx| simulations employing the default
   ``MirrorType=HRMA`` option.


.. parameter:: GratingType

   One of three options: ``HETG``, ``LETG``, or ``NONE``.
   Chandra carries two sets of diffraction gratings: the Low Energy
   Transmission Grating (LETG) and the High Energy Transmission Grating
   (HETG) (see :ref:`grating-modules` for a full description).
   The performance of either instrument can be simulated
   using this parameter.
   Imaging observations can be simulated by setting
   ``GratingType=NONE``.

   The grating efficiency models in |marx| currently rely on
   a set of efficiency tables provided by the HETG and LETG IPI teams.
   These tables include grating efficiencies for orders -11 to 11
   for the HETG and for the LETG, orders from -25 to 25.

   An additional parameter has been added to allow the user to
   disable the grating efficiency calculation.
   If the parameter :par:`Use_Unit_Efficiencies=yes`, rays which
   intersect the HETG or LETG will still be diffracted but no
   efficiency filter will be applied. Hence all orders will have
   an equal probability of being populated.

Focal plane detectors
---------------------

.. parameter:: DetectorType

   The user has the choice of all four Chandra focal plane
   detectors including the ``ACIS-I``, ``ACIS-S``, ``HRC-I`` and ``HRC-S``, 
   see :ref:`sect-detectormodel`.
   ``DetectorType`` can also be set to ``NONE``. In this case,
   |marx| does not project the rays to the focal plane but stops at
   the last simulated element, either the HRMA or the gratings
   if included. This option is useful for producing rayfiles which
   can be run through |marx| again e.g. using different detectors.

   .. figure:: ../Reference/chipmap.*
      :height: 250 px       
      :align: center
      :name: Chip map

      Layout of Chandra flight focal plane detectors.
      The chips are numbered with their standard Chandra identifications.
      Note, the ACIS-I nominal aimpoint falls on chip 3 while the aimpoint
      for the ACIS-S array corresponds to chip 7. For the HRC-S, the
      nominal aimpoint is near the center of MCP 1. The sizes of the MCPs
      and CCDs are drawn roughly to scale, the detector separations and chip gaps are not.

   |marx| automatically places the SIM in the appropriate position
   such that the center of the source coincides with the
   default aimpoint for the selected detector.
   For actual Chandra observations using ACIS, any combination of 6 CCDs
   may be used at one time. However, at present |marx| simulations with ACIS
   only include those CCDs which comprise the selected imager
   (i.e. chips 0-3 for ACIS-I and chips 4-9 for ACIS-S).


.. parameter:: HRC-HESF

   If the HRC--S detector is selected, users have the
   option of including a model of the High Energy Suppression
   Filter (HESF) (a.k.a. The Drake Flat).
   Setting the parameter ``HRC-HESF="yes"`` includes the HESF;
   however, as we note below, the :par:`DetOffsetZ` parameter must also
   be modified to move the HESF into the beam.


.. parameter:: DetIdeal

   (*default*: ``no``)
   The quantum efficiency of the specified detector can
   be suppressed using the ``DetIdeal`` parameter. If ``DetIdeal="yes"``,
   the focal plane geometry of the selected detector is preserved, but
   the efficiency is assumed to be unity.


Focal Plane Position
--------------------

The focal plane science instruments on Chandra are mounted on a
movable platform called the Science Instrument Module (SIM)
that allows the different detectors to be selected. Movement
along the optical axis is also possible to adjust the focus.
|marx| simulates the SIM movement with three parameters:

.. parameter:: DetOffsetX

   (*default*: 0) Offset in mm from the nominal on-axis, in-focus SIM position.

   In the |marx| coordinate system (which is the same as the
   Chandra coordinate system), the X axis corresponds to the
   optical axis (see :ref:`sect-coordsystem`).
   Therefore, the ``DetOffsetX`` parameter
   can be used to simulate defocused Chandra observations.
   The maximum X motion of the SIM is -9 mm and +10 mm.
   Movements greater than :math:`\sim 2` mm from the best focus position
   produce ring--like images for point sources.
   This functionality is useful for studying photon pileup
   in the ACIS CCDs. Defocusing is one possible
   means of minimizing this effect for a given observation.

.. parameter:: DetOffsetZ

   (*default*: 0) Offset in mm from the nominal on-axis, in-focus SIM position.

   This parameter can be used to translate
   the SIM in the direction perpendicular to the grating
   dispersion. If the HESF (a.k.a. Drake Flat) is to be used, the
   ``DetOffsetZ`` parameter should be set to a value of 7.25 mm.
   To use the LESF, a value of ``DetOffsetZ=-6.5`` should be used.


Source Definition
=================

Specifying sources in |marx| is equivalent to choosing a position on
the sky, a spectral energy distribution, and a spatial distribution
for the incoming photons. For the latter two source characteristics,
a number of simple options are built into |marx|.

Source Position
---------------

.. parameter:: SourceRA

   (*default*: 40)
   RA of source in the sky in decimal degrees. 
   Corresponds on the ``RA_TARG`` FITS header keyword in a standard
   Chandra Level 2 events file.

.. parameter:: SourceDEC

   (*default*: 60)
   RA of source in the sky in decimal degrees. 
   Corresponds on the ``DEC_TARG`` FITS header keyword in a standard
   Chandra Level 2 events file.

.. parameter:: RA_Nom

   (*default*: 40)
   RA of nominal aimpoint in the sky in decimal degrees. 
   Corresponds on the ``RA_NOM`` FITS header keyword in a standard
   Chandra Level 2 events file.

.. parameter:: Dec_Nom

   (*default*: 60)
   RA of nominal aimpoint in the sky in decimal degrees. 
   Corresponds on the ``DEC_NOM`` FITS header keyword in a standard
   Chandra Level 2 events file.

.. parameter:: Roll_Nom

   (*default*: 45)
   Roll angle in the sky in decimal degrees. 
   Corresponds on the ``ROLL_NOM`` FITS header keyword in a standard
   Chandra Level 2 events file.

If the values of :par:`SourceRA` and :par:`SourceDEC` are different
from :par:`RA_Nom` and :par:`Dec_Nom`, the source will be off-axis.


Source Spectrum and Spatial Distribution
----------------------------------------
This is described in more details in :ref:`sect-sourcemodels`. Here, we
summarize the most important points.

Users have two options for specifying the spectral energy distribution
of source photons: a built-in FLAT spectrum model
which produces uniform flux over the specified energy range, or
a FILE mode which reads the spectrum from an external ASCII file.
The :par:`SpectrumType` parameter selects between these two options.
If the FLAT spectrum is selected, the :par:`SourceFlux` parameter
is used to determine the overall normalization of the spectrum in
photons/sec/cm^2.
The :par:`MinEnergy` and :par:`MaxEnergy` energy parameters determine
the energy range in keV over which photons will be generated for the
FLAT spectral model. Both parameters may be set to the same value
to generate a monochromatic source.

If the FILE mode is selected, the user must specify the name
of an input ASCII file containing the spectral energy distribution
using the :par:`SpectrumFile` parameter.
The input ASCII file should contain two columns separated by at
least one space where the first column gives the energy grid
in keV and the second column gives the flux density at that energy
in units of photons/sec/cm^2/keV.
No limits are placed on the number of points in the input file
and the file is assumed to be ordered by increasing energy.
|marx| checks for this criterion by calculating and reporting the
integrated flux from the specified file. :marxtool:`xspec2marx` is a script
installed with |marx| to convert `XSPEC`_ output to the right format.

In FILE mode, the :par:`SourceFlux` parameter can be used
to set the overall normalization of the input spectral energy
distribution. Setting :par:`SourceFlux` to a positive, non-zero
value will cause |marx| to renormalize the spectrum read from
the ASCII file to the specified total flux.
If :par:`SourceFlux=-1` (or any number less than 0), |marx|
will use the normalization inherent in the input spectrum.
In this manner, several sources with a consistent spectral shape
but varying total flux can be simulated using a single input spectrum
file.

The spatial distribution of source photons in |marx| is determined
by the choice of the :par:`SourceType` parameter.

The following sources are currently available:

- ``POINT``: Point Source
- ``GAUSS``: Radially symmetric Gaussian
- ``BETA``: Cluster Beta model
- ``DISK``: Disk or annulus (e.g. SN remnant)
- ``LINE``: Straight line
- ``IMAGE``: Input from a FITS image file
- ``SAOSAC``: Input from an SAOSAC FITS rayfile
- ``RAYFILE``: Input from a |marx| rayfile
- ``USER``: Dynamically linked user–supplied model

The ``IMAGE``, ``SAOSAC`, and ``RAYFILE`` source options
all take an additional parameter specifying the name of the
external file to use. With the exception of the ``SAOSAC`` and ``RAYFILE``
options, all |marx| source models obey the :par:`SourceRA`
and :par:`SourceDEC` parameters.
For non-point source models, the center of the source will be placed
at the coordinates specified by the (:par:`SourceRA`, :par:`SourceDEC`)
parameters. In the case of the ``IMAGE`` source type, the center
of the image will be located at the specified position.

The ``USER`` source model requires two additional parameters.
:par:`UserSourceFile` specifies the path to the dynamically linked
source file and should be the full, absolute pathname due to
peculiarities in the manner in which the dynamic linker locates
modules. The value of the parameter :par:`UserSourceArgs` will depend
on the specifics of the user model being linked.

All source models are described in detail in :ref:`sect-sourcemodels`.

Aspect Dither Motion
--------------------

Once the source characteristics and science instrument configuration
have been specified, the only remaining option the user must choose
is whether or not to include a simulation of the Chandra aspect
motion. |marx| includes an internal simulation of the standard lissajous
dither pattern which Chandra traverses over the course of an observation.

If :par:`DitherModel=INTERNAL`, |marx| will apply an internal simulation
of the Chandra aspect dither pattern.  This motion will result in
a blurring of the source image when viewed in focal plane
coordinates.
If a dither model is applied to the simulation, |marx| calculates
aspect-corrected sky coordinates. These values are ultimately to the FITS events file
by :marxtool:`marx2fits` is used.

For actual Chandra data sets, residual errors in the aspect correction
pipeline will introduce uncertainties into the derived Sky X and
Y coordinates. |marx| includes a simulation of these uncertainties
through the :par:`AspectBlur` parameter.  Other errors affecting the
derived Sky coordinates include the detector pixelization blur
(associated with the non-zero size of the pixel, also known as
truncation blur), and the pixel randomization blur (induced from
conversion of an integer pixel coordinate to a real-valued one).  The
user has some control over the form of the randomization blur via the
:marxtool:`marx2fits` ``--pixadj`` option.

Figure :ref:`dither <fig-ditherexp>` shows an example of a simulated
ACIS-I observation of a cluster of galaxies with and without
aspect motion included.

.. _fig-ditherexp:

.. figure:: dither_exp.*
   :alt: Example of ACIS-I simulation with and without dither
   :align: center

   Simulation showing the effects of the internal dither model in |marx|.
   The panel on the left shows a simulated ACIS-I observation of
   a cluster of galaxies with no dither included in Sky coordinates.
   The right panel shows the same simulation
   with |marx|'s INTERNAL dither model turned on.
   Note how the aspect motion has blurred the ACIS chip gaps
   but *not* the cluster image since aspect correction has been
   applied to the Sky coordinates displayed here.


The functional form of the motion model is described in
:ref:`simulatingaspect`.
In general, the form of the dither model has been adjusted to
correspond to the current parameters used for ACIS observations.
HRC observations with dither can be simulated by adjusting the
:par:`DitherAmp_RA` and :par:`DitherAmp_Dec` parameters from
8 arcsec to 20 arcsec.

Finally, if :par:`DitherModel=FILE`, |marx| will use the contents on
an aspect solution file (ASPSOL) to specify the dither motion pattern.
The name of the ASPSOL file to use is specified by the :par:`DitherFile`
parameter. ASPSOL files can be produced by
the CXCDS aspect pipeline or :marxtool:`marxasp`.
The FILE mode can be useful for generating |marx| simulations
which use the same aspect dither motion as an existing Chandra
dataset or a previous simulation.
The time interval covered by the ASPSOL file must equal or exceed the
requested exposure time of the simulation. If the end of the ASPSOL
file is reached before the requested exposure time, |marx| will truncate
the simulation at that point.

Running the Simulation
======================

Once your system has been configured appropriately and any desired
modifications have been made to the ``marx.par`` parameter file,
the simulation is ready to run.
If the parameters in the ``marx.par`` file are already set
appropriately, the simulation can be launched simply by typing
``marx`` at the shell prompt.
|marx| will print out a number of diagnostic messages as the simulation
proceeds indicating which configuration is being used as well as
which data files were accessed. Output from an example
using the ACIS-I with dither enabled is shown here::

    unix% marx
    MARX version 4.0.8, Copyright (C) 2002 Massachusetts Institute of Technology
   
    	/usr/local/src/marx_4.0.8-dist/marx/data/hrma/EKCHDOS06.rdb
    Reading binary HRMA optical constants:
	/usr/local/src/marx_4.0.8-dist/marx/data/hrma/iridium.dat
	/usr/local/src/marx_4.0.8-dist/marx/data/hrma/corr_1.dat
	/usr/local/src/marx_4.0.8-dist/marx/data/hrma/corr_3.dat
	/usr/local/src/marx_4.0.8-dist/marx/data/hrma/corr_4.dat
	/usr/local/src/marx_4.0.8-dist/marx/data/hrma/corr_6.dat
    Reading scattering tables
	/usr/local/src/marx_4.0.8-dist/marx/data/hrma/scat_p1_M.bin
	/usr/local/src/marx_4.0.8-dist/marx/data/hrma/scat_h1_M.bin
	/usr/local/src/marx_4.0.8-dist/marx/data/hrma/scat_p3_M.bin
	/usr/local/src/marx_4.0.8-dist/marx/data/hrma/scat_h3_M.bin
	/usr/local/src/marx_4.0.8-dist/marx/data/hrma/scat_p4_M.bin
	/usr/local/src/marx_4.0.8-dist/marx/data/hrma/scat_h4_M.bin
	/usr/local/src/marx_4.0.8-dist/marx/data/hrma/scat_p6_M.bin
	/usr/local/src/marx_4.0.8-dist/marx/data/hrma/scat_h6_M.bin
    Initializing ACIS-I detector...
    Reading ACIS-I/S FEF File
    	/usr/local/src/marx_4.0.8-dist/marx/data/caldb/acisfef.fits
    Reading ACIS-I QE/Filter Files
	/usr/local/src/marx_4.0.8-dist/marx/data/caldb/acisD1997-04-17qeN0004.fits for [CCDID = 0]
	/usr/local/src/marx_4.0.8-dist/marx/data/caldb/acisD1997-04-17qeN0004.fits for [CCDID = 1]
	/usr/local/src/marx_4.0.8-dist/marx/data/caldb/acisD1997-04-17qeN0004.fits for [CCDID = 2]
	/usr/local/src/marx_4.0.8-dist/marx/data/caldb/acisD1997-04-17qeN0004.fits for [CCDID = 3]
    [Using INTERNAL dither model]
    Initializing source type POINT...
    System initialized.

    Starting simulation.  Exposure Time set to 3.000000e+04 seconds
    Collecting 100000 photons...
	67631 collected.
    Reflecting from HRMA
    Detecting with ACIS-I

    Writing output to directory 'point' ...
    Total photons: 67631, Total Photons detected: 18060, (efficiency: 0.267037)
       (efficiency this iteration  0.267037)  Total time: 30000.079736

Once the initialization is complete, |marx| will begin processing
groups of rays. Again, diagnostic messages will be generated which track
the simulation's progress, i.e. ``Collecting...``, ``Reflecting...``, etc.
A short synopsis will also be printed at the end of each group of rays
indicating the number of rays processed, the number actually
"detected", the efficiency for this iteration, and the total
integration time incurred so far.
When the number of rays specified have been processed or the indicated
integration time has been reached, the simulation will terminate.

.. parameter:: Verbose

   (*default*: ``yes``)
   The diagnostic messages can be quieted by setting the parameter
   ``Verbose="no"``.

|marx| Native Binary Output Files
=================================

Depending on the values of the :par:`OutputDir` and :par:`OutputVectors`
parameters, |marx| will by default create a directory containing a number
of binary output files. Usually, a user will not use these files directly, but
convert them to fits files using :marxtool:`marx2fits` (see below). 
The native binary format is discussed in more detail in the description of the
parameter :par:`Outputvectors`.

These native binary vectors provide convenient access to the individual
properties of detected photons. For example, to create an ASCII file
containing only the times and pulse heights for a set of detected photons,
we can use::

    unix% marx --dump point/time.dat point/pha.dat > list.txt
    unix% more list.txt
    #            TIME             PHA
        3.199424e+00             241
        3.702556e+00             302
        3.722314e+00             256
	4.840378e+00             257
	5.336663e+00             284

In this example, the |marx| simulation directory was assumed
to be named "point". Alternatively, for IDL users, the routine
:marxtool:`read_marx_file` can be used to read these binary output vectors
into internal IDL variables.
These direct means of accessing the properties of detected photons
can be much more efficient than reading individual columns from
the equivalent FITS events file, especially for large simulations.


FITS Events Files
=================

The contents of a |marx| simulation output directory may be recast
in a standard CXC Level 1 FITS events file using the :marxtool:`marx2fits`
tool.
Events files created in this way contain the standard "detected"
event quantities such as pixel position, pulse height, time, etc.
In addition, columns are created in the FITS binary events table
for the various "simulation" variables (true photon energy,
dispersed order, mirror reflection shell, etc.).
|marx| event files can be used transparently
with the `CIAO`_ extraction tools as well as XSELECT in the
`FTOOLS <http://heasarc.gsfc.nasa.gov/docs/software/ftools>`_
software suite available from
`HEASARC <http://heasarc.gsfc.nasa.gov>`_.

Combining multiple |marx| Simulations
=====================================

Complex |marx| simulations can be built using the :marxtool:`marxcat` tool.
This tool concatenates the results of multiple |marx| runs and
takes as input a list of simulation output directories.
As output, it creates a new directory containing the merged
binary output vectors from the specified component directories.
The resulting merged output vectors will be ordered by photon
arrival time. :marxtool:`marx2fits` can of course still be used to convert
concatenated simulations into event files.

The :marxtool:`marxcat` tool works by merging the various binary output
vectors contained in the indicated |marx| output directories. It is the
user's responsibility to ensure that the simulations being
concatenated are commensurate.
For example, combining simulations with differing pointing
positions (as defined by :par:`RA_Nom` and :par:`Dec_Nom`)
will produce erroneous results. :marxtool:`marxcat` will compare the contents
of the directories being merged and skip any files which do not
have counterparts in all the directories.
