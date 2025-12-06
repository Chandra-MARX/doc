.. _saosac:

Using |marx| with SAOSAC
==========================

.. warning:: Out of date.

   Some information in section might be out of date. It will be rewritten soon.

For calibration purposes, the Mission Support Team (MST) has developed
an extremely high-fidelity raytrace of the HRMA onboard Chandra called
SAOSAC. SAOSAC is the definitive CXC mirror model and includes many of
the details of the HRMA’s physical construction such as the stray light
baffles and support structures as well as a detailed model of the
reflective properties of the mirror surface. Using XRCF and, ultimately,
on-orbit calibration data, SAOSAC will be "tuned" to reproduce actual
HRMA performance to a high degree of accuracy. SAOSAC serves as baseline
for the HRMA model contained within |marx|. In fact, the |marx| HRMA
model is a simplified version of SAOSAC and includes as many of SAOSAC’s
features as can be reasonably be reproduced while still maintaining
|marx| 's speed and portability.

Using SAOSAC Rayfiles in |marx|
----------------------------------

For many purposes, the HRMA model within |marx| will be sufficiently
accurate. However, users wishing to study very subtle effects caused by
fine details in the HRMA may wish to run simulations utilizing the
SAOSAC mirror model. Users involved in analysis of calibration data are
one obvious example. In such a situation, the user might wish to use
SAOSAC in combination with the detector models or grating models
available within |marx|. The |marx| package provides this capability
by ingesting SAOSAC FITS format rayfiles.

At the current time, it is not planned to distribute the SAOSAC mirror
model to the user community. Instead, SAOSAC rayfiles will be
pre-computed and distributed as needed. These rayfiles take the form of
FITS files containing binary tables of photon or "ray" properties. In
order to provide users with the option of using the SAOSAC mirror model,
|marx| is capable of ingesting standard SAOSAC FITS rayfiles.

The interface to SAOSAC rayfiles is implemented in |marx| by setting
the value of the :par:`SourceType` parameter to ``SAOSAC``. The path to the
SAOSAC rayfile to be accessed is specified using the :par:`SAOSACFile`
parameter. For example, if we wanted to run a |marx| simulation of the
HSI first light test at XRCF, we might use a command similar to:

::

    unix% marx SourceType="SAOSAC" SAOSACFile="C-IXH-PI-3.001.fits"

where C-IXH-PI-3.001.fits in this case is the rayfile appropriate for
that test. 

.. figure:: fig_saosac.*
   :align: center

   The distribution of focal plane photon positions for a |marx| simulation created
   using an SAOSAC FITS rayfile. This rayfile corresponds to XRCF test ID C-IXH-PI-3.001 and
   contains 10000 rays. The XRCF test in question was performed with the HRMA 5.0 mm out of
   focus and this defocus value is reproduced in the simulation.

