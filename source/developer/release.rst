
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

#) Update version string in e.g. the start-up message or |marx| or in the
   comments in ``marx.par``. The best way to do this is properly to grep for
   ``5.0.0`` (or whatever the previous version was called).
#) Update NEWS files in the root directory.
#) commit changes to git
#) ``git tag v5.1.0``
#) ``git push --tags reproname`` Push tag to all repositories that should have a copy.
#) ``git archive --format=tar --prefix=marx-5.1.0/ v5.1.0 | gzip >
   marx-dist-5.1.0.tar.gz``
#) Sign with your private key: ``gpg --armor --detach-sig
   marx-dist-5.1.0.tar.gz``
#) Calculate hash, so that user can verify error-free download: ``sha1sum marx-dist-5.1.0* > sha1sums.txt``
#) ``scp marx-dist-5.1.0.tar.gz space:/space/ftp/pub/cxc/marx/v5.1`` (make
   directory as required)
#) ``scp marx-dist-5.1.0.tar.gz.asc space:/space/ftp/pub/cxc/marx/v5.1``
#) ``scp sha1sums.txt space:/space/ftp/pub/cxc/marx/v5.1``
#) Provide tar file also via https: ``scp marx-dist-5.1.0.tar.gz space:/space/web/ASC/marx-5.1``


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
