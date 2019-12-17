.. _sect-sourcemodels:

The spectrum and the spatial shape of the X-ray source
======================================================

|marx| provides support for both extended and point sources, which can
be either on or off–axis. The sources can have a flat energy spectrum or
they can use an energy spectrum supplied by the user and in the next section we
describe those options. Then, we explain the different models for the spatial
distribution that these source can have on the sky. 
The following sources are currently available:

- ``POINT``: Point Source
- ``GAUSS``: Radially symmetric Gaussian
- ``BETA``: Cluster Beta model
- ``DISK``: Disk or annulus (e.g. SN remnant)
- ``LINE``: Straight line
- ``IMAGE``: Input from a FITS image file
- ``SAOSAC``: Input from an SAOSAC FITS rayfile
- ``RAYFILE``: Input from a |marx| rayfile
- ``SIMPUT``: Input from a fits file following the `SIMPUT standard`_.
- ``USER``: Dynamically linked user–supplied model

First, it is important
to have an understanding of what a source means in the context of
|marx|. It is particularly important to understand how
|marx| interacts with a source model for the proper implementation of
a user–defined source. As far as |marx| is concerned, a source is
characterized by the distribution of rays in energy, time, and direction
that it produces at the entrance aperture of the telescope. Implicit in
this characterization is the assumption that the source is sufficiently
far away that the flux does not vary with position across the telescope.

To be more precise, let

.. math:: F(t,E,{\hat{p}},{\vec{x}}) ({\hat{p}}\cdot{\mbox{d}\vec{A}\;}) {\mbox{d}\Omega\;} {\mbox{d}E\;} {\mbox{d}t\;}

denote the number of rays with energy between :math:`E` and
:math:`E + dE`, and whose directions lie in a solid angle
:math:`d\Omega` about the direction :math:`{\hat{p}}`, crossing an area
element :math:`{\mbox{d}\vec{A}\;}` at :math:`{\vec{x}}` during the time
:math:`dt`. That is, :math:`F(t,E,{\hat{p}},{\vec{x}})` is a space-time
dependent flux density. If the source is very far away, as is the case
for objects of astrophysical interest, the spatial dependence of the
flux density may be ignored when :math:`{\vec{x}}` refers to points near
the telescope. For this reason, :math:`F` will be assumed to be
independent of :math:`{\vec{x}}`. Similarly, since the angular
acceptance of the telescope is very small (on the order of arc-minutes),
to first order we need only consider area elements
:math:`{\mbox{d}\vec{A}\;}` whose normals are in the direction of the
source. Hence, :math:`{\hat{p}}\cdot{\mbox{d}\vec{A}\;}` will simply be
written as :math:`{\mbox{d}A\;}`.

We can consider various classes of source models according to whether or
not :math:`F` factors. For example, all |marx| sources (with the
exception of ``USER`` sources) produce fluxes that are time-independent
with an energy spectrum that is uncorrelated with the direction of the
flux (see `USER Source`_ for more information about the
``USER`` source). For the rest of this section, we will only consider
the class of models for which :math:`F` can be written

.. math:: F(t,E,{\hat{p}}) = f(t) \cdot f_E(E) \cdot f_p({\hat{p}}).

When such a factorization is possible, it will be assumed that
:math:`f_E(E)` and :math:`f_p({\hat{p}})` are normalized, i.e.,

.. math:: 1 = \int_{\Omega} {\mbox{d}\Omega\;} f_p({\hat{p}}),

and

.. math:: 1 = \int{\mbox{d}E\;} f_E(E) .

With this normalization,

.. math:: f(t) = \int {\mbox{d}E\;} \int_{\Omega} {\mbox{d}\Omega\;} F(t, E, {\hat{p}})

is simply the total flux, which can depend upon time. In the following,
we shall call :math:`f_E` the *energy spectrum*, and :math:`f_p` the
*angular distribution* of the source.

Spectrum of the simulated X-ray source
-------------------------------------------

In the |marx| parameter file, ``marx.par``, the parameter
:par:`SpectrumType` is used to specify the function :math:`f_E` for the
following source types: ``"POINT"``, ``"LINE"``, ``"GAUSS"``, ``"BETA"``, 
``"DISK"``, and ``"IMAGE"`` (the other source have a source specific way to
input the energy, e.g. for a ``"SAOSAC"`` source the energy of each ray is
already included in the ray file).

Currently,
:math:`f_E` can only be a ``FLAT`` spectrum or a ``FILE`` spectrum.
Similarly, when :math:`f(t)` is time-independent, as it for all
|marx| sources in this class, then its value is specified by the
:par:`SourceFlux` parameter. For simulations with :par:`SpectrumType="FLAT"`, the
function :math:`f_E` is assumed to be constant over the specified energy
range with a normalization given by :par:`SourceFlux`. Alternatively, the FILE
type will use a tabulated spectral energy distribution read from an
external ASCII file. The following parameters describe the source spectrum:

.. parameter:: SpectrumType

   Select spectrum type. Can be ``FLAT`` or ``FILE``.

.. parameter:: SourceFlux

   Incoming ray flux (photons/sec/cm2). For
   :par:`SpectrumType="FLAT"` this number must be positive. If
   :par:`SpectrumType="FILE"` this number can be positive to renormalize the
   spectrum file to the given source flux. If it is negative, then the
   normalization from the :par:`SpectrumFile` will be used. 

.. parameter:: SpectrumFile

   Input spectrum filename (only used if
   :par:`SpectrumType="FILE"`). The file has to consist of two columns of data
   with no header line. The first column contains the energy of the upper bin
   edge in keV, the second the flux density in photons/s/cm^2/keV in that bin
   (the flux in the first row is ignored, because there is no row before
   which would define the lower energy edge of the bin).
   Various tools exist to help in generating this file:
   
       - :marxtool:`marxflux` can be used to generate a file with the right format
         from an `ISIS`_ model,
       - :marxtool:`xspec2marx` helps with converting from
         `XSPEC`_ output,
       -  and there are also instructions how to generate a file
          `from observations with Sherpa
          <http://cxc.harvard.edu/sherpa/threads/marx/>`_ or :ref:`creating_sherpa_spectrum`.

.. parameter:: MinEnergy

   MIN ray energy in keV (only used if :par:`SpectrumType="FLAT"`)

.. parameter:: MaxEnergy

   MAX ray energy in keV (only used if :par:`SpectrumType="FLAT"`)



Spatial distribution of the simulated source
------------------------------------------------

The distribution function :math:`f_p({\hat{p}})` characterizes the
angular distribution of the flux and, hence, the angular distribution of
the source. The nominal aimpoint of the observation (given by :par:`RA_Nom` and
:par:`Dec_Nom`) can differ from the source position (given by :par:`SourceRA`
and :par:`SourceDEC`) to simulate off-axis sources.

By convention, :math:`f_p({\hat{p}})` is assumed to be normalized to
unity, i.e.,

.. math::

   1 = \int_{0}^{\pi} \sin\theta {\mbox{d}\theta\;}
         \int_0^{2\pi} d{\phi} f_p(\theta, \phi) ,

where :math:`{\hat{p}}` has been expressed in spherical coordinates. For
an azimuthally symmetric source, :math:`f_p` is independent of
:math:`\phi` and the normalization condition reduces to

.. math:: 1 = 2\pi \int_{0}^{\pi} {\mbox{d}\theta\;} \sin\theta  f_p(\theta) .

In |marx| the following parameter selects model for the spatial distribution of the source:

.. parameter:: SourceType

   The following values are allowed: ``"POINT"``, ``"LINE"``, ``"GAUSS"``, ``"BETA"``, 
   ``"DISK"``, ``"IMAGE"``, ``"SAOSAC"``, ``"RAYFILE"``, ``"SIMPUT"``, and ``"USER"``. Depending on the source model chosen,
   further parameters (such as the radius of the disk) may be required.

Each availble model is now described in more detail.

.. index::
   pair: Source Model; POINT

.. _sect-models-POINT:

POINT Source
^^^^^^^^^^^^

The ``POINT`` source corresponds to an angular distribution function
given by

.. math::

   f_p(\theta, \phi) = \frac{1}{2\pi} \delta (\phi)
         \delta(1 - \cos \theta)

A ``POINT`` source requires no further parameter to specify the spatial distribution.


.. index::
   pair: Source Model; LINE

LINE Source
^^^^^^^^^^^

The ``LINE`` source corresponds to an angular distribution function
given by

.. math::

   f_p(\theta, \phi) = \frac{1}{\theta_0\theta}\cdot
        \frac{1}{2} \big[\delta(\phi - \phi_0)
             + \delta(\phi - \phi_0 - \pi) \big]

for :math:`\theta < \theta_0` and zero otherwise. 

.. parameter:: S-LinePhi

   Line source orientation angle  :math:`\phi_0` (degrees)

.. parameter:: S-LineTheta

   Line source length :math:`\theta_0` (arcsec)


.. index::
   pair: Source Model; GAUSS

GAUSS Source
^^^^^^^^^^^^

The ``GAUSS`` source corresponds to an angular distribution function
given by

.. math:: f_p(\theta, \phi) = \frac{1}{\pi} e^{-\theta^2/\theta_0^2}

where :math:`\theta_0` determines the width of the Gaussian
distribution:

.. parameter:: S-GaussSigma

.. index::
   pair: Source Model; BETA

BETA Source
^^^^^^^^^^^

The ``BETA`` source corresponds to an angular distribution function
given by

.. math::

   f_p(\theta, \phi) = \frac{1}{2\pi}
       \cdot
         \frac{6}{\theta_c}(\beta - \frac{1}{2})
         \big[ 1 + (\frac{\theta}{\theta_c})^2 \big]^{-3\beta + \frac{1}{2}}.

This distribution is used to model galaxy clusters.

.. parameter:: S-BetaCoreRadius

   Core radius :math:`\theta_c` (arcsec)

.. parameter:: S-BetaBeta

   :math:`\beta` value


.. index::
   pair: Source Model; DISK

.. _sect-models-DISK:

DISK Source
^^^^^^^^^^^

The ``DISK`` source corresponds to an angular distribution function
given by

.. math::

   f_p(\theta, \phi) = \frac{1}{2\pi}
          \cdot \frac{2}{\theta_1^2 - \theta_0^2}

for :math:`\theta_0 <= \theta < \theta_1`. Outside this region, it is
zero. This source actually generates a ring structure and is
useful for modeling a supernova remnant.

.. parameter:: S-DiskTheta0

   Min disk :math:`\theta_0` (arcsec)

.. parameter:: S-DiskTheta1

   Max disk :math:`\theta_1` (arcsec)


.. index::
   pair: Source Model; IMAGE

.. _sect-imagesource:

IMAGE Source
^^^^^^^^^^^^
This option creates photons distributed on the sky according to an input image.
The probability that a ray starts at a given position is proportional to the pixel value at this point. 
Within a pixel, the position is randomized.
|marx| inspects the header of the file for a WCS specification and extracts the pixel scale. 
However, it does **not** extract the position or orientation on the sky.
|marx| will just assume that the image is centered on the optical axis and that the axes directions
are aligned with the detector axes.

.. parameter:: S-ImageFile


.. index::
   pair: Source Model; SAOSAC source

SAOSAC Source
^^^^^^^^^^^^^
The ``SAOSAC`` source allows SAOSAC raytrace files to be used as input for |marx|. SAOSAC is a high-fidelity raytracer
for the Chandra mirrors, with a much higher level of detail than the module supplied with |marx|.
Only in very rare cases is this needed for the end-user. More details can be found in :ref:`saosac`.

.. parameter:: SAOSACFile


.. index::
   pair: Source Model; RAYFILE source

RAYFILE Source
^^^^^^^^^^^^^^
The ``RAYFILE`` source can be used to dublicate the source properties of a previous |marx| simulation.
Using this as a source keeps the photon properties energy and position
as specified in the ray file.
Thus, the *source* properties are identical to those used to 
generate the original ray file, but the *Chandra response* to them might be
different, e.g. if a different detector or dither is chosen.
Rayfiles are produced by setting :par:`DumpToRayFile=yes`.

.. parameter:: RayFile


.. index::
   pair: Source Model; SIMPUT


SIMPUT Source
^^^^^^^^^^^^^
|marx| supports the `SIMPUT standard`_, which is a fits based
description of sources, that allows a large number of sources with different
spectra, light curves, and shapes on the sky. This file format is supported by a
number of other simulators (e.g. for ATHENA), so integrating it in |marx|
allows users to use the same source specification for different X-ray missions.
The support in |marx| is through the `SIMPUT code`_ which needs to be installed
separately and is linked dynamically at runtime if :par:`SourceType="SIMPUT"`.

.. parameter:: S-SIMPUT-Source

.. parameter:: S-SIMPUT-Library


.. index::
   pair: Source Model; USER

.. _sect-usersource:

USER Source
^^^^^^^^^^^

The ``USER`` source is the most versatile of the |marx| sources. With
a user–defined source, each ray may be given an independent energy,
time, and direction. This flexibility means that one does not need to
require that the flux density factorize as was assumed for the other
|marx| sources. Using a ``USER`` source model, sources whose spectrum
changes with time, complex extended objects, etc. can be simulated.

.. parameter:: UserSourceFile

.. parameter:: UserSourceArgs
   
A user-defined source model must be created by the user using a language
such as C and then compiled as a shared object. During run-time,
|marx| will dynamically link to this shared object and use it to
generate rays.
It is important to understand that creating a user-defined source
does not mean that |marx|  must be recompiled. If that were the case,
then there would be no value to a user-defined source.

We include several examples in the ``marx/doc/examples/user-source/`` directory
in the |marx| distribution. Some of the examples might be useful as-is, e.g. a
source that samples photons from an input event list. Other examples are meant
to show you how ``USER`` sources can be programmed. If you write a user source
that you are willing to share with others, please contact |marx-email|.

Creating a ``USER`` source is relatively simple and is best accomplished
using the C programming language. The C source file must define three
functions that |marx| will call during run-time::

       user_open_source
       user_close_source
       user_create_ray

The ``user_open_source`` function will be called by |marx|  before any
rays are generated. The purpose of this function is to initialize any
data structures required by the ``user_create_ray`` function. The
``user_create_ray`` function will be called one time for each ray
generated. The purpose of this routine is to assign an energy, time, and
direction to a ray. Finally, the ``user_close_source`` function will be
called when |marx|  has finished processing rays. Each of these
functions are described in more detail below.

user_open_source
~~~~~~~~~~~~~~~~~~~

.. highlight:: c

The ``user_open_source`` function has the prototype::

      int user_open_source (char **argv, int argc,
                            double area,
                            double cosx,
                            double cosy,
                            double cosz);

The value of the ``marx.par`` parameter :par:`UserSourceArgs` will be
broken into an array of whitespace separated strings and passed to
``user_open_source`` via the ``argv`` parameter. The parameter ``argc``
indicates the number of such strings. The actual meaning of these
strings will depend upon the details of the user-defined source. For
example, if the user-defined source needs to read an external data file,
the parameter can represent the name of the data file.

The ``area`` parameter specifies the area in cm\ :math:`^2` of the
entrance aperture of the mirror. Knowledge of this value is necessary to
compute the time interval between rays since the incoming flux must be
multiplied by this value to generate the total incoming photon rate.

The other three parameters ``cosx``, ``cosy``, and ``cosz`` are the
direction cosines of a ray from a reference point on the source to the
origin of the |marx|  coordinate system. These numbers are derived
from the |marx|  parameter file :par:`SourceRA` and
:par:`SourceDEC` parameters. For an on axis source, ``cosy`` and
``cosz`` will be set to zero, but ``cosx`` will be set to ``-1``. If the
reference point of the user defined source is always on axis, these
parameters may be ignored and the actual parameter values for
:par:`SourceRA` and :par:`SourceDEC` will have no affect on the rays
generated by source. However, if one would like to position the source
off-axis via the :par:`SourceRA` and :par:`SourceDEC` parameters, the values
of the direction cosines will need to be taken into account. An example
of this is presented below.

Upon success, ``user_open_source`` must return ``0``. If for any reason
it fails, e.g, unable to open a file, it must return ``-1``.

The simplest example of ``user_open_source`` is one which does nothing::

      int user_open_source (char **argv, int argc,
                            double cosx,
                            double cosy,
                            double cosz)
      {
         return 0;   /* Success */
      }

user_close_source
~~~~~~~~~~~~~~~~~~~~~

The ``user_close_source`` function has the prototype:

::

       void user_close_source (void);

Its purpose is to free up any resources acquired by the source. For
example, if the source dynamically allocated memory,
``user_close_source`` should deallocate it.

user_create_ray
~~~~~~~~~~~~~~~~~~

The ``user_create_ray`` function is the function that actually defines
the source by endowing each ray with a direction, energy, and time. It
has the following prototype::

       int user_create_ray (double *delta_t, double *energy,
                            double *cosx, double *cosy, double *cosz);

Since the purpose of this routine is to assign a ray an energy, time, and
direction, the parameters are actually pointer types and the requested
information is passed back to the calling routine via the parameter
list. Before ``user_create_ray`` is called, |marx| uses the :par:`SpectrumType`
in ``marx.par`` to assign an energy. This allows user sources to assign a ray
direction depending on this energy, but it has the downside that the definition
of :par:`SpectrumType` has to be valid even if ``user_create_ray`` assigns an
energy for the ray itself.  Except for the energy, the ray is completely
undefined prior to calling ``user_create_ray``.

The ``delta_t`` parameter is used to give the ray a time-stamp. Actually
it does not refer directly to the absolute time of the ray; rather, its
value should refer to the time since the last ray was generated. For
example, if a ray is generated every second,

::

       *delta_t = 1.0;

should be used. If ``*delta_t`` is set to ``-1.0``, then |marx|  will
generate the time based on the :par:`SourceFlux` parameter. Otherwise, the
value should be set in a manner consistent with the flux and the
geometric area of the mirror. The meaning of the parameters that specify the
direction cosines should be rather clear.


Compiling a User-Defined Source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The procedure for compiling a user-defined source as a shared object
will depend upon the operating system. For details, consult you compiler
and linker manual. For the purposes of this section, it is assumed that
the file containing the code for the user-defined source is called
``mysource.c``. This may be compiled as a shared object under **Linux**
using ``gcc`` via the command::

        gcc -shared mysource.c -o mysource.so

If ``mysource.c`` requires other libraries, they should also be included
on the command line. The syntax is slightly different under **Solaris**::

        cc -G mysource.c -o mysource.so

To actually use the source in |marx| , set the ``marx.par`` parameter
:par:`SourceType` to ``"USER"`` and also set the parameter :par:`UserSourceFile`
to point to the full absolute filename for ``mysource.so``. It is
usually necessary to use an absolute filename because of the way the
dynamic linker searches for shared objects. Finally, set the parameter
:par:`UserSourceArgs` to a value that is appropriate to your source.

If running ``marx`` using your dynamically linked source causes it to
crash, do not assume that the bug is in |marx| . Rather, it is most
likely a bug in your code. Make sure that the interface routines are
properly prototyped and that the routines return the proper values to
|marx| . If you use dynamic memory allocation, check the return status
of routines such as ``malloc``. Finally, look at the examples provided
with the |marx|  distribution and try to run those.

Examples of User-Defined Sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The simplest source is that of a point source. Although |marx| 
already provides built-in support for this source, it is instructive to
write it as a user-defined source. Here is the complete C code for such
a source::

    #include <stdio.h>

    static double Source_CosX;
    static double Source_CosY;
    static double Source_CosZ;

    int user_open_source (char **argv, int argc, double area,
                          double cosx, double cosy, double cosz)
    {
       Source_CosX = cosx;
       Source_CosY = cosy;
       Source_CosZ = cosz;
       return 0;
    }

    void user_close_source (void)
    {
    }

    int user_create_ray (double *delta_t, double *energy,
                         double *cosx, double *cosy, double *cosz)
    {
       *cosx = Source_CosX;
       *cosy = Source_CosY;
       *cosz = Source_CosZ;

       *delta_t = -1.0;
       *energy = -1.0;

       return 0;
    }

First of all, note that ``energy`` and ``delta_t`` have been set equal
to ``-1.0`` in ``user_create_ray``. This indicates to |marx|  that it
should compute the time and energy of the ray via the :par:`SpectrumType`
and :par:`SourceFlux` parameters. For this reason, the ``area`` parameter
was not used by ``user_open_source``. Since the direction cosines passed
to ``user_open_source`` refers to the vector from the position of the
source to the origin where the telescope is located, those values were
saved and used in ``user_create_ray``.

