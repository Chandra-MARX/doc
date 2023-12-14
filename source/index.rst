Welcome to MARX's documentation!
================================

.. admonition:: Current version of |marx| is |release|. 

   Version 5.5.3 is identical to the previous version 5.5.2
   except to a small tweak in the installation scripts that help
   when compiling marx on Apple's ARM chips.
   See :ref:`installing` for installation instructions.


.. warning:: 
   
   This is the last release of the |marx| 5.x series. In the next release, 
   we will introduce a better treatment of ACIS grades and sub-pixel
   positions. Also, we will remove a few tools that convert marx binary
   results into other formats. Going forward, the only supported tool for
   this purpose is :marxtool:`marx2fits`, followed by standard `CIAO`_
   procedures to make images or extract spectra. We will remove all the IDL
   tools shipped with |marx| (e.g. :marxtool:`make_image`) and  
   :marxtool:`marx2dpde` and :marxtool:`marx2img`.


|marx| is a suite of programs created and maintained by the
`MIT/CXC/HETG group <http://space.mit.edu/cxc/>`_ group and is designed
to enable the user to simulate the on-orbit performance of the Chandra
X-ray Observatory. |marx| provides a detailed ray-trace
simulation of how Chandra responds to a variety of astrophysical
sources and can generate standard FITS event files and images as
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
