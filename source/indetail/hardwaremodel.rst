.. _sect-modelsforthespacecraft:

The |marx| Models for the Spacecraft
====================================

|marx| provides the capability to simulate the various combinations of
scientific instruments onboard the Chandra satellite and includes models
of the Chandra mirrors, the low- and high-energy transmission grating
assemblies (LETG and HETG), and the HRC and ACIS focal plane detectors.
|marx| also provides support for simulations of ground–based
calibration tests at XRCF. The HRMA shutter assembly is modeled as well
as sources at a finite distance. The purpose of this Section is to
provide technical information about the implementation of the various
subsystems of |marx|.

With very few exceptions, a |marx| user should not change the parameters 
that control the spacecraft model. Their defaults are based on the best 
available Chandra calibration information. Thus, only very few |marx| 
parameters are described in this Section. For reference a list of all
parameters that control the spacecraft model can be found in :ref:`spacecraftpars`.


.. _sect-coordsystem:

The |marx| Coordinate System
------------------------------

The coordinate system used by |marx| is shown in `Figure Coordinate System`_.
The origin is in the vertical plane of symmetry of the system. The
orientation is such that the X–axis is parallel to the optical axis of
the telescope and increases away from the focal plane. Thus,
astrophysical sources are at a distance of :math:`x=+\infty`. The Z–axis
is perpendicular to the horizontal plane of symmetry of the telescope
passing through the X–axis and parallel to the SIM translation
direction. The Y–axis completes the system and corresponds to the
dispersion direction for the gratings on Chandra. The origin of the
|marx| coordinate system is located at the center of the Rowland
torus.

.. figure:: coord.*
   :align: center
   :name: Figure Coordinate System
   :alt: See text for a description of the coordinate system.

   The MARX Coordinate System.

This coordinate system is equivalent to the Chandra coordinate system
described in the Chandra Observatory Guide. More information on the
|marx| and Chandra coordinate systems can be found in several CXC Manuals
available from http://cxc.harvard.edu/ciao/manuals.html . 
The physical placements of the mirror, gratings,
detectors and other hardware components of Chandra in |marx| were
taken from those documents.



.. index::
   single: HRMA

.. _sect-HRMA:

HRMA model
----------

The HRMA onboard Chandra consists of four Wolter Type I mirrors. These
mirrors are nested and each shell consists of a paraboloid at the front
and a hyperboloid at the back. The physical geometry of the HRMA is
defined externally to |marx| through the file EKCHDOS06.rdb. This file
is produced by the CXC Calibration group and contains information about
the size, shape, and placement of the hyperboloid and paraboloid mirror
elements. This information includes the offsets and rotations of the
various mirror shells relative to the optical axis. During the
simulation, the paths of individual photons are traced through this
geometric structure.

The mirror support structure of the HRMA is modeled by default with
:par:`HRMA_Use_Struts=yes`. It can be disabled and |marx| could instead
include a uniform reduction in the total effective area of the HRMA.
The degree of vignetting can be adjusted via the :par:`HRMAVig` parameter. In
general, this parameter should not be modified.

HRMA Reflectivity Model
^^^^^^^^^^^^^^^^^^^^^^^

When a ray encounters a mirror surface, |marx| calculates the
probability that the photon is reflected or absorbed based on the
properties of the mirror coating and the energy and incidence angle of
the photon. The mirror shells are assumed to be coated with iridium and
the iridium optical constants as provided by the Henke Tables are used
to compute the reflectivity of the mirrors as a function of energy.
Comparison of the resulting HRMA effective area with that produced by
SAOSAC raytraces agree to less than 1% over the energy range 0.03–10 keV.

HRMA Scattering Model
^^^^^^^^^^^^^^^^^^^^^^

The point spread function (PSF) of the HRMA is largely determined by two
components: the gross physical shape of the mirrors and scattering of
photons due to small–scale surface irregularities. The physical geometry
of the mirrors is implemented as discussed above. To treat the
scattering properties of the HRMA, |marx| provides two options.

First, a simple Gaussian “blur” may be applied to photon reflections.
The direction of a ray after reflection from the mirror surface is
determined by the orientation of the surface normal at the point of
reflection. This simple model assumes that the direction of the normal
can vary from its ideal direction according to a Gaussian probability
distribution whose standard deviation is given by the HRMABlur
parameters. Blur parameters are specified for each of the parabolic and
hyperbolic HRMA elements (e.g. :par:`H1Blur` for hyperbolic mirror of shell 1).
This model produces a reasonable approximation
to the measured core of the HRMA PSF.

In addition to a Gaussian core, the HRMA PSF exhibits energy–dependent
extended tails as seen in SAOSAC simulations. By default, |marx| uses
a scattering model based on the treatment of HRMA scattering used by the
MST’s high fidelity raytrace SAOSAC. The probability that a photon’s
scattered direction is displaced from a perfect reflection is determined
using the results of WFOLD scattering tables which specify the
probability that a photon of a given energy is scattered into a given
angle. The HRMA raytrace in |marx| accounts for the individual scattering properties of the
various mirror components. For reference, SAOSAC breaks the HRMA P and H
optics into many segments with an associated WFOLD scattering
table for each to better treat the changes in surface properties along
the mirror surfaces. The files used by
|marx| represent the scattering properties for the midpoint of each
hyperbolic and parabolic section of the HRMA. They do not include any
alignment or gravity induced errors which are handled by the physical
model of the HRMA. The normalization of the various WFOLD scattering
tables can be adjusted using the ScatFactor parameters (e.g. :par:`H1ScatFactor`). The WFOLD
scattering model can be disabled in |marx| by setting the parameter
:par:`HRMA_Use_WFold="no"`.

.. _grating-modules:

Grating Modules
---------------

**Chandra** contains two distinct grating assemblies called the HETG and
the LETG. The parameter :par:`GratingType` selects the grating for a |marx| simulation.
The HETG is meant to be used for high energy X–rays and the
LETG is optimized for low energy X–rays. Actually, the HETG consists of
two types of gratings: MEG for medium energy rays, and HEG for high
energy rays. The LETG consists entirely of LEG type gratings. Each
grating facet is arranged such that its geometric center lies on a
**Rowland Torus**. The MEG torus is rotated by :math:`-5` degrees with
respect to the LEG torus, and the HEG torus is rotated by :math:`+5`
degrees with respect to the LEG torus.

After a ray leaves the mirror it travels towards the detector. If the
gratings are being used, the ray will intersect the grating and undergo
a diffraction process. Actually, a certain percentage of the rays will
not strike a grating facet; instead some will be absorbed by the grating
assembly. The percentage of rays that intersect with a facet is
specified by the appropriate vignetting parameter, :par:`LEGVig` if the LETG is
being used, or :par:`HEGVig` and :par:`MEGVig` if the HETG is used.

|marx| currently knows very little about the actual location of
individual grating facets. The assumption is that the HRMA and the
grating assembly is aligned such that the probability of a ray striking
a facet is maximized, and the percentage that miss is controlled by the
vignetting factor.

The LETG includes a complex support structure consisting of a triangular
“coarse” support and a mesh of “fine” wire supports. Both of these
“fine” and “coarse” wire support structures result in additional
diffraction patterns. The LETG grating model in |marx| includes the
multiple diffractions due to these support structures. Roughly 10% of
the detected photons will be diffracted by one or both of these support
structures. The reader is referred to the
http://cxc.harvard.edu/proposer/POG/html/chap9.html for more details.

Intersection with the Rowland Torus
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Rowland torus is defined by the equation

.. math:: (x^2 + y^2 + z^2)^2 = 4 R^2 (x^2 + z^2)
   :label: eqtorus

where :math:`R` is the Rowland radius. To determine the intersection of
a ray with the torus, the ray equation

.. math:: {\vec{x}}= {\vec{x}}_0 + {\hat{p}}t
   :label: eqray

is substituted into the equation for the torus. This yields the fourth
order equation for :math:`t`

.. math::
   :label: quartic

   \begin{split}
    0 = t^4 &+ 4 ({\hat{p}}\cdot{\vec{x}}_0)t^3  \\
            &+ 2t^2 \big(|{\vec{x}}|^2 + 2({\hat{p}}\cdot{\vec{x}}_0)^2 - 2R^2(p_x^2 + p_z^2)\big) \\
            &+ 4t \big(|{\vec{x}}_0|^2 ({\hat{p}}\cdot{\vec{x}}_0) - 2R^2(p_x x_0 + p_z z_0)\big)  \\
            &+ |{\vec{x}}_0|^4 - 4R^2 (x_0^2 + z_0^2)
   \end{split}

where the vector :math:`{\vec{x}}_0` has components
:math:`(x_0, y_0, z_0)`. The four roots of this equation are a
manifestation of the fact that a line can intersect the torus at four
different places.

An important case is when :math:`{\vec{x}}_0 = \vec{0}` where an
enormous simplification occurs and the equation reduces to

.. math:: 0 = t^4 - 4R^2t^2(p_x^2 + p_z^2).

This equation has a double root at :math:`0` and non-zero roots at

.. math:: t = \pm 2R\sqrt{p_x^2 + p_z^2}.
   :label: t0

In the coordinate employed by |marx| , rays travel in the negative
:math:`x` direction from the **HRMA** to the torus. This means that the
solution of interest is the *most negative* root of :eq:`quartic`. Such a
root corresponds to the first intersection point of the ray with the
torus.

Even if :math:`{\vec{x}}_0` is non-zero, one can always project the ray
to the :math:`x = 0` plane to make the component :math:`x_0 = 0`. One
can then argue that the remaining two components :math:`z_0` and
:math:`y_0` will be small (i.e., :math:`z_0<<R`) since the rays from the
HRMA will be converging to the focal point located at the center of the
torus. The upshot is that :eq:`t0` is a good zeroth order approximation to
the exact solution and that one can use this value as the starting point
in an iterative solution to :eq:`quartic`. Newton’s method is used by MARX,
although a closed form solution exists for the quartic equation.


Let :math:`t` be the solution to the equation :math:`0 = f(t)` and let
:math:`t_0` represent an approximate root. If
:math:`\delta t = t - t_0`, then a taylor expansion yields

.. math::

   \begin{split}
      0 = & f(t) \\
        = & f(t_0 + \delta t) \\
        = & f(t_0) + \delta t f'(t_0) + \cdots
   \end{split}

or

.. math:: t = t_0 - \frac{f(t_0)}{f'(t_0)} + \cdots.

Newton’s method follows from the last expression as an iterative
solution of the form

.. math:: t_{k+1} = t_k - \frac{f(t_k)}{f'(t_k)}.
   :label: newton

For the quartic equation

.. math:: 0 = t^4 + at^3 + bt^2 + ct + d,

Newton’s method yields the iterative scheme

.. math:: t_{k+1} = \frac{(3t_k^2 + 2at_k + b)t_k^2 - d}{(4t_k + 3a)t_k^2 + 2bt_k + c}
   :label: iterat

From :eq:`quartic`, it follows that

.. math::

   \begin{split}
      a = & 4{\hat{p}}\cdot{\vec{x}}_0 \\
      b = & 2|{\vec{x}}|^2 + 4({\hat{p}}\cdot{\vec{x}}_0)^2 - 4R^2(p_x^2 + p_z^2) \\
      c = & 4|{\vec{x}}_0|^2 {\hat{p}}\cdot{\vec{x}}_0 - 8R^2 p_z z_0 \\
      d = &  |{\vec{x}}_0|^4 - 4R^2 z_0^2
   \end{split}

where :math:`x_0` has been set to zero in accordance with the
understanding that **the ray has been projected to the x = 0
plane**. This means that

.. math:: t_0 = -2R\sqrt{p_x^2 + p_z^2}

should be used to seed :eq:`iterat`.

The previous analysis is appropriate for any torus whose symmetry axis
is aligned with the |marx| :math:`y` axis. This is the case for the
LETG; however the tori that make up the HETG differ from the LETG torus
by a rotation. In particular, the MEG torus differs from the LEG torus
by a rotation of :math:`-5` degrees about the :math:`x` axis. Similarly,
the HEG torus is rotated by :math:`+5` degrees the other direction. In
the following, we consider the more general case of a torus that is
rotated by an angle :math:`\theta` about the :math:`x` axis.

Let :math:`{\cal R}(\theta)` represent a rotation about the :math:`x`
axis by an angle theta. It takes a vector :math:`\vec{v}` and transforms
it into a new vector :math:`\vec{v'}` via

.. math:: \vec{v}' = {\cal R}(\theta) \vec{v}
   :label: rotation

where the components of :math:`\vec{v}'` satisfy

.. math::

   \begin{split}
      v_x' = & v_x \\
      v_y' = & v_y \cos\theta + v_z \sin\theta \\
      v_z' = & -v_y \sin\theta + v_z\cos\theta.
   \end{split}

At this point :eq:`rotation` could be applied to points on the torus to
obtain a rotated version of :eq:`eqtorus` and the preceding analysis
repeated with the new, more complicated, equation. However, it is easier
to work in a rotated coordinate system where the equation of the torus
retains its form given in :eq:`eqtorus`. So, the prescription for
computing the intersection with a rotated torus looks like this:

#. After projecting :math:`{\vec{x}}_0` to the :math:`x = 0` plane,
   rotate :math:`{\vec{x}}_0` and :math:`{\hat{p}}` via
   :math:`{\cal R}(-\theta)`.

#. Perform the intersection calculation outlined above using the rotated
   values of :math:`{\vec{x}}_0` and :math:`{\hat{p}}`. This calculation
   will result in the intersection point :math:`{\vec{x}}` with
   components expressed in the rotated frame.

#. Rotate all vectors back using :math:`{\cal R}(\theta)`. The result
   will be that the intersection point :math:`{\vec{x}}` will be
   expressed in the unrotated frame.

To illustrate this procedure, consider the special case of
:math:`{\vec{x}}_0 = 0`. In the unrotated case, we found :eq:`t0` as the
solution. For a rotation by an angle :math:`\theta`, the solution in the
rotated frame will be

.. math::

   \begin{aligned}
       {\vec{x}}' &= {\hat{p}}' t_0   \\
                    &= -2R {\hat{p}}' \sqrt{p_x^2 + (p_z\cos\theta + p_y\sin\theta)^2}
                        \\
   \end{aligned}

which when rotated back to the original frame yields

.. math::

   {\vec{x}}= -2R {\hat{p}}\sqrt{p_x^2 + (p_z\cos\theta - p_y\sin\theta)^2}.

Diffraction of the Ray
^^^^^^^^^^^^^^^^^^^^^^^

Consider a ray with wavelength :math:`\lambda` and direction
:math:`{\hat{p}}` incident upon a diffraction grating of period
:math:`d` located at position :math:`{\vec{x}}` and normal
:math:`\hat{n}`. The grating lines are assumed to oriented in the
direction :math:`\hat{l}`. See Figure :ref:`Fig-Diffraction`. 
In a very general way, the diffraction equation can be written in vector form as
:math:`\hat{p}' \times \hat{n} = \hat{p} \times \hat{n} + (m
\lambda/d)\hat{l}`.
Taking the dot product of this equation with :math:`\hat{d}` and
:math:`\hat{l}` respectively, it can be shown
that a ray diffracting into order :math:`m` will move in a direction
:math:`{\hat{p}}'` determined by the conditions:
 
.. math::
   :label: diffract0

   \begin{aligned}
       {\hat{p}}'\cdot\hat{l} &= {\hat{p}}\cdot\hat{l} \\
       {\hat{p}}'\cdot\hat{d} &= {\hat{p}}\cdot\hat{d} + \frac{m\lambda}{d}
   \end{aligned}

where

.. math:: \hat{d} = \hat{n} \times \hat{l}.

(And because these vectors form an orthonormal basis the following is also true:
:math:`\hat{l} = \hat{d} \times \hat{n}` and :math:`\hat{n} = \hat{l} \times
\hat{d}`.)

.. _Fig-Diffraction:

.. figure:: grating.*
   :align: center
   
   Diffraction Coordinate System

   Figure showing the orthogonal coordinate system local to an individual grating
   facet. The vector :math:`\hat{n}` is normal to the facet and :math:`\hat{l}` is in the direction of the grating lines. The
   vector :math:`\hat{d}` is in the dispersion direction. The incident ray is
   given by :math:`\hat{p}` and the diffracted ray is :math:`\hat{p}'`.

Since :math:`\hat{n}`, :math:`\hat{l}`, and :math:`\hat{d}` form a
right-handed orthonormal coordinate system, it trivially follows that


.. math::
   :label: diffracted

   {\hat{p}}' = ({\hat{p}}\cdot\hat{l})\hat{l}
           + ({\hat{p}}\cdot\hat{d} + \frac{m\lambda}{d})\hat{d}
           + \hat{n} \sqrt{1
                          - ({\hat{p}}\cdot\hat{l})^2
                          - ({\hat{p}}\cdot\hat{d} + \frac{m\lambda}{d})^2}.

After diffraction, the ray will travel along the trajectory

.. math:: {\vec{x}}(t) = {\vec{x}}+ {\hat{p}}'t.

Note that :eq:`diffracted` may be put into a more familiar form as
follows. Since the component of the ray in the :math:`\hat{l}` direction
is not changed by the grating, the effect of the diffraction is simply a
rotation of :math:`{\hat{p}}` about the :math:`\hat{l}` axis by some
angle. Let :math:`{\vec{p}_{\perp}}` denote the projection of
:math:`{\hat{p}}` onto the :math:`(\hat{d},\hat{n})` plane, and let
:math:`\theta` be the angle between :math:`{\vec{p}_{\perp}}` and
:math:`\hat{n}`. Define :math:`{{\vec{p}_{\perp}}\,\!\!\!\!'}` and
:math:`\theta'` in a similar fashion (see Figure :ref:`Fig-Diffraction-plane`).

.. _Fig-Diffraction-plane:

.. figure:: diffract.*
   :align: center

   Diffraction in a plane

   Diffraction in the :math:`(n, d)` plane. Here :math:`\theta` is the angle the projection of the incoming
   ray onto the :math:`\hat{d}\hat{n}` plane  makes with respect to the normal, and :math:`\theta` is the angle between the normal and
   the projection of the outgoing ray.


It follows from :eq:`diffract0` that

.. math:: p_{\perp} \sin \theta' = p_{\perp} \sin \theta - \frac{m\lambda}{d},

where
:math:`p_{\perp} = |{\vec{p}_{\perp}}| = |{{\vec{p}_{\perp}}\,\!\!\!\!'}|`.
In fact, the previous equation reduces to the well known diffraction
equation when :math:`{\hat{p}}` has no component in the :math:`\hat{l}`
direction. Using these definitions, one can write :eq:`diffracted` in the
form

.. math::

   {\hat{p}}' = ({\hat{p}}\cdot\hat{l})\hat{l}
           - (p_{\perp} \sin{\theta'}) \hat{d}
           + (p_{\perp} \cos{\theta'}) \hat{n}.

In general, :math:`\hat{n}` and :math:`\hat{l}` are complicated
functions of the position of the grating. However, for gratings of
infinitesimal size (For finite size facets, the grating normal will have to be looked up in a facet database.) 
positioned on the surface of the Rowland torus,
:math:`\hat{n}` will be directed towards the origin, i.e.,

.. math:: \hat{n} = -\frac{{\vec{x}}}{|{\vec{x}}|}

Similarly, :math:`\hat{l}` may be determined from the condition that the
facets are arranged such that :math:`\hat{l}` has no :math:`y`
component (We are working in the natural coordinate system of the torus. Thus these equations hold for the LETG and
the HETG.) and that it is normal to :math:`\hat{n}`. That is,

.. math::

   \begin{split}
      0 &= \hat{l}\cdot\hat{y} \\
      0 &= \hat{l}\cdot\hat{n} \\
      1 &= |\hat{l}|
   \end{split}

from which it follows that

.. math::

   \hat{l} = \frac{1}{\sqrt{n_x^2 + n_z^2}}
                 \begin{pmatrix}
                    n_z\\
                    0\\
                    -n_x
                 \end{pmatrix}.

Since the LETG gratings have a support structure that also acts as a
diffraction grating, we need to consider a more general orientation of
the :math:`\hat{l}` axis that consists of a rotation about the
:math:`\hat{n}` axis by some angle :math:`\theta`. This means that the
rotated vectors,

.. math::

   \begin{aligned}
     \hat{l}_{\theta} &= \hat{l} \cos\theta + \hat{d}\sin\theta \\
     \hat{d}_{\theta} &= -\hat{l} \sin\theta + \hat{d}\cos\theta,
   \end{aligned}

should be used in :eq:`diffracted` to yield

.. math::

   {\hat{p}}' = ({\hat{p}}\cdot\hat{l}_{\theta})\hat{l}_{\theta}
           + ({\hat{p}}\cdot\hat{d}_{\theta} + \frac{m\lambda}{d})\hat{d}_{\theta}
           + \hat{n} \sqrt{1
                          - ({\hat{p}}\cdot\hat{l}_{\theta})^2
                          - ({\hat{p}}\cdot\hat{d}_{\theta} + \frac{m\lambda}{d})^2}.

.. _Gratingefficiency:

Grating Efficiency
^^^^^^^^^^^^^^^^^^

The grating efficiency is a function of many quantities such as the
geometrical parameters that specify the bar shape, the chemical
composition and thickness of the layers that make up the plating base of
the grating, etc. An extensive effort has been made to quantitatively
understand the relationship of these quantities to the grating
efficiency (see the http://space.mit.edu/HETG/report.html).

In early versions of |marx| a simple, uniform rectangular bar
model was used to calculate the diffraction efficiency of the HETG and
LETG grating facets. Based on comparison to synchrotron measurements,
the rectangular grating bar model appears to be accurate to
approximately 5% over most of the HETG’s operating passband. This model
does not meet the HETG calibration goal of 1%. Consequently, the current |marx|
version uses a new grating efficiency model based on
tabulated facet data from sub–assembly and XRCF data.

.. parameter:: UseGratingEffFiles

   Use grating efficiency tables?  These efficiency
   tables have been provided by the HETG IPI team and include grating
   efficiencies for orders -11 to 11. In the case of the LETG tables,
   orders from -25 to 25 are included. Individual tables have been
   calculated for each mirror shell and include the inter-grating
   vignetting. Users can still access the old uniform bar facet
   model by setting ``UseGratingEffFiles=no``, but this is not 
   recommended.

.. parameter:: Use_Unit_Efficiencies 

   If `yes`, rays which intersect the HETG or LETG will
   still be diffracted but no efficiency filter will be applied. Hence all
   orders will have an equal probability of being populated. This mode is
   useful for studying the characteristics of higher order dispersed
   photons without having to run very large simulations in order to build
   up reasonable statistics.

.. _misalignments:

Facet Period Variations and Misalignments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The HETG onboard Chandra consists of 336 individual grating facets.
During the XRCF calibration of the HETG, it was discovered that 6 MEG
grating facets were mis-aligned by angles ranging from 3 to 24 arcmins.
The effects of these mis-aligned facets is shown in
`Figure Misalignment`_. 

.. figure:: mis_align_defocus.*
   :align: center
   :name: Figure Misalignment

   An image from XRCF test D-HXH-AL-27.001 showing the
   MEG 3rd order Al-K defocused to 65.54 mm. The
   main :math:`K\alpha` line, satellite line, and :math:`K\beta`/O-K lines are
   visible in the left panel. The enlarged view in the right panel
   shows the effects of the mis-aligned gratings.

|marx| allows to specify
the mis-alignment angles and period variations of groups of facets 
as a function of azimuthal angle around the HETG support
structure. Sector files describing the properties of the facets as a
function of angle (including the mis-aligned MEG facets) have been
provided by the HETG IPI team and reside in the ``MARX_DATA_DIR``
directory. 

.. parameter:: Use_HETG_Sector_Files

.. parameter:: Use_LETG_Sector_Files 
   
   Sector files are currently unavailable for
   the LETG, so this option is off by default when simulating LETG
   observations. Instead, the misalignmens is treated statistically
   using :par:`legdTheta` parameter.

There was a long standing issue of a relative rotation between the LETG and the
ACIS detector. The root of this problem was tracked down (with the help of
|marx|) to a rotation offset between the aspect coordinate system and the focal
plane detector system. This offset was masked by compensating rotations of the
detectors from astrometric analysis, and manifested itself as a small rotation
of the LEG dispersion arm on the ACIS detector. Changes were added to CIAO 4.3
that effectively adds an additional rotation to the LETG when used with ACIS. 

.. parameter:: LETG_ACIS_dTheta


.. _sect-detectormodel:

Detector Models
---------------

The detector models in |marx| are all consist of at least four
components: geometry, filter transmissions, detector quantum efficiency,
and spectral resolution. The specifics of these components for each of
the four Chandra focal plane detectors is discussed here.

Detector Geometry
^^^^^^^^^^^^^^^^^

The physical placement of the detectors in the Chandra focal plane is
based on reference data given in the CXC coordinates documents. These
data include locations and tilts in three dimensions for each CCD in the
ACIS-I and ACIS-S arrays as well as all four MCPs in the HRC-I and
HRC-S. The detector geometric model in |marx| reproduces the tilts of
the ACIS-S CCD to follow the "bowl"-shaped HRMA focal surface and the
arc of the six ACIS-S CCDs which follows the curved Rowland focal
surface (see http://asc.harvard.edu/proposer/POG/html/index.html
for a more detailed description).

Similarly, the tilts of the three MCPs in the HRC-S spectroscopic array
are reproduced. Chip and plate gaps as appropriate are also included in
the geometric model. |marx| writes the raw U and V coordinates for the
HRC-S to the ``hrc_u.dat`` and ``hrc_v.dat`` files and they will appear in the events files created with
:marxtool:`marx2fits`.

Filters
^^^^^^^

ACIS
~~~~

Both the ACIS-I and ACIS-S CCD arrays include UV/visual optical blocking
filters to protect the CCDs from non-X-ray photons. |marx| models
these filters using tabulated transmission efficiencies supplied by G.
Chartas (Penn State). Separate tables are used for the filters on the
ACIS-I and ACIS-S arrays. This transmission efficiency calculation can
be disabled in |marx| using the parameter :par:`DetIdeal="yes"`.

HRC
~~~

The HRC-I and HRC-S detectors include a set of UV/Ion shields to block
UV photons and low energy ions. In the case of the HRC-I, a single
uniform UV/Ion shield covers the entire surface of the MCP. As with the
ACIS optical blocking filters, |marx| uses an external data file
containing tabulated efficiencies to model the shield’s transmission and
this transmission can be disabled with :par:`DetIdeal="yes"`.

The UV/Ion shield configuration of the HRC-S array is slightly more
complicated and includes four distinct regions each with a unique
transmission efficiency. For an overview of the HRC–S shield
configuration see:
http://cxc.harvard.edu/proposer/POG/html/chap7.html.

|marx| uses four individual data files to specify the transmission
of these regions. The central region of the HRC-S UV/Ion shield includes
a “T” shaped region of thicker Al which can be used to preferentially
reject low energy photons. This Low Energy Suppression Filter (LESF)
region is included in the |marx| model of the HRC–S UV/Ion shield. If
the LESF is to be used, the SIM should be repositioned using
:par:`DetOffsetZ=-6.5` to place dispersed spectrum over the LESF. Users should
consult the http://cxc.harvard.edu/proposer/POG/html/chap7.html for
more information on the LESF.

As a final complication, the UV/Ion shield on the HRC-S array is
physically offset from the MCP surfaces by approximately 10 mm. This
separation can lead to “shadowing” near the edges of differing filter
regions. This effect is included in |marx| and the separation is
controlled with the :par:`HESFOffsetX` parameter.

Detector Quantum Efficiency
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The detector quantum efficiency is modeled in exactly the same manner
for both the ACIS and HRC detectors. External data files are used to
define the quantum efficiency as a function of photon energy for each
detector. Using this function, |marx| calculates a cumulative
probability as a function of photon energy. For each photon which
reaches the detector surface, a random number is then generated and
compared with the cumulative probability in order to determine whether
the photon was detected.

Unique quantum efficiency curves are used for the MCPs in the HRC–I and
HRC-S; however, all three HRC-S MCPs are currently assumed to have the
same quantum efficiency. As the Chandra calibration effort progresses,
these curves will be replaced by specific curves for each MCP.
Quantum efficiency (QE) files are available for the 10 CCDs
comprising the ACIS-I and ACIS-S detectors.

If the parameter :par:`DetIdeal="yes"`, the QE of the selected focal plane
detector (including any filter transmission) will be set to unity.

Detector Spectral Resolution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The detector redistribution function determines the mapping of photon
energy to detected pulse height (PH). These functions determine the
intrinsic spectral resolution of the different detectors. |marx| uses
a mixture of calibration information and simple analytic forms to
approximate these functions. More accurate redistribution functions can
be applied to |marx| simulations using the :marxtool:`marxrsp` tool discussed :ref:`rsp`.

.. _ACISCTI:

ACIS
~~~~

The redistribution of the ACIS detector is exceedingly complex. Both the
gain and spectral resolution of each of the 10 ACIS CCDs varies with
position on the chip. Due to the radiation damage induced increase in
charge transfer inefficiency (CTI), the spatial variations of the
frontside chips are especially large. Fortunately, an extensive effort
has been undertaken by the CXC Calibration group to measure these
variations as a function position for each of the ACIS CCDs. Currently,
the ACIS-S aimpoint CCD (chip ID 7) has calibration data specifying the
gain and spectral resolution for each 32x32 pixel region on the chip.
Due to reduced signal to noise, the remaining backside chip (chip ID 5)
has been calibrated on 64x64 pixel regions. The remaining 8 frontside
CCDs are calibrated in 256x32 pixel segments. For each of these CCD
calibration regions, the CXC has determined a unique gain and functional
fit to the redistribution function. The redistribution model in 
utilizes this calibration information when determining the
observed PHA channel for a given detected event.

The CXC Calibration group currently models the ACIS redistribution using
a functional form consisting of multiple Gaussian components. The
internal |marx| redistribution function reproduces *only* the primary
peak of the ACIS response, assuming a single Gaussian whose width is
determined by the CXC CCD Calibration data mentioned above.

.. outofdate:

   Currently, MARX uses FEF and not the gain file.
   The variations with energy and position of the Gaussian widths are encoded
   in a FITS binary table designated with the :par:`ACIS_Gain_Map_File`
   parameter. This file conforms to the format of an ACIS Gain Map file
   defined in the
   http://space.mit.edu/CXC/docs/ARD_ICD/ACIS_ARD_ICD_2.1.ps.gz with
   the addition of an extra column specifying the width of the primary
   redistribution peak.

The gain and spectral response of the ACIS CCDs are also functions of
focal plane temperature and change over time both over years as the
spacecraft and the detectors age, and also within an observation as the
focal plane temperature changes. In recent years, temperature changes
within an observation increased as Chandra's thermal insulation
degraded. |marx| cannot predict the temperature of the focal plane and
simulations assume nominal gain files from the CXC Calibration group.


More information on the ACIS energy resolution can be found at
http://cxc.harvard.edu/proposer/POG/html/chap6.html#tth_sEc6.7 .

HRC
~~~

The MCPs which comprise the HRC-I and HRC-S detectors have very limited
spectral resolution with :math:`\sigma_E / E \sim 1`. As with the ACIS
CCDs, the redistribution function is assumed to be a Gaussian. The width
of the MCPs distribution, however, is more complicated and is
represented in |marx| by

.. math::

   \sigma(E) = \left\{
       \begin{array}{ll}
       a_0 \sqrt{ E }~~~~~~ & E < 0.5 ~\mbox{keV} \\
       a_1 E^{0.1}    & 0.5 < E < 2.0 ~\mbox{keV} ~~.\\
       a_2            & E > 2.0 ~\mbox{keV}
       \end{array}
                  \right.
   \label{eqn:hrc_res}

Here :math:`E` is the photon energy and :math:`a_0`, :math:`a_1`, and
:math:`a_2` are constants which have been adjusted to approximately
reproduce the preliminary XRCF measurements of the HRC redistribution
function.

Detector Spatial Resolution
^^^^^^^^^^^^^^^^^^^^^^^^^^^

ACIS
~~~~
No extra blur is applied to ACIS simulations.

HRC
~~~

The physical characteristics and readout electronics of the HRC MCPs add
a “blur” to the observed system point spread function in addition to the
intrinsic FWHM of the HRMA. In |marx|, this blur is modeled as the sum
of two Gaussians and a Lorentzian.
Since the 2d Lorentzian diverges, it has to be cutoff at some
radius, :math:`R_\mathrm{max}`.  Its normalized form is given by

 .. math::

    L(r) = \frac{L_0}{1+r^2/g^2}

where :math:`1/L_0 = g^2 \pi \log(1 + R_\mathrm{max}^2/g^2)`.
Then :math:`1 = \int_0^{R_\mathrm{max}} (2 \pi r) L(r) \;dr`.

The 2-d gaussian has the normalized form

.. math::

   G(r) = \exp(-\frac{r^2}{2\sigma^2}) / (2 \pi \sigma^2)\\
   1 = \int (2 \pi r) G(r) \;dr
 
The parameters that specify the coefficients of all functions are listed 
in :ref:`HRCIparameters` and :ref:`HRCSparameters`.

.. index::
   single: HESF
   single: Drake Flat

HESF
~~~~

Due to the poor intrinsic energy resolution of the HRC-S, order sorting
for astrophysical spectra obtained with the LETG+HRC-S combination
not possible in practice. In an attempt to ameliorate this problem, the High Energy
Reflection Filter (HESF) was added to the original HRC-S design. The
HESF (a.k.a. Drake Flat) is a two facet filter coated with Cr and C
which can be inserted into the Chandra beam by a translation of the SIM
along the :math:`Z` axis. Above the Cr L and C K edges, the reflectivity
of the filter is designed to be low, thus suppressing higher order
photons. `Figure Drake Flat` shows a schematic of the HESF. More details
on the HESF are available in the
http://cxc.harvard.edu/proposer/POG/html/chap7.html .

.. figure:: drake.*
   :name: Figure Drake Flat
   :align: center

   Schematic of the HRC–S High Energy Suppression Filter (HESF). Figure courtesy
   of Dr. Jeremy Drake (SAO/CXC).

|marx| includes the HESF in its raytrace calculation if the parameter
:par:`HRC-HESF="yes"`. The reflectivity of the of Cr and C surface coatings is
calculated internally. If the HESF is to be used, the SIM should be
repositioned using :par:`DetOffsetZ=-5.471` to place the HESF in the Chandra
beam.


Simulating ground calibration data
===================================

With appropriate configuration, |marx| can be used to simulate
data taken during the calibration phase of the Chandra mission at the
X–Ray Calibration facility (XRCF) in Huntsville, AL. By default,
|marx| simulates the flight performance of the Chandra satellite.
However, a number of effects contribute to differences between the
flight and XRCF performance of Chandra. A brief summary of these effects
are listed here.

-  Additional HRMA blur: The effects of gravity on the HRMA at XRCF
   produce an additional “blurring” of the mirror’s point spread
   function (PSF) relative to the flight performance. This behavior can
   be adjusted with the :par:`P1Blur`, :par:`P3Blur`, :par:`P4Blur`, and :par:`P6Blur` 
   and the :par:`H1Blur`, :par:`H3Blur`, :par:`H4Blur`, and  :par:`H6Blur` parameters.

-  Change of HRMA Focus position: Since the x-ray source at XRCF was at
   a finite distance from the HRMA, the effective location of the
   “focus” falls at a different location along the optical axis than the
   default flight configuration. Changing the :par:`DetOffsetX` parameter will
   move the location of the focal plane relative to the HRMA.

-  Finite Source Size: Due to its finite distance, the EIPS x-ray source
   used at XRCF was actually resolved by the HRMA resulting in a broader
   PSF than one would measure for a point source. A simple way to
   include this affect is to use the ``DISK`` source model to simulate an
   extended source. Alternatively, one could use the ``IMAGE`` source model
   in conjunction with actual FITS images of the EIPS source provided by
   the http://wwwastro.msfc.nasa.gov/xray/xraycal/spot .

-  Finite Source Distance: By default |marx|, assumes that sources
   are sufficiently far away that photons impinging on the HRMA can be
   assumed to be parallel to the optical axis. At XRCF, the calibration
   source was not far enough away from the focal plane for this
   assumption to hold. For XRCF simulations, the :par:`SourceDistance`
   parameter should be set to a value of 537.587 meters.

-  Modified Rowland Diameter: The difference in the location of the
   focal plane at XRCF results in a different Rowland geometry for the
   HETG and LETG spectrometers. This geometry is controlled via the
   :par:`HEGRowlandDiameter`, :par:`MEGRowlandDiameter`, and
   :par:`LEGRowlandDiameter` parameters.

To simulate XRCF data, these parameters should be modified in your
``marx.par`` file. The table provides a summary of the relevant
parameters, their default values, and values appropriate for simulating
XRCF data. An example XRCF simulation is
shown in the :ref:`figure below <fig-xrcf>` for test ID D-IXH-PI-3.003.

========================= =========== ==========
Parameter                 Default     XRCF      
========================= =========== ==========
:par:`P1Blur`             0.18129215  0.362
:par:`H1Blur`             0.13995037  0.280
:par:`P3Blur`             0.11527828  0.230
:par:`H3Blur`             0.16360829  0.327
:par:`P4Blur`             0.12891340  0.258
:par:`H4Blur`             0.098093014 0.196
:par:`P6Blur`             0.076202759 0.152
:par:`H6Blur`             0.079767401 0.160
:par:`DetOffsetX`         0.0         -194.925
:par:`SourceType`         POINT       DISK
:par:`S-DiskTheta0`       0.0         0.0
:par:`S-DiskTheta1`       0.0         0.0767372
:par:`SourceDistance`     0.0         537.587
:par:`HEGRowlandDiameter` 8632.48     8587.88
:par:`MEGRowlandDiameter` 8632.48     8587.88
:par:`LEGRowlandDiameter` 8637.00     8593.12
========================= =========== ==========

.. _fig-xrcf:

.. figure:: compare_xrcf.*
   :align: center

   A comparison between data from XRCF test ID D-IXH-PI-3.003 and a corresponding MARX simulation. The MARX simulation was 9.7 mm out of focus like the XRCF test.

