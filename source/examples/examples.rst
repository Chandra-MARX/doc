.. _examples:

***********************
Examples of MARX in use
***********************

This section contains examples of |marx| in use from rather trivial use cases
to complex and demanding analysis scripts. Going through these examples is the
best way to discover the power of |marx|. They also provide a great starting point
for developing your own analysis.

All examples assume that you are working in a directory where you have write permission
and enough disk space for the simulation.  It is also assumed that the
|marx| executables are on the search path and that the |marx| parameter
files ``marx.par``, ``marxasp.par``, and ``marxpileup.par`` are located in the
current directory or in the path of your ``PFILES`` environment variable.
If you installed |marx| as described in :ref:`installing`, the
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
common programs are `Xspec`_, `Sherpa`_, and `ISIS`_. Our examples use
`Sherpa`_, because it is typically installed when you install `CIAO`_.
It should be easy to adapt the examples for other spectral analysis systems as well.

We use Python as a scripting language and the
`Python interface to CIAO <https://cxc.cfa.harvard.edu/ciao/scripting/runtool.html>`_
to call `CIAO`_ tools. Even if you are not familiar with Python, it should not be
difficult to convert the examples to shell scripts. For example::

    rt.dmcopy(f"marx_saotrace.fits[@{evt2file}[GTI4]]", "marx_saotrace-filtered.fits", clobber=True)

translates to a command line of::

    unix% dmcopy "marx_saotrace.fits[@${evt2file}[GTI4]]" marx_saotrace-filtered.fits clobber=yes

|marx| itself currently does not have a nice Python interface, so to call |marx| we simply
pass a string directly from Python to the shell, such as::

    import subprocess
    out = subprocess.call('marx SourceType="point" OutputDir="result"', shell=True)

which is the equivalent of the shell command::

    unix% marx SourceType="point" OutputDir="result"

If we run |marx| multiple times in one example, we can use Python to parameterize that::

    for i in range(5):
        out = subprocess.call(f'marx MinEnergy={i} MaxEnergy={i+1} OutputDir="result_{i}"', shell=True)

Still, it should not be difficult to convert these examples to shell scripts so that
they can be pasted directly on the command line.

We present the following examples:

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
