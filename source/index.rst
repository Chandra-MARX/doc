Welcome to MARX's documentation!
================================

.. admonition:: Current version of |marx| is |release|

   We now recommend to install |marx| together with CIAO as described in
   https://cxc.cfa.harvard.edu/ciao/download/ .
   Of course, it is still possible to install |marx| from
   source as described in :ref:`installing`.

.. warning::
   Marx 6.0 is **not** fully backward compatible with version 5.x. In particular,

   * The :par:`Verbose` parameter now requires an integer for finer control of
     the verbosity level.
   * We removed obsolete tools that convert marx binary
     results into other formats. Going forward, the only supported tool for
     this purpose is :marxtool:`marx2fits`, followed by standard `CIAO`_
     procedures to make images or extract spectra.

   This version also improves error checking and user feedback in case of parameters errors
   as well as some bug fixes.
   See :ref:`highlights` for a full list of changes.


|marx| is a suite of programs created and maintained by the
`MIT/CXC/HETG group <http://space.mit.edu/cxc/>`_ group and is designed
to enable the user to simulate the on-orbit performance of the Chandra
X-ray Observatory. |marx| provides a detailed ray-trace
simulation of how Chandra responds to a variety of astrophysical
sources and can generate standard FITS event files as
output. It contains detailed models for Chandra's High Resolution
Mirror Assembly (HRMA), the HETG and LETG gratings, and all the focal
plane detectors.

If you publish any work that made use of |marx|, please cite the
paper `Raytracing
with MARX: x-ray observatory design, calibration, and support (Davis et al. 2012, SPIE 8443, 84431A) <http://adsabs.harvard.edu/abs/2012SPIE.8443E..1AD>`_.


.. toctree::
   :maxdepth: 2

   inbrief/overview
   examples/examples
   indetail/docs
   tests/index

   Reference/reference


Indices and tables
==================

* :ref:`parindex`
* :ref:`genindex`
* :ref:`search`

Contributing to MARX
====================

.. toctree::
   :maxdepth: 2

   developer/contributing
   developer/release
