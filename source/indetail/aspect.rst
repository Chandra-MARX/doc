.. _simulatingaspect:

Simulating Aspect with |marx|
-----------------------------


    Motion or change, and identity or rest, are the first and second
    secrets of nature.

       -- Ralph Waldo Emerson

Introduction
^^^^^^^^^^^^

In the course of a normal science observation, the Chandra line-of-sight
pointing position on the sky moves. This “dither” motion serves several
purposes including sub-sampling of the point spread function as well as
averaging over uncertainties in quantum efficiency from detector element
to element. In the case of the HRC MCPs, it also evenly distributes the
dosage received over many microchannel pores extending the life of the
detector. Typically this dither motion will follow a Lissajous pattern
over an area up to 20 arcsec in size and is referred to as Normal Point
Mode (NPM) (http://cxc.harvard.edu/proposer/POG/html/chap5.html). The Chandra
Aspect camera system provides pointing information over the course of
this dither motion and, when processed through the CXCDS Aspect
pipeline, allows the effects of dither to be removed from the final
image. |marx| provides the capability to include the effects of
dither motion in Chandra simulations.

The net result of dither motion is that the image of a given source will
move in the Chandra focal plane as a function of time. When all photons
from the observation are combined, the resulting image will be blurred
in the Focal Plane (FP) coordinate systems. These system corresponds to
the CHIP, DET, or TDET columns in the FITS events file. The CXCDS Level
1 pipeline corrects for this blurring and produces “aspect–corrected”
Sky pixel coordinates. These coordinates appear in the FITS events file
as the X and Y columns. |marx| computes a simple approximation to
the Level 1 pipeline aspect correction. For a more detailed discussion
of these coordinate systems, the user is referred to 
http://cxc.harvard.edu/contrib/jcm/ncoords.ps.

If dither is selected for the simulation, images created from the CHIP,
DET, or TDET pixel positions will reflect the motion of the Chandra
line-of-sight. |marx| also emulates the aspect pipeline and calculates
aspect-corrected Sky ``X`` and ``Y`` values. These sky pixel values are written
to the standard output directory specified by the :par:`OutputDir` parameter in
the native binary format files ``sky_ra.dat`` and ``sky_dec.dat``. If the
:marxtool:`marx2fits` post-processing tool is used, the aspected-corrected Sky pixel
values are written to the FITS events file in the ``X`` and ``Y`` columns. For
simulations with no dither, the FP and Sky coordinate positions are
equivalent.

For actual Chandra flight data, residual errors in the reconstruction
are expected to add a “blurring” to detected photon positions which is
essentially Gaussian. This is simulated by |marx| through
the use of the :par:`AspectBlur` parameter, which has a default value of 0.07
arcsec. The detector pixelization and randomization blurs are
simulated by :marxtool:`marx2fits`, where the user may specify several types of
pixel randomization using its ``--pixadj`` option.

|marx| provides two options for simulating dither motion. The
choice of dither model is determined by the value of the :par:`DitherModel`
parameter. The two models are discussed individually below. By default
``Dithermodel=INTERNAL`` and dither motion is included. The following parameter
in ``marx.par`` controls which type of dither model is used:

.. parameter:: DitherModel

   Dither Model [`NONE`, `INTERNAL`, `FILE`]

.. parameter:: AspectBlur

   Uncertainty of the Aspect reconstruction (sigma - arcsec).
   Number taken from http://cxc.harvard.edu/cal/ASPECT/img_recon/report.html
   (version: 06/29/11).

.. figure:: dither_combo.*
   :alt: Example of simulation with dither enabled
   :align: center

   Simulation showing the effects of the internal dither model in
   |marx|. The panel on the left shows an image of a typical |marx| point
   source simulation with no dither included in Focal Plane (FP)
   coordinates. The right panel shows the same simulation
   with |marx| INTERNAL dither mode turned on. Note that
   in Sky ``X`` and ``Y`` coordinates the images would both
   resemble point sources due to the aspect correction.
   The color scales have been adjusted and are not identical in the
   two panels.



|marx| Internal Dither Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

|marx| provides an emulation of the NPM Lissajous dither pattern.
This internal model is selected by setting ``DitherModel=INTERNAL``. The
form of the dither pattern is determined by the amplitude, phase and
period for both the RA and DEC axes. |marx| also includes the ability
to “dither” the roll angle of the spacecraft during the simulation. In
general, the roll angle of Chandra during a science observation will not
vary; however, there may prove to be some small variations and this
capability allows their effects to be studied.

When using the internal model, the deviations applied to the position of
the line–of–sight over the course of the simulation are calculated using
the following expressions:

.. math::

   \Delta Pos = A  ~\sin \biggl(\frac{2 \pi t}{P} + Phase \biggr)

.. math::

   \theta = \theta_0 + A  ~\sin \biggl(\frac{2 \pi t}{P} + Phase \biggr)

The first equation corresponds the deviations along the RA and DEC
axes, while the second gives the expression for the roll angle
deviation. In both equations, :math:`A` and :math:`P` correspond to the
amplitude and period of the variations and :math:`t` is time. 
:math:`\theta_0` represents the nominal roll angle
of the simulation.

Each of these parameters is controlled by an entry in the marx.par
parameter file. An example of the effects of dither on a simulated
ACIS-I point source observation is shown in `Example of a dither file`_. The
images are displayed in Focal Plane (FP) coordinates.

The :marxtool:`marxasp` tool will create an ASPSOL file containing the aspect motion
for a simulation which used the |marx| internal dither model. This
ASPSOL file can be used in conjunction with normal `CIAO`_ tool :ciao:`asphist` to
produce an aspect histogram file. See :marxtool:`marxasp` for more details.

Set :par:`DitherModel=INTERNAL` and use the parameters described in :ref:`sect-internalditherpars` in 
``marx.par`` to control the internal dither model.


.. figure:: fig_asol.*
   :alt: Example of contents of a :marxtool:`marxasp` ASPSOL file
   :align: center
   :name: Example of a dither file

   The variation in the declination of the simulated Chandra
   aimpoint with time as encoded in an ASPSOL file
   produced using :marxtool:`marxasp`.


Aspect File Mode
^^^^^^^^^^^^^^^^

In addition to its internal dither calculation mode, |marx| can
generate simulations using aspect solution files created by the CXCDS
aspect pipeline. For each observation, the CXCDS produces an aspect
solution giving the Chandra pointing as a function of time. These files
are FITS binary tables of the format described in the table below
(CXC ASPSOL ICD, Rev 2.4). The ASPSOL (or PCAD) files for a given
Chandra observation can be retrieved from the CXC Archive. 
Set :par:`DitherModel=FILE` and the file to
be used is determined with the DitherFile parameter:

.. parameter:: DitherFile 

If the input file
is not a valid ASPSOL file, |marx| will exit with an error message.
The time interval covered by the ASPSOL file must equal or exceed the
requested exposure time of the simulation. If the end of the ASPSOL file
is reached before the requested exposure time, |marx| will truncate
the simulation at that point.

For reference, the following table lists the columns in an ASPSOL file:

============== ====== ============================== =====
Column         Type   Comment                        Units
============== ====== ============================== =====
time           double Time                           s
ra             double RA of MNC frame (x-axis)       deg
dec            double DEC of MNC frame (x-axis)      deg
roll           double ROLL of MNC frame              deg
ra_err         float  Uncertainty in RA              deg
dec_err        float  Uncertainty in DEC             deg
roll_err       float  Uncertainty in ROLL            deg
dy             float  dY of STF frame - FC frame     mm
dz             float  dZ of STF frame - FC frame     mm
dtheta         float  dTHETA of STF frame - FC frame deg
dy_err         float  Uncertainty in dY              mm
dz_err         float  Uncertainty in dZ              mm
dtheta_err     float  Uncertainty in dTHETA          deg
q_att          double S/C attitude quaternion        --
roll_bias      float  Roll bias rate                 deg/s
pitch_bias     float  Pitch bias rate                deg/s
yaw_bias       float  Yaw bias rate                  deg/s
roll_bias_err  float  Roll bias rate error           deg/s
pitch_bias_err float  Pitch bias rate error          deg/s
yaw_bias_err   float  Yaw bias rate error            deg/s
============== ====== ============================== =====


