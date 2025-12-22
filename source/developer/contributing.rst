Contributing code or documentation
==================================

|marx| is developed by the MIT/CXC group and made available under the GPL v2 license
in source code form. The latest release can be found at `distribution`_.

The developers use the `git version control system <https://git-scm.com/>`_
and host the code on github.
We welcome pull requests through github for all apects of the |marx| software, which
includes the following repositories:

- https://github.com/Chandra-MARX/marx : |marx| source code.
  Building the source code has only minimal requirements (a C compiler and GNU autotools).
- https://github.com/Chandra-MARX/doc : This keeps the source code for the documentation.
  The documentation is written using `Sphinx <http://www.sphinx-doc.org/>`_ and requires
  a number of packages to be build:

  - Python, sphinx, matplotlib.
  - |marx|, `CIAO`_ (incl. the CALDB and the ACIS background files),
    `Sherpa`_, and `SAOTrace`_ to run the examples and
    generate the associated figures. The examples expect all |marx| binaries and
    ``trace-nest`` (from `SAOTrace`_) to be in the system path. They also expect
    the ``PFILES`` environment variable to point to the |marx| parameter files.
  - Longer running tests are in the `tests/` subdirectory. These are written as
    `Jupyter notebooks <https://jupyter.org/>`_ and additionally require
    astropy, myst_nb (for chaching and building the notebooks with sphinx).
    The notebooks also need |marx| and `SAOTrace`. If they are not on the system path,
    they can be specified in a ``marx_examples.cfg`` files in the ``tests/`` directory.

    
- https://github.com/Chandra-MARX/marx-test : This repository focusses on CI-like tests
  that have additional requirements beyond the basic |marx| build (if it only needs
  |marx| and some shell script, it should to into |marx| itself).
  For example, some tests need `CIAO`_, or additional Python packages.
  
