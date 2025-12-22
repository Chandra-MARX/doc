*******************************
MARX Frequently Asked Questions
*******************************

I have a question about marx that is not addressed here. Where can I get additional help?
============================================================================================
|marx| specific questions should be sent to |marx-email|.  If
your question is related to `CIAO`_, then you should contact the `CXC helpdesk <http://asc.harvard.edu/helpdesk/index.html>`_.


Do you distribute marx binaries?
================================
Yes, see :ref:`installing` for details on how to obtain pre-compiled
binaries via conda.


How do I create an ARF and RMF that match my marx simulation?
=============================================================
The answer to this question may be found :ref:`ex-ciao`.


Can I simulate arbitrary combinations of ACIS CCDs in marx?
===========================================================
The simple answer is "no". Out of the box, |marx| allows users to
select either the ACIS-S array (6 CCDs) or the ACIS-I array (4 CCDs).
Arbitrary mixtures of chips from the two arrays are not currently
supported although we plan to add that option in a future version
of |marx|.

In the meantime, if you do need to simulate other combinations,
one can assemble such composites by creating the desired ACIS-S 
and ACIS-I chips separately and them merging the resulting event
lists with the :ciao:`dmmerge` tool in `CIAO`_. For such mergers, both pieces
of the simulation must have the same aimpoint position. 
This configuration can be accomplished by a SIM translation in |marx|
using the :par:`DetOffsetX` and :par:`DetOffsetZ` parameters.

For example, to create a |marx| simulation where the default
ACIS-S aimpoint was used, but ACIS-I chips were also active
during the observation, one would do two separate simulations.
The ACIS-S portion of the simulation would utilize the |marx| defaults.
The simulation of the ACIS-I chips however would require moving
the SIM to position the ACIS-I detector correctly relative to the
default ACIS-S aimpoint. The appropriate values in the ``marx.par`` file 
would be::

  DetOffsetX=0.0990000
  DetOffsetZ=43.4590

Note that the :par:`DetOffsetY` parameter is not modified since SIM motion
along the Y axis is not permitted. For simulations using the default
ACIS-I aimpoint, the ACIS-S simulation would need to be offset
using the values::

  DetOffsetX=-0.0990000
  DetOffsetZ=-43.4590

The :ciao:`dmmerge` tool will produce some warning messages during the
combination of the two event lists, but should produce a valid
FITS event file. Unwanted CCDs can be removed using :ciao:`dmcopy`.

Can I simulate CTI-corrected observations in marx?
==================================================

No. |marx| does not currently recognize the new format
of the CTI-corrected FEF file available in the CALDB (versions 2.18
and higher). So simulations cannot be created directly
which feature the improved spectral response of the front-illuminated
CCDs after CTI correction. Users wishing to simulate CTI--corrected
spectra can however use the :marxtool:`marxrsp` tool to fold a given |marx|
simulation through an existing RMF created from the CTI--corrected FEF. 


Is it possible to run marx with a constant effective area?
==========================================================

If by "constant" you mean an effective area that does not not depend
upon energy, then the answer is yes.   To do so, use the following
configuration::

  DetIdeal=yes
  HRMA_Ideal=yes HRMAVig=1.0
  Use_Unit_Efficiencies=yes
  mode=h

The :par:`DetIdeal=yes` setting tells |marx| to assume that the detectors
have 100 percent quantum efficiency.  The line involving the
``HRMA*`` parameters indicates that perfect reflectivity from the
mirrors is to be assumed and that no rays will suffer vignetting from
the various baffles.  The :par:`Use_Unit_Efficiencies=yes` parameter
setting comes into play only in when the gratings (LETG or HETG)
are used.  It causes the diffraction efficiencies for all orders to
be equal, i.e., all diffraction orders will be equally probable.
Finally, the :par:`mode=h` line will cause |marx| to not save these
values in the ``marx.par`` file.

Keep in mind that some photons will still be lost if they scatter from
the mirror and not hit the detector, fall in detector gaps, etc.
