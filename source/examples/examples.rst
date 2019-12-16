.. _examples:

***********************
Examples of MARX in use
***********************

This section contains examples of |marx| in use from rather trivial use cases to complex and demanding analysis scripts. Going through these examples is the best way to discover the power of |marx|. They also provide a great starting point for developing your own analysis.

All of the examples assume
that you are working in a directory where you have write permission
and enough disk space for the simulation.  It is also assumed that the
|marx| executables are on the search path and that the |marx| parameter
files ``marx.par``, ``marxasp.par``, and 
``marxpileup.par``) are located in the current directory.  Assuming you installed |marx| as described in :ref:`installing`, the
latter requirement may be accomplished by running::

  unix% marx --help
    .
    .
  marx parameter files may be found in:
   /opt/marx5.5/share/marx/pfiles/

Simply copy the files from the indicated directory to the current one::

  unix% cp /opt/marx5.5/share/marx/pfiles/*.par .

In most examples, |marx| is used together with a spectral analysis program to 
write the input spectrum or to analyze the results. The most
common programs are `Xspec`_, `Sherpa`_, and `ISIS`_. For each example, we pick
one of those programs and provide instructions, but it should be easy to adapt
the examples for other spectral analysis systems as well.
(Note that in some installations it can happen that `CIAO`_ and `ISIS`_ have conflicts.  In these cases it is
useful to setup `CIAO`_ only when needed and open a new terminal after
that.)


.. toctree::
   :maxdepth: 1
 
   ACISpowerpileup/powerlaw
   aped/aped
   hetgplaw/hetgplaw
   LETGpow/letgplaw
   marxcat/marxcat
   background/background
   simobs/simobs

Further examples of |marx| use can be found on the `CIAO thread
pages <http://cxc.harvard.edu/ciao/threads/all.html>`_:

- `Using MARX to Create an Event File from ChaRT
  Rays <http://cxc.harvard.edu/ciao/threads/marx/>`_
- `Creating an Input Spectrum for Running MARX Simulations <http://cxc.harvard.edu/sherpa/threads/marx/>`_
- `Using MARX to Simulate an Existing Observation <http://cxc.harvard.edu/ciao/threads/marx_sim/>`_
- `Using MARX to Simulate a Planned
  Observation <http://cxc.harvard.edu/ciao/threads/marx_unobs_sim/>`_
