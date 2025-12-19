
Making a release
================

.. note::
   The |marx| source packages and documentation are build and deployed locally on MIT servers,
   thus these instructions will not be relevant for people outside the MIT/CXC
   group.

Preparation
-----------
Ensure that ``NEWS`` in the source directory and ``source/inbrief/news.rst`` in
the documentation repository describe the new release.

Source repro
------------
(Commands are shown here as an example for a release called ``5.1.0``.)

#) git checkout master
#) *if necessary*: Update the copyright statements in the individual files::

      grep -rli 'Copyright (C) 2002-2013 Massachusetts Institute of Technology' * | xargs -i@ sed -i 's/Copyright (C) 2002-2013 Massachusetts Institute of Technology/Copyright (C) 2002-2015 Massachusetts Institute of Technology/g' @

   Note separate copyright in ``jdmath/COPYRIGHT``.

#) Update version string in e.g. in the
   comments in ``*.par`` (if backwards incompatible changes have been done) and update
   ``MARX_VERSION`` and ``MARX_VERSION_STRING`` in ``marx.h``.
#) Update NEWS files in the root directory.
#) commit changes to git
#) ``git tag v5.1.0``
#) ``git push --tags reproname`` Push tag to all repositories that should have a copy.
#) Create a release on the github repository page for marx, using the tag created above.


Documentation repro
-------------------

#) update ``copyright``, ``version``, and ``release`` in ``conf.py``. (Note
   that the copyright year turn up further down for LaTeX and epub again.)
#) Update any notes on the front page ``index.rst`` etc.
#) Update ``inbrief/news.rst``.
#) Update file name in ``aliases.txt`` and ``inbrief/install.rst``.
#) ``make clean``
#) Install marx and set path in ``source/examples/config.inc`` to it, so that
   the examples are build with the new version.
#) ``make figures``
#) ``make examples``
#) ``make html``. Fix any errors that come up.
#) ``scp -r build/html/* space:/space/web/ASC/marx-5.1`` (Create directory on
   space as required.)
#) On ``/space/web/ASC``: ``rm marx; ln -s marx-5.1 marx``.

Get the word out
----------------

#) Announce release to cxc at mit.edu
#) Announce release on marx-users at space.mit.edu
#) Ask T. Gorcas to include release in next Chandra electronic announcement
#) Ask CIAO team to advertise release through the CIAO Twitter, facebook, Google+ feeds.
